from torch.utils.data.sampler import *
from torch.utils.data.distributed import DistributedSampler
import random
import time
import math


class AncSampler(DistributedSampler):
    r'''
    A batch sampler controls the data sharding, data shuffling and data loading order with proper indices

    The data sharding is chunk based. For example, to shard a dataset with 10 elements into 2 splits, 
    the result data index would be [[0,1,2,3,4],[5,6,7,8,9]] instead of [[0,2,4,6,8],[1,3,5,7,9]]

    Args:
        dataset: dataset from which to load the data.
        batch_size (int): how many samples per batch to load.
        world (int, optional): data parallel world size (default: ``1``).
        rank (int, optional): data parallel rank of current process (default: ``0``).
        num_workers (int): how many subprocesses to use for data
            loading. ``0`` means that the data will be loaded in the main process.
        shuffle (bool, optional): set to ``True`` to have the data reshuffled
            at every epoch (default: ``False``).
        drop_last (bool, optional): set to ``True`` to drop the last incomplete batch,
            if the dataset size is not divisible by the batch size. If ``False`` and
            the size of dataset is not divisible by the batch size, then the last batch
            will be smaller. (default: ``False``).
        seed (int, optional): seed for randomness (default: ``0``).
        resume_step (int, optional): the step to resume from, 
            the previous steps will be skipped (default: ``0``).
        repeat (bool, optional): set to ``True`` to repeat the indices when gone through 
            all the data. If ``False`` than StopIteration will be raised when all data 
            is consumed (default: ``False``).
    '''
    def __init__(
        self,
        dataset,
        batch_size,
        world = 1,
        rank = 0,
        num_workers = 1,
        shuffle = False,
        drop_last = False,
        seed = 0,
        resume_step = 0,
        repeat = False,
        global_shuffle = False,
        ratios = [1],
        chunk_granularity = -1,
    ):
        self.sub_lengths = dataset.get_sub_lengths()
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.resume_step = resume_step
        self.step = resume_step
        self.seed = seed
        self.last_iter_epoch = -1
        self.indices = None
        self.repeat = repeat
        self.inner_epoch_count = 0
        self.global_shuffle = global_shuffle
        self.num_replicas = world
        self.rank = rank
        self.epoch = 0
        self.drop_last = drop_last
        self.chunk_granularity = chunk_granularity
        if len(ratios) == 1:
            self.ratios = ratios * len(self.sub_lengths)
        else:
            assert len(ratios) == len(self.sub_lengths)
            self.ratios = ratios
        ds_length = 0
        for item, ratio in zip(self.sub_lengths, self.ratios):
            if isinstance(item, list):
                ds_length += math.ceil(sum(item) * ratio)
            else:
                ds_length += math.ceil(item * ratio)
        if self.drop_last and ds_length % self.num_replicas != 0:
            self.num_samples = math.ceil((ds_length - self.num_replicas) / self.num_replicas)
        else:
            self.num_samples = math.ceil(ds_length / self.num_replicas)
        self.total_size = self.num_samples * self.num_replicas
        self.shuffle = shuffle
        if getattr(self, "dataset", None) is not None:
            self.dataset = None

    def _get_indices_with_ratio(self, indices, ratio):
        ratio_int = math.floor(ratio)
        ratio_float = ratio - ratio_int
        res = []
        for _ in range(ratio_int):
            tmp_indices = indices[:]
            if self.shuffle:
                random.shuffle(tmp_indices)
            if self.chunk_granularity > 0:
                num_chunks = (len(tmp_indices) + self.chunk_granularity - 1) // self.chunk_granularity
                for i in range(num_chunks):
                    res.append(tmp_indices[i * self.chunk_granularity: (i + 1) * self.chunk_granularity])
            else:
                res.append(tmp_indices)
        if ratio_float > 0:
            tmp_indices = indices[:]
            if self.shuffle:
                random.shuffle(tmp_indices)
            tmp_indices = tmp_indices[:math.ceil(ratio_float * len(tmp_indices))]
            if self.chunk_granularity > 0:
                num_chunks = (len(tmp_indices) + self.chunk_granularity - 1) // self.chunk_granularity
                for i in range(num_chunks):
                    res.append(tmp_indices[i * self.chunk_granularity: (i + 1) * self.chunk_granularity])
            else:
                res.append(tmp_indices)
        if self.shuffle:
            random.shuffle(res)
        return res

    def _get_indices(self, sub_lengths, offset=0, return_sub_indices=False, ratio=[1]):
        indices_list = []
        random.seed(self.seed)
        accumulate_length = offset
        if len(ratio) == 1:
            ratio = ratio * len(sub_lengths)
        else:
            assert len(ratio) == len(sub_lengths)
        for i, item in enumerate(sub_lengths):
            sub_indices = list(range(accumulate_length, accumulate_length + item))
            sub_indices = self._get_indices_with_ratio(sub_indices, ratio[i])
            indices_list += sub_indices
            accumulate_length += item

        if self.shuffle:
            random.shuffle(indices_list)
        if return_sub_indices:
            return indices_list
        indices = []
        for item in indices_list:
            indices += item
        return indices

    def create_chunk_indices_from_bz_and_worker(self, indices):
        # calculate num batches per worker
        num_batches = (self.num_samples + self.batch_size - 1) // self.batch_size
        last_batch_size = self.num_samples - (num_batches - 1) * self.batch_size
        num_batches_per_worker = num_batches // self.num_workers
        remain = num_batches - self.num_workers * num_batches_per_worker
        num_batches_per_each_worker = [num_batches_per_worker + 1] * remain + [num_batches_per_worker] * (self.num_workers - remain)
        assert sum(num_batches_per_each_worker) == num_batches
        last_batch_worker_id = self.num_workers - 1 if remain == 0 else remain - 1

        if self.repeat and self.shuffle:
            random.seed(self.seed)
        while True:
            self.inner_epoch_count += 1
            indices_per_worker = []
            offset = 0
            for i in range(self.num_workers):
                cur_worker_indices = []
                for batch_cnt in range(num_batches_per_each_worker[i]):
                    cur_batch_size = self.batch_size
                    if i == last_batch_worker_id and batch_cnt == num_batches_per_each_worker[i] - 1:
                        cur_batch_size = last_batch_size
                    cur_worker_indices.append(indices[offset: offset + cur_batch_size])
                    offset += cur_batch_size
                indices_per_worker.append(cur_worker_indices)

            for i in range(num_batches_per_worker):
                for wid in range(self.num_workers):
                    is_last_batch = wid >= remain and i == num_batches_per_each_worker[wid] - 1 and not self.repeat
                    yield indices_per_worker[wid][i], is_last_batch
            for wid in range(remain):
                is_last_batch = not self.repeat
                yield indices_per_worker[wid][-1], is_last_batch
            if not self.repeat:
                break
            if self.global_shuffle:
                random.shuffle(indices)
            elif self.shuffle:
                shift_offset = random.randint(0, len(indices))
                indices = indices[shift_offset:] + indices[:shift_offset]

    def __iter__(self):
        indices = []
        if self.epoch == self.last_iter_epoch:
            indices = self.indices
        else:
            self.last_iter_epoch = self.epoch
            if isinstance(self.sub_lengths[0], list):
                sub_indices_list = []
                accumulate_length = 0
                for i, item in enumerate(self.sub_lengths):
                    sub_indices = self._get_indices(item, accumulate_length, True, [self.ratios[i]])
                    accumulate_length += sum(item)
                    sub_indices_list += sub_indices
                if self.shuffle:
                    random.shuffle(sub_indices_list)
                for item in sub_indices_list:
                    indices += item
            else:
                indices = self._get_indices(self.sub_lengths, ratio=self.ratios)
                if self.global_shuffle:
                    random.shuffle(indices)
            
            if not self.drop_last:
                # add extra samples to make it evenly divisible
                padding_size = self.total_size - len(indices)
                if padding_size <= len(indices):
                    indices += indices[:padding_size]
                else:
                    indices += (indices * math.ceil(padding_size / len(indices)))[
                        :padding_size
                    ]
            else:
                # remove tail of data to make it evenly divisible.
                indices = indices[: self.total_size]
            assert len(indices) == self.total_size

            # we do the chunk sharding here
            indices = indices[self.rank * self.num_samples : (self.rank + 1) * self.num_samples]
            self.indices = indices
        assert len(indices) == self.num_samples
        # further split the per rank indices into num_workers splits
        indices_generator = self.create_chunk_indices_from_bz_and_worker(indices)

        # skip the indices that already been consumed
        for i in range(self.resume_step):
            _ = next(indices_generator)

        # yield empty indices to let workers follow the original order
        # otherwise, the first generated indices would be consumed by worker 0
        # while they should be consumed by cur_wid
        cur_wid = self.resume_step % self.num_workers
        for i in range(cur_wid):
            yield [], False

        while True:
            try:
                self.step += 1
                yield next(indices_generator)
            except StopIteration:
                break

    def set_step(self, step):
        self.resume_step = step
        self.step = step
    
    def __len__(self):
        # this is a batch sampler, return the number of batches
        if not self.repeat:
            if self.drop_last:
                return self.num_samples // self.batch_size
            else:
                return (self.num_samples + self.batch_size - 1) // self.batch_size
        else:
            return 1000000000000

    def _set_ckpt(self, state):
        self.__dict__.update(state)

    def _get_ckpt(self):
        state = self.__dict__
        state['resume_step'] = self.step
        state['last_iter_epoch'] = -1
        state['indices'] = None
        return state


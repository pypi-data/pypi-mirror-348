import threading
import time
import asyncio


class AsyncSnowflakeIdGenerator:
    """
    雪花算法优化版，支持异步并发环境下的唯一 ID 生成。
    """
    epoch = 1640995200000
    node_id_bits = 10
    sequence_bits = 12
    max_node_id = -1 ^ (-1 << node_id_bits)
    sequence_mask = -1 ^ (-1 << sequence_bits)
    node_id_shift = sequence_bits
    timestamp_shift = sequence_bits + node_id_bits

    _lock = asyncio.Lock()  # 将锁类型更换为asyncio.Lock
    _sequence = 0
    _last_timestamp = -1
    _node_id = None

    def __init__(self, node_id=1):
        assert 0 <= node_id <= self.max_node_id, "Node ID 超出范围"
        self._node_id = node_id

    async def generate_id(self):
        """异步生成长整型唯一 ID"""
        async with AsyncSnowflakeIdGenerator._lock:
            timestamp = int(time.time() * 1000)

            while timestamp < AsyncSnowflakeIdGenerator._last_timestamp:
                timestamp = int(time.time() * 1000)

            if timestamp == AsyncSnowflakeIdGenerator._last_timestamp:
                AsyncSnowflakeIdGenerator._sequence = (AsyncSnowflakeIdGenerator._sequence + 1) & self.sequence_mask
                if AsyncSnowflakeIdGenerator._sequence == 0:
                    timestamp = await self._wait_for_next_millis(timestamp)
            else:
                AsyncSnowflakeIdGenerator._sequence = 0

            AsyncSnowflakeIdGenerator._last_timestamp = timestamp

            new_id = (
                    ((timestamp - self.epoch) << self.timestamp_shift)
                    | (self._node_id << self.node_id_shift)
                    | AsyncSnowflakeIdGenerator._sequence
            )

            return new_id

    async def _wait_for_next_millis(self, last_timestamp):
        """异步等待下一毫秒"""
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            await asyncio.sleep(0.001)
            timestamp = int(time.time() * 1000)
        return timestamp


class SnowflakeIdGenerator:
    """
    雪花算法优化版，支持并发环境下的唯一 ID 生成。
    """

    epoch = 1640995200000
    node_id_bits = 10
    sequence_bits = 12
    max_node_id = -1 ^ (-1 << node_id_bits)
    sequence_mask = -1 ^ (-1 << sequence_bits)
    node_id_shift = sequence_bits
    timestamp_shift = sequence_bits + node_id_bits

    _lock = threading.Lock()
    _sequence = 0
    _last_timestamp = -1
    _node_id = None

    def __init__(self, node_id=1):
        assert 0 <= node_id <= self.max_node_id, "Node ID 超出范围"
        self._node_id = node_id

    def generate_id(self):
        """生成长整型唯一 ID"""
        with SnowflakeIdGenerator._lock:
            timestamp = int(time.time() * 1000)

            while timestamp < SnowflakeIdGenerator._last_timestamp:
                timestamp = int(time.time() * 1000)

            if timestamp == SnowflakeIdGenerator._last_timestamp:
                SnowflakeIdGenerator._sequence = (SnowflakeIdGenerator._sequence + 1) & self.sequence_mask
                if SnowflakeIdGenerator._sequence == 0:
                    timestamp = self._wait_for_next_millis(timestamp)
            else:
                SnowflakeIdGenerator._sequence = 0

            SnowflakeIdGenerator._last_timestamp = timestamp

            new_id = (
                    ((timestamp - self.epoch) << self.timestamp_shift)
                    | (self._node_id << self.node_id_shift)
                    | SnowflakeIdGenerator._sequence
            )

            return new_id

    def _wait_for_next_millis(self, last_timestamp):
        """等待下一毫秒"""
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            time.sleep(0.001)
            timestamp = int(time.time() * 1000)
        return timestamp

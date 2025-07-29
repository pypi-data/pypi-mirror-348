import asyncio

from .aiohttp_session import post_to_loki


class AsyncFlushManager:
    def __init__(self, logger):
        self.logger = logger
        self._flush_task: asyncio.Task | None = None

    def check_and_flush(self):
        if len(self.logger.log_buffer) >= self.logger.options.batch_size:
            asyncio.create_task(self.logger.flush_logs())
        else:
            self._schedule_flush()

    def _schedule_flush(self):
        if self._flush_task and not self._flush_task.done():
            return
        self._flush_task = asyncio.create_task(self._delayed_flush())

    async def _delayed_flush(self):
        await asyncio.sleep(self.logger.options.flush_interval)
        await self.logger.flush_logs()

    async def send_logs(self, buffer_copy):
        await post_to_loki(buffer_copy, self.logger.options)

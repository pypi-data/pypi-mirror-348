# togou/file_writer.py

import os
import json
import pickle
import time
import asyncio
import threading
import multiprocessing
import logging
from typing import Any, Union

import aiofiles
from redlock import Redlock


class SafeFileWriter:
    def __init__(
        self,
        redis_servers=None,
        max_retries=5,
        retry_delay=0.2,
        log_level=logging.INFO,
        encoding="utf-8",
    ):
        """
        安全文件写入器，支持分布式锁、本地多线程/多进程锁、异步写入。
        """
        self.redis_servers = redis_servers or [{"host": "localhost", "port": 6379, "db": 0}]
        self.redlock = Redlock(self.redis_servers)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.encoding = encoding

        # 本地锁（防止线程/进程冲突）
        self.thread_lock = threading.Lock()
        self.process_lock = multiprocessing.Lock()
        self.async_lock = asyncio.Lock()

        # 日志设置
        self.logger = logging.getLogger("SafeFileWriter")
        self.logger.setLevel(log_level)
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _acquire_distributed_lock(self, resource_key):
        for attempt in range(self.max_retries + 1):
            dist_lock = self.redlock.lock(resource_key, ttl=30000)  # 30 秒锁
            if dist_lock:
                self.logger.debug(f"Acquired distributed lock for: {resource_key}")
                return dist_lock
            if attempt < self.max_retries:
                self.logger.warning(f"Lock failed for {resource_key}, retrying...")
                time.sleep(self.retry_delay)
            else:
                raise RuntimeError(f"Unable to acquire distributed lock: {resource_key}")

    def _release_distributed_lock(self, dist_lock):
        try:
            self.redlock.unlock(dist_lock)
            self.logger.debug("Released distributed lock")
        except Exception as e:
            self.logger.error(f"Error releasing distributed lock: {e}")

    def _ensure_path_exists(self, file_path):
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                self.logger.info(f"Created directory: {dir_path}")
            except Exception as e:
                raise PermissionError(f"Cannot create directory {dir_path}: {e}")
        if os.path.exists(file_path) and not os.access(file_path, os.W_OK):
            raise PermissionError(f"No write access to file: {file_path}")

    def _serialize_content(self, content: Any, mode: str = "json") -> Union[str, bytes]:
        if isinstance(content, (str, bytes)):
            return content
        if mode == "json":
            return json.dumps(content, ensure_ascii=False)
        elif mode == "pickle":
            return pickle.dumps(content)
        elif mode == "raw":
            return str(content)
        else:
            raise ValueError(f"Unsupported serialization mode: {mode}")

    def write(
        self,
        file_path: str,
        content: Any,
        mode: str = "a",
        serialize: str = "json",
        binary: bool = False,
    ):
        """
        同步写入接口（自动判断当前是否在异步环境）。
        """
        try:
            loop = asyncio.get_event_loop()
            if asyncio.current_task(loop):
                return self.write_async(file_path, content, mode, serialize, binary)
        except RuntimeError:
            pass  # 非异步环境

        with self.thread_lock:
            with self.process_lock:
                self._ensure_path_exists(file_path)
                dist_lock = self._acquire_distributed_lock(file_path)
                try:
                    data = self._serialize_content(content, serialize)
                    write_mode = mode + "b" if isinstance(data, bytes) or binary else mode

                    with open(file_path, write_mode, encoding=None if binary else self.encoding) as f:
                        f.write(data)
                    self.logger.info(f"Wrote to file: {file_path}")
                finally:
                    self._release_distributed_lock(dist_lock)

    async def write_async(
        self,
        file_path: str,
        content: Any,
        mode: str = "a",
        serialize: str = "json",
        binary: bool = False,
    ):
        """
        异步写入接口（带 asyncio 协程锁保护）。
        """
        async with self.async_lock:
            self._ensure_path_exists(file_path)
            data = self._serialize_content(content, serialize)
            write_mode = mode + "b" if isinstance(data, bytes) or binary else mode

            loop = asyncio.get_event_loop()
            dist_lock = await loop.run_in_executor(None, self._acquire_distributed_lock, file_path)
            try:
                async with aiofiles.open(file_path, write_mode, encoding=None if binary else self.encoding) as f:
                    await f.write(data)
                self.logger.info(f"Wrote to file: {file_path}")
            finally:
                await loop.run_in_executor(None, self._release_distributed_lock, dist_lock)

    def write_lines(
            self,
            file_path: str,
            lines: list[str],
            mode: str = "a",
            binary: bool = False,
    ):
        """
        批量写入多行文本（同步）。
        默认每行末尾自动补 \n。
        """
        content = "\n".join(lines) + "\n"
        self.write(
            file_path=file_path,
            content=content,
            mode=mode,
            serialize="raw",
            binary=binary,
        )

    async def write_lines_async(
            self,
            file_path: str,
            lines: list[str],
            mode: str = "a",
            binary: bool = False,
    ):
        """
        批量写入多行文本（异步）。
        默认每行末尾自动补 \n。
        """
        content = "\n".join(lines) + "\n"
        await self.write_async(
            file_path=file_path,
            content=content,
            mode=mode,
            serialize="raw",
            binary=binary,
        )

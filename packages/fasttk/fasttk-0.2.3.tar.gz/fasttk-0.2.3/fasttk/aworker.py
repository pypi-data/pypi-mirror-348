
import asyncio
import logging
from uuid import uuid4 as random_uuid, UUID
from threading import Thread
from queue import Queue as TQueue, Empty
from typing import Coroutine, Callable, Any
from tkinter import Tk

logger = logging.getLogger("FastTk.AsyncWorker")

class AsyncWorker:
    
    _thread: Thread
    _queue: TQueue[tuple[Coroutine, UUID] | None]
    _callback: TQueue[tuple[UUID, bool, Any] | None]
    _closed: bool
    _checker_id: str
    _root: Tk
    _mapping: dict[UUID, tuple[Callable, Callable]]

    def __init__(self, root: Tk):
        self._thread = Thread(target=self._entrance, name="fasttk.AsyncWorker")
        self._queue = TQueue()
        self._callback = TQueue()
        self._closed = False
        self._checker_id = root.after_idle(self.checker)
        self._root = root
        self._mapping = {}
    
    def checker(self) -> None:
        try:
            pack = self._callback.get_nowait()
            self._callback.task_done()
            if not pack:
                return None
            uuid, use_result, args = pack
            then, err = self._mapping.pop(uuid)
            if use_result:
                try:
                    then(args)
                except Exception as e:
                    err(e)
            else:
                err(args)
        except Empty:
            self._checker_id = self._root.after(1, self.checker)
        except Exception:
            logger.error(
                "Error occurred during AsyncWorker callback:",
                exc_info=True
            )
            self._checker_id = self._root.after_idle(self.checker)
        else:
            self._checker_id = self._root.after_idle(self.checker)

    async def _async_worker(self):
        while True:
            pack = await asyncio.to_thread(self._queue.get)
            self._queue.task_done()
            if not pack:
                break
            task, uuid = pack
            try:
                result = await task
                self._callback.put((uuid, True, result))
            except Exception as e:
                self._callback.put((uuid, False, e))

    def _entrance(self):
        logger = logging.getLogger("FastTk.AsyncWorker.Thread")
        logger.info("Start asyncio thread.")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._async_worker())
        finally:
            loop.stop()
            loop.close()
        logger.info("Asyncio thread exited.")
        
    
    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        if not self._closed:
            self._closed = True
            logger.info("Stopping AsyncWorker.")
            self._root.after_cancel(self._checker_id)
            self._queue.put(None)
            self._thread.join()

    def run(self, task: Coroutine, then: Callable, error: Callable) -> None:
        uuid = random_uuid()
        self._mapping[uuid] = (then, error)
        self._queue.put((task, uuid))


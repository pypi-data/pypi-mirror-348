"""
A simple, built-in logging server
"""

from __future__ import annotations
from typing import Optional, List, Tuple

import struct
import pickle
import asyncio
import logging
from threading import Thread
from queue import Queue, Empty

LOG = logging.getLogger(__name__)


class LogServer:
    """A simple, internal logging server that reinjects remote log messages

    Each submodule of palaestrAI that gets spawned lives in a separate
    process. As the ::`~spawn_wrapper` takes care of reinitializing the
    logger, it replaces all defined log handlers with a
    :py:class:`logging.SocketHandler`. This log server is ran by the
    ::`Executor` and receives all those messages. They are re-injected in the
    main process' logging system and treated according to the original
    logging configuration.
    """

    def __init__(self, listen_host: str, listen_port: int):
        """Constructs a new log server for a given address and port

        Parameters
        ----------
        listen_host : str
            The address the log server should bind to
        listen_port : int
            The port the log server should bind to
        """
        self._listen_host = listen_host
        self._listen_port = listen_port
        self._server = None
        self._clients: List[Tuple] = []
        self._obj_queue: Queue = Queue()
        self._running = True
        self._spiller_thread: Optional[Thread] = None

    def _add_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        LOG.debug(
            "LogServer(id=0x%x) registered a new client (%s, %s).",
            id(self),
            reader,
            writer,
        )
        self._clients.append(
            (
                reader,
                writer,
                asyncio.create_task(self._read_from_client(reader)),
            )
        )

    def _spill_messages(self):
        while self._running or not self._obj_queue.empty():
            try:
                logobj = self._obj_queue.get(block=True, timeout=0.1)
            except Empty:
                continue
            record = logging.makeLogRecord(logobj)
            LOG.debug("LogServer received new record: %s", record)
            logging.getLogger(record.name).handle(record)

    async def _read_from_client(self, reader: asyncio.StreamReader):
        while True:
            chunk = await reader.read(4)
            msglen = struct.unpack(">L", chunk)[0]
            chunk = await reader.read(msglen)
            while len(chunk) < msglen:
                chunk = chunk + await reader.read(msglen - len(chunk))
            try:
                logobj = pickle.loads(chunk)
                if not logobj:
                    continue
                self._obj_queue.put(logobj)
            except:
                continue

    async def start(self):
        self._spiller_thread = Thread(target=self._spill_messages)
        self._spiller_thread.start()
        self._server = await asyncio.start_server(
            self._add_client,
            host=self._listen_host,
            port=self._listen_port,
        )
        await self._server.start_serving()

    async def stop(self):
        self._running = False
        self._server.close()
        for reader, writer, task in self._clients:
            task.cancel()
            writer.close()
        await self._server.wait_closed()
        self._spiller_thread.join()

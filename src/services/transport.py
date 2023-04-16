import abc
import asyncio
from asyncio import StreamReader, StreamWriter


class SCPI(abc.ABC):
    delimiter: str

    @abc.abstractmethod
    async def write(self, command: str) -> str:
        ...

    @abc.abstractmethod
    async def query(self, command: str, timeout: int = 1) -> str:
        ...

    @abc.abstractmethod
    async def read(self) -> str:
        ...

    @abc.abstractmethod
    def clear_command(self, command: str) -> str:
        ...


class TCPTransport(SCPI):
    delimiter: str = '\n'
    _reader: StreamReader
    _writer: StreamWriter
    _chunk_size: int = 20 * 1024

    def __init__(self, host: str, port: str) -> None:
        # TODO Добавить обработку ошибок
        self._reader, self._writer = asyncio.open_connection(host, port)

    async def _write(self, command: str) -> None:
        self._writer.write(command.encode())
        await self._writer.drain()

    async def _read(self) -> str:
        data = await self._reader.read(self._chunk_size)
        return data.decode()

    async def write(self, command: str) -> None:
        await self._write(self.clear_command(command))

    async def read(self) -> str:
        return await self._read()

    async def query(self, command: str, timeout: int = 1) -> str:
        await self.write(command)
        await asyncio.sleep(timeout)
        return await self.read()

    def clear_command(self, command: str) -> str:
        return command + self.delimiter


class TestTransport(SCPI):
    delimiter: str = '\n'

    def __init__(self, reader: dict) -> None:
        self._writer = {}
        self._reader = reader
        self._read_count = 1

    async def write(self, command: str) -> None:
        self._writer[len(self._writer) + 1] = self.clear_command(command)

    async def read(self) -> str:
        data = self._reader[self._read_count]
        self._read_count += 1
        if self._read_count > 3:
            self._read_count = 1
        return data

    async def query(self, command: str, timeout: int = 0.01) -> str:
        await self.write(command)
        await asyncio.sleep(timeout)
        return await self.read()

    def clear_command(self, command: str) -> str:
        return command + self.delimiter

    @property
    def writer(self) -> dict:
        return self._writer

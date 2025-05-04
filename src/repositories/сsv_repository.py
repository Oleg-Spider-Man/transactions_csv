import os
from abc import ABC, abstractmethod
from typing import AsyncIterator

import aiofiles


# определить репозиторий и сервис для ксв после чата серв и репо
class AbstractCsvRepository(ABC):
    @abstractmethod
    async def check_file(self, file_path: str):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

    @abstractmethod
    async def check_headers(self, file_path: str) -> str:
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

    @abstractmethod
    async def get_rows(self, file_path: str) -> AsyncIterator[str]:
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


# 1 - проверка наличия файла. 2 - заголовки. 3 - цикл по строкам генератор.


class CsvFileRepository(AbstractCsvRepository):
    async def check_file(self, file_path: str):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        return "файл найден"

    async def check_headers(self, file_path: str) -> str:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            header_line = await f.readline()
            return header_line

    async def get_rows(self, file_path: str) -> AsyncIterator[str]:
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
            await f.readline()  # Пропускаем заголовок
            # async for line in f:
            #     yield line.strip()
            while True:
                line = await f.readline()
                if not line:
                    break
                yield line.strip()

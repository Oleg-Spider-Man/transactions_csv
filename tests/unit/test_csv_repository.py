import pytest
from src.repositories.сsv_repository import CsvFileRepository


test_args = ["--file", "src/test.csv", "--start_date", "2023-10-01", "--end_date", "2023-10-03"]


@pytest.mark.asyncio
async def test_csv_check_file():

    repo = CsvFileRepository()  # фикстуру для репо или вверху
    result_check_file = await repo.check_file(test_args[1])
    assert result_check_file == "файл найден"

    with pytest.raises(FileNotFoundError) as exc_info:
        await repo.check_file(test_args[2])
    assert str(exc_info.value) == "Файл не найден: --start_date"


@pytest.mark.asyncio
async def test_csv_check_headers():
    repo = CsvFileRepository()
    result_check_file = await repo.check_headers(test_args[1])
    assert result_check_file == "date,category,amount,description"


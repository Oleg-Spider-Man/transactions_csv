import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Анализ финансовых транзакций')
    parser.add_argument('--file', required=True, help='Путь к CSV файлу')
    parser.add_argument('--start_date', help='Дата начала периода (YYYY-MM-DD)')
    parser.add_argument('--end_date', help='Дата конца периода (YYYY-MM-DD)')

    return parser.parse_args()

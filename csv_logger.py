import csv
from datetime import datetime
from pathlib import Path
from typing import Literal


class OperationLogger:
    def __init__(self, csv_file: str = "twitter_operations.csv"):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.csv_path = self.log_dir / csv_file
        self._ensure_headers()

    def _ensure_headers(self):
        if not self.csv_path.exists():
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'operation',
                    'success',
                    'target_profile',
                    'details',
                    'session_total'
                ])

    def log_operation(
        self,
        operation: Literal['follow', 'unfollow'],
        success: bool,
        target_profile: str = '',
        details: str = '',
        session_total: int = 0
    ):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                operation,
                success,
                target_profile,
                details,
                session_total
            ])

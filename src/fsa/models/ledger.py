import logging
from typing import Union
import csv
import pathlib
from fsa.settings import BASE_URL
from fsa.exceptions import LedgerExecption
from fsa.utils.request_utils import requests_retry_session

logger = logging.getLogger(__name__)


class Ledger:
    api_endpoint = f"{BASE_URL}/ledger"

    def __init__(self, account):
        self.account = account

    @property
    def balance(self) -> float:
        """Find the last transaction and report the balance

        Returns
            float
        """
        params = dict(account_id=self.account.id)
        response = requests_retry_session().get(self.api_endpoint, params=params)
        data = response.json()
        if not data:
            return 0
        return float(data[-1].get("balance"))

    @property
    def records(self) -> dict:
        """Query ledger records from API by account id

        Returns
            List[Dict] : ledger records
        """
        params = dict(account_id=self.account.id)
        response = requests_retry_session().get(self.api_endpoint, params=params)
        return response.json()

    def append(self, account_id, record_date, credit=0, debit=0, memo="") -> dict:
        """Create a ledger entry

        Args
            account_id (int)        : account the ledger entry belongs to
            record_date (datetime)  : record date of ledger entry
            credit (float)          : amount gte zero
            debit (float)           : amount gte zero
            memo (str)              : optional text to help describe ledger entry

        Returns
            json response as dict containing the ledger record data
        """
        payload = dict(
            account_id=account_id,
            record_date=record_date,
            credit=credit,
            debit=debit,
            balance=self.balance + credit - debit,
            memo=memo,
        )
        response = requests_retry_session().post(self.api_endpoint, data=payload)
        return response.json()

    def to_csv(self, csv_dir: Union[str, pathlib.Path], stem: str = "export") -> None:
        """Export account ledger to csv

        Args
            csv_dir : path to export directory
            stem    : file stem of csv report

        Returns
            None

        Raises
            LedgerException : raised when the directory assigned to csv export path is not valid
        """
        exportable_path = False
        file_name = f"{stem}.csv"
        csv_path = None

        if isinstance(csv_dir, pathlib.Path):
            csv_path = csv_dir / file_name
            exportable_path = csv_dir.exists()

        elif isinstance(csv_dir, str):
            csv_path = pathlib.Path(csv_dir) / file_name
            exportable_path = csv_path.parent.exists()

        if not exportable_path:
            raise LedgerExecption(f"invalid ledger export path: {csv_dir}")

        with open(csv_path, "w") as f_out:
            _records = self.records
            fieldnames = _records[0].keys()
            dict_writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(_records)

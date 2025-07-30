import datetime as dt
import re
from pathlib import Path

from ynab_unlinked.context_object import YnabUnlinkedContext
from ynab_unlinked.models import Transaction

ANCHOR_LINE = "FECHA|CONCEPTO|LOCALIDAD|IMPORTE"
TRANSACTION_PATTER = re.compile(r"^(\d{2}/\d{2})\|(.+?)\|.+?\|(.*EUR).*")


class SabadellParser:
    def parse(
        self, input_file: Path, context: YnabUnlinkedContext
    ) -> list[Transaction]:
        lines = input_file.read_text(encoding="cp1252").splitlines()
        start = False
        transactions: list[Transaction] = []
        for line in lines:
            if ANCHOR_LINE in line:
                start = True
                continue

            if not start:
                continue

            if groups := TRANSACTION_PATTER.match(line):
                transactions.append(
                    Transaction(
                        date=self.__parse_date(groups[1]),
                        payee=self.__parse_payee(groups[2]),
                        amount=-self.__parse_amount(groups[3]),
                    )
                )
            else:
                start = False

        return transactions

    def __parse_date(self, raw: str) -> dt.date:
        current_year = dt.date.today().year
        return dt.datetime.strptime(f"{raw}/{current_year}", "%d/%m/%Y").date()

    def __parse_payee(self, raw: str) -> str:
        return raw.title()

    def __parse_amount(self, raw: str) -> float:
        return float(raw.replace("EUR", "").replace(",", "."))

    def name(self) -> str:
        return "sabadell"

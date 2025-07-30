import datetime as dt
from collections.abc import Generator
from pathlib import Path

import typer
from rich import print
from rich.prompt import Confirm, Prompt
from rich.status import Status

from ynab_unlinked import display
from ynab_unlinked.config import (
    TRANSACTION_GRACE_PERIOD_DAYS,
    Checkpoint,
    Config,
    EntityConfig,
)
from ynab_unlinked.context_object import YnabUnlinkedContext
from ynab_unlinked.entities import Entity
from ynab_unlinked.exceptions import ParsingError
from ynab_unlinked.matcher import match_transactions
from ynab_unlinked.models import MatchStatus, Transaction, TransactionWithYnabData
from ynab_unlinked.payee import set_payee_from_ynab
from ynab_unlinked.ynab_api.client import Client

# Request transactions to the YNAB API from the last checkpoint date minus 10 days for buffer
TRANSACTIONS_DAYES_BEFORE_LAST_EXTRACTION = 10


def add_past_to_transactions(
    transactions: list[Transaction], checkpoint: Checkpoint | None
):
    if checkpoint is None:
        return

    for t in transactions:
        if t.date < checkpoint.latest_date_processed + dt.timedelta(
            days=TRANSACTION_GRACE_PERIOD_DAYS
        ):
            t.past = True


def add_counter_to_existing_transactions(transactions: list[Transaction]):
    """
    This method check every transaction that has the same date, payee and amount
    and increments its counter to ensure that they have a unique import ID when
    being added to YNAB.
    """
    counters: dict[str, int] = {}
    for t in transactions:
        if t.id not in counters:
            counters[t.id] = 0
        else:
            counters[t.id] += 1
            t.counter = counters[t.id]


def preprocess_transactions(
    transactions: list[Transaction], checkpoint: Checkpoint | None
):
    add_past_to_transactions(transactions, checkpoint)
    add_counter_to_existing_transactions(transactions)


def filter_transactions(
    transactions: list[Transaction], checkpoint: Checkpoint | None
) -> Generator[Transaction]:
    if checkpoint is None:
        yield from transactions
        return

    yield from (t for t in transactions if t.date >= checkpoint.latest_date_processed)


def get_or_prompt_account_id(config: Config, entity_name: str) -> str:
    if entity_name in config.entities:
        return config.entities[entity_name].account_id

    print(f"Lets select the account for {entity_name.capitalize()}:")
    client = Client(config)

    accounts = [acc for acc in client.accounts() if not acc.closed]

    for idx, acc in enumerate(accounts):
        print(f" - {idx + 1}. {acc.name}")

    acc_num = Prompt.ask(
        "What account are the transactions going to be imported to? (By number)",
        choices=[str(i) for i in range(1, len(accounts) + 1)],
        show_choices=False,
    )
    account = accounts[int(acc_num) - 1]

    print(f"[bold]Account selected: {account.name}")

    config.entities[entity_name] = EntityConfig(account_id=account.id)
    config.save()

    return account.id


def process_transactions(
    entity: Entity,
    input_file: Path,
    context: YnabUnlinkedContext,
) -> None:
    """
    Process the transactions from the input file, match them with YNAB data, and upload them to YNAB.

    If the Entity calling this method does not have a config stored, the user will be prompted to select an account
    this entity should publish transactions to. This account will be used moving forward when using this entity.

    If the user called `yul -a` the user will always be promptped to select
    and account and the selected account won't be saved for this particular entity.
    """

    config = context.config
    show = context.show
    reconcile = context.reconcile

    acount_id = get_or_prompt_account_id(config, entity.name())

    try:
        parsed_input = entity.parse(input_file, context)
    except ParsingError as e:
        print(f"[bold red] Error when parsing {e.input_file}")
        print(f"  Message: {e.message}")
        raise typer.Exit(1) from e

    checkpoint = config.entities[entity.name()].checkpoint

    preprocess_transactions(parsed_input, checkpoint)

    if show:
        display.transaction_table(parsed_input)
        return

    transactions = [
        TransactionWithYnabData(t)
        for t in filter_transactions(
            parsed_input,
            checkpoint,
        )
    ]

    client = Client(config)

    with Status("Reading transactions..."):
        ynab_transactions = client.transactions(
            account_id=acount_id,
            since_date=(
                checkpoint.latest_date_processed
                - dt.timedelta(days=TRANSACTIONS_DAYES_BEFORE_LAST_EXTRACTION)
                if checkpoint
                else None
            ),
        )
    print("[bold green]✔ Transactions read")

    with Status("Augmenting transactions..."):
        match_transactions(transactions, ynab_transactions, reconcile, config)
        set_payee_from_ynab(transactions, client, config)
    print("[bold green]✔ Transactions augmneted with YNAB information")

    display.transactions_to_upload(transactions)

    if not any(t.needs_creation for t in transactions):
        print("[bold blue]🎉 All done! Nothing to do.")
        config.update_and_save(transactions[0], entity.name())
        return

    if partial_matches := [
        t
        for t in transactions
        if t.match_status is MatchStatus.PARTIAL_MATCH and t.needs_creation
    ]:
        display.partial_matches(partial_matches)
        print(
            "\nIf these partial matches are ok, you can accept them and we will keep track of the "
            "payee name for future reference."
        )
        final_matching = (
            MatchStatus.MATCHED
            if Confirm.ask("Do you want to accept these matches?")
            else MatchStatus.UNMATCHED
        )
        for t in partial_matches:
            t.match_status = final_matching
            if final_matching == MatchStatus.UNMATCHED:
                t.reset_matching()

        if final_matching == MatchStatus.MATCHED:
            # If the user agreed to match these, add renaming rules to config
            config.add_payee_rules(partial_matches)

    with Status("Preparing transactions to upload..."):
        new_transactions = [t for t in transactions if t.needs_creation]

    print(f"[bold]Transactions to import:       {len(new_transactions)}")

    if Confirm.ask("Do you want to continue and create the transactions?"):
        with Status("Creating/Updating transactions..."):
            client.create_transactions(acount_id, new_transactions)

        config.update_and_save(transactions[0], entity.name())

    print("[bold blue]🎉 All done!")

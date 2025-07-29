import asyncio
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Annotated

import typer

from mm_okx.cli import commands

app = typer.Typer(no_args_is_help=True, help="Account API commands")

AccountArg = Annotated[Path, typer.Argument(help="Path to account TOML file")]


def decimal_parser(value: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation:
        raise typer.BadParameter(f"Invalid decimal: {value}") from None


@app.command(name="buy-market")
def buy_market_command(
    account: AccountArg, inst_id: Annotated[str, typer.Option()], sz: Annotated[Decimal, typer.Option(parser=decimal_parser)]
) -> None:
    asyncio.run(commands.account.buy_market.run(account, inst_id, sz))


@app.command(name="currencies")
def currencies_command(account: AccountArg, ccy: Annotated[str | None, typer.Option()] = None) -> None:
    asyncio.run(commands.account.currencies.run(account, ccy))


@app.command(name="deposit-address")
def deposit_address_command(account: AccountArg, ccy: Annotated[str, typer.Option()]) -> None:
    asyncio.run(commands.account.deposit_address.run(account, ccy))


@app.command(name="deposit-history")
def deposit_history_command(account: AccountArg, ccy: Annotated[str | None, typer.Option()] = None) -> None:
    asyncio.run(commands.account.deposit_history.run(account, ccy))


@app.command(name="funding-balances")
def funding_balances_command(account: AccountArg, ccy: Annotated[str | None, typer.Option()] = None) -> None:
    asyncio.run(commands.account.funding_balances.run(account, ccy))


@app.command(name="order-history")
def order_history_command(account: AccountArg, inst_id: Annotated[str | None, typer.Option()] = None) -> None:
    asyncio.run(commands.account.order_history.run(account, inst_id))


@app.command(name="sell-market")
def sell_market_command(
    account: AccountArg, inst_id: Annotated[str, typer.Option()], sz: Annotated[Decimal, typer.Option(parser=decimal_parser)]
) -> None:
    asyncio.run(commands.account.sell_market.run(account, inst_id, sz))


@app.command(name="trading-balances")
def trading_balances_command(account: AccountArg, ccy: Annotated[str | None, typer.Option()] = None) -> None:
    asyncio.run(commands.account.trading_balances.run(account, ccy))


@app.command(name="transfer-to-funding")
def transfer_to_funding_command(
    account: AccountArg, ccy: Annotated[str, typer.Option()], amt: Annotated[Decimal, typer.Option(parser=decimal_parser)]
) -> None:
    asyncio.run(commands.account.transfer_to_funding.run(account, ccy, amt))


@app.command(name="transfer-to-trading")
def transfer_to_trading_command(
    account: AccountArg, ccy: Annotated[str, typer.Option()], amt: Annotated[Decimal, typer.Option(parser=decimal_parser)]
) -> None:
    asyncio.run(commands.account.transfer_to_trading.run(account, ccy, amt))


@app.command(name="withdraw")
def withdraw_command(
    account: AccountArg,
    ccy: Annotated[str, typer.Option()],
    amt: Annotated[Decimal, typer.Option(parser=decimal_parser)],
    fee: Annotated[Decimal, typer.Option(parser=decimal_parser)],
    to_addr: Annotated[str, typer.Option()],
    chain: Annotated[str | None, typer.Option()] = None,
) -> None:
    asyncio.run(commands.account.withdraw.run(account=account, ccy=ccy, amt=amt, fee=fee, to_addr=to_addr, chain=chain))


@app.command(name="withdraw-history")
def withdrawal_history_command(
    account: AccountArg, ccy: Annotated[str | None, typer.Option()] = None, wd_id: Annotated[str | None, typer.Option()] = None
) -> None:
    asyncio.run(commands.account.withdrawal_history.run(account, ccy, wd_id))

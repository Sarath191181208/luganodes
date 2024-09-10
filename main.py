import asyncio
from typing import List
from connection import LogsRPCRequestParams, send_track_deposits_request

from db import initialize_db, insert_deposit
from config import CONTRACT_ADDRESS
from models import Deposit


def save_deposits(deposits: List[Deposit]):
    for dep in deposits:
        insert_deposit(dep)


async def main():
    await send_track_deposits_request(
        LogsRPCRequestParams(address=CONTRACT_ADDRESS), save_deposits
    )


if __name__ == "__main__":
    initialize_db()
    asyncio.get_event_loop().run_until_complete(main())

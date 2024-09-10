import json
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass, field

import asyncio
import websockets

from config import MORALIS_API_KEY, WEBSOCKET_URL
from utils import remove_null_values
from models import Deposit

import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

from web3 import Web3
from moralis import evm_api

from config import CONTRACT_ADDRESS, CONTRACT_ABI, ALCHEMY_URL

w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


@dataclass
class LogsRPCRequestParams:
    address: Optional[str]
    topics: List[str] = field(default_factory=list)


async def send_json_rpc_request(request: Dict, callback_fn: Callable):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        try:
            await websocket.send(json.dumps(request))
            async for msg in websocket:
                logger.info("Received event")
                await callback_fn(msg)

        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
            raise


def get_logs_request(params: LogsRPCRequestParams) -> Dict:
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getLogs",
        "params": [
            {
                "address": params.address,
                "fromBlock": "0x13C1E44",
                "toBlock": "latest",  
                "topics": params.topics,  
            }
        ],
    }
    __import__("pprint").pprint(request)
    return request


def get_realtime_logs_request(params: LogsRPCRequestParams) -> Dict:
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": [
            "logs",
            remove_null_values(
                {
                    "address": params.address,
                    "topics": None if len(params.topics) == 0 else params.topics,
                }
            ),
        ],
    }
    __import__("pprint").pprint(request)
    return request


async def send_track_deposits_request(
    request_params: LogsRPCRequestParams,
    callback_fn: Callable[[List[Deposit]], None],
) -> None:
    # req = get_realtime_logs_request(request_params)
    req = get_logs_request(request_params)

    async def recv_req(data):
        # const decodedData = w3.eth.abi.decodeLog(EVENT_ABI, event.data, event.topics);
        # _data = data
        data = json.loads(data)
        print(data)
        if not "result" in data:
            return
        if len(data["result"]) < 1:
            return
        ids_list = []
        if len(data["result"]) > 1:
            for res in data["result"]:
                ids_list.append(res["blockNumber"])
        else:
            ids_list.append(data["params"]["result"]["blockNumber"])
        print(data)
        tasks = [extract_req_data(int(id.removeprefix("0x"), 16)) for id in ids_list[:2]]
        print(ids_list[:2])
        results = await ( asyncio.gather(*tasks ))
        results = [x for x in results if x is not None]
        print(results)
        deposits = [item for sublist in results for item in sublist]
        deposits = deposits if deposits is not None else []
        callback_fn(deposits)

    await send_json_rpc_request(req, recv_req)


async def extract_req_data(block_number: int) -> Optional[List[Deposit]]:
    params = {
        "chain": "eth",
        "include": "internal_transactions",
        "block_number_or_hash": str(block_number),
    }

    result = evm_api.block.get_block(
        api_key=MORALIS_API_KEY,
        params=params,  # type: ignore
    )

    if "transactions" not in result:
        return None

    with open(f"{block_number}.json", "w") as f:
        json.dump(result, f, indent=4)

    deposits = [
        Deposit(
            blockNumber=transaction["block_number"],
            blockTimestamp=transaction["block_timestamp"],
            pubkey=transaction["from_address"],
            hash=transaction["hash"],
            fee=transaction["transaction_fee"],
        )
        for transaction in result["transactions"]
    ]

    return deposits


if __name__ == "__main__":
    from config import CONTRACT_ADDRESS

    asyncio.get_event_loop().run_until_complete(
        send_track_deposits_request(
            LogsRPCRequestParams(address=CONTRACT_ADDRESS), lambda _: None
        )
    )

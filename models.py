from dataclasses import dataclass
from typing import List, Optional
import json

@dataclass
class Deposit:
    blockNumber: str
    blockTimestamp: str
    hash: str 
    fee: Optional[str] = None
    pubkey: Optional[str] = None

    @staticmethod
    def from_json(data):
        return Deposit(
            blockNumber=data['blockNumber'],
            blockTimestamp=data['blockTimestamp'],
            fee=data.get('fee'),
            hash=data['hash'],
            pubkey=data.get('pubkey')
        )

    def to_json(self):
        return {
            "blockNumber": self.blockNumber,
            "blockTimestamp": self.blockTimestamp,
            "fee": self.fee,
            "hash": self.hash,
            "pubkey": self.pubkey
        }

@dataclass
class Result:
    address: str
    blockHash: str
    blockNumber: str
    data: str
    logIndex: str
    topics: List[str]
    transactionHash: str
    transactionIndex: str

    @staticmethod
    def from_json(data):
        return Result(
            address=data['address'],
            blockHash=data['blockHash'],
            blockNumber=data['blockNumber'],
            data=data['data'],
            logIndex=data['logIndex'],
            topics=data['topics'],
            transactionHash=data['transactionHash'],
            transactionIndex=data['transactionIndex']
        )

    def to_json(self):
        return {
            "address": self.address,
            "blockHash": self.blockHash,
            "blockNumber": self.blockNumber,
            "data": self.data,
            "logIndex": self.logIndex,
            "topics": self.topics,
            "transactionHash": self.transactionHash,
            "transactionIndex": self.transactionIndex
        }

@dataclass
class Params:
    subscription: str
    result: Result

    @staticmethod
    def from_json(data):
        return Params(
            subscription=data['subscription'],
            result=Result.from_json(data['result'])
        )

    def to_json(self):
        return {
            "subscription": self.subscription,
            "result": self.result.to_json()
        }

@dataclass
class LogsWSSubscription:
    jsonrpc: str
    id: int
    params: Params

    @staticmethod
    def from_json(data):
        return LogsWSSubscription(
            jsonrpc=data['jsonrpc'],
            id=data['id'],
            params=Params.from_json(data['params'])
        )

    def to_json(self):
        return {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
            "params": self.params.to_json()
        }

if __name__ == "__main__":
    # Example JSON input
    json_data = '''{
        "jsonrpc":"2.0",
        "method":"eth_subscription",
        "params": {
            "subscription":"0x4a8a4c0517381924f9838102c5a4dcb7",
            "result":{
                "address":"0x8320fe7702b96808f7bbc0d4a888ed1468216cfd",
                "blockHash":"0x61cdb2a09ab99abf791d474f20c2ea89bf8de2923a2d42bb49944c8c993cbf04",
                "blockNumber":"0x29e87",
                "data":"0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000003",
                "logIndex":"0x0",
                "topics":["0xd78a0cb8bb633d06981248b816e7bd33c2a35a6089241d099fa519e361cab902"],
                "transactionHash":"0xe044554a0a55067caafd07f8020ab9f2af60bdfe337e395ecd84b4877a3d1ab4",
                "transactionIndex":"0x0"
            }
        }
    }'''

    # Deserialize JSON string to Python object
    eth_subscription_obj = LogsWSSubscription.from_json(json.loads(json_data))
    print(eth_subscription_obj)

    # Serialize Python object back to JSON string
    json_output = json.dumps(eth_subscription_obj.to_json(), indent=4)
    print(json_output)

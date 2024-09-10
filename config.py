import os
from dotenv import load_dotenv

load_dotenv()

_alchemy_api_key = os.environ.get("ALCHEMY_API_KEY", None)
_alchemy_ws_key = os.environ.get("ALCHEMY_WS_KEY", None)

if _alchemy_api_key is None:
    raise Exception(
        "The env variable `ALCHEMY_API_KEY` isn't defined try `source .env`"
    )
if _alchemy_ws_key is None:
    raise Exception("The env variable `ALCHEMY_WS_KEY` isn't defined try `source .env`")

_MORALIS_API_KEY = os.environ.get("MORALIS_API_KEY", None)

if _MORALIS_API_KEY is None:
    raise Exception("The env variable `MORALIS_API_KEY` isn't defined try `source .env`")

MORALIS_API_KEY = _MORALIS_API_KEY


# Connect to Alchemy's Ethereum node using HTTP Provider
ALCHEMY_URL = f"https://eth-mainnet.g.alchemy.com/v2/{_alchemy_api_key}"
WEBSOCKET_URL = f"wss://eth-mainnet.g.alchemy.com/v2/{_alchemy_ws_key}"

# Define the Beacon Deposit Contract address and ABI
CONTRACT_ADDRESS = "0x00000000219ab540356cBB839Cbe05303d7705Fa"

# f = urllib.request.urlopen(
#     "https://api.etherscan.io/api?module=contract&action=getabi&address=0x00000000219ab540356cbb839cbe05303d7705fa&APIKEY=P8RQCIYSKNFH66PHEUP4ZPVQ77NVIWSZYB"
# )
# CONTRACT_ABI = json.loads(json.load(f)["result"])

CONTRACT_ABI = [{
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "pubkey", "type": "bytes"},
        {"indexed": True, "name": "withdrawal_credentials", "type": "bytes"},
        {"indexed": False, "name": "amount", "type": "uint256"},
        {"indexed": False, "name": "signature", "type": "bytes"},
    ],
    "name": "DepositEvent",
    "type": "event",
}]

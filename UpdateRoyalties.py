import json
from api.metaplex_api import MetaplexAPI
from cryptography.fernet import Fernet
import base58
from solana.keypair import Keypair 
from solana.rpc.api import Client
from solana.transaction import Transaction, TransactionInstruction
from solana.system_program import *
from solana.rpc import types
import os
import time
import requests
import base64

from metaplex.metadata import (
    get_metadata_account,
    unpack_metadata_account,
)
from metaplex.transactions import update_token_metadata

privkey = ""
with open("key.txt", 'r') as outfile:
    privkey = outfile.readline()

byte_array = base58.b58decode(privkey)
account = Keypair().from_secret_key(byte_array)

api_endpoint4 = "https://free.rpcpool.com/"
api_endpoint3 = "https://ssc-dao.genesysgo.net/"
api_endpoint2 = "https://shy-wild-resonance.solana-mainnet.quiknode.pro/b71b11f1e1bb100d98f6340bc4ac8cd3c4aa77c8/"
api_endpoint = "https://solana-api.projectserum.com/"


var_targets = 5
var_timeout = 50
var_finalized = False

ref = "https://twitter.com"
rpc_endpoint = "https://solana-api.projectserum.com/"
header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Referrer': ref, 'Origin': ref}

#rpc_endpoint = "https://free.rpcpool.com/"
#header = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

#init metaplex-api
cfg = {"PRIVATE_KEY": base58.b58encode(account.secret_key).decode("ascii"), "PUBLIC_KEY": str(account.public_key), "DECRYPTION_KEY": Fernet.generate_key().decode("ascii")}
api = MetaplexAPI(cfg)
client = Client(api_endpoint)
signer = str(account.public_key)


def getMetadata(account):
    payload = '{"jsonrpc": "2.0","id": 1,"method": "getAccountInfo","params": ["' + str(account) + '", {"encoding": "jsonParsed"}]}'
    r = requests.post(rpc_endpoint, data=payload, headers=header, timeout=2)
    json = r.json()
    data = base64.b64decode(json["result"]['value']['data'][0])
    metadata = unpack_metadata_account(data)
    return metadata

##########################################
# START CONFIG
##########################################
new_fee = 9700 #97% to make purchases at secondary market possible (ME 2% fee, SA 3% fee)

new_authority = str(account.public_key)
update_authority = PublicKey(new_authority)

mints = [ "GFCy1NacyonbMoPtN7ng5bhwcJ9iJhcdAdyBWoy8FY37"
, "7UP2vUFGzWM84d2doUmDcrAGrdVsbqBUezQrFVqdpiAS"
, "B6asPZtzhRJBCdSHG8WqxPvd7qSikiZpyULJUiZJV9Ys"
]
##########################################
# END CONFIG
##########################################

for i in range(0, len(mints)):
    contract_key = mints[i]
    print(contract_key)

    mint = PublicKey(contract_key)
    acc = get_metadata_account(contract_key)
    metadata = getMetadata(acc)
    new_link = metadata["data"]["uri"]

    creators = []
    creators_share = []
    creators_verified = []
                    
    creators.append(new_authority)
    creators_share.append(100)
    creators_verified.append(True)

    res = api.update_token_metadata(api_endpoint, mint, new_link, metadata["data"], creators, creators_verified, creators_share, new_fee, 3, False, var_timeout, var_targets, var_finalized)
    result_tmp = json.loads(res)
    print(result_tmp)
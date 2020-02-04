from web3 import Web3, HTTPProvider
from django.contrib.staticfiles.storage import staticfiles_storage
import json
w3 = Web3(HTTPProvider('http://localhost:8545'))


def contract_deployed(name, address=None):
    with open(staticfiles_storage.path(name + ".json")) as f:
        info_json = json.load(f)

    try:
        abi = info_json["abi"]
        networks = list(info_json['networks'].values())
        if address is not None:
            _address = address
        else:
            _address = Web3.toChecksumAddress(networks[len(networks) - 1]['address'])
    except Exception as e:
        raise Exception("Cannot connect to deployed contact, check ABI: \n\n{}".format(e))

    return w3.eth.contract(address=_address, abi=abi)


def contract_to_deploy(name, from_address, params=None):
    with open(staticfiles_storage.path(name + ".json")) as f:
        info_json = json.load(f)
    abi = info_json["abi"]
    bytecode = info_json["bytecode"]

    # Create our contract class.
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # issue a transaction to deploy the contract.
    # tx_hash = contract.constructor().transact({
    #     'from': from_address,
    # })
    if params is not None:
        tx_hash = contract.constructor(*params).transact({"from": from_address})
    else:
        tx_hash = contract.constructor().transact({"from": from_address})
    # wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    return contract(tx_receipt.contractAddress), tx_hash

from dotenv import load_dotenv
import os

from web3 import Web3, HTTPProvider
from web3.datastructures import AttributeDict
from exceptions import ProviderNotConnectedError
from abi import getABI, getEvents
from mongo import DataBase
import pprint

load_dotenv()

contractAbi = getABI("Lootbox")
contractEvents = getEvents(abi=contractAbi, eventNames=("LootboxCreated"))

db = DataBase("TEST")
collection = db.get_collection("indexed_events")


def initializeConnection():
    infuraHTTPProvider = Web3(HTTPProvider(
        f'https://sepolia.infura.io/v3/{os.getenv("INFURA_KEY")}'))
    isConnected = infuraHTTPProvider.is_connected()

    if not isConnected:
        raise ProviderNotConnectedError
    else:
        return infuraHTTPProvider


def connectToContract(contract_address: str):
    provider = initializeConnection()
    return provider.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contractAbi)


def getAllContractEventsData(fromBlock: int = 0):
    contract = connectToContract(
        "0x61B8b65aA97D4A4eBFB590F2969AA5D0F337B212")

    allLogs = []

    for item in contractEvents:
        if 'event' in item:
            eventLogs = contract.events[item['event']].create_filter(
                fromBlock=fromBlock)
            entries = eventLogs.get_all_entries()

            for i in entries:
                item = dict(AttributeDict(i))
                node = {
                    **dict(AttributeDict(item['args'])),
                    'blockNumber': item['blockNumber']
                }

                for it in node.keys():
                    if isinstance(node[it], list):
                        itemsFormatted = []

                        for n in node[it]:
                            if isinstance(n, AttributeDict):
                                itemToDict = dict(AttributeDict(n))
                                itemsFormatted.append(itemToDict)
                            else:
                                itemsFormatted.append(n)

                        node[it] = itemsFormatted
                    elif isinstance(node[it], AttributeDict):
                        node[it] = dict(AttributeDict(node[it]))

                allLogs.append(node)

    result = collection.insert_many(allLogs)
    pprint.pp(result)


if __name__ == '__main__':
    getAllContractEventsData()

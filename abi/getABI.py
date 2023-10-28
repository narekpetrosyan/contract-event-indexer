import json
import os


def getABI(abiFileName: str = ""):
    if not abiFileName:
        raise Exception("ABI file name not provided")

    filePath = os.path.join("contracts/", f"{abiFileName}.json")
    with open(filePath) as f:
        info_json = json.load(f)
    return info_json

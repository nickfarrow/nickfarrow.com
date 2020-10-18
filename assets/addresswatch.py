import subprocess
import requests
import time
import argparse

# ETHERSCAN API KEY
API_KEY = "F9XFJY5G3GVIS1VQC6WD8N8B5BA9PGN4SU"

# Argument parser
parser = argparse.ArgumentParser("Watch ERC-20 send txs from an address and sound alarms")
parser.add_argument("-a", "--address", default="0xeb31973e0febf3e3d7058234a5ebbae1ab4b8c23", help="Watch address")
parser.add_argument("-b", "--block", default="1", help="Start block, send txs after this block height will sound the alarm.")
args = parser.parse_args()

address = args.address
block = args.block

# Linux / Mac(?)
def beep():
    cmd = "mpg123 ./gold_please.mp3"
    for i in range(3):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(2)
        p.kill()
    print("BEEP")
    return

# WINDOWS
# import winsound
# def beep():
#   winsound.Beep(2500, 100)
#   return

def get_eth_txn_status(txnid, block):

    etherscan_url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock={block}&sort=asc&apikey={API_KEY}'

    etherscan_response = requests.get(etherscan_url).json()
    #print(etherscan_response)
    result = etherscan_response['result']

    for i in range(len(result)):
        for key in etherscan_response['result'][i].keys():
            print(key, etherscan_response['result'][i][key])
        print("\n\n")

        if etherscan_response['result'][i]['from'] == address:
            beep()
            block = etherscan_response['result'][i]['blockNumber']
            block = str(int(block)+1)
            print("\n\n\n")

    return block

beep()

i = 0
while True:
    try:
        i += 1
        print("Checking...{}, {}".format(i, block))
        block = get_eth_txn_status("", block)
        time.sleep(20)
    except Exception as e:
        print(e)
        continue

from web3 import Web3
from web3.middleware import geth_poa_middleware

from contract import abi, api

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware,layer=0)

contract = w3.eth.contract(address=api,abi=abi)

# print(w3.eth.get_balance('0x259D7eD76c37E4559A4d71bb65e2F36cc5C44acD'))
# print(w3.eth.get_balance('0xeF94E7Af0aD60f9c0b8e1A8075443C719f4f3021'))
# print(w3.eth.get_balance('0x5dfCDe5456EA8ab34C2e0817076c93B7848d298d'))
# print(w3.eth.get_balance('0x5aBBAD597462089571F475ABbb70270993dB2D19'))
# print(w3.eth.get_balance('0xD2D9fD9a871c4c5e5763370FC447c3328999b786'))

#0x08eD5eD02c68fe8c17fFC3538Ec627e92eE1d74a
#hjvctysd3264GFDSt?
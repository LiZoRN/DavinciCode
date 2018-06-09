# _*_ coding: utf-8 _*_
__author__ = 'lizorn'
__date__ = '2018/6/7 16:00'

from web3 import Web3
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
print(web3.eth.getBlock('latest'))
print(web3.eth.getBlock(0))
print(web3.eth.blockNumber)

from connection import contract
from utils import catch


@catch("Ошибка при создании недвижимости: ")
def createEstate(public_key, size, photo, rooms, estate_type):
    tx = contract.functions.createEstate(size, photo, rooms, estate_type).transact(
        {'from': public_key})


@catch("Ошибка при создании объявления:")
def createAd(public_key,estate_id, price):
    tx = contract.functions.createAd(estate_id, price).transact({'from': public_key})


@catch("Ошибка при изменении статуса недвижимости:")
def updateEstateStatus(public_key,estate_id,new_status):
    tx = contract.functions.updateEstateStatus(estate_id, bool(new_status)).transact({'from': public_key})



@catch("Ошибка при изменении статуса объявления:")
def updateAdStatus(public_key,ad_id,new_status):
    tx = contract.functions.updateAdStatus(ad_id, bool(new_status)).transact({'from': public_key})


@catch("Ошибка при покупке недвижимости:")
def buyEstate(public_key,ad_id,price):
    tx = contract.functions.buyEstate(ad_id).transact({'from': public_key, 'value': price})

@catch("Ошибка при получении баланса:")
def getBalance(public_key):
    return contract.functions.getBalance(public_key).call()



@catch("Ошибка при выводе средств:")
def withDraw(public_key,amount):
    return contract.functions.withDraw(amount).transact({'from': public_key})


@catch("Ошибка при получении информации о недвижимости:")
def getEstates():
    return contract.functions.getEstates().call()



@catch("Ошибка при получении информации о объявлениях:")
def getAds():
    return contract.functions.getAds().call()



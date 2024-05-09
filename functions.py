from connection import contract
from consts import EstateType, Status
from utils import catch, pretty_estate, pretty_ad


@catch("Ошибка при создании недвижимости: ")
def createEstate(public_key):
    size = int(input("Введите размер недвижимости м^2: "))
    photo = input("Введите URL изображения недвижимости: ")
    rooms = int(input("Введите количество комнат: "))
    estate_type = input("Введите тип недвижимости (House, Flat, Loft): ")

    tx = contract.functions.createEstate(size, photo, rooms, EstateType.get(estate_type.lower())).transact(
        {'from': public_key})

    print("Создано. Хеш транзакции: %s" % tx.hex())


@catch("Ошибка при создании объявления:")
def createAd(public_key):
    estate_id = int(input("Введите ID недвижимости: "))
    price = int(input("Введите цену недвижимости в wei: "))

    tx = contract.functions.createAd(estate_id, price).transact({'from': public_key})
    print("Создано. Хеш транзакции: %s" % tx.hex())


@catch("Ошибка при изменении статуса недвижимости:")
def updateEstateStatus(public_key):
    estate_id = int(input("Введите ID недвижимости: "))
    new_status = input("Введите новый статус (closed, opened): ")

    tx = contract.functions.updateEstateStatus(estate_id, Status.get(new_status.lower())).transact({'from': public_key})
    print("Обновлено. Хеш транзакции: %s" % tx.hex())


@catch("Ошибка при изменении статуса объявления:")
def updateAdStatus(public_key):
    ad_id = int(input("Введите ID объявления: "))
    new_status = input("Введите новый статус (closed, opened): ")

    tx = contract.functions.updateAdStatus(ad_id, Status.get(new_status.lower())).transact({'from': public_key})
    print("Обновлено. Хеш транзакции: %s" % tx.hex())


@catch("Ошибка при покупке недвижимости:")
def buyEstate(public_key):
    ad_id = int(input("Введите ID объявления, по которому вы хотите купить недвижимость: "))
    price = int(input("Введите цену покупки в wei: "))

    tx = contract.functions.buyEstate(ad_id).transact({'from': public_key, 'value': price})
    print("Оплата прошла успешно. Хеш транзакции: %s" % tx.hex())


@catch("Ошибка при получении баланса:")
def getBalance(public_key):
    balance = contract.functions.getBalance(public_key).call()
    print(f"Ваш баланс на смарт-контракте: {int(balance)} wei")


@catch("Ошибка при выводе средств:")
def withDraw(public_key):
    amount = int(input("Введите сумму для вывода в wei: "))

    tx = contract.functions.withDraw(amount).transact({'from': public_key})
    print("Вывод успешен. Хеш транзакции: %s" % tx.hex())


@catch("Ошибка при получении информации о недвижимости:")
def getEstates(public_key):
    estates = contract.functions.getEstates().call()
    print("Доступные недвижимости: " + ("" if len(estates) else "нет"))
    for estate in estates: pretty_estate(estate)


@catch("Ошибка при получении информации о объявлениях:")
def getAds(public_key):
    ads = contract.functions.getAds().call()
    print("Доступные объявления: " + ("" if len(ads) else "нет"))
    for ind, ad in enumerate(ads):
        print(f"{ind}. ", end="")
        pretty_ad(ad)

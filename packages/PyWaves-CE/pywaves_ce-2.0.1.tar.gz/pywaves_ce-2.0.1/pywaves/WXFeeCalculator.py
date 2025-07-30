import pywaves as pw
import requests
import math

class WXFeeCalculator(object):

    priceConstantExp = 8
    discountAssetDecimals = 8
    #baseFee = 1000000

    def __init__(self):
        self.settings = requests.get(pw.MATCHER + '/matcher/settings').json()
        self.matcher = pw.MATCHER
        self.node = pw.NODE
        self.baseFee = self.settings['orderFee']['composite']['default']['dynamic']['baseFee']

    def _correctRate(self, rate, assetDecimals):
        return rate * math.pow(10, (assetDecimals - self.priceConstantExp))

    def _getAssetDecimals(self, assetId):
        if assetId == pw.DEFAULT_CURRENCY: #'WAVES':
            return 8
        else:
            assetInfo = requests.get(self.node + '/assets/details/' + assetId).json()

            return assetInfo['decimals']

    def _getMinFee(self, assetId):
        assetRate = self.settings['rates'][assetId]

        return int(self.baseFee * assetRate) + 1

    def _getMinFeeInDiscountAsset(self, assetId):
        discount = self.settings['orderFee']['composite']['discount']['value']
        discountAssetRate = self.settings['rates'][assetId]

        return int(self.baseFee * discountAssetRate * (100 - discount) / 100) + 1

    def calculateDynamicFee(self):
        return self.baseFee

    def calculateDynamicDiscountFee(self):
        discount = self.settings['orderFee']['composite']['discount']['value']
        discountAssetId = self.settings['orderFee']['composite']['discount']['assetId']
        discountAssetRate = self.settings['rates'][discountAssetId]
        correctedRate = self._correctRate(discountAssetRate, self.discountAssetDecimals)
        calculatedFee = int(self.baseFee * correctedRate * (100 - discount) / 100) + 1
        minFee = self._getMinFeeInDiscountAsset(discountAssetId)

        return max(calculatedFee, minFee)

    def calculatePercentSellingFee(self, priceAsset, amountAsset, amountToSell):
        minFee = self.settings['orderFee']['composite']['custom'][amountAsset + '-' + priceAsset]['percent']['minFee']
        calculatedFee = int(amountToSell * minFee / 100) + 1
        minFee = self._getMinFee(amountAsset)

        return max(calculatedFee, minFee)

    def calculatePercentDiscountedSellingFee(self, priceAssetId, amountAssetId, amountToSell):
        discount = self.settings['orderFee']['composite']['discount']['value']
        minFee = self.settings['orderFee']['composite']['custom'][amountAssetId + '-' + priceAssetId]['percent']['minFee']
        discountAssetId = self.settings['orderFee']['composite']['discount']['assetId']
        rates = self.settings['rates']
        discountAssetRate = self._correctRate(rates[discountAssetId], self.discountAssetDecimals)
        amountAssetDecimals = self._getAssetDecimals(amountAssetId)
        amountAssetRate = self._correctRate(rates[amountAssetId], amountAssetDecimals)
        calculatedFee = int(amountToSell * (minFee / 100) * (discountAssetRate / amountAssetRate) * (100 - discount) / 100) + 1
        minFee = self._getMinFeeInDiscountAsset(discountAssetId)

        return max(calculatedFee, minFee)

    def calculatePercentBuyingFee(self, amountAssetId, priceAssetId, price, amountToBuy):
        minFee = self.settings['orderFee']['composite']['custom'][amountAssetId + '-' + priceAssetId]['percent']['minFee']
        priceAssetDecimals = self._getAssetDecimals(priceAssetId)
        amountAssetDecimals = self._getAssetDecimals(amountAssetId)
        price = price / math.pow(10, priceAssetDecimals)
        amount = amountToBuy / math.pow(10, amountAssetDecimals)
        calculatedFee = amount * price * minFee / 100
        calculatedFee = int(calculatedFee * math.pow(10, priceAssetDecimals))
        minFee = self._getMinFee(priceAssetId)

        return int(max(calculatedFee, minFee))

    def calculatePercentDiscountedBuyingFee(self, priceAssetId, price, amountToBuy):
        discount = self.settings['orderFee']['composite']['discount']['value']
        discountAssetId = self.settings['orderFee']['composite']['discount']['assetId']
        rates = self.settings['rates']
        discountAssetRate = self._correctRate(rates[discountAssetId], self.discountAssetDecimals)
        priceAssetDecimals = self._getAssetDecimals(priceAssetId)
        price = price / math.pow(10, priceAssetDecimals)
        priceAssetRate = self._correctRate(rates[priceAssetId], priceAssetDecimals)
        calculatedFee = int(amountToBuy * price / math.pow(10, self.priceConstantExp) * self.baseFee / 100 * (discountAssetRate / priceAssetRate) * (100 - discount) / 100) + 1
        minFee = self._getMinFeeInDiscountAsset(discountAssetId)

        return max(calculatedFee, minFee)

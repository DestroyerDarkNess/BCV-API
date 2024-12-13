import aiohttp
from typing import Dict, Optional
from bs4 import BeautifulSoup

class MoneyData:
    def __init__(self):
        self.ID = ""
        self.Icon = ""
        self.Value = ""
        
class NetworkResult:
    def __init__(self):
        self.HTMLSource = None
        self.IsSuccessStatusCode = False
        self.StatusCode = None
        
class BCV:
    def __init__(self):
        self.Base = "https://www.bcv.org.ve/"
        self.MoneyIDList = ["euro", "yuan", "lira", "rublo", "dolar"]

    async def get_data(self) -> Optional[Dict[str, MoneyData]]:
        result = None
        response = await self.get_web_page(self.Base)
        
        if response is None or not response.IsSuccessStatusCode:
            return result

        result = {}
        document = BeautifulSoup(response.HTMLSource, 'html.parser')

        for money_id in self.MoneyIDList:
            money_element = document.find(id=money_id)
            if money_element is not None:
                money_data = self.get_money_data(money_element)
                if money_data is not None:
                    result[money_id] = money_data

        return result

    async def get_web_page(self, url_target: str) -> NetworkResult:
        try:
            result = NetworkResult()
            async with aiohttp.ClientSession() as session:
                async with session.get(url_target, ssl=False) as response:
                    if response.status == 200:
                        content = await response.text()
                        result.HTMLSource = content
                        result.IsSuccessStatusCode = True
                    else:
                        result.StatusCode = response.status
            return result
        except Exception as e:
            return None

    def get_money_data(self, parent_element) -> Optional[MoneyData]:
        try:
            row = parent_element.find(class_="field-content")
            id_ = row.find("span").text
            img_url = self.Base + row.find("img")["src"]
            value = row.find("strong").text

            money_data = MoneyData()
            money_data.ID = id_
            money_data.Icon = img_url
            money_data.Value = value

            return money_data

        except Exception:
            return None


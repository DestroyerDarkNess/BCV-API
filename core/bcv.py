import asyncio
from typing import Dict, Optional
from bs4 import BeautifulSoup
import requests

class MoneyData:
    def __init__(self):
        self.ID = ""
        self.Icon = ""
        self.Value = ""

class BCV:
    def __init__(self):
        self.Base = "https://www.bcv.org.ve/"
        self.MoneyIDList = ["euro", "yuan", "lira", "rublo", "dolar"]

    async def get_data(self) -> Optional[Dict[str, MoneyData]]:
        result = None
        response = await self.get_web_page(self.Base)

        if response is None:
            return result

        if response.status_code == 200:
            result = {}

            document = BeautifulSoup(response.text, 'html.parser')

            for money_id in self.MoneyIDList:
                money_element = document.find(id=money_id)
                if money_element is not None:
                    money_data = self.get_money_data(money_element)
                    if money_data is not None:
                        result[money_id] = money_data

        return result

    async def get_web_page(self, url: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, requests.get, url)

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


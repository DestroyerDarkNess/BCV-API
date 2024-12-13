import asyncio
from core.bcv import BCV

async def main():
    bcv = BCV()
    data = await bcv.get_data()

    if data:
        for money_id, money_data in data.items():
            print(f"ID: {money_data.ID}")
            print(f"Icon URL: {money_data.Icon}")
            print(f"Value: {money_data.Value}")
            if money_data.Date is not None:
                print(f"Date: {money_data.Date.strftime('%A, %d %B %Y')}")
            print("-" * 20)
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    asyncio.run(main())

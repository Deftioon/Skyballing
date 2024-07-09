import requests
import typing
import base64
import json

with open("src\skyballing\modifiers.json", "r") as file:
    const = json.load(file)

class Query:
    @staticmethod
    def create_line(value):
        line = const[value]
        return f'"{list(line.keys())[0]}":"{list(line.values())[0]}"'
    
    @staticmethod
    def create_query(*args: typing.Tuple[str]):
        output = ""
        for i in args:
            output += Query.create_line(i) + ","
        output = output[:-1]
        output = f'{{{output}}}'
        return output
    
    @staticmethod
    def create_encoded_query(*args: typing.Tuple[str]):
        query = Query.create_query(*args)
        return str(Query.encode(query))[2:-1]
    
    def create_dict_query(*args: typing.Tuple[str]):
        query = Query.create_query(*args)
        dicts = json.loads(query)
        # jsons = json.dumps(dicts)
        return dicts
    
    @staticmethod
    def generate_url(item: str, *args: typing.Tuple[str]):
        query = Query.create_encoded_query(*args)
        return f"https://sky.coflnet.com/item/{item}/?itemFilter={query}&range=active"
    
    def generate_queried_url(item: str, *args: typing.Tuple[str]):
        query = Query.create_encoded_query(*args)
        return f"https://sky.coflnet.com/api/auctions/tag/{item}/recent/overview?query={query}"

    def generate_simple_url(item: str):
        return f"https://sky.coflnet.com/api/auctions/tag/{item}/recent/overview"
    
    @staticmethod
    def get_queried_recent(item: str, *args: typing.Tuple[str]):
        query = Query.create_dict_query(*args)
        params = query
        url = f"https://sky.coflnet.com/api/auctions/tag/{item}/recent/overview"
        return requests.get(url, params=params).json()
    
    @staticmethod
    def get_queried(item: str, *args: typing.Tuple[str]):
        url = Query.generate_queried_url(item, *args)
        return requests.get(url).json()
    
    @staticmethod
    def decode(data: str):
        data = data + "=" * (4 - len(data) % 4)
        return base64.b64decode(data).decode("utf-8")
    
    @staticmethod
    def encode(data: str):
        return base64.b64encode(data.encode("utf-8"))
    
    def main(mode: str):
        if mode == "manual":
            item = input("Enter the item name: ")
            modifiers = tuple(input("Enter the modifiers: ").split(" "))
            extras = int(input("Enter any extra price modifiers: "))

            url = Query.generate_url(item, *modifiers)
            print(url)

            day_avg = int(input("Enter the average price for the day: ")) + extras
            week_avg = int(input("Enter the average price for the week: ")) + extras
            month_avg = int(input("Enter the average price for the month: ")) + extras

            price_list = [day_avg, week_avg, month_avg]
            sorted_price = sorted(price_list)
            avg_price = 0.1 * sorted_price[-1] + 0.3 * sorted_price[-2] + 0.6 * sorted_price[-3]

            margin = 0.97
            taxed = Prices.after_tax(avg_price)

            print(f"Estimated Value: {avg_price}\nAfter Tax: {taxed}\nMargin: {1 - margin}%\nLowball Price: {margin * taxed}" )

        elif mode == "auto":
            item = input("Enter the item name: ")
            modifiers = tuple(input("Enter the modifiers: ").split(" "))

            url = Query.create_query(item, *modifiers)   
            price = requests.get(url).json()
            # TODO finish this

class Prices:
    @staticmethod
    def calc_avg(data: dict, key: str):
            total = 0
            for i in data:
                total += i[key]
            return total / len(data)
    
    @staticmethod
    def after_tax(price: int):
        if price < 10_000_000:
            return price * 0.99
        elif price < 100_000_000:
            return price * 0.98
        else:
            return price * 0.975
        
    @staticmethod
    def get_price_hist(item: str):
        current = requests.get(f"https://sky.coflnet.com/api/item/price/{item}/current").json()
        day = requests.get(f"https://sky.coflnet.com/api/item/price/{item}/history/day").json()
        week = requests.get(f"https://sky.coflnet.com/api/item/price/{item}/history/week").json()
        month = requests.get(f"https://sky.coflnet.com/api/item/price/{item}/history/month").json()
    
        current_avg = (current["buy"] + current["sell"]) / 2
        day_avg = Prices.calc_avg(day, "avg")
        week_avg = Prices.calc_avg(week, "avg")
        month_avg = Prices.calc_avg(month, "avg")
    
        return [current_avg, day_avg, week_avg, month_avg]
    
    @staticmethod
    def get_recent(item, *args):
        url = Query.generate_simple_url(item)
        data = requests.get(url).json()
        return data

    @staticmethod
    def recent_prices(item, *args):
        data = Query.get_queried_recent(item, *args)
        price_avg = Prices.calc_avg(data, "price")

        return price_avg
    
    @staticmethod
    def recent_prices_new(item, *args):
        data = Query.get_queried(item, *args)
        price_avg = Prices.calc_avg(data, "price")

        return price_avg
    
print(Prices.recent_prices("SUPERIOR_DRAGON_HELMET", "MYTHIC"))
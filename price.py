import requests 

def get_coin_price(coin_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")
    

if __name__ == "__main__":
    get_coin_price(coin_id="bitcoin", currency="usd")
    get_coin_price(coin_id="ethereum", currency="usd")
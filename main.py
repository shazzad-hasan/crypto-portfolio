import requests 
import sqlite3
import datetime
import database
import csv
import argparse

conn = sqlite3.connect("portfolio.db")
c = conn.cursor()

def get_coin_price(coin_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    return coin_price

def show_coin_price(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")

def add_investment(coin_id, currency, amount, sell, price):
    insert_query = "INSERT INTO investments VALUES (?,?,?,?,?,?);"
    values = (coin_id, currency, amount, sell, price, datetime.datetime.now())
    
    c.execute(insert_query, values)
    conn.commit()

    if sell:
        print(f"Added sell of {amount} {coin_id}")
    else:
        print(f"Added buy of {amount} {coin_id}")

def get_investment_value(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    read_query = """
        SELECT amount FROM investments
        WHERE coin_id=? AND currency=? AND sell=?;
    """
    buy_result = c.execute(read_query, (coin_id, currency, False)).fetchall()
    sell_result = c.execute(read_query, (coin_id, currency, True)).fetchall()

    buy_amount = sum([row[0] for row in buy_result])
    sell_amount = sum([row[0] for row in sell_result])
    total = buy_amount - sell_amount

    print(f"You have a total of {total} {coin_id} worth {total * coin_price} {currency.upper()}")

def main():
    parser = argparse.ArgumentParser(description="Manage cryptocurrency investments.")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for adding investment
    add_parser = subparsers.add_parser("add", help="Add a new investment")
    add_parser.add_argument("coin_id", type=str, help="ID of the coin")
    add_parser.add_argument("currency", type=str, help="Currency")
    add_parser.add_argument("amount", type=float, help="Amount of the coin")
    add_parser.add_argument("sell", type=int, choices=[0, 1], help="0 for buy, 1 for sell")
    add_parser.add_argument("price", type=float, help="Price of the coin")

    # Subparser for getting investment value
    value_parser = subparsers.add_parser("value", help="Get the value of an investment")
    value_parser.add_argument("coin_id", type=str, help="ID of the coin")
    value_parser.add_argument("currency", type=str, help="Currency")

    args = parser.parse_args()

    if args.command == "add":
        add_investment(args.coin_id, args.currency, args.amount, args.sell, args.price)
    elif args.command == "value":
        get_investment_value(args.coin_id, args.currency)
    else:
        parser.print_help()

    # Close the connection
    c.close()
    conn.close()

    
if __name__ == "__main__":
    main()
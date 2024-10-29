import csv
import random
from datetime import datetime, timedelta 

coins = ['Bitcoins', 'Ethereum', 'Thther', 'BNB', 'Solona', 
         'USDC', 'XRP', 'Dogecoin', 'Toncoin', 'TRON']

def generate_data(num_rows):
    data = []
    for _ in range(num_rows):
        coin_id = random.choice(coins)
        currency = 'usd'
        amount = round(random.uniform(0.1, 20.0), 2)
        sell = random.randint(0, 1)
        price = round(random.uniform(500, 50000), 2)
        timestamp =datetime.now() + timedelta(seconds=random.randint(0, 1000))
        data.append([coin_id, currency, amount, sell, price, timestamp])
    return data 


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['coin_id', 'currency', 'amount', 'sell', 'price', 'date'])
        csvwriter.writerows(data)
    print(f"Data successfully written to {filename}.")


if __name__=="__main__":
    data = generate_data(30)
    save_to_csv(data, "investments.csv")
import sqlite3 
from datetime import datetime 
import csv

conn = sqlite3.connect("portfolio.db")
c = conn.cursor()

# Create investments table
def create_table():
    create_table_query = """
    CREATE TABLE investments (
        coin_id TEXT,
        currency TEXT,
        amount REAL,
        sell INT,
        price REAL,
        date TIMESTAMP
    );
    """
    c.execute(create_table_query)
    conn.commit()

def import_data_from_csv(file):
    with open(file, "r") as csvfile:
        csv_rdr = csv.reader(csvfile)
        next(csv_rdr)

        insert_query = """
            INSERT INTO investments (coin_id, currency, amount, sell, price, date) 
            VALUES (?, ?, ?, ?, ?, ?);
        """
        for row in csv_rdr:
            coin_id = row[0]
            currency = row[1]
            amount = float(row[2])
            sell = int(row[3])
            price = float(row[4])
            date = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S.%f')
            c.execute(insert_query, (coin_id, currency, amount, sell, price, date))
        conn.commit()

if __name__=="__main__":
    create_table()
    import_data_from_csv("investments.csv")

    # Close the connection
    c.close()
    conn.close()

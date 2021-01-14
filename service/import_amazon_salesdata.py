import tkinter as tk
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl import Workbook
import sqlite3
import datetime
from pathlib import Path
import sys
from tkmacosx import Button
import caribou

exchange_rate = {
    "EUR": "7.72",
    "GBP": "8.52",
    "USD": "6.88",
    "JPY": "0.064",
    "CAD": "5.27",
}

exchange_rate_currency = [
    "EUR",
    "GBP",
    "USD",
    "JPY",
    "CAD"
]


def import_amazon_salesdata(reports_file_path, dbdir, example_dir):
    conn = sqlite3.connect(dbdir)
    c = conn.cursor()
    file_list = os.listdir(reports_file_path)
    file_counter = 0

    for filename in file_list:
        if filename.endswith(".csv"):
            try:
                c.execute(
                    "SELECT * FROM imported_files WHERE file_name=?", (filename,))
                if c.fetchone() is None:
                    c.execute("INSERT INTO imported_files VALUES (?,?)",
                              (filename, datetime.date.today()))
                    file_counter += 1

                    df = pd.read_csv(os.path.join(
                        reports_file_path, filename), sep='\t')

                    try:
                        df.drop_duplicates('amazon-order-id',
                                           keep='first', inplace=True)
                        df.dropna(0, how='any', subset=[
                            'item-price'], inplace=True)
                        df.dropna(0, how='any', subset=[
                            'currency'], inplace=True)
                        df.dropna(0, how='any', subset=[
                            'quantity-shipped'], inplace=True)

                        df = df.drop(
                            df[~df.currency .isin(exchange_rate_currency)].index)

                    except Exception as ex:
                        print("data operation error: " + str(ex))
                    try:
                        df = df[df['item-price'] != 0]
                    except:
                        print("type error")
                for index, row in df.iterrows():
                    unit_price = round(float(row['item-price']) * float(
                        exchange_rate.get(row['currency'])) / int(row['quantity-shipped']), 2)
                    c.execute("""
                            INSERT INTO sales(
                                client,
                                amazon_order_id,
                                product_name,
                                quantity,
                                unit_price,
                                purchase_date,
                                logistics,
                                logistics_number,
                                receiver,
                                receiver_address,
                                original_unit_price,
                                original_currency,
                                sales_channel,
                                ship_address_1,
                                ship_address_2,
                                ship_address_3,
                                ship_city,
                                ship_state,
                                ship_postal_code,
                                ship_country,
                                buyer_name
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                              (
                                  filename,
                                  row['amazon-order-id'],
                                  row['product-name'],
                                  row['quantity-shipped'],
                                  unit_price,
                                  row['purchase-date'],
                                  row['carrier'],
                                  row['tracking-number'],
                                  row['recipient-name'],
                                  str(row['ship-address-1']) + str(row['ship-address-2']) + str(row['ship-address-3']) + str(
                                      row['ship-city']) + str(row['ship-state']) + str(row['ship-postal-code']) + str(row['ship-country']),
                                  row['item-price'] /
                                  row['quantity-shipped'],
                                  row['currency'],
                                  row['sales-channel'],
                                  row['ship-address-1'],
                                  row['ship-address-2'],
                                  row['ship-address-3'],
                                  row['ship-city'],
                                  row['ship-state'],
                                  row['ship-postal-code'],
                                  row['ship-country'],
                                  row['buyer-name'],
                              )
                              )
                    conn.commit()
            except Exception as e:

                print(
                    f"error importing transaction: " + str(e))

    c.execute(
        "SELECT SUM(unit_price * quantity) from sales WHERE assignment IS NULL")
    fetchResult = c.fetchone()
    conn.close()
    if fetchResult[0] == None:
        return {
            "title": "Currenxie",
            "message": f"error"
        }
    return {
        "title": "Currenxie",
        "message": f"{file_counter} has been imported \nThe Remaining sales data: {round(fetchResult[0],2)}"
    }

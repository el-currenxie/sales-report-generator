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


def generate_sales_report(trade_file, dbdir, example_dir):
    conn = sqlite3.connect(dbdir)
    c = conn.cursor()

    df = pd.read_csv(trade_file)
    wb = load_workbook(example_dir)
    ws = wb.active

    # check the remaining sales
    c.execute(
        "SELECT SUM(unit_price * quantity) FROM sales WHERE assignment IS NULL")

    if c.fetchone() < df.Amount.sum():
        return {
            "title": "Error",
            "message": "Not Enough Sales Data"
        }

    c.execute("SELECT id FROM sales WHERE assignment IS NULL ORDER BY id LIMIT 1")

    current_id = int(c.fetchone()[0])

    for index, row in df.iterrows():
        trade_reference = row['Serial No.']
        beneficiary_name = row['Beneficiary Name']
        trade_amount = round(row['Amount'] / 1.0015, 5)
        beneficiary_id = str(row['ID No.'])
        mobile = str(row['Mobile'])

        while trade_amount > 0:
            c.execute(
                "SELECT id, amazon_order_id, product_name, quantity, unit_price, purchase_date FROM sales WHERE id =? LIMIT 1", (current_id, ))

            try:
                id, order_id, product_name, quantity, unit_price, purchase_date = c.fetchone()
            except Exception as e:
                return {
                    "title": "ERROR",
                    "message": str(e)
                }

            unit_price = round(unit_price, 2)
            product_name = str(product_name)[:34]
            total_price = unit_price * quantity
            purchase_date = purchase_date[:10].replace('-', '')

            if trade_amount > total_price:
                trade_amount = trade_amount - total_price

            else:
                unit_price = round(trade_amount, 2)
                total_price = round(trade_amount, 2)
                quantity = 1
                trade_amount = 0
            try:
                c.execute("UPDATE sales SET assignment =? WHERE id =?",
                          (trade_reference, id))
            except Exception as e:
                return {
                    "title": "ERROR",
                    "message": str(e)
                }

            current_id += 1

            ws.append([order_id, purchase_date, beneficiary_name, beneficiary_id, "CNY", total_price,
                       "香港", "CURRENXIE LIMITED", "478788634943", "货物贸易", product_name, quantity, unit_price, '', '', '', product_name, mobile, 'Amazon'])

    wb.save(os.path.join(Path.home(), "Desktop", "FUIOU-sales-report.xlsx"))
    conn.commit()
    conn.close()
    return {
        "title": "Currenxie",
        "message": "DONE"
    }

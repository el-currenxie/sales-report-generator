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


def generate_payeco_sales_report(trade_file, dbdir, example_dir):
    conn = sqlite3.connect(dbdir)
    c = conn.cursor()

    df = pd.read_csv(trade_file)
    wb = Workbook()
    ws = wb.active
    ws.append([
        "amazon-order-item-id",
        "purchase-date",
        "product-name",
        "quantity-shipped",
        "currency",
        "item-price",
        "carrier",
        "tracking-number",
        "sales-channel",
        "indicative_fx_rate",
        "total_amount",
        "payment_signature_id",
        "seller_identifier",
        "beneficiary_name",
        "beneficiary_id",
        "ship_address_1",
        "ship_address_2",
        "ship_address_3",
        "ship_city",
        "ship_state",
        "ship_postal_code",
        "ship_country",
        "buyer_name",
    ])

    # check the remaining sales
    c.execute(
        "SELECT SUM(unit_price * quantity) FROM sales WHERE payeco_assignment IS NULL")

    if c.fetchone() < df.Amount.sum():
        return {
            "title": "Error",
            "message": "Not Enough Sales Data"
        }

    c.execute(
        "SELECT id FROM sales WHERE payeco_assignment IS NULL ORDER BY id LIMIT 1")

    current_id = int(c.fetchone()[0])

    for index, row in df.iterrows():
        trade_reference = row['Serial No.']
        beneficiary_name = row['Beneficiary Name']
        trade_amount = round(row['Amount'] * 1.0005, 5)
        beneficiary_id = str(row['ID No.'])
        client_abbreviation = row['Trx Description']

        while trade_amount > 0:
            c.execute("""
            SELECT
                id,
                amazon_order_id,
                product_name,
                quantity,
                unit_price,
                purchase_date,
                original_currency,
                original_unit_price,
                logistics,
                logistics_number,
                sales_channel,
                ship_address_1,
                ship_address_2,
                ship_address_3,
                ship_city,
                ship_state,
                ship_postal_code,
                ship_country,
                buyer_name
            FROM sales
            WHERE id =? LIMIT 1
            """, (current_id, ))

            try:
                (
                    id,
                    order_id,
                    product_name,
                    quantity,
                    unit_price,
                    purchase_date,
                    original_currency,
                    original_unit_price,
                    logistics,
                    logistics_number,
                    sales_channel,
                    ship_address_1,
                    ship_address_2,
                    ship_address_3,
                    ship_city,
                    ship_state,
                    ship_postal_code,
                    ship_country,
                    buyer_name,
                ) = c.fetchone()
            except Exception as e:
                return {
                    "title": "ERROR",
                    "message": str(e)
                }
            unit_price = round(unit_price, 5)
            product_name = str(product_name)[:34]
            total_price = unit_price * quantity

            if trade_amount > total_price:
                trade_amount = trade_amount - total_price

            else:
                unit_price = round(trade_amount, 5)
                total_price = round(trade_amount, 5)
                quantity = 1
                trade_amount = 0
            try:
                c.execute(
                    "UPDATE sales SET payeco_assignment =? WHERE id =?", (trade_reference, id))
            except Exception as e:
                return {
                    "title": "ERROR",
                    "message": str(e)
                }

            current_id += 1

            ws.append([
                order_id,
                purchase_date,
                product_name,
                quantity,
                original_currency,
                original_unit_price,
                logistics,
                logistics_number, sales_channel,
                exchange_rate.get(original_currency),
                total_price,
                trade_reference,
                client_abbreviation,
                beneficiary_name,
                beneficiary_id,
                ship_address_1,
                ship_address_2,
                ship_address_3,
                ship_city,
                ship_state,
                ship_postal_code,
                ship_country,
                buyer_name,
            ])

    wb.save(os.path.join(Path.home(), "Desktop", "Payeco-sales-report.xlsx"))
    conn.commit()
    conn.close()
    return {
        "title": "Currenxie",
        "message": "DONE"
    }

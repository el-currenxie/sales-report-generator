import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
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

# read amazon sales report
# check if the file has been imported before
# call db function to store the necessary info

#update db > report remaining sales vol

#check remaining sales vol before executing


exchange_rate = {
    "EUR": "7.72",
    "GBP": "8.52",
    "USD": "6.88",
    "JPY": "0.064",
    "CAD": "5.27",
}

dbdir = os.path.join(Path.home(),'Desktop','sales.db')

if hasattr(sys, "_MEIPASS"):
    example_dir = os.path.join(sys._MEIPASS, 'example_receipt.xlsx')
else:
    example_dir = 'example_receipt.xlsx'


def import_amazon_salesdata(reports_file_path):
    conn = sqlite3.connect(dbdir)
    c = conn.cursor()
    file_list = os.listdir(reports_file_path)
    file_counter = 0

    for filename in file_list:
        if filename.endswith(".csv"):
            c.execute("SELECT * FROM imported_files WHERE file_name=?", (filename,))
            if c.fetchone() is None:
                c.execute("INSERT INTO imported_files VALUES (?,?)", (filename, datetime.date.today()))
                file_counter += 1

                df = pd.read_csv(os.path.join(reports_file_path,filename), sep='\t')

                try:
                    df.drop_duplicates('amazon-order-id', keep='first', inplace=True)
                    df.dropna(0, how='any', subset= ['item-price'], inplace = True)
                    df.dropna(0, how='any', subset=['currency'], inplace=True)
                    df.dropna(0, how='any', subset=['quantity-shipped'], inplace=True)
                except:
                    print("data operation error")
                try:
                    df = df[df['item-price'] != 0]
                except:
                    print("type error")

                for index, row in df.iterrows():            
                    try:

                        unit_price = round(float(row['item-price']) * float(exchange_rate.get(row['currency'])) / int(row['quantity-shipped']),2)
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
                                str(row['ship-address-1']) + str(row['ship-address-2']) + str(row['ship-address-3']) + str(row['ship-city']) + str(row['ship-state']) + str(row['ship-postal-code']) + str(row['ship-country']),
                                row['item-price']/row['quantity-shipped'],
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
                    except:
                        print(f"error importing transaction {row['amazon-order-id']}")
    conn.commit()
    c.execute("SELECT SUM(unit_price * quantity) from sales WHERE assignment IS NULL")
    messagebox.showinfo("Currenxie", f"{file_counter} has been imported \nThe Remaining sales data: {round(c.fetchone()[0],2)}")
    conn.close()

def generate_sales_report(trade_file):
    conn = sqlite3.connect(dbdir)
    c = conn.cursor()

    df = pd.read_csv(trade_file)
    wb = load_workbook(example_dir)
    ws = wb.active

    # check the remaining sales
    c.execute("SELECT SUM(unit_price * quantity) FROM sales WHERE assignment IS NULL")

    if c.fetchone() < df.Amount.sum():
        messagebox.showinfo("Currenxie", "Not Enough Sales Data")
        return

    c.execute("SELECT id FROM sales WHERE assignment IS NULL ORDER BY id LIMIT 1")

    current_id = int(c.fetchone()[0])
    print(current_id)

    for index, row in df.iterrows():
        trade_reference = row['Serial No.']
        beneficiary_name = row['Beneficiary Name']
        trade_amount = round(row['Amount'] / 1.0015, 5)
        beneficiary_id = str(row['ID No.'])



        while trade_amount > 0:
            c.execute("SELECT id, amazon_order_id, product_name, quantity, unit_price, purchase_date FROM sales WHERE id =? LIMIT 1", (current_id, ))

            try:
                id, order_id, product_name, quantity, unit_price, purchase_date = c.fetchone()
            except:
                messagebox.showinfo("Currenxie", "ERROR")
            unit_price = round(unit_price,2)
            product_name = str(product_name)[:34]
            total_price = unit_price * quantity
            purchase_date = purchase_date[:10].replace('-', '')


            if trade_amount > total_price:
                trade_amount = trade_amount - total_price


            else:
                unit_price = round(trade_amount,2)
                total_price = round(trade_amount,2)
                quantity = 1
                trade_amount = 0
            try:
                c.execute("UPDATE sales SET assignment =? WHERE id =?", (trade_reference, id))
            except:
                messagebox.showinfo("Currenxie", "ERROR")

            current_id += 1

            ws.append([order_id, purchase_date, beneficiary_name, beneficiary_id, "CNY", total_price, "香港", "CURRENXIE LIMITED", "478788634943", "货物贸易", product_name, quantity, unit_price])



    wb.save(os.path.join(Path.home(),"Desktop","FUIOU-sales-report.xlsx"))
    conn.commit()
    conn.close()
    messagebox.showinfo("Currenxie", "DONE")

def generate_payeco_sales_report(trade_file):
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
    c.execute("SELECT SUM(unit_price * quantity) FROM sales WHERE payeco_assignment IS NULL")

    if c.fetchone() < df.Amount.sum():
        messagebox.showinfo("Currenxie", "Not Enough Sales Data")
        return

    c.execute("SELECT id FROM sales WHERE payeco_assignment IS NULL ORDER BY id LIMIT 1")

    current_id = int(c.fetchone()[0])
    print(current_id)

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
                )= c.fetchone()
            except:
                messagebox.showinfo("Currenxie", "ERROR")
            unit_price = round(unit_price,5)
            product_name = str(product_name)[:34]
            total_price = unit_price * quantity



            if trade_amount > total_price:
                trade_amount = trade_amount - total_price


            else:
                unit_price = round(trade_amount,5)
                total_price = round(trade_amount,5)
                quantity = 1
                trade_amount = 0
            try:
                c.execute("UPDATE sales SET payeco_assignment =? WHERE id =?", (trade_reference, id))
            except:
                messagebox.showinfo("Currenxie", "ERROR")

            current_id += 1

            ws.append([
                order_id, 
                purchase_date, 
                product_name, 
                quantity, 
                original_currency, 
                original_unit_price,
                logistics, 
                logistics_number,sales_channel, 
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


    wb.save(os.path.join(Path.home(),"Desktop","Payeco-sales-report.xlsx"))
    conn.commit()
    conn.close()
    messagebox.showinfo("Currenxie", "DONE")

def update_db_struct(version):
    print("migration")
    migrations_path= os.path.join(Path.home(),'Desktop', 'migrations')
    caribou.upgrade(db_url=dbdir, migration_dir=migrations_path, version=version)

    # # udpate record
    # reports_file_path = os.path.join(Path.home(),'Desktop','reports')
    # conn = sqlite3.connect(dbdir)
    # c = conn.cursor()
    # file_list = os.listdir(reports_file_path)
    # file_counter = 0

    # for filename in file_list:
    #     if filename.endswith(".csv"):
    #         c.execute("SELECT * FROM imported_files WHERE file_name=?", (filename,))
    #         if c.fetchone() is not None:
    #             df = pd.read_csv(os.path.join(reports_file_path,filename), sep='\t')

    #             try:
    #                 df.drop_duplicates('amazon-order-id', keep='first', inplace=True)
    #                 df.dropna(0, how='any', subset= ['item-price'], inplace = True)
    #                 df.dropna(0, how='any', subset=['currency'], inplace=True)
    #                 df.dropna(0, how='any', subset=['quantity-shipped'], inplace=True)
    #             except:
    #                 print("data operation error")
    #             try:
    #                 df = df[df['item-price'] != 0]
    #             except:
    #                 print("type error")

    #             for index, row in df.iterrows():            
    #                 try:
    #                     c.execute("""
    #                     update sales
    #                     set
    #                         ship_address_1,
    #                         ship_address_2,
    #                         ship_address_3,
    #                         ship_city,
    #                         ship_state,
    #                         ship_postal_code,
    #                         ship_country,
    #                         buyer_name
    #                     where amazon_order_id
    #                     """,
    #                     (
    #                         row['ship-address-1'],
    #                         row['ship-address-2'],
    #                         row['ship-address-3'],
    #                         row['ship-city'],
    #                         row['ship-state'],
    #                         row['ship-postal-code'],
    #                         row['ship-country'],
    #                         row['buyer-name'],
    #                         row['amazon-order-id']
    #                     ))
    #                 except:
    #                     print(f"error importing transaction {row['amazon-order-id']}")
    # conn.commit()
    # conn.close()
    print("finish")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.get_csv = Button(
            self,
            text='click Here to import sales data',
            command=self.update_db
        )    
        self.get_csv.pack(side="top")

        self.export_sales = Button(
            self,
            text='click Here to Genereate fuiou sales reports',
            command=self.get_sales_report
        )
        self.export_sales.pack(side="top")

        self.export_sales = Button(
            self, 
            text='click Here to Genereate Payeco sales reports',
            command=self.get_payeco_sales_report
        )
        self.export_sales.pack(side="top")

        self.export_sales = Button(
            self, 
            text='update_db_struct',
            command=self.updatupdate_db_structe_db
        )
        self.export_sales.pack(side="top")

        self.quit = Button(
            self, 
            text="QUIT", 
            fg="red", 
            command=self.master.destroy
        )
        self.quit.pack(side="bottom")

    def update_db(self):
        messagebox.showinfo("Currenxie", "Select your reports folder")
        reportsDir = filedialog.askdirectory()
        import_amazon_salesdata(reportsDir)

    def updatupdate_db_structe_db(self):
        update_db_struct("20191015121212")

    def get_sales_report(self):
        messagebox.showinfo("Currenxie", "Select your TRADES FILE")
        file_path = filedialog.askopenfilename()
        generate_sales_report(file_path)

    def get_payeco_sales_report(self):
        messagebox.showinfo("Currenxie", "Select your TRADES FILE")
        file_path = filedialog.askopenfilename()
        generate_payeco_sales_report(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('400x150')
    root.title('Currenxie Sales Generator')
    root.iconbitmap("logo.icns")
    app = Application(master=root)
    app.mainloop()  

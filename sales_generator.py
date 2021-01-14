import caribou
import datetime
import os
import pandas as pd
import sqlite3
import sys
import tkinter as tk
from pathlib import Path
from openpyxl import load_workbook
from openpyxl import Workbook
from tkinter import messagebox
from tkinter import filedialog
from tkmacosx import Button

from service.import_amazon_salesdata import import_amazon_salesdata
from service.generate_payeco_sales_report import generate_payeco_sales_report
from service.generate_sales_report import generate_sales_report
from service.update_db_struct import update_db_struct

# read amazon sales report
# check if the file has been imported before
# call db function to store the necessary info

# update db > report remaining sales vol

# check remaining sales vol before executing


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).parent

    return os.path.join(base_path, relative_path)


workspace = os.path.join(Path.home(), 'Desktop', 'sales_generator')
if not os.path.exists(workspace):
    os.makedirs(workspace)

dbdir = os.path.join(workspace, 'sales.db')

example_dir = resource_path('resource/example_receipt.xlsx')


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

        self.export_sales = Button(
            self,
            text='create_db_struct',
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
        try:
            messagebox.showinfo("Currenxie", "Select your reports folder")
            reportsDir = filedialog.askdirectory()
            result = import_amazon_salesdata(reportsDir, dbdir, example_dir)
            messagebox.showinfo(result['title'], result['message'])
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def create_db(self):
        try:
            result = update_db_struct("20000101000000", workspace, dbdir)
            messagebox.showinfo(result['title'], result['message'])
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def updatupdate_db_structe_db(self):
        try:
            result = update_db_struct("20191015121212", workspace, dbdir)
            messagebox.showinfo(result['title'], result['message'])
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def get_sales_report(self):
        try:
            messagebox.showinfo("Currenxie", "Select your TRADES FILE")
            file_path = filedialog.askopenfilename()
            result = generate_sales_report(file_path, dbdir, example_dir)
            messagebox.showinfo(result['title'], result['message'])
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    def get_payeco_sales_report(self):
        try:
            messagebox.showinfo("Currenxie", "Select your TRADES FILE")
            file_path = filedialog.askopenfilename()
            result = generate_payeco_sales_report(
                file_path, dbdir, example_dir)
            messagebox.showinfo(result['title'], result['message'])
        except Exception as e:
            messagebox.showinfo("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('400x150')
    root.title('Currenxie Sales Generator')
    root.iconbitmap("logo.icns")
    app = Application(master=root)
    app.mainloop()

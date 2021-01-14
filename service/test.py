
from import_amazon_salesdata import import_amazon_salesdata
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

result = import_amazon_salesdata(
    os.path.join(Path.home(), 'Desktop', 'sales_report'), dbdir, resource_path('resource/example_receipt.xlsx'))

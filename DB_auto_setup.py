import sqlite3
import wget
import requests
import urllib.request as rq
import pandas as pd
from threading import Thread
from time import sleep
from datetime import date
import calendar

from SQL_queries import SQL_queries

months_dict = {
    "Jan" : "January",
    "Feb" : "February",
    "Mar" : "March",
    "Apr" : "April",
    "May" : "May",
    "Jun" : "June",
    "Jul" : "July",
    "Aug" : "August",
    "Sep" : "September",
    "Oct" : "October",
    "Nov" : "November",
    "Dec" : "December"
}

class DB_auto_setup:

    def __init__(self, DB_name, excel_sheet_name, columns_csv, csv_file, table_name, table_columns,
                specializations, url=""):
        requests.packages.urllib3.disable_warnings()
        self.DB_name = DB_name
        self.NRF_Excel_path = ""
        self.excel_sheet_name = excel_sheet_name
        self.columns_csv = columns_csv
        self.csv_file = csv_file
        self.table_name = table_name
        self.table_columns = table_columns
        self.url = url
        self.specializations = specializations

        # Default date modified in case can't connect to the internet
        self.last_modified = ""
        self.set_last_modified()

        check_date = Thread(target=self.update)
        check_date.start()

    #
    # Methods to set up a DB and update it
    #

    def set_up_DB(self, url="https://www.nrf.ac.za/wp-content/uploads/2022/"
                            "08/Current-Rated-Researchers-22-August-2022.xlsx"):
        self.download_from_url(url)
        self.set_excel_file_name()
        self.set_up_prev_version()
        self.excel_to_csv(self.NRF_Excel_path, self.excel_sheet_name, self.columns_csv)
        self.csv_to_db(self.csv_file, self.table_name, self.table_columns)
        self.clean_data()

    def update(self):
        while True:
            # Check if the file on the sever is outdated, if not download and convert to DB format.
            # This will repeat every 1 min.
            self.url = self.build_url()
            try:
                # somewhere write to file to save the date permanently
                if requests.head(self.url, verify=False).status_code == 200:
                    data = rq.urlopen(self.url)
                    date_and_time = data.headers['last-modified']
                    if date != self.last_modified:
                        # We now gave a new last modified value, so we alter the values we have in the file and in the
                        # last modified variable
                        # Download the Excel file then create the NRF database
                        self.set_up_DB(self.url)
                        self.write_last_modified(date_and_time)
                        self.set_last_modified()
                        print("Successfully updated DB!")
                        # clean data here
            except:
                print(str(date.today())+" :Could not download NRF excel file, "
                                        "please check your internet connection or the URL.")
            sleep(300)

    def set_up_prev_version(self):
        conn = sqlite3.connect(self.DB_name)
        cursor = conn.cursor()
        query = SQL_queries.delete_table("PreviousResearchers")
        cursor.execute(query)
        conn.commit()
        query = "ALTER TABLE Researchers RENAME To PreviousResearchers;"
        cursor.execute(query)
        conn.commit()
        try:
            conn = sqlite3.connect(self.DB_name)
            cursor = conn.cursor()
            query = SQL_queries.clean_data(self.specializations, table="PreviousResearchers")
            cursor.execute(query)
            conn.commit()
        except sqlite3.Error:
            print("Failed to clean data")

    def set_last_modified(self):
        try:
            with open("Data/Last_modified.txt") as filestream:
                self.last_modified = filestream.readline()
        except:
            print("Unable to open file!")

    @staticmethod
    def write_last_modified(last_modified):
        file = open("Data/Last_modified.txt", "w")
        file.write(last_modified)
        file.close()

    def clean_data(self):
        try:
            conn = sqlite3.connect(self.DB_name)
            cursor = conn.cursor()
            query = SQL_queries.clean_data(self.specializations)
            cursor.execute(query)
            conn.commit()
        except sqlite3.Error:
            print("Failed to clean data")

    def set_excel_file_name(self):
        last_modified_list = self.last_modified.split(" ")
        self.NRF_Excel_path = "Data/"
        self.NRF_Excel_path += "Current-Rated-Researchers-" + last_modified_list[1] + "-" \
                               + months_dict[last_modified_list[2]]\
                               + "-" + last_modified_list[3] + ".xlsx"

    #
    #
    #
    #
    #Methods to convert from one format to another.
    #
    #
    #

    @staticmethod
    def excel_to_csv(filepath, sheet, columns=None):
        try:
            # convert excel data
            data_xls = pd.read_excel(filepath, sheet, dtype=str, index_col=None)
            if columns is not None:
                data_xls.columns = columns

            data_xls.to_csv('Data/DB.csv', encoding='utf-8', index=False, header=True)
        except:
            print("Could not convert to csv format!")

    def csv_to_db(self, csv_file, table_name, columns):
        try:
            # Creating a connection to the database
            conn = sqlite3.connect(self.DB_name)
            cursor = conn.cursor()
            # Deleting the old table to replace with a new one
            cursor.execute(SQL_queries.delete_table(table_name))

            # Reading csv file, then creating an empty table and appending the csv file data to it
            df = pd.read_csv(csv_file)
            cursor.execute(SQL_queries.create_table(table_name, columns))
            df.drop([0], inplace=True)
            df.to_sql(table_name, conn, if_exists="append", index=False)
        except:
            print("Could not create DB table from csv file")

    #
    #
    #  Internet related methods.
    #
    #

    @staticmethod
    def download_from_url(url):
        try:
            # Download file then save to Data folder, then check if it has changed
            wget.download(url, "Data")

        except requests.exceptions.RequestException:
            print("Could not find the file")

    @staticmethod
    def build_url():
        # Build url based on the NRF url format
        month_num = '{:02d}'.format(date.today().month)
        year_num = str(date.today().year)
        month_name = calendar.month_name[date.today().month]
        day_num = '{:02d}'.format(date.today().day)

        url = "https://www.nrf.ac.za/wp-content/uploads/" + \
              year_num + "/" + month_num + "/Current-Rated-Researchers-" + \
              day_num + "-" + month_name + "-" + year_num + ".xlsx"
        return url

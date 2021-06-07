__author__ = "Yu Du"
__Email__ = "yu.du@clinchoice.com"
__date__ = "Nov 24,2020"

######################################################################################################################
import pandas as pd
import sqlite3
import pickle


class DB_writer(object):
    """docstring for compiler
	This file is for recording purpose and is NOT functional.
    """

    def __init__(self, path):
        """
		stats about the database
		"""
        self.PATH = path
        self.sheets = None
        self.forms = None
        self.dict = None
        self.all_forms = {}
        self.num_forms = None

    def read_data(self):
        df = pd.ExcelFile(self.PATH)
        self.sheets = df.sheet_names
        return self.sheets

    def get_forms(self):
        """
		return a list of forms
		"""
        self.read_data()
        self.forms = self.sheets[1:-1]
        return self.forms

    def get_dictionary(self):
        self.dict = self.sheets[-1]
        return self.dict

    def read_table(self, sheet_name):
        df = pd.read_excel(self.PATH, sheet_name)
        return df

    def get_all(self):
        for form in self.forms:
            df = self.read_table(form)
            df = df.loc[df.iloc[:, 0] == form]
            self.all_forms[form] = df
        return self.all_forms

    def get_fields(self, form):
        self.get_all()
        return self.all_forms[form]['FieldOID']

    def write_dictionary(self):
        df = pd.read_excel(PATH,'Dictionary')
        unique_dict = set(df['Data_Dictionary_Name'])
        store = dict() # data structure to store the ecrf dictionaries. Dictionary with key being the dictionary name and value is pandas dataframe 
        for dict_name in unique_dict:
            store[dict_name] = df.loc[df['Data_Dictionary_Name'] == dict_name]
        dict_file = open('./dictionary', 'wb')
        pickle.dump(store, dict_file)
        dict_file.close()











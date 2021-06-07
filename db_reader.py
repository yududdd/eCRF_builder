__author__ = "Yu Du"
__Email__ = "yu.du@clinchoice.com"
__date__ = "Nov 24,2020"
######################################################################################################################
import sqlite3
import pandas as pd
import pickle


class DB(object):
	"""docstring for db-reader"""
	def __init__(self):
		"""
		stats about the database
		"""
		self._PATH = './data/ecrf.db'
		self._conn = None
		self.num_fields = None
		self.num_forms = None
		self.last_login = None
		self.na_dict = []
		self._read_db()

	def _read_db(self):
		"""
		read the local sqlite database
		:return: Null
		"""
		try:
			self._conn = sqlite3.connect(self._PATH)
			print(sqlite3.version)
		except sqlite3.Error as e:
			print(e)
		return self._conn

	def get_stats(self):
		"""
		get the stats about the database, number of forms, fields and last login
		:return: self.num_forms, self.num_fields
		"""
		# TODO: add last login information
		count_query = """SELECT Count(*) from forms"""
		countfields_query = """SELECT Count(*) from fields"""
		c = self._conn.cursor()
		c.execute(count_query)
		self.num_forms,  = c.fetchall()[0]
		c.execute(countfields_query)
		self.num_fields, = c.fetchall()[0]
		return self.num_forms, self.num_fields

	def get_columns(self):
		pass

	def get_forms(self):
		"""
		get all of the forms in the database
		:return: tuple with formoid and formname
		"""
		# select_query = """SELECT DISTINCT(formoid), formname from fields"""
		select_query = """SELECT DISTINCT(`FormOID \n(Dataset Name)`), `eCRF (Form) Name` from fields"""
		c = self._conn.cursor()
		c.execute(select_query)
		records = c.fetchall()
		c.close()
		return records

	def get_fields(self, form):
		"""
		get all of the fields within specified form
		:param form: the form for which extracted from
		:return:list of fields
		"""
		# select_query = """SELECT FieldOID FROM fields WHERE formoid = ?"""
		select_query = """SELECT FieldOID FROM fields WHERE `FormOID \n(Dataset Name)` = ?"""
		c = self._conn.cursor()
		c.execute(select_query, (form,))
		records = c.fetchall()
		c.close()
		return records

	def get_records(self, formoid):
		"""
		function to extract all the fields
		:param: the form to extract from
		:return: all the records with selected fields in pandas table format
		"""
		# placeholder = '?'
		# placeholders = ','.join(placeholder * len(fields))
		# select_query = """SELECT * FROM fields WHERE formoid = ?"""
		select_query = """SELECT * FROM fields WHERE `FormOID \n(Dataset Name)` = ?"""
		df = pd.read_sql_query(select_query, self._conn, params=[formoid])
		return df

	def get_selectedForm(self, forms):
		"""
		get selected forms from the list
		:return:
		"""
		placeholder = '?'
		placeholders = ','.join(placeholder * len(forms))
		# select_query = """SELECT DISTINCT(formoid), formname from fields WHERE formoid IN (%s)""" %placeholders
		select_query = """SELECT DISTINCT(`FormOID \n(Dataset Name)`), `eCRF (Form) Name`
		from fields WHERE `FormOID \n(Dataset Name)` IN (%s)""" % placeholders
		c = self._conn.cursor()
		c.execute(select_query, forms)
		records = c.fetchall()
		c.close()
		return records

	def get_selectedFields(self, fields):
		"""
		function to extract all the fields
		:param: the form to extract from
		:return: all the records with selected fields in pandas table format
		"""
		placeholder = '?'
		placeholders = ','.join(placeholder * len(fields))
		select_query = """SELECT * FROM fields WHERE fieldoid IN (%s)""" %placeholders
		
		df = pd.read_sql_query(select_query, self._conn, params=fields)
		return df

	def get_dict(self, dict_name):
		"""
		function to extract field dictionary
		:param: the dictionary name to extract
		:return: a pandas dataframe of the specified dictionary
		"""
		dbfile = open('./data/dictionary', 'rb')
		db = pickle.load(dbfile) 
		dbfile.close()
		try:
			return db[dict_name] #to return only the dictionary name and user string
		except KeyError:
			self.na_dict.append(dict_name)
			print("no key " + dict_name)


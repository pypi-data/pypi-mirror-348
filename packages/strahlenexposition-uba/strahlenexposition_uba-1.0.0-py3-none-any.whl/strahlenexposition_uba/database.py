import os
import sqlite3
from collections import defaultdict
from pathlib import Path

import polars as pl

from strahlenexposition_uba.constants import (
	COLUMNS_DOSISWERTE_AGG,
	COLUMNS_EINZELWERTE,
	COLUMNS_OPTIONALWERTE,
	COLUMNS_UCODES,
)
from strahlenexposition_uba.logger_config import get_logger


class DataManager:
	"""
	Manages SQLite database connections and operations.
	Should be used for data operations (write, fetch, update). Handles foreign key references.
	"""

	def __init__(self, db_path: Path):
		"""
		Sets db_path and fetchs untersuchungscode mapping (UCode: id) from db if exists.

		Args:
			db_path (Path): Absolute Path to the SQLite database file.
		"""
		self.db_path = db_path
		self.ucode_mapping = self._get_ucode_id_mapping()
		self.dropped_ucodes = defaultdict(int)

	def insert_untersuchungscodes(self, ucode_data: pl.DataFrame) -> None:
		"""
		Inserts multiple rows into the `Untersuchungscodes` table.

		Args:
			ucode_data (pl.DataFrame): DataFrame with columns "Ucode", "Bezeichnung", "Unit_Dosiswert", "Unit_DLP",
				"DRW_aktuell", "DRW_Vorschlag", "DRW_DLP_aktuell", "EUCLID_DRW", "EU_DRW", "US_DRW", "Schweiz_DRW",
				"Österreich_DRW", "EUCLID_DRW_DLP", EU_DRW_DLP", "US_DRW_DLP", "Schweiz_DLP", "Österreich_DLP".
		"""
		self._validate_input(expected=COLUMNS_UCODES, exist=ucode_data.columns, table="Untersuchungscodes")
		ucode_list = ucode_data[COLUMNS_UCODES].rows()

		columns = ", ".join(COLUMNS_UCODES)
		query_placeholders = ", ".join(["?"] * len(COLUMNS_UCODES))
		update_clause = ", ".join([f"{col}=excluded.{col}" for col in COLUMNS_UCODES])
		query = (
			f"INSERT INTO Untersuchungscodes ({columns}) "
			f"VALUES ({query_placeholders}) ON CONFLICT DO UPDATE SET {update_clause}"
		)

		self._execute_query(query, records=ucode_list, many=True)
		get_logger().info(f"Inserted {len(ucode_list)} Untersuchungscodes (duplicates may be skipped).")
		self.ucode_mapping = self._get_ucode_id_mapping()

	def insert_into_eingelesene_dateien_on_failure(self, metadata: dict) -> None:
		"""Inserts file/sheet information that failed processing pipeline into table 'eingelesene_dateien'.
		Replaces existing entry if unique contraints are violated.

		Args:
			metadata (dict): Dictionary with keys "Dateiname", "Arbeitsblatt", "Jahr", "erfolgreich"
		"""
		self._validate_input(
			expected=["Jahr", "Dateiname", "Arbeitsblatt", "erfolgreich"],
			exist=metadata.keys(),
			table=metadata["Arbeitsblatt"],
		)

		query = (
			"INSERT OR REPLACE INTO eingelesene_dateien (Dateiname, Arbeitsblatt, Jahr, erfolgreich) "
			"VALUES (?, ?, ?, ?)"
		)
		records = list(map(metadata.get, ["Dateiname", "Arbeitsblatt", "Jahr", "erfolgreich"]))
		self._execute_query(query=query, records=records)
		get_logger().debug(
			f"Inserted entry {metadata['Dateiname']} {metadata['Arbeitsblatt']} into eingelesene_dateien."
		)

	def insert_into_eingelesene_dateien(self, metadata: dict) -> int:
		"""Inserts information about filename and sheet as well as year, Aerztl_Stelle into eingelesene_dateien table
		on success. Replaces existing entry if unique contraints are violated.

		Args:
			metadata (dict): Dictionary with keys "Dateiname", "Arbeitsblatt", "Aerztl_Stelle", "Jahr", "erfolgreich"

		Returns:
			int: id of inserted entry
		"""

		self._validate_input(
			expected=["Jahr", "Dateiname", "Aerztl_Stelle", "Arbeitsblatt", "erfolgreich"],
			exist=metadata.keys(),
			table=metadata["Arbeitsblatt"],
		)
		query = (
			"INSERT OR REPLACE INTO eingelesene_dateien (Dateiname, Arbeitsblatt, Jahr, Aerztl_Stelle, erfolgreich) "
			"VALUES (?, ?, ?, ?, ?) RETURNING rowid"
		)
		values = list(map(metadata.get, ["Dateiname", "Arbeitsblatt", "Jahr", "Aerztl_Stelle", "erfolgreich"]))
		id = self._execute_query(query=query, records=values, fetch=True)
		get_logger().debug(
			f"Inserted entry {metadata['Dateiname']} {metadata['Arbeitsblatt']} with id {id} into eingelesene_dateien."
		)
		return id

	def insert_einzelwerte(self, metadata, df: pl.DataFrame) -> tuple[list[int], pl.Series]:
		"""Inserts records from one sheet into the `Einzelwerte` table, mapping Untersuchungscode to ID.
		Inserts entry for sheet/file into `eingelesene Dateien` receiving information from metadata.

		Args:
			metadata (dict): Dictionary with keys ["Dateiname", "Arbeitsblatt", "Jahr", "erfolgreich"]
			df (pl.DataFrame): A DataFrame containing columns
				ID_der_RX, Untersuchungscode, Aerztl_Stelle, DFP, AGD, CTDI, Dosiswert, Jahr
		"""
		df_old = df.clone()
		df = self._replace_untersuchungscode_with_id(df)
		dropped_rows = df["UCode_id"].is_null()
		# Count number of dropped values per UCode which isnt found
		list_dropped_ucodes = df_old.filter(dropped_rows)["Untersuchungscode"].value_counts().rows()
		for key, value in list_dropped_ucodes:
			self.dropped_ucodes[key] += value
		df = df.drop_nulls(subset=["UCode_id"])

		metadata["erfolgreich"] = 1
		arbeitsblatt_id = self.insert_into_eingelesene_dateien(metadata=metadata)

		if df.is_empty():
			return
		df = df.with_columns(pl.lit(arbeitsblatt_id).alias("Arbeitsblatt_id"))

		try:
			self._validate_input(expected=COLUMNS_EINZELWERTE, exist=df.columns, table="einzelwerte")
			records = df[COLUMNS_EINZELWERTE].rows()

			query = (
				"INSERT INTO Einzelwerte (ID_der_RX, UCode_id, Arbeitsblatt_id, DFP, AGD, CTDI, Dosiswert) "
				"VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING rowid"
			)
			einzelwert_ids = self._execute_query(query, records, many=True, fetch=True)
			get_logger().debug(f"Inserted {len(records)} rows into Einzelwerte.")
		except Exception as e:
			metadata["erfolgreich"] = 0
			self.insert_into_eingelesene_dateien(metadata=metadata)
			get_logger().error(f"Failed to insert data into DB: {e}")
			raise e
		return einzelwert_ids, dropped_rows

	def insert_optionalwerte(self, df: pl.DataFrame) -> None:
		"""Inserts values (e.g. DLP values) into Optionalwerte table.

		Args:
			df (pl.DataFrame): DataFrame with columns Einzelwert_id, Spaltenname, Wert
		"""
		self._validate_input(expected=COLUMNS_OPTIONALWERTE, exist=df.columns, table="Optionalwerte")
		records = df[COLUMNS_OPTIONALWERTE].rows()

		query = "INSERT INTO Optionalwerte (Einzelwert_id, Spaltenname, Wert) VALUES (?, ?, ?)"
		self._execute_query(query, records, many=True)
		get_logger().debug(f"Inserted {len(records)} rows into Optionalwerte.")

	def replace_dosiswerte_agg(self, df: pl.DataFrame, clear_all_data: bool = True) -> None:
		"""Deletes all existing data from Dosiswerte_AGG table in db and inserts new aggregated dosiswerte from df.

		Args:
			df (pl.DataFrame): aggregated data from einzelwerte with columns: "ID_der_RX", "UCode_id", "Aerztl_Stelle",
				"Dosiswert", "Anzahl_Werte", "Jahr"
			clear_all_data (bool): If True all existing data is deleted. Set to add data without deletion.
		"""
		df = self._replace_untersuchungscode_with_id(df)
		df = df.drop_nulls(subset=["UCode_id"])
		self._validate_input(expected=COLUMNS_DOSISWERTE_AGG, exist=df.columns, table="Dosiswerte_AGG")
		if clear_all_data:
			self._delete_dosiswerte_agg_table_data()

		records = df[COLUMNS_DOSISWERTE_AGG].rows()
		columns = ", ".join(COLUMNS_DOSISWERTE_AGG)
		placeholders = ", ".join(["?"] * len(COLUMNS_DOSISWERTE_AGG))
		query = f"INSERT INTO Dosiswerte_AGG ({columns}) VALUES ({placeholders})"
		self._execute_query(query, records, many=True)
		get_logger().info(f"Inserted {len(records)} rows into Dosiswerte_AGG.")

	def get_einzelwerte_with_details(self) -> pl.DataFrame:
		"""Retrieve all einzelwerte from table with Jahr, Aerztl_Stelle, ID_der_RX, UCode.

		Returns:
			pl.DataFrame: DataFrame with column Jahr, Aerztl_Stelle, ID_der_RX, Untersuchungscode, Dosiswert
		"""
		query = (
			"SELECT d.Jahr, d.Aerztl_Stelle, e.ID_der_RX, u.UCode as Untersuchungscode, e.Dosiswert "
			"FROM Einzelwerte as e "
			"JOIN eingelesene_dateien as d on e.Arbeitsblatt_id = d.id "
			"JOIN Untersuchungscodes as u on e.UCode_id = u.id"
		)
		einzelwerte = self._execute_query(query=query, fetch=True)
		return einzelwerte

	def get_einzelwerte_with_details_and_worksheet_info(self) -> pl.DataFrame:
		"""Retrieve all einzelwerte from table with Jahr, Aerztl_Stelle, ID_der_RX, UCode, Dateiname and Arbeitsblatt.
		TODO: mit Imke besprechen, warum oben nicht Dateiname & Arbeitsblatt ausgegeben werden, obwohl gejoint wurde?

		Returns:
			pl.DataFrame: DataFrame with columns Jahr, Aerztl_Stelle, ID_der_RX, Untersuchungscode, Dosiswert,
			Dateiname and Arbeitsblatt
		"""
		query = (
			"SELECT d.Jahr, d.Dateiname, d.Arbeitsblatt, d.Aerztl_Stelle, e.ID_der_RX, u.UCode as Untersuchungscode, "
			"e.Dosiswert , opt.Wert as Gerätebezeichnung  "
			"FROM Einzelwerte as e "
			"JOIN eingelesene_dateien as d on e.Arbeitsblatt_id = d.id "
			"JOIN Untersuchungscodes as u on e.UCode_id = u.id "
			"LEFT JOIN (SELECT Einzelwert_id, Wert FROM Optionalwerte WHERE Spaltenname='Gerätebezeichnung') "
			"AS opt on e.id = opt.Einzelwert_id"
		)

		einzelwerte = self._execute_query(query=query, fetch=True)
		return einzelwerte

	def get_number_einzelwerte_optionalwerte(self) -> tuple[int, int]:
		"""Retrieve number of mandatory and optional values in the db"""
		num_einzelwerte = self._execute_query(query="SELECT COUNT(*) FROM Einzelwerte", fetch=True)
		num_optionalwerte = self._execute_query(query="SELECT COUNT(*) FROM Optionalwerte", fetch=True)
		return num_einzelwerte, num_optionalwerte

	def _delete_dosiswerte_agg_table_data(self):
		query = "DELETE FROM Dosiswerte_AGG"
		self._execute_query(query=query)
		get_logger().info("Deleted all rows from Dosiswerte_AGG table")

	def is_file_already_processed(self, filename: str, sheet: str, year: int) -> bool:
		"""Checks if the file/sheet/year combination has already been marked as processed.

		Args:
			filename (str): file to be checked
			sheet (str): sheet of file to be checked
			year (int): year of collection of data in file

		Returns:
			bool: True if a row with erfolgreich=1 exists for the given parameters; otherwise False.
		"""
		query = (
			"SELECT COUNT(*) FROM eingelesene_dateien "
			"WHERE Dateiname = ? AND Arbeitsblatt = ? AND Jahr = ? AND erfolgreich = 1"
		)
		values = (filename, sheet, year)
		result = self._execute_query(query=query, records=values, fetch=True)
		count = result if result else 0
		return count > 0

	def get_ucode_details(self, ucodes: list[int] | int) -> pl.DataFrame:
		"""Retrieves rows from Untersuchungscode table for specified ucodes.

		Args:
			ucodes (list[int] | int): single ucode or list of ucodes.

		Returns:
			pl.DataFrame: Row data from Untersuchungscode table.
		"""
		if isinstance(ucodes, int):
			ucodes = (ucodes,)
		elif isinstance(ucodes, list):
			ucodes = tuple(ucodes)
		placeholders = ",".join(["?"] * len(ucodes))
		query = f"SELECT * FROM Untersuchungscodes WHERE UCode IN ({placeholders});"
		return self._execute_query(query=query, records=ucodes, fetch=True)

	def get_agg_dosis_with_ucode_data(self) -> pl.DataFrame:
		"""Retrieves data from Dosiswerte_AGG table with corresponding data from Untersuchungscode table.

		Returns:
			pl.DataFrame: Data containing aggregated values, Jahr, Aerztl_Stelle, ID_der_RX, ucode data and
			reference values
		"""
		query = (
			"SELECT uc.UCode, uc.Bezeichnung, uc.Unit_Dosiswert, uc.DRW_aktuell, uc.Deff,"
			"uc.DRW_Vorschlag, uc.EUCLID_DRW, uc.EU_DRW, uc.US_DRW, uc.Schweiz_DRW, uc.Österreich_DRW, "
			"dw.Dosiswert, dw.Anzahl_Werte, dw.Jahr AS Jahr, dw.Aerztl_Stelle, dw.ID_der_RX "
			"FROM Untersuchungscodes AS uc "
			"LEFT JOIN Dosiswerte_AGG AS dw ON uc.id = dw.UCode_id;"
		)
		return self._execute_query(query=query, fetch=True)

	def _get_ucode_id_mapping(self) -> dict[int, int]:
		"""Retrieves a mapping of `UCode` to `id` from the `Untersuchungscodes` table.

		Returns:
			dict[int, int]: A mapping {Ucode: id}.
		"""
		query = "SELECT UCode, id FROM Untersuchungscodes"
		result = self._execute_query(query=query, fetch=True)
		return dict(zip(result["UCode"].to_list(), result["id"].to_list(), strict=True))

	def _replace_untersuchungscode_with_id(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		Replaces the `Untersuchungscode` column with `UCode_id` using a dictionary mapping.
		Rows with ucodes that do not exist in mapping are dropped.

		Args:
			df (pl.DataFrame): Input DataFrame, containing a 'Untersuchungscode' column.
		Returns:
			pl.DataFrame: The same DataFrame with 'Untersuchungscode' replaced by 'UCode_id'.
		"""
		if "Untersuchungscode" not in df.columns:
			msg = "DataFrame has no 'Untersuchungscode' column. Skipping ID mapping a"
			get_logger().error(msg=msg)
			raise Exception(msg)
		if self.ucode_mapping is None:
			msg = "No ucode data exists in db. Insert ucodes to database table from excel file."
			get_logger().error(msg)
			raise Exception(msg)

		# Convert the original column to an integer, map to ID, then drop any rows that fail mapping
		col_index = df.columns.index("Untersuchungscode")
		ucode_col = df["Untersuchungscode"].replace_strict(self.ucode_mapping, default=None).alias("UCode_id")
		df.replace_column(col_index, ucode_col)
		if ucode_col.null_count() > 0:
			get_logger().debug(f"{ucode_col.null_count()} rows from dataframe with ucodes not stored in ucode table.")
		return df

	def _execute_query(
		self, query: str, records: tuple | list = (), fetch: bool = False, many: bool = False
	) -> None | pl.DataFrame | int | float | str:
		"""Executes a SQL query with optional record insertion and result fetching.

		Args:
			query (str): The SQL query to execute.
			records (tuple | list, optional): The data to insert or update in the query.
				If `many` is True, this should be a list of tuples. Defaults to an empty tuple.
			fetch (bool, optional): Whether to fetch and return results from a `SELECT` query. Defaults to False.
			many (bool, optional): Whether to execute `executemany()` for batch inserts/updates. Defaults to False.

		Returns:
			None | polars.DataFrame| int | float | str: Returns a dataframe or a single value of fetched results
			if `fetch` is True; otherwise, returns None.

		Raises:
			sqlite3.Error: If an error occurs during query execution, logs the error and raises an exception.
		Example:
			>>> query = 'SELECT id FROM Untersuchungscodes WHERE UCODE = ?'
			>>> id = self.execute(query=query, records=(1080,), fetch=True)
			>>> 3
		"""

		def execute_multiple_with_fetch(cursor, query, record):
			cursor.execute(query, record)
			return cursor.fetchall()[0][0]

		try:
			with self._connect() as conn:
				cursor = conn.cursor()
				if many:
					if fetch:
						values = [execute_multiple_with_fetch(cursor, query, record) for record in records]
						return values
					else:
						cursor.executemany(query, records)
						return
				else:
					cursor.execute(query, records)
				if fetch:
					result = cursor.fetchall()
					column_names = [desc[0] for desc in cursor.description]  # Extract column names
					if len(result) == 1 and len(result[0]) == 1:
						return result[0][0]
					return pl.DataFrame(result, schema=column_names, orient="row", infer_schema_length=None)
		except sqlite3.Error as e:
			get_logger().error(f"Error executing query: {query}\n{e}", exc_info=True)
			raise

	def _connect(self) -> sqlite3.Connection:
		"""
		Establishes a connection to the SQLite database and enables foreign key constraints.

		Returns:
			sqlite3.Connection: open connection that can be used for transactions
		"""
		conn = sqlite3.connect(self.db_path)
		# enable foreign key, disabled by default in sqlite for backwards compatibility
		conn.execute("PRAGMA foreign_keys = ON;")
		return conn

	@staticmethod
	def _validate_input(expected: list[str], exist: list[str], table: str) -> None:
		# Validates that required columns are present in the DataFrame.
		missing_cols = set(expected) - set(exist)
		if missing_cols:
			raise ValueError(f"Missing columns in DataFrame: {missing_cols} to insert to table {table}")


def init_db(db_path: Path, schema_path: Path = None) -> None:
	"""
	Initializes the database by executing an SQL schema script and stores db file to db_path.
	Standard sql schema skips table creation if database and table already exist.

	Args:
		db_path (Path): dest Path to the database file.
		schema_path (Path): defaults to None, allows to provide custom sql schema for development purpose.


	Example:
		>>> init_db(Path("dest/path/to/database.db"))
	"""
	if isinstance(db_path, Path):
		db_path.parent.mkdir(parents=True, exist_ok=True)
	elif db_path != ":memory:":
		raise ValueError("db_path argument not specified correctly. Use a Path object or ':memory:'")
	if schema_path is None:
		schema_path = Path(os.path.join(Path(__file__).resolve().parent, "sql", "schema.sql"))

	if not schema_path.exists():
		error_msg = f"Schema file {schema_path} not found. Cannot initialize DB."
		get_logger().error(error_msg)
		raise FileNotFoundError(error_msg)

	with open(schema_path, encoding="utf-8") as f:
		sql_script = f.read()

	with sqlite3.connect(db_path) as conn:
		conn.execute("PRAGMA foreign_keys = ON;")
		conn.executescript(sql_script)

	get_logger().info(
		f"Executed SQL database initialisation script defining table schema: {schema_path}."
		f"If a table already exists, this has no effect. Database is stored at {db_path}."
	)

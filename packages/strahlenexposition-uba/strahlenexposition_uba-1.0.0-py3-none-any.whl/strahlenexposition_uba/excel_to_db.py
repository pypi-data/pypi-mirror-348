import logging
import os
import re
from collections import defaultdict
from pathlib import Path

import polars as pl

import strahlenexposition_uba.database as db
from strahlenexposition_uba.constants import BAYERN_PATTERN, COLUMNS_UCODES, FILE_ENDINGS
from strahlenexposition_uba.formatter import (
	COLUMN_METADATA,
	BayernFormatter,
	LongTableFormatter,
	NewTableFormatter,
)
from strahlenexposition_uba.logger_config import get_logger


class AllSheetsFailedError(Exception):
	"""Raised when all Excel sheets fail due to missing columns."""

	pass


class FileFinder:
	"""
	Searches for Excel files within a specified directory (recursively)
	"""

	def __init__(self, directory: Path):
		"""Initializes FileFinder and finds all excel files from a parent directory recursively.

		Args:
			directory (Path): Path to the parent directory
		"""
		self.directory = directory
		self.files = self.find_excel_files()

	def find_excel_files(self) -> list:
		"""
		Searches for all files matching predefined Excel file endings (e.g., ``.xlsx``, ``.xls``),
		within the given directory and its subdirectories.

		Returns:
			list: A list of absolute file paths for all detected Excel files.
		"""
		# Check if filenames are unique. If not warn the user and urge them to change one.
		files_by_year = defaultdict(list)
		for year in os.listdir(self.directory):
			year_path = os.path.join(self.directory, year)
			if os.path.isdir(year_path):  # Only process directories (which are years)
				for _, _, filenames in os.walk(year_path):
					for filename in filenames:
						files_by_year[year].append(filename)

		# Check for duplicate files within each year
		for year, files in files_by_year.items():
			seen_files = set()
			for file in files:
				filename = os.path.basename(file)  # Get just the filename (no path)
				if filename in seen_files:
					get_logger().error(
						f"Filename '{filename}' occurs multiple times in '{year}'. Please change or remove one"
					)
				else:
					seen_files.add(filename)

		return [
			os.path.join(root, file)
			for root, _, files in os.walk(self.directory)
			for file in files
			if file.endswith(FILE_ENDINGS)
		]


class ExcelToSQLiteConverter:
	"""Converts Excel files to SQLite database entries."""

	def __init__(self, db_path: Path, data_path: Path):
		"""Initializes the converter with a database manager and
		by adding Untersuchungscodes to a table in the database

		Args:
			db_path (Path): Path to the SQLite database
		"""
		self.warnings = []
		self.failed_sheets = 0
		self.db_manager = db.DataManager(db_path)
		self.refiner = SQLiteTableRefiner()
		self.data_path = data_path
		ucode_file = os.path.join(
			data_path,
			"241216_R-Skripte_Vorlagen_U-Codes_und_Berichte",
			"02-Untersuchungscodes_und_DRW.xlsx",
		)
		if os.path.exists(ucode_file):
			logging.info("Processing Untersuchungscodes...")
			ucodes = pl.read_excel(ucode_file, sheet_name="Alle")[COLUMNS_UCODES]
			self.db_manager.insert_untersuchungscodes(ucodes)
		else:
			logging.error("Untersuchungscodes file missing!")
			raise FileNotFoundError("Untersuchungscodes file missing!")

	def convert_and_store_excel(self, file: str) -> pl.DataFrame:
		"""Reads Excel file, tries for every sheet to transform into a Polars DataFrame and inserts data into
		the database. Adds metadata to table ``eingelesene_dateien``, mandatory values to ``Einzelwerte`` and
		optional values in long format to ``Optionalwerte``.

		Args:
			file (str): Path to the Excel file to be converted.

		Raises:
			AllSheetsFailedError: If all sheets in the Excel file fail to process.
		"""
		self.warnings = []  # Reset Warnings and failed sheets
		self.failed_sheets = 0
		metadata = self.get_info_from_filename(file)  # Returns dict with [filename, year, aerztl_stelle]
		if metadata["Aerztl_Stelle"] is None:
			self.db_manager.insert_into_eingelesene_dateien_on_failure(metadata)
			return

		# Read all sheets in the excel file
		dict_of_dfs = self._read_excel_sheets(file)

		# Check for Neue Vorlage
		metadata["is_wide"] = list(dict_of_dfs.keys())[0] == "Allgemeine Angaben"
		if metadata["is_wide"]:  # In erstem Sheet sind keine Informationen bei neuer Vorlage
			del dict_of_dfs["Allgemeine Angaben"]

		# Process excel sheets one by one and keep the results of clean passes
		for sheetname, df in dict_of_dfs.items():
			metadata["Arbeitsblatt"] = sheetname
			if self.db_manager.is_file_already_processed(metadata["Dateiname"], sheetname, metadata["Jahr"]):
				get_logger().debug(
					f"File {os.path.basename(file)} sheet {sheetname} already processed and written to db."
				)
				continue
			try:
				self.process_one_sheet(df=df, metadata=metadata)
			except Exception as e:
				if isinstance(e, KeyError):  # Skip sheets that we believe do not contain data due to their format
					self.failed_sheets += 1
				else:  # Log the sheet as failed and continue with the next one
					get_logger().error(
						f"Unable to process sheet {os.path.basename(file), sheetname} : {e}", exc_info=False
					)
					metadata["erfolgreich"] = 0
					self.db_manager.insert_into_eingelesene_dateien_on_failure(metadata)

		# If all sheets failed. Log the warning messages, write to database and raise error.
		if self.failed_sheets == len(dict_of_dfs):
			metadata["Arbeitsblatt"] = 0
			metadata["erfolgreich"] = 0
			self.db_manager.insert_into_eingelesene_dateien_on_failure(metadata)
			raise AllSheetsFailedError("In none of the sheets could we identify an ID column")

	def process_one_sheet(self, df: pl.DataFrame, metadata: dict) -> tuple[pl.DataFrame, pl.DataFrame]:
		"""Formats a single Excel sheet by finding the template, processing the data and splitting it into
		mandatory and optional data for the different database tables. Then inserts the data into the db.

		Args:
			df (pl.DataFrame): The DataFrame representing the raw sheet data.
			metadata (dict): A dictionary with the keys "Dateiname", "Arbeitsblatt", "Jahr", "Aerztl_Stelle",
				"is_bayern", "is_wide"
		"""
		if metadata["is_bayern"]:  # Checks for the old Bayern Vorlage.
			# TODO: Check if this clashes with the new BYAeK data as they are not using this format any more
			df = BayernFormatter(metadata=metadata).process_df(df=df)
		elif metadata["is_wide"]:
			df = NewTableFormatter(metadata=metadata).process_df(df=df)
		else:
			df = LongTableFormatter(metadata=metadata).process_df(df=df)

		einzelwerte, optionalwerte = self.refiner.refine_einzelwerte(df=df)
		try:
			einzelwert_ids, dropped_rows = self.db_manager.insert_einzelwerte(metadata=metadata, df=einzelwerte)
		except Exception:
			return
		optionalwerte = self.refiner.refine_optionalwerte(
			optionalwerte=optionalwerte,
			einzelwert_id=einzelwert_ids,
			dropped_rows=dropped_rows,
		)
		self.db_manager.insert_optionalwerte(optionalwerte)

	def get_info_from_filename(self, file: str) -> dict:
		"""Extracts metadata from the filename for the ``eingelesene_dateien`` table in the database.

		Args:
			file (str): Absolute path of the excel file.

		Returns:
			dict: Extracted metadata including Dateiname, Jahr, Aerztl_Stelle and is_bayern.
		"""
		root, filename = os.path.split(file)
		match = re.search(r"DRW_(\d{4})_Originalmeldungen", root)
		try:
			metadata = {
				"Dateiname": filename,
				"Jahr": int(match.group(1)),
				"Aerztl_Stelle": self._check_aerztl_stelle(file),
				"is_bayern": re.search(BAYERN_PATTERN, file),
			}
		except Exception as e:
			get_logger().error(e)
			metadata = {
				"Dateiname": filename,
				"Jahr": int(match.group(1)),
				"Aerztl_Stelle": None,
				"Arbeitsblatt": 0,
				"erfolgreich": 0,
			}
		return metadata

	@staticmethod
	def _check_aerztl_stelle(filename: str):
		"""Tries to retrieve information about the aerztl_stelle from the filename or its directory.

		Args:
			filename (str): Absolute path of the excel file.

		Raises:
			ValueError: If unable to find a unique match for the Aerztl Stelle
		"""

		def get_relevant_filepath(file):
			start = re.search("DRW_(?:\d{4})_Originalmeldungen", file).end()
			return file[start + 1 :]

		name = get_relevant_filepath(filename)
		subs = ["BB", "BE", "BU", "BW", "BY", "HE", "HH", "MV", "NI", "NO", "NW", "RP", "SA", "SH", "SN", "ST", "TH"]
		aerztl_stelle = {sub for sub in subs if sub in name}

		if len(aerztl_stelle) == 2 and "ST" in aerztl_stelle:
			aerztl_stelle.remove("ST")  # Ignore 'STAND' and 'ST_LSA' substrings

		if len(aerztl_stelle) == 1:
			# Differentiate between KV and AeK. Also add HB to NI and differentiate NW
			aerztl_stelle = next(iter(aerztl_stelle))
			match aerztl_stelle:
				case "NI":
					aerztl_stelle += "HB"
				case "SA":
					aerztl_stelle = "ST"
				case "BY" | "HH" | "RP" | "SH":
					aerztl_stelle += "AeK" if any(sub in name for sub in ("LÄK", "AeK", "ÄK")) else "KV"
				case "NW":
					aerztl_stelle = "WL" if any(sub in name for sub in ("NWL", "NWW", "NW_W")) else "NO"
			return aerztl_stelle
		else:
			raise ValueError(f"Couldn't uniquely identify aerztl. Stelle for {name}. Please adjust the filename")

	@staticmethod
	def _read_excel_sheets(file: str) -> dict:
		"""Reads an Excel file and returns its sheets as a dictionary of DataFrames.

		Args:
			file (str): Absolute path of the excel file.
		"""
		dict_of_dfs = pl.read_excel(
			file, has_header=False, sheet_id=0, raise_if_empty=False, read_options={"dtypes": "string"}
		)
		# Remove empty tables
		keys = list(dict_of_dfs.keys())
		for key in keys:
			if dict_of_dfs[key].is_empty():
				del dict_of_dfs[key]

		# Check for Neue Vorlage
		return dict_of_dfs


class SQLiteTableRefiner:
	"""
	A class to split data into mandatory and optional data and melts the optional data into a long data format
	to save space in the database. Correct matching of the optional and mandatory data is ensured.
	"""

	def __init__(self):
		self.mandatory_columns = [
			meta["standard_name"] for meta in COLUMN_METADATA.values() if meta["category"] in ["id", "mandatory"]
		] + ["Dosiswert"]

	def refine_einzelwerte(self, df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
		"""
		Refines the dataframe by splitting it into mandatory and optional data,.

		Args:
			df (pl.DataFrame): Input dataframe.

		Returns:
			tuple[pl.DataFrame, pl.DataFrame]: Refined mandatory and optional dataframes.
		"""
		mandatory_data, optional_data = self._split_dataframe(df)
		return mandatory_data, optional_data

	def refine_optionalwerte(
		self, optionalwerte: pl.DataFrame, einzelwert_id: list, dropped_rows: pl.Series
	) -> pl.DataFrame:
		"""Melts the wide dataframe of optional values to a long format. Requires the
		einzelwert_id and which rows were dropped from the einzelwerte dataframe to
		ensure the correct match between the two tables

		Args:
			optionalwerte (pl.DataFrame): Dataframe of optional columns with the same length
				as the mandatory_data dataframe returned by :func:`refine_einzelwerte`.
			einzelwert_id (list): List of the einzelwert_id from table ``Einzelwerte``. May be shorter
				than ``len(optionalwerte)``
			dropped_rows (list): pl.Series of length of optionalwerte with boolean values

		Returns:
			pl.DataFrame: Long dataframe with columns ``Einzelwert_id``, ``Spaltenname`` and ``Wert``
		"""
		return (
			optionalwerte.lazy()
			.filter(~dropped_rows)
			.with_columns(pl.Series("Einzelwert_id", einzelwert_id))
			.unpivot(index="Einzelwert_id", variable_name="Spaltenname", value_name="Wert")
			.drop_nulls(subset="Wert")
			.collect()
		)

	def _split_dataframe(self, df: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
		optional_present_columns = [
			meta["standard_name"]
			for meta in COLUMN_METADATA.values()
			if meta["category"] == "optional" and meta["standard_name"] in df.columns
		]
		mandatory_data = df.select(self.mandatory_columns)
		optional_data = df.select(optional_present_columns)
		return mandatory_data, optional_data

import contextlib
import logging
import os
import re

import polars as pl

import strahlenexposition_uba.database as db
from strahlenexposition_uba.constants import COLUMNS_UCODES


class ExcelToDbProcessor:
	"""
	Orchestrates reading Excel files and inserting them into the database.
	Currently Reading untersuchungscode and import files.
	Should be replaced by reading original data when processing pipeline is ready.
	"""

	def __init__(self, db_manager: db.DataManager, data_dir: str):
		self.db_manager = db_manager
		self.data_dir = data_dir

	@staticmethod
	def _extract_year_from_filename(filename: str) -> int:
		"""Extracts the year from filenames like 'DRW_2023_data_import.xlsx'."""
		match = re.search(r"_(\d{4})_data_import", filename)
		return int(match.group(1)) if match else None

	def process_import_excel_to_db(self):
		import_data_dir = os.path.join(self.data_dir, "250127_02_Importierte_Daten")
		# Process all Excel files in the data folder matching the pattern
		for file in os.listdir(import_data_dir):
			# keine zahnaerztlichen import excel
			if re.search(r"_\d{4}_data_import\.xlsx$", file):
				file_path = os.path.join(import_data_dir, file)
				year = self._extract_year_from_filename(file)
				logging.info(f"Processing {file} (Year: {year})...")

				# Read sheets
				self.process_einzelwerte_sheet(file_path, year=year)

				self.process_dosiswerte_agg_sheet(file_path, year=year)

	def process_einzelwerte_sheet(self, file_path, year: int):
		filename = os.path.basename(file_path)
		sheet = "Einzelwerte"

		if self.db_manager.is_file_already_processed(filename=filename, sheet=sheet, year=year):
			logging.info(f"File {filename} sheet {sheet} already processed and written to db.")
			return
		columns = [
			"ID_der_RX",
			"Untersuchungscode",
			"Aerztl_Stelle",
			"Dateiname",
			"Arbeitsblatt",
			"DFP_formatted",
			"AGD_formatted",
			"DLP_formatted",
			"CTDI_formatted",
			"Dosiswert",
		]
		einzelwerte = self._load_data_from_sheet(file_path=file_path, sheet=sheet, year=year, columns=columns)
		einzelwerte = einzelwerte.rename(
			{"DLP_formatted": "DLP", "CTDI_formatted": "CTDI", "AGD_formatted": "AGD", "DFP_formatted": "DFP"}
		)
		row = einzelwerte.row(0, named=True)
		metadata = {
			"Dateiname": filename,
			"Jahr": row["Jahr"],
			"Aerztl_Stelle": row["Aerztl_Stelle"],
			"Arbeitsblatt": sheet,
			"erfolgreich": 1,
		}
		self.db_manager.insert_into_eingelesene_dateien(metadata=metadata)

		# Aerztl_Stelle is obtained from eingelesene_dateien table but import excel has all aerztl_stelle in one sheet
		# -> use workaround to compare aggregation
		def workaround_aerzt_stelle(einzelwerte_as: pl.DataFrame):
			row = einzelwerte_as.row(0, named=True)
			metadata = {
				"Dateiname": f"{filename}{row['Aerztl_Stelle']}",
				"Jahr": row["Jahr"],
				"Aerztl_Stelle": row["Aerztl_Stelle"],
				"Arbeitsblatt": sheet,
				"erfolgreich": 1,
			}
			with contextlib.suppress(Exception):
				self.db_manager.insert_einzelwerte(metadata=metadata, df=einzelwerte_as)
			return einzelwerte_as.sample(0)  # return anything for map_groups - this isn't used

		einzelwerte.group_by("Aerztl_Stelle").map_groups(lambda data: workaround_aerzt_stelle(data))

	def process_dosiswerte_agg_sheet(self, file_path, year) -> None:
		filename = os.path.basename(file_path)
		sheet = "Dosiswerte_AGG"
		if self.db_manager.is_file_already_processed(filename=filename, sheet=sheet, year=year):
			logging.info(f"File {filename} sheet {sheet} already processed and written to db.")
			return
		columns = [
			"ID_der_RX",
			"Untersuchungscode",
			"Aerztl_Stelle",
			"Dosiswert",
			"Anzahl_Werte",
		]
		dosiswerte_agg = self._load_data_from_sheet(file_path=file_path, sheet=sheet, year=year, columns=columns)
		row = dosiswerte_agg.row(0, named=True)
		metadata = {
			"Dateiname": filename,
			"Jahr": row["Jahr"],
			"Aerztl_Stelle": row["Aerztl_Stelle"],
			"Arbeitsblatt": sheet,
		}
		if dosiswerte_agg.is_empty():
			metadata["erfolgreich"] = 0
			self.db_manager.insert_into_eingelesene_dateien_on_failure(metadata=metadata)
		else:
			self.db_manager.replace_dosiswerte_agg(df=dosiswerte_agg, clear_all_data=False)
			metadata["erfolgreich"] = 1
			self.db_manager.insert_into_eingelesene_dateien(metadata=metadata)

	def process_untersuchungscodes_to_db(self) -> None:
		ucode_file_path = os.path.join(
			self.data_dir,
			"241216_R-Skripte_Vorlagen_U-Codes_und_Berichte",
			"02-Untersuchungscodes_und_DRW.xlsx",
		)
		# load untersuchungscodes from  excel and insert to db
		if os.path.exists(ucode_file_path):
			logging.info("Processing Untersuchungscodes...")
			ucodes = pl.read_excel(ucode_file_path, sheet_name="Alle")[COLUMNS_UCODES]
			self.db_manager.insert_untersuchungscodes(ucodes)
		else:
			print("Untersuchungscodes file missing!")

	def _load_data_from_sheet(self, file_path: str, sheet: str, year: int, columns: list[str]) -> pl.DataFrame:
		try:
			sheet_data = (
				pl.read_excel(file_path, sheet_name=sheet).select(columns).with_columns(pl.lit(year).alias("Jahr"))
			)
			return sheet_data
		except Exception as e:
			logging.error(f"Error reading {file_path} {sheet}. Returning empty DataFrame: {e.with_traceback}")
			return pl.DataFrame()

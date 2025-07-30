import argparse
import os
from pathlib import Path

import polars as pl
from xlsxwriter import Workbook

from strahlenexposition_uba import database as db
from strahlenexposition_uba import logger_config
from strahlenexposition_uba.dashboard import DashboardApp
from strahlenexposition_uba.data_science import create_ucode_summary_table
from strahlenexposition_uba.excel_to_db import ExcelToSQLiteConverter, FileFinder
from strahlenexposition_uba.preprocess import calculate_agg_values, load_pseudonyms
from strahlenexposition_uba.report import PdfReportGenerator
from strahlenexposition_uba.tmp_insert_data import ExcelToDbProcessor


def run_process_pipeline(
	base_path: str,
	read_original_excel: bool = True,
	read_import_excel: bool = False,
	pdf_report_years: list[int] = None,
	generate_table: bool = True,
	start_dash: bool = False,
):
	"""Run selected components in the data processing pipeline.
		See parameter description for pipeline step details:

	Args:
		base_path (str): Path of directory that contains data_dir, database folder, output folder (and optionally
			repository).
		read_original_excel (bool, optional): Read and process original excel files containing original data from
			aerztl_stellen, aggregate values and write to database. Defaults to False.
		read_import_excel (bool, optional): (for development) Read already preprocessed and aggregated import excels
			and write to separate database file. Defaults to False.
		pdf_report_years (list[int]): Creates report (with and without pseudonymisation) for selected years retrieving
			data from database. Defaults to None.
		start_dash (bool, optional): (beta state) Launch a local interactive dashboard to visualize data for selected
			ucodes as in pdf report. Defaults to False.
	"""
	# configure path based on base_path
	if not base_path:
		base_path = Path(__file__).resolve().parents[3]

	DB_FILE_DIR = os.path.join(base_path, "database")
	if not os.path.exists(DB_FILE_DIR):
		os.mkdir(DB_FILE_DIR)
	DEST_FILE_DIR = os.path.join(base_path, "output")
	if not os.path.exists(DEST_FILE_DIR):
		os.mkdir(DEST_FILE_DIR)
	LOG_FILE_DIR = os.path.join(base_path, "logs")
	logger_config.setup_logger(log_dir=LOG_FILE_DIR, name_prefix="report")
	logger_config.get_logger().info("Logger is initialized for reading data to database and pdf generation.")

	DATA_DIR = os.path.join(base_path, "KI-Labor_strukturiert")
	if not os.path.exists(DATA_DIR):
		logger_config.get_logger().warning(f"Data directory {DATA_DIR} does not exist.")

	DB_FILE_PATH_RAW = Path(os.path.join(DB_FILE_DIR, "raw_strahlenexposition.db"))
	DB_FILE_PATH_IMPORT = Path(os.path.join(DB_FILE_DIR, "import_strahlenexposition.db"))

	if read_original_excel:
		excel_to_db(db_file_path=DB_FILE_PATH_RAW, data_dir=DATA_DIR)
		aggregate_data(db_file_path=DB_FILE_PATH_RAW)
	if read_import_excel:
		import_excel_to_db(db_file_path=DB_FILE_PATH_IMPORT, data_dir=DATA_DIR)
	if pdf_report_years:
		create_pdf_report(
			db_file_path=DB_FILE_PATH_RAW, years=pdf_report_years, dest_path=DEST_FILE_DIR, data_dir=DATA_DIR
		)
		# create_pdf_report(db_file_path=DB_FILE_PATH_IMPORT, years=pdf_report_years) # use this for report comparison
	if generate_table:
		create_xls_tables(db_file_path=DB_FILE_PATH_RAW, years=pdf_report_years, dest_path=DEST_FILE_DIR)
	if start_dash:
		start_interactive_dash_plots(db_file_path=DB_FILE_PATH_RAW)


def create_pdf_report(db_file_path: Path, years: list[int], dest_path: str, data_dir: str):
	"""Generates two PDF reports (with and without pseudonymization) for selected years and writes it to file system.
		Report contains one page for each UCode in the data filtered by selected years that exist in Untersuchungsode
		table.

	Args:
		db_file_path (Path): Absolute Path to the SQLite database file.
		years (_type_): List of years to include in the report.
		dest_path (str): Path of directory to write pdf files to.
		data_dir (str): Path of data directory (where 'pseudonym_mapping.csv' is stored).
	"""
	logger_config.get_logger().info("Start pdf report generation.")
	data_manager = db.DataManager(db_file_path)
	agg_data = data_manager.get_agg_dosis_with_ucode_data()
	report_generator = PdfReportGenerator(data=agg_data)
	report_generator.generate_report(years, dest_path=dest_path)
	try:
		pseudonym_mapping = load_pseudonyms(data_dir=data_dir, aerztl_stellen=agg_data["Aerztl_Stelle"].unique())
		report_generator.generate_report(years, dest_path=dest_path, pseudonyms=pseudonym_mapping)
	except (FileNotFoundError, ValueError) as e:
		logger_config.get_logger().warning("Could not create pseudonymized report.")
		logger_config.get_logger().error(e)
		return


def create_xls_tables(db_file_path: Path, years: list[int], dest_path: str):
	"""Handles the writing of the summary statistics per UCode to excel.

	Args:
		db_file_path (Path): Absolute Path to the SQLite database file.
		years (list[int]): List of years to include in the table.
		dest_path (str): Path of directory to write excel files to.
	"""
	logger_config.get_logger().info("Start creating summary tables excel file.")
	data_manager = db.DataManager(db_file_path)
	df_table = data_manager.get_agg_dosis_with_ucode_data()
	if not years:
		years = df_table.get_column("Jahr").unique()
	years_as_str = "_".join(str(x) for x in years)
	xls_table = create_ucode_summary_table(df_table, years)
	output_path = os.path.join(dest_path, f"{years_as_str}_ucode_tables.xls")
	with Workbook(output_path) as wb:
		xls_table.write_excel(workbook=wb, worksheet="Überblick", float_precision=2)

		for digit in range(1, 9):
			xls_table_grp = xls_table.filter(pl.col("Code").str.starts_with(digit))
			xls_table_grp.write_excel(workbook=wb, worksheet=f"sheet_{digit}", float_precision=2)


def excel_to_db(db_file_path: Path, data_dir: Path):
	"""Reads, processes and writes all excel file data to the db.

	Args:
		db_file_path (Path): Absolute Path to the SQLite database file.
		data_dir (Path):Path of data directory. Must contain directory "250122_Originalmeldungen" where the original
			excel with dose data from Aerztliche Stelle are stored and directory
			"241216_R-Skripte_Vorlagen_U-Codes_und_Berichte" containing "02-Untersuchungscodes_und_DRW.xlsx"..
	"""
	data_path = Path(os.path.join(data_dir, "250122_Originalmeldungen"))
	db.init_db(db_path=db_file_path)
	finder = FileFinder(data_path)
	processor = ExcelToSQLiteConverter(db_path=db_file_path, data_path=data_dir)
	for file in finder.files:
		try:
			processor.convert_and_store_excel(file)
		except Exception as e:
			logger_config.get_logger().error(f"couldn't process file {os.path.basename(file)}:{e}", exc_info=False)
	num_einzelwerte, num_optionalwerte = processor.db_manager.get_number_einzelwerte_optionalwerte()
	# Message for dropped UCodes
	lines = ["The following codes were dropped:", "Untersuchungscode: frequency"]
	for code, freq in sorted(processor.db_manager.dropped_ucodes.items()):
		lines.append(f"{code}: {freq}")
	log_message = "\n".join(lines)
	logger_config.get_logger().warning(log_message)

	logger_config.get_logger().info(
		f"Now there are {num_einzelwerte} Einzelwerte and {num_optionalwerte} Optionalwerte in DB."
	)


def aggregate_data(db_file_path: Path):
	"""Aggregates values from table Einzelwerte.
		Calculates median and number of values grouped by "Jahr", "Aerztl_Stelle", "ID_der_RX", "Untersuchungscode" and
		writes it to table "Dosiswerte_AGG"

	Args:
		db_file_path (Path): Absolute Path to the SQLite database file.
	"""
	data_manager = db.DataManager(db_file_path)
	einzelwert_data = data_manager.get_einzelwerte_with_details()
	agg_data = calculate_agg_values(df=einzelwert_data, value_column="Dosiswert")
	data_manager.replace_dosiswerte_agg(agg_data)


def import_excel_to_db(db_file_path: Path, data_dir: str):
	"""Reads already preprocessed and aggregated import excels and write to separate database file.
		This can be used for data amd report comparison between orginal workflow (R scripts + manual da manipulation)
		and the new complete python workflow.

	Args:
		db_file_path (Path): Absolute Path to the SQLite database file based on import excel files.
		data_dir (str): Path of data directory. Must contain directory "250127_02_Importierte_Daten" where the original
			excel with dose data from Aerztliche Stelle are stored and directory
			"241216_R-Skripte_Vorlagen_U-Codes_und_Berichte" containing "02-Untersuchungscodes_und_DRW.xlsx".
	"""
	db.init_db(db_path=db_file_path)
	data_manager = db.DataManager(db_file_path)
	excel_to_db_processor = ExcelToDbProcessor(data_manager, data_dir)
	excel_to_db_processor.process_untersuchungscodes_to_db()
	excel_to_db_processor.process_import_excel_to_db()
	logger_config.get_logger().info("Finished import excel to db")


def start_interactive_dash_plots(db_file_path: Path):
	"""Locally start a interactive dashboard (plotly dash) to visualize data per ucode.

	Args:
		db_file_path (Path): Absolute Path to the SQLite database file.
	"""
	db_manager = db.DataManager(db_file_path)

	# start prototype Dash app
	dashboard = DashboardApp(db_manager)
	dashboard.run(debug=False)


def main():
	# Argument parser for CLI flags
	parser = argparse.ArgumentParser(description="Run the data processing pipeline skipping some steps.")

	parser.add_argument(
		"--skip-read-original-excel",
		dest="read_original_excel",
		action="store_false",
		help="Skip reading original Excel and writing data to the database.",
	)
	parser.add_argument(
		"--read-import-excel",
		dest="read_import_excel",
		action="store_true",
		help="Read preprocessed/manipulated import Excel files with already aggregated data into separate database.",
	)

	parser.add_argument(
		"--pdf-report-years",
		dest="pdf_years",
		nargs="+",
		type=int,
		metavar="YEAR",
		help="Generate a PDF report for selected years (space-separated). Example: --pdf-report-years 2020 2021 2022",
	)
	parser.add_argument(
		"--start-dash", dest="start_dash", action="store_true", help="Launch the interactive dashboard."
	)
	parser.add_argument(
		"--path",
		dest="base_path",
		type=str,
		help=(
			"Set the base path where the 'KI-Labor_strukturiert' data folder is located"
			"and the database files and output will be stored."
		),
	)
	parser.add_argument(
		"--no-table", dest="generate_table", action="store_false", help=("Omit generation of the Ucode summary tables.")
	)

	# Parse arguments
	args = parser.parse_args()

	# Run the process pipeline with parsed arguments
	run_process_pipeline(
		base_path=args.base_path,
		read_original_excel=args.read_original_excel,
		read_import_excel=args.read_import_excel,
		start_dash=args.start_dash,
		pdf_report_years=args.pdf_years,
		generate_table=args.generate_table,
	)


if __name__ == "__main__":
	main()

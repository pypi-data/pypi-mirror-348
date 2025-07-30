import os

import polars as pl

from strahlenexposition_uba.logger_config import get_logger


def load_pseudonyms(data_dir: str, aerztl_stellen: pl.Series) -> dict[str, str]:
	"""Load pseudonym mapping for Aerztl_Stelle values and validate required keys.
		Searches recursively for pseudonym_mapping.csv in data_dir, loads pseudonyms as dict and validates the mapping.

	Args:
		data_dir (str): data directory where pseudonym_mapping.csv is stored
		aerztl_stellen (pl.Series): unique values for Aerztl_Stelle to be pseudonymized.

	Raises:
		KeyError: if file does not have columns 'Aerztl_Stelle' and 'pseudonym'
		FileNotFoundError: if psuedonym_mapping.csv does not exist
		ValueError: if multiple files exists or any Aerztl_Stelle values are missing.


	Returns:
		dict[str, str]: pseudonym mapping formatted as {aerztl_stelle_name: psuedonym_1, ..}
	"""
	pseudonym_file = _find_unique_pseudonym_file(data_dir=data_dir, filename="pseudonym_mapping.csv")

	df = pl.read_csv(pseudonym_file)
	if "Aerztl_Stelle" not in df.columns or "pseudonym" not in df.columns:
		raise KeyError(f"'{pseudonym_file}' must contain 'Aerztl_Stelle' and 'pseudonym' columns.")

	_check_all_present(required=aerztl_stellen, existing=df["Aerztl_Stelle"])

	return dict(zip(df["Aerztl_Stelle"], df["pseudonym"], strict=True))


def _find_unique_pseudonym_file(data_dir: str, filename: str) -> str:
	"""Recursively find a single matching file by name in a directory."""
	matches = [os.path.join(root, filename) for root, _, files in os.walk(data_dir) if filename in files]
	if not matches:
		raise (
			FileNotFoundError(
				f"Could not find {filename} in {data_dir}. "
				f"Create a {filename} in expected format: \n "
				"Aerztl_Stelle, pseudonym \n "
				"aerztl_stelle_1_real_name, pseudonym_1"
			)
		)
	elif len(matches) > 1:
		raise (
			ValueError(
				f"Multiple files named {filename} found in {data_dir}. Ensure only one pseudonym mapping file exists."
			)
		)
	else:
		get_logger().info(f"Apply pseudonymisation using file: {matches[0]}")
		return matches[0]


def _check_all_present(required: pl.Series, existing: pl.Series) -> None:
	"""Check if all required values are present in existing values."""
	if not required.is_in(existing).all():
		raise (
			ValueError(
				"Some Aerztl_Stellen are missing in pseudonym mapping. "
				"Add missing entries to pseudonym_mapping.csv: "
				f"{required.filter(~required.is_in(existing))}"
			)
		)


def calculate_agg_values(df: pl.DataFrame, value_column: str = "Dosiswert") -> pl.DataFrame:
	"""Calculates aggregated values
		Calculates median and number of values grouped by "Jahr", "Aerztl_Stelle", "ID_der_RX", "Untersuchungscode".

		All Rows in the result data frame containing value_column/median = null are dropped with warning.

	Args:
		df (pl.DataFrame): with columnn  "Jahr", "Aerztl_Stelle", "ID_der_RX", "Untersuchungscode" and <value_column>
		value_column (str): numeric column to aggegate on. Defaults to "Dosiswert".

	Raises:
		ValueError: if df is empty
		KeyError: if required columns are missing

	Returns:
		pl.DataFrame: Data frame containing aggregated data in value_column and an additional anzahl_werte column.
	"""
	group_by_cols = ["Jahr", "Aerztl_Stelle", "ID_der_RX", "Untersuchungscode"]
	if df.is_empty():
		raise ValueError("DataFrame is empty.")
	if not set(group_by_cols + [value_column]).issubset(set(df.columns)):
		missing_cols = [col for col in group_by_cols + [value_column] if col not in df.columns]
		raise KeyError(f"Missing column(s) {missing_cols} to calculate_agg_values")

	agg_operations = [
		pl.col(value_column).count().alias("Anzahl_Werte"),
		pl.col(value_column).median().round(3).alias(value_column),
	]
	agg_data = df.group_by(group_by_cols).agg(agg_operations)
	null_count = agg_data[value_column].null_count()
	if null_count > 0:
		get_logger().warning(
			f"{value_column} aggregation resulted in {null_count} null values. Dropping rows with null value."
		)
		agg_data = agg_data.drop_nans(value_column)
	return agg_data

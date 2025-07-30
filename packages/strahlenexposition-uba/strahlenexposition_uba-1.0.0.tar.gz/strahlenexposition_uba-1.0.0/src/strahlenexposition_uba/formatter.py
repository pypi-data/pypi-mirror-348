import re

import numpy as np
import polars as pl

from strahlenexposition_uba.constants import COLUMN_METADATA, COLUMNS_BLACKLIST, UCODE_TO_DOSISWERT_MAPPING
from strahlenexposition_uba.logger_config import get_logger


class LongTableFormatter:
	"""
	Formats and preprocesses long-table dataframes (old template).
	"""

	def __init__(self, metadata: dict):
		"""Initializes LongTableFormatter with a metadata dictionary.

		Args:
			metadata (dict): metadata (dict): A dictionary with the keys "Dateiname", "Arbeitsblatt", "Jahr",
				"Aerztl_Stelle"
		"""
		self.metadata = metadata
		self.colnames = None
		self.first_row = None
		self.header_length = 0
		self.column_mapping = {}
		self.column_dtypes = {}

		self.id_columns = [meta["standard_name"] for meta in COLUMN_METADATA.values() if meta["category"] == "id"]
		self.mandatory_columns = [
			meta["standard_name"] for meta in COLUMN_METADATA.values() if meta["category"] == "mandatory"
		]

	def process_df(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		Processes the input DataFrame by applying a series of transformations to convert it into the desired format.

		This method performs the following steps in order:
			#. Extracts column names from the header rows
			#. Removes leading rows (metadata or header rows) from the DataFrame
			#. Removes columns which contain no data or are blacklisted
			#. Renames the DataFrame's columns based on the column metadata
			#. Adds UCode 8010 to DVT data where no UCodes are provided
			#. Check whether all id columns and at least one value column is present
			#. Forward fill id columns to prevent unnecessary row dropping
			#. Cleans data by stripping unnecessary characters, converting number formats, and casting numeric columns
			#. Add empty columns to archieve the desired format for writing to the database
			#. Fixes the dataframes where there are alternating rows with either CTDI or DLP but not both in one column.
			#. Add ``Dosiswert`` column and write correct data from mandatory column into it
			#. Repeat mean values according to ``(An)zahl`` column if present

		Args:
			df (pl.DataFrame): The input Polars DataFrame that is to be processed.
					This DataFrame may include extra header rows, inconsistent column names,
					and improperly formatted data.

		Returns:
			pl.DataFrame: The transformed Polars DataFrame, cleaned and standardized according to the defined pipeline.

		Example:
			>>> metadata = {
			>>> 	"Dateiname": "Example1.xlsx",
			>>> 	"Jahr": 2020,
			>>>		"Aerztl_Stelle": "BW",
			>>> 	"Arbeitsblatt": "SQL Results",
			>>> }
			>>> df = pl.DataFrame({
			>>> 	"col1": ["ID", "1", "2", "3"],
			>>>		"col2": ["UCode", "1001", "1001", "1002"],
			>>>		"col3": ["CTDIvol", "9.5", "83.2", "10.8"],
			>>>	})
			>>> df = LongTableFormatter(metadata=metadata).process_df(df=df)
		"""

		return (
			df.with_columns(pl.all().replace("", None))  # Regex filters empty strings and formulas
			.pipe(self._get_colnames)
			.pipe(self._remove_leading_rows)
			.pipe(self._remove_useless_columns)
			.pipe(self._rename_columns)
			.pipe(self._dvt_ucode_check)
			.pipe(self._check_for_mandatory_columns)
			.pipe(self._forward_fill_id_columns)
			.pipe(self._clean_data)
			.pipe(self._add_missing_columns)
			.pipe(self._sanitize_dlp_data)
			.pipe(self._add_dosiswert_column)
			.pipe(self._repeat_mean_values)
		)

	def _get_colnames(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		Identifies column names from the dataframe. Does not change the dataframe.
		Correctly identifies if the data is in wide format but old template.

		Raises:
			KeyError: No ID column identified
			IndexError: Unable to identify all columns
		"""
		# Find rows a column contains the string ID
		for col in df.columns:
			potential_first_rows = np.where(df[col].str.contains("ID"))[0]  # TODO: Do not hardcode "ID"
			if potential_first_rows.size != 0:
				self.first_row = potential_first_rows[0]
				break
		if self.first_row is None:
			raise KeyError("No ID column identified")

		# Check if multiple lines belong to the header, up to 10
		header = (
			df[(self.first_row + 1) :].head(10).to_numpy().astype(str)
		)  # Not including the first line of the header
		try:
			# Regex pattern for decimal numbers
			decimal_pattern = np.vectorize(lambda x: bool(re.match(r"^\s*\d+([.,]\d+)?\s*$", str(x))))
			matches = decimal_pattern(header)
			self.header_length = (
				np.argmax(matches.any(axis=1)) + 1 if np.any(matches) else 1
			)  # Add one for the first line
			self.colnames = (
				df[self.first_row : (self.first_row + self.header_length)].select(pl.all().str.concat("")).row(0)
			)
		except IndexError:
			get_logger().error(header)
			raise
		return df

	def _remove_leading_rows(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		Removes the rows before the actual data begins, based on the information in ``self.first_row``
		and ``self.header_length``, effectively cleaning the DataFrame to start from the first data row.

		"""
		first_data_row = self.first_row + self.header_length
		df = df[first_data_row:]
		return df

	def _remove_useless_columns(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		This method filters out blacklisted and empty columns.
		The removal process is based on regular expression matching, ensuring that columns
		with specific naming conventions are excluded from further processing.
		Also drops non-unique optional columns in order to not lose the entire sheet of information.
		"""
		# Drop entirely empty columns
		idx_nonempty_columns = {i for i, col in enumerate(df.columns) if not df[col].is_null().all()}
		# Remove specific columns as defined in a list
		non_blacklist_columns = {
			i
			for i, col in enumerate(self.colnames)
			if not any(re.search(pattern, col, re.IGNORECASE) for pattern in COLUMNS_BLACKLIST)
		}
		# Remove non-unique versions of optional columns (losing some info is worth it for getting the mandatory data)
		mandatory_and_first_optional_columns = set()
		for pattern, meta in COLUMN_METADATA.items():
			for idx, name in enumerate(self.colnames):
				name_lower = str(name).lower()
				if re.search(pattern, name_lower):
					mandatory_and_first_optional_columns.add(idx)
					if meta["category"] == "optional":
						break  # Stop after the first match for this regex
		idx_keep_columns = idx_nonempty_columns.intersection(
			non_blacklist_columns, mandatory_and_first_optional_columns
		)  # Keep only columns which are in all sets
		if len(idx_keep_columns) < len(df.columns):
			get_logger().debug(
				f"{self.metadata['Dateiname']}, {self.metadata['Arbeitsblatt']}: "
				f"Removed {len(df.columns) - len(idx_keep_columns)} cols from dataframe."
			)
		self.colnames = [self.colnames[i] for i in idx_keep_columns]  # Update self.colnames
		df = df.select([df.columns[i] for i in idx_keep_columns])  # Remove columns from dataframe
		return df

	def _rename_columns(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		This method matches column names in the DataFrame to the standard names defined in the column metadata
		using regular expressions. It ensures that each column is mapped to a unique standardized name.
		If the data is in wide format, the function tries to retrieve the data in long format by unpivoting columns
		identified as mandatory data.

		Raises:
			ValueError: If there are duplicate standardized names after renaming columns and potentially unpivoting,
						indicating that the columns could not be uniquely identified.
		"""
		for current_name, name in zip(df.columns, self.colnames, strict=True):
			name_lower = str(name).lower()
			for pattern, meta in COLUMN_METADATA.items():
				if re.search(pattern, name_lower):
					standardized_name = meta["standard_name"]
					self.column_mapping[current_name] = standardized_name
					self.column_dtypes[standardized_name] = meta["dtype"]
					break  # Stop at the first match

		if len(set(self.column_mapping.values())) < len(self.column_mapping):
			# First, try to lengthen a wide data table along the value columns
			value_columns = [key for key, value in self.column_mapping.items() if value in self.mandatory_columns]
			remaining_columns = [
				key for key, value in self.column_mapping.items() if value not in self.mandatory_columns
			]

			df = df.unpivot(
				value_columns,
				index=remaining_columns,
				variable_name="temporary",
				value_name="value",
			)
			df = df.with_columns(pl.col("temporary").replace(self.column_mapping))

			expr = [
				pl.when(pl.col("temporary") == val).then(pl.col("value")).otherwise(None).alias(val)
				for val in self.mandatory_columns
			]
			df = (
				df.with_columns(expr)
				.drop(["temporary", "value"])
				.filter(~pl.all_horizontal(pl.col(self.mandatory_columns).is_null()))
			)
			self.column_mapping = {
				key: value for key, value in self.column_mapping.items() if value not in self.mandatory_columns
			}
			self.column_mapping = dict(self.column_mapping, **{key: key for key in self.mandatory_columns})

		if len(set(self.column_mapping.values())) < len(self.column_mapping):
			# Retest and error out if the column names are still not unique
			raise ValueError(f"Column names could not be uniquely identified. Found this mapping {self.column_mapping}")
		df = df.select(self.column_mapping.keys()).rename(self.column_mapping)  # Rename and filter columns
		self.colnames = df.columns
		return df

	def _dvt_ucode_check(self, df: pl.DataFrame) -> pl.DataFrame:
		"""If the Untersuchungscode column is empty or wasn't present to begin with
		and the excel contains DVT data, we assume that it is of UCode 8010 and
		add the column with that value to the dataframe.
		"""
		logic = ("Untersuchungscode" not in self.colnames) and (
			"dvt" in self.metadata["Dateiname"].lower() or "dvt" in self.metadata["Arbeitsblatt"].lower()
		)
		if logic:
			df = df.with_columns(pl.lit("8010", dtype=pl.String).alias("Untersuchungscode"))
			get_logger().info(
				f"Added Untersuchungscode 8010 to {self.metadata['Dateiname']}, {self.metadata['Arbeitsblatt']}"
			)
			self.colnames = df.columns
		return df

	def _check_for_mandatory_columns(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Checks whether all id columns and at least one mandatory column is present."""
		present_id_columns = {col: col in self.colnames for col in self.id_columns}
		present_mandatory_columns = {col: col in self.colnames for col in self.mandatory_columns}

		if not all(present_id_columns.values()):
			raise KeyError(f"Unable to find all ID columns. {present_id_columns}")
		# All ID columns and at least one value column need to be present
		elif not any(present_mandatory_columns.values()):
			raise ValueError(
				f"""None of the mandatory data columns found. Check the data. 
				In particular {dict(present_id_columns, **present_mandatory_columns)}"""
			)
		return df

	def _forward_fill_id_columns(self, df: pl.DataFrame) -> pl.DataFrame:
		return df.with_columns(df[self.id_columns].fill_null(strategy="forward"))

	def _clean_data(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		Cleans the data in the provided Polars DataFrame by performing the following operations:
			* Extracting 4 digit numbers from ``Untersuchungscode`` column
			* Dropping rows with NULL values in ID columns.
			* Stripping leading and trailing whitespace from string columns.
			* Replacing commas with dots in string columns to standardize numeric values.
			* Removing trailing dots from string columns.
			* Removing entries which are formatted as datetimes.
			* Removing all ``-`` and ``_``
			* Casting numeric columns to ``Float64`` after converting them to decimal values, ensuring that non-numeric
				entries are removed.
		"""
		# Get ID columns from metadata
		numeric_columns = [
			meta["standard_name"]
			for meta in COLUMN_METADATA.values()
			if meta["dtype"] == pl.Float64
			and meta["standard_name"] in self.colnames  # Columns which occur in the dataframe and contain numbers
		]
		# Test whether the numeric columns contain anything which can not be cast to a number
		df = (
			df.with_columns(pl.col("Untersuchungscode").str.extract(r"(\d{4})"))  # Extract 4 digit string from UCode
			.drop_nulls(self.id_columns)  # Drop rows with NULL in ID columns
			.with_columns(pl.col(numeric_columns).str.replace_all("\s", ""))  # Strip all whitespace in string columns
			.with_columns(pl.col(numeric_columns).str.replace_all(",", "."))  # Switch every comma to a dot
			.with_columns(pl.col(numeric_columns).str.strip_chars_end("."))  # Remove trailing dots
			.with_columns(
				pl.col(numeric_columns).str.replace_all("\d{1,4}[-/]\d{1,4}[-/]\d{1,4}.*", "")
			)  # Remove dates
			.with_columns(pl.col(numeric_columns).str.replace_all("-|_", ""))  # Remove all - and _ in the data
			.with_columns(pl.col(numeric_columns).str.extract(r"(\d+\.?\d*)"))
			.with_columns(pl.col(numeric_columns).cast(pl.Float64).round(2))  # Cast numeric columns to dtype Float64
		)
		return df

	def _add_missing_columns(self, df: pl.LazyFrame) -> pl.DataFrame:
		"""
		If a mandatory column from ``COLUMN_METADATA`` is missing in ``df``, it is added with ``None`` values
		and cast to the appropriate data type.
		"""

		missing_columns = [
			(meta["standard_name"], meta["dtype"])
			for meta in COLUMN_METADATA.values()
			if (
				meta["standard_name"] not in self.colnames  # Columns that don't exist in the DataFrame yet
				and meta["category"] == "mandatory"
			)
		]

		df = df.with_columns([pl.lit(None, dtype=dtype).alias(col) for col, dtype in missing_columns])
		return df

	def _sanitize_dlp_data(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Fixes the dataframes where there are alternating rows with either CTDI or DLP but not both in
		one column. Checks if the format is met, then adds the DLP data to the filled CTDI rows and removes
		rows where CTDI is Null only.
		"""

		def get_sparse_data(df: pl.DataFrame) -> list[tuple[str, str]]:
			"""Returns list of 'ID_der_RX', 'Untersuchungscode' where both 'CTDI' and 'DLP' are
			exactly 50% not Null values"""
			list_sparse_groups = (
				df.group_by(["ID_der_RX", "Untersuchungscode"])
				.agg(
					[
						pl.col("CTDI").count().alias("CTDI_not_null"),
						pl.col("DLP").count().alias("DLP_not_null"),
						pl.len().alias("group_size"),
					]
				)  # Count non-null values in CTDI and DLP
				.with_columns(pl.col(["CTDI_not_null", "DLP_not_null"]) / pl.col("group_size"))
				.with_columns(
					((pl.col("CTDI_not_null") == 0.5) & (pl.col("DLP_not_null") == 0.5)).alias("wrong_format")
				)  # Check if exactly half the CTDI and DLP values are filled and the othre half is NA grouped by IDs
				.filter(pl.col("wrong_format"))
				.select(["ID_der_RX", "Untersuchungscode"])
			).rows()
			return list_sparse_groups

		if "DLP" not in df.columns:  # Nothing to do if no DLP
			return df

		id_ucode_pairs = get_sparse_data(df)  # Returns list[tuple[str, str]]
		if len(id_ucode_pairs) == 0:  # Also nothing to do if there is no sparse data
			return df

		# Convert id_ucode_pairs to a Polars DataFrame
		id_ucode_df = pl.DataFrame(id_ucode_pairs, schema=["ID_der_RX", "Untersuchungscode"], orient="row")
		# Filtered dataframe (matching rows)
		filtered_df = df.join(id_ucode_df, on=["ID_der_RX", "Untersuchungscode"], how="semi")
		# Remaining dataframe (non-matching rows)
		df_remaining = df.join(id_ucode_df, on=["ID_der_RX", "Untersuchungscode"], how="anti")

		dlp_values = filtered_df["DLP"].drop_nulls()  # Extract "DLP" values before dropping null "CTDI" rows
		filtered_df = filtered_df.filter(pl.col("CTDI").is_not_null()).with_columns(
			pl.Series(name="DLP", values=dlp_values)
		)  # Drop rows where "CTDI" is null and add "DLP" values

		result_df = df_remaining.vstack(filtered_df)  # Attach filtered_df back to df_remaining
		return result_df

	def _add_dosiswert_column(self, df: pl.DataFrame) -> pl.DataFrame:
		"""
		Adds a ``Dosiswert`` column based on the ``Untersuchungscode`` using predefined rules.
		If the ``Dosiswert`` is empty afterwards. Throw a warning and try to fill with one of
		the other columns.
		"""

		expr = pl.when(pl.lit(False)).then(None)  # Initialize expression

		for pattern, column in UCODE_TO_DOSISWERT_MAPPING.items():
			condition = pl.col("Untersuchungscode").str.contains(pattern)
			expr = expr.when(condition).then(pl.col(column))
		# Add the fallback value
		expr = expr.otherwise("DFP").alias("Dosiswert")
		# Apply the transformation
		df = df.with_columns(expr)

		null_count_before_fill = df["Dosiswert"].is_null().sum()
		# If the dosiswert column is still empty afterwards, we can fill with any other column
		if null_count_before_fill > 0:
			df = (
				df.with_columns(
					(
						pl.concat_list(self.mandatory_columns).list.eval(pl.element().is_not_null()).list.sum() == 1
					).alias("one_value_col")  # Checks whether exactly one column is filled
				)
				.with_columns(
					pl.when(pl.col("one_value_col") & pl.col("Dosiswert").is_null())
					.then(pl.coalesce(self.mandatory_columns))
					.otherwise("Dosiswert")
					.alias("Dosiswert")
				)
				.drop("one_value_col")
			)
			null_count_after_fill = df["Dosiswert"].is_null().sum()
			if (
				(null_count_before_fill - null_count_after_fill) > 0 & null_count_after_fill > 0
			):  # If nothing changed, the columns were probably not important
				get_logger().warning(
					f"file: ({self.metadata['Dateiname']}, {self.metadata['Arbeitsblatt']}) "
					f"{null_count_before_fill} rows with 'Dosiswert' in wrong data column. "
					f"Filled {null_count_before_fill - null_count_after_fill} from other data columns. "
					f"{null_count_after_fill} rows remain empty."
				)
		return df.drop_nulls("Dosiswert")

	def _repeat_mean_values(self, df: pl.LazyFrame) -> pl.LazyFrame:
		"""Sometimes what appears to be a single value in an excel sheet is
		already an aggregation of multiple values. In that case we repeat the singular
		value n times according to the "Anzahl" column in order to get more accurate summary
		statistics.
		"""
		if "Meldungsart" in self.colnames and "Anzahl" in self.colnames:
			df = (
				df.with_columns(
					#  If "Anzahl" is mising but Meldungsart == "MW" assume its 10 data points
					pl.when((pl.col("Meldungsart") == "MW") & pl.col("Anzahl").is_null())
					.then(pl.lit(10))
					.otherwise(pl.col("Anzahl"))
					.alias("Anzahl")
				)
				.with_columns(
					# Write dosiswerte to a list repeated "Anzahl" times or once if no Anzahl
					pl.col("Dosiswert").repeat_by(pl.col("Anzahl").fill_null(1))
				)
				.explode("Dosiswert")
			)
		return df


class NewTableFormatter(LongTableFormatter):
	"""
	Formats and preprocesses wide-table dataframes (new template).
	"""

	def __init__(self, metadata):
		"""Initialises formatter for the new template. Uses the string ``Gerätebezeichnung`` as
		anchor to find the beginning of the data

		Args:
			metadata (dict): metadata (dict): A dictionary with the keys "Dateiname", "Arbeitsblatt", "Jahr",
				"Aerztl_Stelle"
		"""
		super().__init__(metadata)
		self.betreiber = None
		self.id_der_rx = None
		self.value_columns = None
		self.value_type = None
		self.search_str = "Gerätebezeichnung"

	def process_df(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Processor pipeline which transforms the excel sheet into an input for refiner and the database.
		Check documentation of the called methods for details. Result is aligned with

		Args:
			df (pl.DataFrame): The input Polars DataFrame that is to be processed.
				It must be in the format of the new template from 2023

		Returns:
			pl.DataFrame: The transformed Polars DataFrame, cleaned and standardized according to the defined pipeline.
		"""
		return (
			df.with_columns(pl.all().str.replace("xxx", ""))
			.with_columns(pl.all().replace("", None))
			.pipe(self._get_id_col)
			.pipe(self._remove_junk, search_str=self.search_str)
			.pipe(self._get_colnames)
			.pipe(self._unpivot_dataframe)
			.pipe(super()._check_for_mandatory_columns)
			.pipe(super()._clean_data)
			.pipe(super()._add_missing_columns)
			.pipe(super()._add_dosiswert_column)
		)

	def _get_id_col(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Sets the ID column as ``{Dateiname}_{Arbeitsblatt}``."""
		betreiber_loc = self._find_string_location(df, search_str="Info Betreiber:")[0]
		self.betreiber = df[betreiber_loc[0] + 1 :, betreiber_loc[1]].str.join("_")[0]
		if self.betreiber == "":
			self.betreiber = None
		self.id_der_rx = f"{self.metadata['Dateiname']}_{self.metadata['Arbeitsblatt']}"
		return df

	def _remove_junk(self, df: pl.DataFrame, search_str: str) -> pl.DataFrame:
		"Finds beginning of the data and removes everything to the left and above it"
		data_start_loc = self._find_string_location(df, search_str=search_str)
		if len(data_start_loc) > 1:
			raise ValueError("More than one dataset on this sheet. Duplicate sheet and split the data")
		if len(data_start_loc) == 0:
			raise KeyError(f"Unable to find the beginning of the data: No `{search_str}` entry")
		data_start_loc = data_start_loc[0]
		df = df[data_start_loc[0] :, data_start_loc[1] :]
		return df

	def _generate_column_mapping(self):
		# Generate column mapping
		for name in self.colnames:
			name_lower = str(name).lower()
			for pattern, meta in COLUMN_METADATA.items():
				if re.search(pattern, name_lower):
					standardized_name = meta["standard_name"]
					self.column_mapping[name] = standardized_name
					self.column_dtypes[standardized_name] = meta["dtype"]
					break  # Stop at the first match

	def _get_colnames(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Retrieve column names and which of the columns are data columns, this is necessary for unpivoting the
		dataframe. Creates a mapping from current colnames to standardized names."""
		self.colnames = df.head(2).select(pl.all().str.concat(" ")).row(0)
		# Generate column mapping
		self._generate_column_mapping()
		filtered_items = [(key, value) for key, value in self.column_mapping.items() if value in self.mandatory_columns]
		self.value_columns = [key for key, _ in filtered_items]
		try:
			self.value_type = filtered_items[0][1]  # First colname value. The rest should be the same given the UCode
		except Exception:
			raise ValueError(f"There appears to be no data in the sheet. Found the columns: {self.colnames}") from None
		return df

	def _unpivot_dataframe(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Main processor method for the data sheet. It
		* Removes first two rows which contain the colnames
		* Formats UCodes
		* Adds columns for ID and Betreiber
		* Tries forward then backward fill of the Gerätebezeichnung column
		* Unpivots the value columns to get a long dataframe
		"""
		code_nr = {k: v for k, v in self.column_mapping.items() if v == "Untersuchungscode"}
		df = (
			df.lazy()
			.slice(2)
			.rename(dict(zip(df.columns, self.colnames, strict=True)))
			.rename(code_nr)
			.filter(pl.col("Untersuchungscode").str.contains(r"(\d{4})"))
			.select(
				[
					pl.all().exclude(["Anzahl", "Untersuchungsart"] + self.value_columns),
					pl.lit(self.id_der_rx).alias("ID_der_RX"),
					pl.lit(self.betreiber).alias("Betreiber"),
					pl.concat_list(self.value_columns).alias(self.value_type),
				]
			)
			.with_columns(pl.col("Gerätebezeichnung").fill_null(strategy="forward"))  # Try forward fill
			.with_columns(pl.col("Gerätebezeichnung").fill_null(strategy="backward"))  # Then try backward
			.explode(self.value_type)
			.drop_nulls(self.value_type)
			.collect()
		)
		self.colnames = df.columns
		return df

	@staticmethod
	def _find_string_location(df: pl.DataFrame, search_str: str):
		"Finds tuples of (row, column) where the search string is present"
		mask_df = df.with_columns(
			[
				pl.when(pl.col(col).str.contains(search_str, literal=True)).then(True).otherwise(False).alias(col)
				for col in df.columns
			]  # Mask of df. True if "Gerätebezeichnung" in cell
		)
		matches = (
			mask_df.with_row_index(name="row_nr")
			.unpivot(index="row_nr")
			.filter("value")
			.select(["row_nr", "variable"])
			.rows()
		)
		return matches


class BayernFormatter(NewTableFormatter):
	"""Handles data with the old Bayern template"""

	def __init__(self, metadata: dict):
		"""Initializes BayernFormatter with a metadata dictionary.

		Args:
			metadata (dict): metadata (dict): A dictionary with the keys "Dateiname", "Arbeitsblatt", "Jahr",
				"Aerztl_Stelle"
		"""
		super().__init__(metadata)
		self.betreiber = None
		self.id_der_rx = None
		self.value_columns = None
		self.value_type = None
		self.search_str = "Code-Nr."

	def _get_id_col(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Uses filename as ID for the data. This works since the files are named accordingly.
		Necessary to overwrite the parent function s.t. the pipeline still works"""

		self.id_der_rx = self.metadata["Dateiname"]
		return df

	@staticmethod
	def _clean_colname(x: str | None):
		"""Checks for columns which are named [1-10] and adds a DFP s.t. they are identified as data columns"""
		if x is None:
			return ""
		y = re.search("\d{1,2}", x)
		if y and 1 <= int(y[0]) <= 10:
			return f"DFP {y}"
		else:
			return x

	def _get_colnames(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Checks which of the two formats the data is. Retrieves the column names and makes them unique if necessary.
		Identifies which of the columns contain relevant data."""

		# TODO: Reicht das zur Unterscheidung?
		if self.metadata["Arbeitsblatt"] in ["Durchleuchtungsuntersuchungen", "CT-Untersuchungen"]:
			self.colnames = df.head(2).select(pl.all().str.concat(" ")).row(0)
			self.colnames = [
				x + "1" + str(y) for x, y in zip(self.colnames, range(len(self.colnames)), strict=True)
			]  # Make colnames unique
		else:
			self.colnames = [self._clean_colname(x) for x in df.row(0)]

		# Generate column mapping
		self._generate_column_mapping()
		filtered_items = [(key, value) for key, value in self.column_mapping.items() if value in self.mandatory_columns]
		self.value_columns = [key for key, _ in filtered_items]
		try:
			self.value_type = filtered_items[0][1]  # First colname value. The rest should be the same given the UCode
		except Exception as error:
			raise ValueError(
				f"There appears to be no data in the sheet. Found the columns: "
				f"{self.colnames} \n and filtered items {filtered_items}, original error msg: {error}"
			) from None
		return df

	def _unpivot_dataframe(self, df: pl.DataFrame) -> pl.DataFrame:
		"""Small adjustments from the parent function. Removed parts for
		Betreiber and Gerätebezeichnung as these are not present. Rest is the same."""
		code_nr = {k: v for k, v in self.column_mapping.items() if v == "Untersuchungscode"}

		df = (
			df.lazy()
			.rename(dict(zip(df.columns, self.colnames, strict=True)))
			.rename(code_nr)
			.filter(pl.col("Untersuchungscode").str.contains(r"(\d{4})"))
			.select(
				[
					pl.col("Untersuchungscode"),
					pl.lit(self.id_der_rx).alias("ID_der_RX"),
					pl.concat_list(self.value_columns).alias(self.value_type),
				]
			)
			.explode(self.value_type)
			.drop_nulls(self.value_type)
			.collect()
		)
		self.colnames = df.columns
		return df

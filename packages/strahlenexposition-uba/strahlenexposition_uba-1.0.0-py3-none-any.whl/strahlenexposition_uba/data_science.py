import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import polars as pl
from adjustText import adjust_text
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from strahlenexposition_uba import logger_config
from strahlenexposition_uba.database import DataManager
from strahlenexposition_uba.logger_config import get_logger


### --------------------------- Summary table for UCodes --------------------------- ###
def create_ucode_summary_table(
	df_table: pl.DataFrame, years: list[int] | None, value_text: str = "Dosiswert"
) -> pl.DataFrame:
	"""Creates a dataframe of summary statistics per UCode (optionally only for some of the years).

	Args:
		df_table (pl.DataFrame): Dataframe of values with `{value_test}`, `Jahr`, `Bezeichnung`, `DRW_aktuell`,
			`Deff` and `UCode` columns
		years (list[int] | None): Optional list of years to consider. If None, uses all data
		value_text (str, optional): Name of the value column. Defaults to "Dosiswert".

	Returns:
		pl.DataFrame: Dataframe of summary statistics, each row is one UCode. Ready to export to excel.
	"""

	df_table = df_table.filter(pl.col("Jahr").is_in(years))
	df_table_agg = (
		df_table.group_by(["UCode", "Bezeichnung", "DRW_aktuell", "Deff"])
		.agg(
			[
				pl.len().alias("Anzahl \n Mediane"),
				(
					(pl.col(value_text).quantile(0.75) - pl.col(value_text).quantile(0.25))
					/ (pl.col(value_text).quantile(0.75) + pl.col(value_text).quantile(0.25))
				).alias("Relevanz \n (QCD)"),
				pl.col(value_text).quantile(0.25).alias("P25"),
				pl.col(value_text).quantile(0.5).alias("Median"),
				pl.col(value_text).quantile(0.75).alias("P75"),
			]
		)
		.sort("UCode")
		.with_columns(pl.col("UCode").cast(pl.String))
		.rename({"DRW_aktuell": "DRW", "UCode": "Code"})
		.with_columns(
			[
				pl.col(["Relevanz \n (QCD)", "Deff"]).round(2),
				pl.col(["P25", "Median", "P75"]).round(1),
			]
		)
	)[
		"Code",
		"Bezeichnung",
		"Anzahl \n Mediane",
		"Relevanz \n (QCD)",
		"P25",
		"Median",
		"P75",
		"DRW",
		"Deff",
	]
	return df_table_agg


### --------------------------- Outlier Detection --------------------------- ###
def remove_outliers(df: pl.DataFrame, threshold: float, scaled_col: str) -> tuple[pl.DataFrame, pl.DataFrame]:
	"""Removes all values from <df> greater than <threshold> in the column <y_col>.
	Returns a dataframe without outliers and one with only outliers.

	Args:
		df (pl.DataFrame): dataframe containing the column <y_col>.
		threshold (float): Threshold below which all values in <y_col> should be.
		scaled_col (str): name of column with scaled data, "ratio_of_DRW"

	Returns:
		pl.DataFrame: dataframe with all outliers (values above threshold) removed.
		pl.DataFrame: dataframe with only outliers
	"""

	# remove NaNs, sort by <y_col> (descending)
	df = df.filter(pl.col(scaled_col).is_not_nan())
	df = df.sort(pl.col(scaled_col), descending=True)
	n_datapoints = df.select(pl.len()).item()

	# identify outliers (rows where <y_col> is above <threshold>)
	df_outliers = df.filter(pl.col(scaled_col) > threshold)
	n_outliers = df_outliers.select(pl.len()).item()
	outlier_ratio = n_outliers / n_datapoints
	get_logger().info(
		f"There are {n_outliers} outliers ({outlier_ratio:.2%} of the data) with {scaled_col} > {threshold}."
	)

	# calculate ratio of doses above the DRW
	n_above_DRW = df.filter(pl.col(scaled_col) > 1).select(pl.len()).item()
	above_DRW_ratio = n_above_DRW / n_datapoints
	get_logger().info(f"{above_DRW_ratio:.2%} of the doses applied were above the DRW. ")

	# remove outliers from dataframe
	df_without_outliers = df.filter(pl.col(scaled_col) <= threshold)

	return df_without_outliers, df_outliers


def write_outliers_into_excel_file(
	df_outliers: pl.DataFrame, scaled_col: str, output_path: str, years: list[int] | None
):
	"""Writes all outliers into excel file.

	Args:
		df_outliers (pl.DataFrame): dataframe with all outliers
		scaled_col (str): name of column with scaled doses, e.g. "ratio_of_DRW"
		output_path (str): path to folder "output" where excel will be stored
		years (list[int] | None): years considered in the dataframe. If None, all years are used.
	"""

	# write outliers to Excel file
	title = f"Outliers_{'_'.join(str(x) for x in years)}.xlsx" if years else "Outliers_all_years.xlsx"
	outlier_path = os.path.join(output_path, title)
	df_outliers_pd = df_outliers.to_pandas()  # convert to pandas

	with pd.ExcelWriter(outlier_path, engine="xlsxwriter") as writer:
		df_outliers_pd.to_excel(writer, sheet_name="All outliers", index=False)
		workbook = writer.book
		worksheet = writer.sheets["All outliers"]

		# define formats (avoid thousands separator, number of decimals)
		format_float1 = workbook.add_format({"num_format": "0.0", "align": "right"})
		format_int = workbook.add_format({"num_format": "0", "align": "right"})
		format_string = workbook.add_format({"align": "left"})

		# map formats to columns
		int_columns = ["Jahr", "UCode"]
		float_columns = ["Dosiswert", scaled_col, "DRW_aktuell"]
		string_columns = ["Dateiname", "Arbeitsblatt", "Aerztl_Stelle", "ID_der_RX"]
		col_to_idx = {name: idx for idx, name in enumerate(df_outliers_pd.columns)}

		for col in int_columns:
			idx = col_to_idx[col]
			worksheet.set_column(idx, idx, 8, format_int)

		for col in string_columns:
			idx = col_to_idx[col]
			worksheet.set_column(idx, idx, 15, format_string)

		for col in float_columns:
			idx = col_to_idx[col]
			worksheet.set_column(idx, idx, 15, format_float1)

			# zusätzliche Sheets pro Aerztl_Stelle

		aerztl_stellen = df_outliers_pd["Aerztl_Stelle"].unique()

		for stelle in sorted(aerztl_stellen):
			df_stelle = df_outliers_pd[df_outliers_pd["Aerztl_Stelle"] == stelle]

			# create new sheet for ÄS (set max. length to 31 characters)
			sheet_name = str(stelle)[:31]
			df_stelle.to_excel(writer, sheet_name=sheet_name, index=False)

			# Formatting
			ws = writer.sheets[sheet_name]

			for col in int_columns:
				idx = col_to_idx[col]
				ws.set_column(idx, idx, 8, format_int)

			for col in string_columns:
				idx = col_to_idx[col]
				ws.set_column(idx, idx, 15, format_string)

			for col in float_columns:
				idx = col_to_idx[col]
				ws.set_column(idx, idx, 15, format_float1)


def plot_standardized_dosiswerte_histogram(path: str, df: pl.DataFrame, threshold: float, scaled_col: str, title: str):
	"""Plots a histogram of the standardized dose values with a quantile of choice (e.g. 95% quantile).

	Args:
		path (str): path to folder where the figure is saved
		df (pl.DataFrame): dataframe with column of scaled dose values
		threshold (float): Threshold of scaled dose value to be displayed in histogram, e.g. threshold=10
		scaled_col (str): column name of scaled dose values, e.g. "ratio_of_DRW"
		title (str): title of the plot
	"""

	quantile_value = 0.95
	dosiswerte_std = df.select(scaled_col).to_series().drop_nulls().to_list()
	quantile = np.nanquantile(dosiswerte_std, quantile_value)
	get_logger().info(f"{quantile_value:.1%} of the doses are below {round(quantile, 2)} * DRW.")

	plot_title = title.replace("_", " ")
	df = df.filter(pl.col(scaled_col) < threshold)
	fig = px.histogram(
		df,
		x=scaled_col,
		nbins=1000,
		width=700,
		height=300,
		title=plot_title,
	)
	fig.add_vline(
		x=quantile,
		line_width=2,
		line_dash="dot",
		line_color="darkred",
		annotation_text=f"{100 * quantile_value}% quantile: {round(quantile, 2)}",
		annotation_font_color="darkred",
	)

	filename = title.replace("<br>", "")
	fig.write_image(os.path.join(path, f"{filename}.pdf"))
	return fig


### --------------------------- Clustering --------------------------- ###
def _impute_nans_with_row_mean(df_pivot: pl.DataFrame, cluster_col: str) -> pl.DataFrame:
	"""NaN imputation: For each element in <cluster_col>, the row mean is calculated.
	All NaNs in this row are replaced with the row mean.

	Args:
		df (pl.DataFrame): pivot dataframe with column <cluster_col>
		cluster_col (str): name of column to be clustered by.

	Returns:
		pl.DataFrame: dataframe with row means instead of NaNs
	"""

	# 1. select only columns containing data (cut off first column containing row labels)
	data_cols = [col for col in df_pivot.columns if col != cluster_col]

	# 2. calculate mean of rows
	means_by_row = df_pivot.select(pl.mean_horizontal(*data_cols).alias("row_mean"))

	# 3. Add row mean as new column (temporarily)
	df_with_mean = df_pivot.with_columns([means_by_row["row_mean"]])

	# 4. Replace NaNs in each data column by row_mean
	df_imputed = df_with_mean.with_columns(
		[pl.when(pl.col(col).is_null()).then(pl.col("row_mean")).otherwise(pl.col(col)).alias(col) for col in data_cols]
	)

	# 5. Remove row_mean column
	df_imputed = df_imputed.drop("row_mean")

	return df_imputed


def cluster_by_column(
	path: str, df: pl.DataFrame, data_col: str, cluster_col: str, agg_col: str, quantity: str, years: list[int] | None
):
	"""Peforms a k-means clustering on the UCode-standardized aggregated dose data.
	The median scaled dose per ÄS and UCode is calculated. Then,
	NaN values are replaced with the row mean (the mean per <cluster_col>).
	For clustering of UCodes, a PCA is performed for dimensionality reduction.
	For clustering of Aerztl_Stelle, the original data matrix is used (this was decided
	based on the quality of clustering results).
	K-Means clustering and visualization are called in external functions.

	Args:
		path (str): path to output folder where clustering results will be saved
		df (pl.DataFrame): Dataframe containing columns <data_col>, <cluster_col> and <agg_col>
		data_col (str): Name of column with data, e.g. "ratio_of_DRW" or "QCD"
		cluster_col (str): Name of column by which should be clustered, e.g. "Aerztl_Stelle"
		agg_col (str): Column to be aggregated by, e.g. "UCode"
		quantity (str): choose how data are aggregated. Can be "median" or "QCD"
		years (list[int] | None): years considered in the dataframe. If None, all years are used.
	"""
	# create pivot table with <agg_col> as cols and <cluster_col> as rows.
	# Values: Median or QCD of standardized dose values for all years and IDs,
	# so only one datapoint per <cluster_col> and <agg_col> remains
	if quantity == "median":
		df_agg = df.group_by([cluster_col, agg_col]).agg(pl.median(data_col).alias("value"))

	elif quantity == "QCD":
		df_agg = (
			df.group_by([cluster_col, agg_col])
			.agg([pl.col(data_col).quantile(0.75).alias("q3"), pl.col(data_col).quantile(0.25).alias("q1")])
			.with_columns(((pl.col("q3") - pl.col("q1")) / (pl.col("q3") + pl.col("q1"))).alias("value"))
			.drop(["q1", "q3"])
		)
	else:
		raise ValueError(f"quantity must be 'median' or 'QCD' but is {quantity} instead.")

	# Pivot: cluster_col as rows, agg_col as columns, value as median/QCD
	df_pivot = df_agg.pivot(values="value", index=cluster_col, on=agg_col).sort(cluster_col)

	# Data imputation
	df_imputed = _impute_nans_with_row_mean(df_pivot, cluster_col)

	# extract numeric values from pivot table
	X = df_imputed.select(pl.exclude(cluster_col)).to_numpy()

	if cluster_col == "UCode":
		get_logger().info(f"For clustering of UCodes based on {quantity}, a PCA is performed.")
		exp_var_threshold = 0.95
		X, cum_var = _perform_pca(X, exp_var_threshold)  # PCA for dimensionality reduction
		_scree_plot(path, cluster_col, quantity, exp_var_threshold, cum_var)

	df_clustered = _kmeans(df_imputed, X)

	_plot_clustering_results(path, df_clustered, X, data_col, cluster_col, quantity, years)


def _kmeans(df_clust_input: pl.DataFrame, X: np.ndarray) -> pd.DataFrame:
	"""
	Performs a k-means clustering on df_clust_input. The data are clustered into n_clusters
	groups and the labels are saved in column "Cluster".
	Args:
		df_clust_input (pl.DataFrame): pivot table with Aerztl_Stellen as rows and UCodes as columns
		X (np.ndarray): data from dataframe (without first column) as numpy array

	Returns:
		pd.DataFrame: pandas dataframe with added column "Cluster"
	"""

	# K-Means Clustering
	kmeans = KMeans(n_clusters=4, random_state=42)
	labels = kmeans.fit_predict(X)

	# convert to pandas df, add label column
	df_clustered = df_clust_input.to_pandas()
	df_clustered["Cluster"] = labels

	return df_clustered


def _plot_clustering_results(
	path: str,
	df_clustered: pl.DataFrame,
	X: np.ndarray,
	data_col: str,
	cluster_col: str,
	quantity: str,
	years: list[int] | None,
):
	"""Performs a Principal Component Analysis (PCA) with 2 components on the data for visualization.
	The data points are plotted in 2D with the components as axes and are colored by their cluster label.

	Example with cluster_col="Aerztl_Stelle" and agg_col="UCode":
	Per ÄS, there are n_ucodes features (one for each UCode), or n_ucodes dimensions. Those are reduced to 2D by PCA.

	Args:
		path (str): path to output folder where plots will be saved.
		df_clustered (pd.DataFrame): Pivot table: Aerztl_Stellen vs. UCode with added column "Cluster"
		X (np.ndarray): data from dataframe (without columns "Aerztl_Stelle" and "Cluster") as numpy array
		data_col (str): Name of column with scaled data, e.g. "ratio_of_DRW"
		cluster_col (str): Name of column by which should be clustered, e.g. "Aerztl_Stelle"
		agg_col (str): Column to be aggregated by, e.g. "UCode"
		years (list[int] | None): years considered in the dataframe. If None, all years are used.
	"""
	pca = PCA(n_components=2)
	coords_2d = pca.fit_transform(X)

	df_clustered = df_clustered.copy()
	df_clustered["PCA_1"] = coords_2d[:, 0]
	df_clustered["PCA_2"] = coords_2d[:, 1]

	clusters = sorted(df_clustered["Cluster"].unique())
	colors = plt.get_cmap("jet", len(clusters))

	fig, ax = plt.subplots(figsize=(12, 8))
	texts = []

	for i, cluster in enumerate(clusters):
		cluster_df = df_clustered[df_clustered["Cluster"] == cluster]
		color = colors(i)
		ax.scatter(cluster_df["PCA_1"], cluster_df["PCA_2"], label=f"Cluster {cluster}", color=color, s=50)

		# prepare annotations
		for _, row in cluster_df.iterrows():
			annot_text = str(int(row[cluster_col])) if cluster_col == "UCode" else str(row[cluster_col])
			text = ax.text(row["PCA_1"], row["PCA_2"], annot_text, fontsize=9, weight="bold")
			texts.append(text)

	# automatic placement of annotations
	adjust_text(
		texts,
		arrowprops=dict(arrowstyle="->", color="black", lw=0.6, mutation_scale=6),
		ax=ax,
		expand_text=(1.05, 1.2),
		expand_points=(1.05, 1.2),
		only_move={"points": "y", "text": "xy"},
	)

	years_str = f"years {', '.join(str(x) for x in years)}" if years else "all years"
	filename = f"Clustering_of_{cluster_col}_by_{quantity}_of_{data_col}_for_{years_str}"
	title = filename.replace("_", " ")
	ax.set_title(title)
	ax.set_xlabel("Principal Component 1", fontsize=15)
	ax.set_ylabel("Principal Component 2", fontsize=15)
	ax.legend()
	plt.tight_layout()
	plt.savefig(os.path.join(path, f"{filename}.pdf"))

	return fig


def _scree_plot(
	path: str,
	cluster_col: str,
	quantity: str,
	explained_variance_threshold: float,
	cum_var: list[float],
):
	"""Creates a scree plot (n_components vs. achieved explained variance ratio).

	Args:
		path (str): path to folder where plot is saved
		cluster_col (str): Name of column by which should be clustered, e.g. "Aerztl_Stelle"
		quantity (str): choose how data are aggregated. Can be "median" or "QCD"
		explained_variance_threshold (float): minimum explained variance that should be reached, e.g. 0.95
		cum_var (float): list of achieved explained variance
	"""

	title = f"Scree_plot_of_PCA_for_clustering_of_{cluster_col}_based_on_the_{quantity}"
	plot_title = title.replace("_", " ")

	# Scree Plot
	plt.figure(figsize=(8, 5))
	plt.plot(range(1, len(cum_var) + 1), cum_var * 100, marker="o")
	plt.xlabel("Number of principal components")
	plt.ylabel("Achieved explained variance [%]")
	plt.grid(True)
	plt.axhline(
		y=explained_variance_threshold * 100,
		color="r",
		linestyle="--",
		label=f"{explained_variance_threshold * 100:.0f}% Schwelle",
	)
	plt.title(plot_title)
	plt.legend()
	plt.tight_layout()

	filename = f"{title}.pdf"
	plt.savefig(os.path.join(path, filename))


def _perform_pca(X: np.ndarray, exp_var_threshold: float) -> np.ndarray:
	"""Performs a Principal component analysis (PCA) on the data X to reduce dimensionality.
	This can help to make the clustering more stable.

	Args:
		X (np.ndarray): data to be reduced in dimensionality
		exp_var_threshold (float): threshold of minimum explained variance ratio that the dimensionality-reduced
		data should contain, e.g. 0.95

	Returns:
		np.ndarray: data with reduced dimensions
		float: achieved explained variance
	"""

	# Scale data
	X_scaled = StandardScaler().fit_transform(X)

	# PCA with automatic choice of n_components for 95% explained variance
	pca = PCA(n_components=exp_var_threshold)
	X_pca = pca.fit_transform(X_scaled)

	# achieved explained variance with n_components
	cum_var = np.cumsum(pca.explained_variance_ratio_)

	# Number of components required to reach exp_var_threshold
	n_components = np.argmax(cum_var >= exp_var_threshold) + 1
	get_logger().info(
		f"{n_components} principal components are required for ≥ {exp_var_threshold:.1%} explained variance. \
		Achieved explained variance: {cum_var[n_components - 1]:.2%}"
	)

	return X_pca, cum_var


### --------------------------- General functions --------------------------- ###
def _scale_relative_to_drw(df: pl.DataFrame, y_col: str, scaled_col: str) -> pl.DataFrame:
	"""Add column to <df> with the ratio of the dose and the current DRW.

	Args:
		df (pl.DataFrame): dataframe containing the columns "Dosiswert" and "DRW_aktuell"
		y_col (str): column name of the doses, e.g. "Dosiswert"
		scaled_col (str): name of column with scaled doses, e.g. "ratio_of_DRW"

	Returns:
		pl.DataFrame: dataframe with additional column <scaled_col>
	"""
	df_sc = df.with_columns((pl.col(y_col) / pl.col("DRW_aktuell")).alias(scaled_col))

	return df_sc


def _add_drw_column(DaMa: DataManager, df: pl.DataFrame) -> pl.DataFrame:
	"""Adds column to dataframe with the current DRW for each UCode.

	Args:
		DaMa (DataManager): Sqlite Database with medical ray data
		df (pl.DataFrame): dataframe (single dose values or aggregated data)

	Returns:
		pl.DataFrame: _description_
	"""

	# get all DRWs and save as dictionary
	ucode_details = DaMa.get_ucode_details(df["UCode"].unique())
	ucode_to_drw = dict(zip(ucode_details["UCode"], ucode_details["DRW_aktuell"], strict=False))

	# add as column to df
	df = df.with_columns(
		pl.col("UCode")
		.map_elements(lambda ucode: ucode_to_drw.get(ucode), return_dtype=pl.Float64)
		.alias("DRW_aktuell")
	)

	return df


def open_and_prepare_data(
	path_to_db: str, years: list[int] | None, scaled_col: str
) -> tuple[pl.DataFrame, pl.DataFrame]:
	"""Collects dose data from database, both as individual doses (Einzelwerte) and aggregated
	(only one value per ID_der_RX, year and UCode), filtered by <years>.
	The doses are scaled relative to DRW and stored as new columns in the dataframe.

	Args:
		path_to_db (str): path to database
		years (list[int] | None): years to be included in the dataframe. If None, all years are considered.
		scaled_col (str): name of column with scaled doses, e.g. "ratio_of_DRW"

	Returns:
		tuple[pl.DataFrame, pl.DataFrame]: dataframes with original and scaled doses
	"""
	# create DataManager object
	DaMa = DataManager(path_to_db)

	# retrieve aggregated doses, filter by years, add cols for UCode-scaled and DRW-scaled data
	df_agg = DaMa.get_agg_dosis_with_ucode_data()
	if years:
		df_agg = df_agg.filter(pl.col("Jahr").is_in(years))
	df_agg = _add_drw_column(DaMa, df_agg)
	df_agg = _scale_relative_to_drw(df_agg, y_col="Dosiswert", scaled_col=scaled_col)

	# retrieve individual doses, filter by years, add cols for UCode-scaled and DRW-scaled data
	df_einzel = DaMa.get_einzelwerte_with_details_and_worksheet_info()
	df_einzel = df_einzel.rename({"Untersuchungscode": "UCode"})
	if years:
		df_einzel = df_einzel.filter(pl.col("Jahr").is_in(years))
	df_einzel = _add_drw_column(DaMa, df_einzel)
	df_einzel = _scale_relative_to_drw(df_einzel, y_col="Dosiswert", scaled_col=scaled_col)
	df_einzel = df_einzel.select(
		[col for col in df_einzel.columns if col != "Gerätebezeichnung"] + ["Gerätebezeichnung"]
	)

	return df_agg, df_einzel


def run_datascience_tasks(
	base_path,
	years,
	threshold,
):
	if not base_path:
		base_path = Path(__file__).resolve().parents[3]

	DB_FILE_DIR = os.path.join(base_path, "database")
	os.makedirs(DB_FILE_DIR, exist_ok=True)

	DB_FILE_PATH_RAW = Path(os.path.join(DB_FILE_DIR, "raw_strahlenexposition.db"))

	DEST_FILE_DIR = os.path.join(base_path, "output")
	os.makedirs(DEST_FILE_DIR, exist_ok=True)

	LOG_FILE_DIR = os.path.join(base_path, "logs")
	logger_config.setup_logger(log_dir=LOG_FILE_DIR, name_prefix="datascience")
	logger_config.get_logger().info("Initialize logger for data_science task")

	OUTLIER_DIR = os.path.join(DEST_FILE_DIR, "outlier_analysis")
	os.makedirs(OUTLIER_DIR, exist_ok=True)

	CLUSTER_DIR = os.path.join(DEST_FILE_DIR, "clustering")
	os.makedirs(CLUSTER_DIR, exist_ok=True)

	if not threshold:
		threshold = 5  # default threshold for outlier detection (doses > 5x DRW are outliers)

	scaled_col = "ratio_of_DRW"
	df_agg_raw, df_einzel_raw = open_and_prepare_data(DB_FILE_PATH_RAW, years, scaled_col)

	# Outlier analysis
	years_str = f"years {'_'.join(str(x) for x in years)}" if years else "all_years"
	get_logger().info(f"\n Starting outlier analysis for {years_str}... \n")

	title = f"Histogram_of_the_median_{scaled_col}_per_Einrichtung_<br>for_{years_str}"
	plot_standardized_dosiswerte_histogram(OUTLIER_DIR, df_agg_raw, threshold, scaled_col, title)

	title = f"Histogram_of_{scaled_col}_(Einzelwerte)_<br>for_{years_str}"
	plot_standardized_dosiswerte_histogram(OUTLIER_DIR, df_einzel_raw, threshold, scaled_col, title)

	df_einzel_raw_no_outliers, df_outliers = remove_outliers(df_einzel_raw, threshold, scaled_col)
	write_outliers_into_excel_file(df_outliers, scaled_col, output_path=OUTLIER_DIR, years=years)

	# Clustering
	get_logger().info("\n Starting clustering... \n")
	cluster_by_column(
		CLUSTER_DIR,
		df_einzel_raw_no_outliers,
		scaled_col,
		cluster_col="Aerztl_Stelle",
		agg_col="UCode",
		quantity="median",
		years=years,
	)

	cluster_by_column(
		CLUSTER_DIR,
		df_einzel_raw_no_outliers,
		scaled_col,
		cluster_col="Aerztl_Stelle",
		agg_col="UCode",
		quantity="QCD",
		years=years,
	)

	cluster_by_column(
		CLUSTER_DIR,
		df_einzel_raw_no_outliers,
		scaled_col,
		cluster_col="UCode",
		agg_col="Aerztl_Stelle",
		quantity="QCD",
		years=years,
	)

	cluster_by_column(
		CLUSTER_DIR,
		df_einzel_raw_no_outliers,
		scaled_col,
		cluster_col="UCode",
		agg_col="Aerztl_Stelle",
		quantity="median",
		years=years,
	)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Outlier analysis and clustering of the data.")
	parser.add_argument(
		"--path",
		dest="base_path",
		type=str,
		help=("Set the base path where the folders 'KI-Labor_strukturiert' and 'output' are located."),
	)
	parser.add_argument(
		"--years",
		dest="years",
		nargs="+",
		type=int,
		metavar="YEAR",
		help="Filter database for a selection of years. If not provided, use all data. Example: --years 2020 2021 2022",
	)
	parser.add_argument(
		"--threshold",
		dest="threshold",
		type=int,
		help=(
			"Set threshold for identifying outliers. Number refers to multiples of the DRW, "
			"e.g. --threshold 5 identifies all values that are larger than 5*DRW as outliers"
		),
	)

	# Parse arguments
	args = parser.parse_args()

	run_datascience_tasks(
		base_path=args.base_path,
		years=args.years,
		threshold=args.threshold,
	)

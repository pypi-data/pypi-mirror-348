import argparse
import os
from pathlib import Path

import plotly.express as px
import polars as pl

from strahlenexposition_uba import logger_config
from strahlenexposition_uba.data_science import open_and_prepare_data, remove_outliers


def heatmap_n_overshoot(path: str, df: pl.DataFrame, x0_col: str, x1_col: str, title: str, ratio: bool | None):
	"""Counts the number of dose values that exceed the current DRW and draws them as a heatmap with axes x0_col and
	x1_col. If <ratio> is True, the ratio of doses > DRW is displayed, else the absolute number is displayed.

	Args:
		path (str): path to folder where heatmap will be saved
		df (pl.DataFrame): aggregated (and standardized) dataframe of dose values (1 value per ID_der_RX, year, UCode)
		x0_col (str): x0 axis of heatmap-plot, e.g. "UCode" or "Jahr"
		x1_col (str): x1 axis of heatmap-plot, e.g. "ID_der_RX" or "Aerztl_Stelle"
		title (str): Title of heatmap-plot
		ratio (bool): If true, the ratio of doses > DRW is given. If False, the absolute number is given.

	Raises:
		ValueError: Raises error if x0_col or x1_col are not in df.columns
	"""

	if x0_col not in df.columns or x1_col not in df.columns:
		raise ValueError(f"{x0_col} and/or {x1_col} not in dataframe.")

	if ratio:
		y_col = "ratio_of_doses_above_DRW"
		df_over = df.group_by([x0_col, x1_col]).agg(
			[
				pl.when(pl.col("Dosiswert") > pl.col("DRW_aktuell")).then(1).otherwise(0).sum().alias("n_overshoot"),
				pl.col("Dosiswert").count().alias("n_total"),
			]
		)
		df_over = df_over.with_columns((pl.col("n_overshoot") / pl.col("n_total")).alias(y_col))
	else:
		y_col = "n_overshoot"
		df_over = df.group_by([x0_col, x1_col]).agg(
			pl.when(pl.col("Dosiswert") > pl.col("DRW_aktuell")).then(1).otherwise(0).sum().alias(y_col)
		)
	# cast numerical values to categorial
	df_over = df_over.with_columns(pl.col([x0_col, x1_col]).cast(pl.Utf8))

	_draw_heatmap(path, df_over, x0_col, x1_col, y_col, title=title)


def heatmap_median(path: str, df: pl.DataFrame, scaled_col: str, x0_col: str, x1_col: str, title: str):
	"""Draw medians of standardized data of 'y_col' as heatmap with axes 'x0_col' and 'x1_col'.
	Data are standardized by UCode to make intercomparison between ucodes possible.

	Args:
		path (str): path to folder where heatmap will be saved
		df (pl.DataFrame): aggregated (and standardized) dataframe of dose values (1 value per ID_der_RX, year, UCode)
		scaled_col (str): name of column with scaled data for heatmap (expressed in color), e.g. "ratio_of_DRW"
		x0_col (str): x0 axis of heatmap-plot, e.g. "UCode" or "Jahr"
		x1_col (str): x1 axis of heatmap-plot, e.g. "ID_der_RX" or "Aerztl_Stelle"
		title (str): Title of heatmap-plot
	"""

	median_col = f"Median of {scaled_col}"
	# calculate median of data_col, aggregating by x0_col and x1_col
	df_agg = df.group_by([x0_col, x1_col]).agg(pl.col(scaled_col).median().alias(median_col))

	# cast numerical values to categorial
	if x0_col == "Jahr":
		df_agg = df_agg.with_columns(pl.col(x0_col).cast(pl.Int64), pl.col(x1_col).cast(pl.Utf8))
	else:
		df_agg = df_agg.with_columns(pl.col([x0_col, x1_col]).cast(pl.Utf8))

	_draw_heatmap(path, df_agg, x0_col, x1_col, median_col, title=title)


def _draw_heatmap(path: str, df: pl.DataFrame, x0_col: str, x1_col: str, y_col: str, title: str):
	"""Draw data of 'y_col' as heatmap with axes 'x0_col' and 'x1_col'.

	Args:
		df (pl.DataFrame): dataframe with columns x0_col, x1_col and y_col
		x0_col (str): x0 axis of heatmap-plot, e.g. "UCode", "Aerztl_Stelle" or "Jahr"
		x1_col (str): x1 axis of heatmap-plot, e.g. "ID_der_RX" or "Aerztl_Stelle"
		y_col (str): values of heatmap-plot, e.g. "Dosiswert_Median" or "Dosiswert_P75"
		title (str): title of the heatmap-plot
	"""

	df_pivot = df.to_pandas().pivot(index=x0_col, columns=x1_col, values=y_col)
	df_pivot = df_pivot.dropna(axis=0, how="all")  # delete empty rows
	df_pivot = df_pivot.dropna(axis=1, how="all")  # delete empty columns

	# sort x1 axis: extract IDs, sort numerically, convert to strings
	sorted_x1 = sorted(df_pivot.columns.to_list(), key=lambda x: (int(x) if str(x).isdigit() else float("inf"), str(x)))
	x1_labels = [str(x) for x in sorted_x1]

	# sort x0 axis
	sorted_x0 = sorted(df_pivot.index.tolist())
	x0_labels = [str(y) for y in sorted_x0]

	# cast rows & columns as strings and sort them
	df_pivot.index = df_pivot.index.astype(str)
	df_pivot.columns = df_pivot.columns.astype(str)
	df_pivot = df_pivot.loc[x0_labels]  # sort rows in df
	df_pivot = df_pivot[x1_labels]  # sort columns in df

	plot_title = title.replace("_", " ")
	fig = px.imshow(
		df_pivot,
		labels={"x": x1_col, "y": x0_col, "color": y_col},
		color_continuous_scale="Viridis",
		title=plot_title,
	)

	# explicitly set ticklabels for both axes
	fig.update_xaxes(
		type="category",
		categoryorder="array",
		tickvals=x1_labels,
		ticktext=x1_labels,  # for pseudonymized ÄS: [i for i, x in enumerate(sorted_x1)],
		categoryarray=x1_labels,
		showgrid=False,
	)
	fig.update_yaxes(type="category", tickmode="array", tickvals=x0_labels, ticktext=x0_labels, showgrid=False)

	n_x0 = len(df[x0_col].unique())
	n_x1 = len(df[x1_col].unique())

	# add grid lines manually as shapes
	shapes = []

	# horizontal grid lines (y)
	for y in range(n_x0 + 1):
		shapes.append(
			dict(type="line", x0=-0.5, y0=y - 0.5, x1=n_x1 - 0.5, y1=y - 0.5, line=dict(color="lightgrey", width=1))
		)

	# vertical grid lines (x)
	for x in range(n_x1 + 1):
		shapes.append(
			dict(type="line", x0=x - 0.5, y0=-0.5, x1=x - 0.5, y1=n_x0 - 0.5, line=dict(color="lightgrey", width=1))
		)
	title_font_size = 25

	fig.update_layout(
		width=max(800, n_x1 * 15),  # 15 px per column
		height=max(500, n_x0 * 25),  # 25 px per row
		margin=dict(t=100),
		coloraxis_colorbar=dict(
			orientation="v",
			title_side="right",
			len=0.8,
		),
		title=dict(
			y=0.93,
			x=0.5,
			xanchor="center",
			yanchor="top",
			font=dict(size=title_font_size),
		),
		shapes=shapes,
	)
	filename = title.replace("<br>", "")
	fig.write_image(os.path.join(path, f"{filename}.pdf"), engine="kaleido")


def heatmap_per_stelle_and_year(
	DEST_FILE_DIR: str, df: pl.DataFrame, years: list[int] | None, stellen: list[str], scaled_col: str, quantity: str
):
	"""
	Draws one heatmap per Aerztl_Stelle and year, with ID_der_RX as x axis and UCode as y axis.

	Args:
		DEST_FILE_DIR (str): path to folder where heatmaps are saved
		df (pl.DataFrame): Dataframe including the columns "ID_der_RX", "UCode" and quantity
		years (list[int]): Years to be visualized as separate heatmaps
		stellen (list[str]): Aerztliche Stellen whose data are visualized as separate heatmaps
		scaled_col (str): column name of data to be displayed, e.g. "ratio_of_DRW"
		quantity (str): column name of data to be shown as color dimension. Can be "median" or "n_overshoot".
		If it is "median", the dose values should be UCode-standardized before and stored in column "Dosiswert_Median".
		If it is "n_overshoot", the dataframe should include the current DRW in column "DRW_aktuell"
	"""

	# if no years were selected: retrieve all years in dataframe
	if not years:
		years = list(df.get_column("Jahr").unique())

	for year in years:
		for stelle in stellen:
			df_ij = df.filter((pl.col("Jahr") == year) & (pl.col("Aerztl_Stelle") == stelle))
			if not df_ij.is_empty():
				n_ucodes = len(df_ij.select("UCode").unique())
				n_IDs = len(df_ij.select("ID_der_RX").unique())
				logger_config.get_logger().info(
					f"{year}, {stelle}: {n_ucodes} UCodes, {n_IDs} IDs, {df_ij.shape[0]} datapoints"
				)

				# create folder for stelle if it doesn't exist yet
				path_stelle = os.path.join(DEST_FILE_DIR, stelle)
				if not os.path.exists(path_stelle):
					os.mkdir(path_stelle)

				if quantity == "median":
					title_ij = f"Heatmap_of_{scaled_col}_for_{year}_ÄS={stelle}"
					heatmap_median(path_stelle, df_ij, scaled_col, x0_col="UCode", x1_col="ID_der_RX", title=title_ij)
				elif quantity == "n_overshoot":
					title_ij = f"Heatmap_number_of_Dosiswerte_above_DRW_({year}_ÄS={stelle})"
					heatmap_n_overshoot(
						path_stelle, df_ij, x0_col="UCode", x1_col="ID_der_RX", title=title_ij, ratio=False
					)


def run_heatmap_pipeline(
	base_path,
	years,
	threshold,
):
	if not base_path:
		base_path = Path(__file__).resolve().parents[3]

	DB_FILE_DIR = os.path.join(base_path, "database")  # path to database
	os.makedirs(DB_FILE_DIR, exist_ok=True)

	DEST_FILE_DIR = os.path.join(base_path, "output", "heatmaps")
	os.makedirs(DEST_FILE_DIR, exist_ok=True)

	LOG_FILE_DIR = os.path.join(base_path, "logs")
	logger_config.setup_logger(log_dir=LOG_FILE_DIR, name_prefix="heatmaps")
	logger_config.get_logger().info("Initialize logger")

	if not threshold:
		threshold = 5

	DB_FILE_PATH_RAW = Path(os.path.join(DB_FILE_DIR, "raw_strahlenexposition.db"))

	scaled_col = "ratio_of_DRW"

	df_agg_raw, df_einzel_raw = open_and_prepare_data(DB_FILE_PATH_RAW, years, scaled_col)
	df_agg_raw_no_outliers, _ = remove_outliers(df_agg_raw, threshold, scaled_col)
	df_einzel_raw_no_outliers, _ = remove_outliers(df_einzel_raw, threshold, scaled_col)
	# TODO Entscheidung: Heatmaps pro ÄS und Jahr mit oder ohne Outlier? (Hugo fragen)

	# Heatmaps of all data
	years_str = f"years {'_'.join(str(x) for x in years)}" if years else "all years"
	logger_config.get_logger().info(f"\n Starting to create heatmaps for {years_str}... \n")

	title0 = f"Heatmap_of_the_median_{scaled_col}_(all data)_<br>Aerztl_Stelle_vs_Jahr_for_{years_str}"
	heatmap_median(DEST_FILE_DIR, df_agg_raw, scaled_col, x0_col="Jahr", x1_col="Aerztl_Stelle", title=title0)

	title1 = f"Heatmap_absolute_number_of_doses_above_DRW_<br>_Aerztl_Stelle_vs_Jahr_for_{years_str}"
	heatmap_n_overshoot(DEST_FILE_DIR, df_agg_raw, x0_col="Jahr", x1_col="Aerztl_Stelle", title=title1, ratio=False)

	title2 = f"Heatmap_ratio_of_doses_above_DRW_(all data)_<br>Aerztl_Stelle_vs_Jahr_for_{years_str}"
	heatmap_n_overshoot(DEST_FILE_DIR, df_agg_raw, x0_col="Jahr", x1_col="Aerztl_Stelle", title=title2, ratio=True)

	title3 = f"Heatmap_of_the_median_{scaled_col}_(all data)_<br>Aerztl_Stelle_vs_UCode_for_{years_str}"
	heatmap_median(DEST_FILE_DIR, df_agg_raw, scaled_col, x0_col="Aerztl_Stelle", x1_col="UCode", title=title3)

	title4 = f"Heatmap_of_the_median_{scaled_col}_(outliers_removed)_<br>Aerztl_Stelle_vs_UCode_for_{years_str}"
	heatmap_median(
		DEST_FILE_DIR, df_agg_raw_no_outliers, scaled_col, x0_col="Aerztl_Stelle", x1_col="UCode", title=title4
	)

	# Individual heatmaps for each ÄS and year
	aerztl_stellen = sorted(list(df_agg_raw.select("Aerztl_Stelle").unique().to_series()))
	heatmap_per_stelle_and_year(DEST_FILE_DIR, df_einzel_raw, years, aerztl_stellen, scaled_col, quantity="median")
	heatmap_per_stelle_and_year(DEST_FILE_DIR, df_einzel_raw, years, aerztl_stellen, scaled_col, quantity="n_overshoot")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Visualize data as heatmaps given the basepath to the repository.")
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
		help="Filter database for a selection of years. If not provided, all data are used. Example: --years 2020 2021",
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

	run_heatmap_pipeline(
		base_path=args.base_path,
		years=args.years,
		threshold=args.threshold,
	)

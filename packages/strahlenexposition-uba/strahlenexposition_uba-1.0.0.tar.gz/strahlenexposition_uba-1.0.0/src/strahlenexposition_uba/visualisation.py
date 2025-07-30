import numpy as np
import plotly.graph_objects as go
import polars as pl


### --------------------------- Plot Functions --------------------------- ###
def plot_violin(agg_data: pl.DataFrame, group_by: str, y_col: str, legend=False) -> go.Figure:
	"""Creates a violin plot to show dose distribution by group for one UCode, with reference lines and annotations.
		This function is used in the reports to plot distribution of "Dosiswert" across a grouping column
		(e.g., "Aerztl_Stelle"). Reference lines are added for:

			- Aktueller DRW (current diagnostic reference value)
			- Neuer DRW (proposed reference value, if existing)
			- Q3 (75th percentile)

		Reference values are taken from the first row of `agg_data`.

	Args:
		agg_data (pl.DataFrame): Filtered dataset containing data for plot. Must include columns group_by, y_col,
			'DRW_aktuell', 'DRW_Vorschlag', 'UCode', 'Unit_Dosiswert'
		group_by (str): Column Name (eg Aerztl_Stelle). Plots will contain one violin for each unique value of group_by.
		y_col (str): Column containing y value (e.g. Dosiswert)
		legend (bool): Whether to display legend for reference lines, defaults to False.

	Returns:
		go.Figure: A Plotly violin plot containing one violin per unique group_by value.
	"""
	ucode_meta = agg_data.row(0, named=True)
	dosiswert_typ = _get_dosiswert_type(ucode_meta, value_text=y_col)
	x_unique = sorted(agg_data[group_by].unique().to_list())
	value_counts_df = agg_data[group_by].value_counts().sort(group_by)
	drw_aktuell = ucode_meta["DRW_aktuell"]
	# Calculate y-axis limit
	ymax = 2 * max(agg_data[y_col].quantile(0.9) or 0, drw_aktuell or 0)
	q3 = agg_data[y_col].quantile(0.75, interpolation="linear")

	fig = go.Figure()

	# Add violin plot, reference lines and annotations
	_add_violin_plot(fig, agg_data, group_by, y_col)
	_add_reference_line(fig, y=drw_aktuell, label="Aktueller DRW", color="#c84644", legend=legend)
	_add_reference_line(fig, y=ucode_meta["DRW_Vorschlag"], label="Neuer DRW", color="#95ba83", legend=legend)
	_add_reference_line(fig, y=q3, label="Q3 (75th Percentile)", color="#284d71", legend=legend)
	_add_text_annotations(fig, value_counts_df, group_by)

	_configure_violin_layout(fig, group_by, dosiswert_typ, x_unique, ymax)

	return fig


def empty_figure_with_text() -> go.Figure:
	# For dash only: Returns an empty figure with a text annotation indicating that a year selection is required.
	fig = go.Figure()
	fig.add_annotation(
		text="Wähle mindestens ein Jahr aus.",
		x=0.5,
		y=0.5,
		xref="paper",  # position relative to the entire figure
		yref="paper",
		showarrow=False,
		font=dict(size=20),
	)
	fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False))
	return fig


def _add_reference_line(fig: go.Figure, y: float, label: str, color: str, legend: bool):
	"""Adds a single horizontal reference line to the given figure.

	Args:
		fig (go.Figure): The figure to modify.
		x_vals (list[any]): The x-axis values for the reference line.
		y (float): The y-coordinate of the reference line.
		label (str): Label for the reference line. (used if legend = True)
		color (str): Line color.
		legend (bool): Whether to show legend.
	"""
	if not y:
		return
	label = f"{label}: {y:.2f}"
	fig.add_shape(
		type="line",
		xref="paper",
		yref="y",
		x0=0,
		x1=1,
		y0=y,
		y1=y,
		line=dict(color=color, dash="dot"),
	)

	if legend:
		# Workaround: Add an invisible Scatter to show legend label
		fig.add_trace(
			go.Scatter(
				x=[None],
				y=[None],
				mode="lines",
				line=dict(color=color, dash="dot"),
				name=label,
				showlegend=True,
			)
		)


def _add_violin_plot(fig, agg_data: pl.DataFrame, group_by: str, y_col: str):
	# Adds a violin plot (with multiple violins) to provided figure. see plot_violin doc for parameter details

	# create one row per group with y_vals list as column to avoid creation of multiple data frames
	grouped = agg_data.group_by(group_by, maintain_order=True).agg(pl.col(y_col).alias("y_vals"))

	# add violin and boxplot separately for each group to have full control of layout
	for row in grouped.iter_rows(named=True):
		group = row[group_by]
		y_vals = row["y_vals"]

		fig.add_trace(
			go.Violin(
				x=[group] * len(y_vals),
				y=y_vals,
				showlegend=False,
				side="positive",
				fillcolor="rgba(0,0,0,0)",
				spanmode="hard",
				line_color="#284d71",
				line_width=2,
				marker_size=3,
				points="outliers",
				jitter=0.2,
			)
		)

		fig.add_trace(
			go.Box(
				x=[group] * len(y_vals),
				y=y_vals,
				name=str(group),
				marker_color="#284d71",
				line_width=2,
				width=0.2,
				fillcolor="#d1d2dc",
				line_color="#284d71",
				boxpoints=False,
				showlegend=False,
			)
		)


def _add_text_annotations(fig, value_counts_df, group_by):
	# Adds text annotations to figure to display the number of data points.
	hover_texts = value_counts_df.with_columns(
		pl.concat_str([pl.lit("Anzahl Datenpunkte: "), pl.col("count").cast(pl.Utf8)]).alias("hover_text")
	)["hover_text"].to_list()
	fig.add_trace(
		go.Scatter(
			x=value_counts_df[group_by],
			y=[0] * len(value_counts_df),
			text=value_counts_df["count"].cast(pl.Utf8),
			mode="text",
			textposition="bottom center",
			showlegend=False,
			hovertext=hover_texts,
			hoverinfo="text",
		)
	)


def _configure_violin_layout(fig: go.Figure, group_by: str, dosiswert_typ: str, x_unique: list, ymax: float) -> None:
	# Configures layout of violin plot (containing all elements as reference lines, annotations, violins)
	num_violins = len(x_unique)
	base_width = 200  # Minimum base width
	width_per_violin = 200  # Width increase per violin
	fig_height = 800

	# Compute dynamic figure dimensions
	fig_width = min(max(base_width + num_violins * width_per_violin, 600), 2500)  # Constrain within min/max

	fig.update_layout(
		font=dict(size=20),
		xaxis_title=group_by,
		yaxis_title=dosiswert_typ,
		yaxis=dict(range=[-ymax / 16, ymax]),
		xaxis=dict(
			tickmode="array",
			categoryorder="array",
			categoryarray=x_unique,
			tickvals=list(range(len(x_unique))),
			ticktext=x_unique,
			type="category",
			range=[-0.5, len(x_unique) - 0.5],
		),
		xaxis_tickangle=-60,
		legend=dict(title="", x=0.0, y=-0.4, font=dict(size=24)),
		template="plotly_white",
		width=fig_width,
		height=fig_height,
	)


### --------------------------- Table Functions --------------------------- ###
def create_descr_statistics(agg_data: pl.DataFrame, value_column: str) -> pl.DataFrame:
	"""Create a descriptive statistics table grouped by year.
		Calculates:
			- # Einzelwerte (sum of 'Anzahl_Werte')
			- # Mediane (number of median values)
			- Min, Max, Mean (MW), Median
			- Percentiles (P25, P75, P90)
			- Quartile Coefficient of Dispersion (QCD)

		The function computes statistics for each year and a total "Gesamt" row,
		then reshapes the result into a pivoted table with statistics as rows and years as columns.

	Args:
			agg_data (pl.DataFrame): Input DataFrame with at least the columns "Jahr", "Anzahl_Werte", and the given
				`value_column`.
			value_column (str): Column name in `agg_data` containing the values for which statistics will be calculated
				(e.g., "Dosiswert").

	Returns:
			pl.DataFrame: Pivoted DataFrame containing descriptive statistics per year and for total.
	"""

	agg_operations = [
		pl.col("Anzahl_Werte").sum().cast(str).alias("# Einzelwerte"),
		pl.len().cast(str).alias("# Mediane"),
		pl.col(value_column).min().map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32).alias("Min"),
		pl.col(value_column).mean().map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32).alias("MW"),
		pl.col(value_column).median().map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32).alias("Median"),
		pl.col(value_column)
		.quantile(0.25, interpolation="linear")
		.map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32)
		.alias("P25"),
		pl.col(value_column)
		.quantile(0.75, interpolation="linear")
		.map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32)
		.alias("P75"),
		pl.col(value_column)
		.quantile(0.90, interpolation="linear")
		.map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32)
		.alias("P90"),
		pl.col(value_column).max().map_elements(lambda x: np.round(x, 2), return_dtype=pl.Float32).alias("Max"),
		(
			(pl.col(value_column).quantile(0.75) - pl.col(value_column).quantile(0.25))
			/ (pl.col(value_column).quantile(0.75) + pl.col(value_column).quantile(0.25))
		)
		.round(2)
		.alias("QCD"),
	]
	grouped_stats = (
		agg_data.group_by("Jahr")
		.agg(agg_operations)
		.with_columns(pl.col("Jahr").cast(pl.Int32))
		.sort("Jahr")
		.with_columns(pl.col("Jahr").cast(pl.Utf8))
	)
	gesamt_stats = agg_data.select(agg_operations).with_columns(pl.lit("Gesamt").alias("Jahr"))
	gesamt_stats = gesamt_stats.select(grouped_stats.columns)  # ensure column order
	summary_df = pl.concat([grouped_stats, gesamt_stats], how="vertical")

	summary_df = summary_df.melt(id_vars=["Jahr"], variable_name="Statistik", value_name="Wert")
	summary_df = summary_df.pivot(values="Wert", index="Statistik", on="Jahr")

	return summary_df


def create_country_table(ucode_dict: dict, value_text: str = "Dosiswert") -> pl.DataFrame:
	"""Create a country comparison table from a dictionary of dose reference values.
		Depending on whether the `value_text` relates to DLP or DRW, selects appropriate keys
		from the input dictionary and reshapes the data into a long-format table.

	Args:
			ucode_dict (dict): Dictionary containing country-specific dose reference values.
				Expected to include either DRW keys:
				'EUCLID_DRW', 'EU_DRW', 'US_DRW', 'Schweiz_DRW', 'Österreich_DRW' or DLP keys:
				'EUCLID_DRW_DLP', 'EU_DRW_DLP', 'US_DRW_DLP', 'Schweiz_DLP', 'Österreich_DLP'.
			value_text (str, optional): Value/Column name of relevant data. Defaults to "Dosiswert".

	Returns:
			pl.DataFrame: A Polars DataFrame with two columns:
				- "Land/Gruppe": Country or region label
				- type_unit_label: The selected dose value with unit
	"""
	type_unit_label = _get_dosiswert_type(ucode_dict, value_text=value_text)
	ucode_data = pl.DataFrame(data=ucode_dict)
	country_cols = (
		["EUCLID_DRW_DLP", "EU_DRW_DLP", "US_DRW_DLP", "Schweiz_DLP", "Österreich_DLP"]
		if "DLP" in value_text.upper()
		else ["EUCLID_DRW", "EU_DRW", "US_DRW", "Schweiz_DRW", "Österreich_DRW"]
	)
	ucode_countries = ucode_data[country_cols]
	country_overview = (
		ucode_countries.unpivot()
		.rename({"variable": "Land/Gruppe", "value": type_unit_label})
		.with_columns(pl.col(type_unit_label).cast(str).fill_null("NA"))
	)
	return country_overview


### --------------------------- Helper Functions --------------------------- ###
# TODO move somewhere else, use existing mapping from other branch?
def _get_dosiswert_type(ucode: dict, value_text: str = "") -> str:
	"""Maps the dose value type based on UCode metadata.

	Args:
		ucode (dict): Must contain keys 'UCode' and 'Unit_Dosiswert'/'Unit_DLP'
		value_text (str, optional): Only relevant if it is DLP. Defaults to "".

	Returns:
		str: value type combined with respective unit, e.g. 'DFP [cGy cm2]'
	"""

	value_text_upper = value_text.upper()
	code = str(ucode["UCode"])

	if "DLP" in value_text_upper:
		unit_ref_value = ucode["Unit_DLP"]
		return f"DLP [{unit_ref_value}]"
	else:
		unit_ref_value = ucode["Unit_Dosiswert"]

	# Determine value type label based on the first character of ucode
	type_mapping = {
		"1": "CTDIvol",
		"7": "CTDIvol",
		"3": "AGD",
	}

	return f"{type_mapping.get(code[0], 'DFP')} [{unit_ref_value}]"

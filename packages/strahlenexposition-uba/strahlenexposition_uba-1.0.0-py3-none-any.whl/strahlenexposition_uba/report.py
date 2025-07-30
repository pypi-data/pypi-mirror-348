import base64
import importlib.resources
import os

import jinja2
import plotly
import plotly.graph_objects
import plotly.graph_objects as go
import polars as pl
from weasyprint import HTML

from strahlenexposition_uba import assets, templates
from strahlenexposition_uba.database import DataManager
from strahlenexposition_uba.logger_config import get_logger
from strahlenexposition_uba.visualisation import (
	create_country_table,
	create_descr_statistics,
	empty_figure_with_text,
	plot_violin,
)


class BaseReportGenerator:
	"""Abstract base class for generating reports (interactive dash or pdf) from dose value data."""

	def __init__(self, data: pl.DataFrame):
		"""Initializes ReportGenerator by setting unique ucodes/years and computing labels.

		Args:
			data (pl.DataFrame): Must contain column "UCode", "Jahr", "Dosiswert","Anzahl_Werte" and group column.
		"""
		self.data = data
		self.available_ucodes = self.data["UCode"].unique().to_list()
		self.available_ucode_labels = self._create_ucode_labels()  # dict contains code, label pairs
		self.value_column = "Dosiswert"  # TODO: Handle DLP?

	def _create_ucode_labels(self) -> dict[int, str]:
		# Create labels as dict in format {<ucode>:"<ucode>) - <Bezeichnung>", ..}
		ucode_details = self.data.unique(subset=["UCode"], keep="any")
		return dict(
			zip(
				ucode_details["UCode"].to_list(),  # Extract UCode as keys
				(ucode_details["UCode"].cast(str) + " - " + ucode_details["Bezeichnung"]).to_list(),  # Labels as values
				strict=True,
			)
		)


class PdfReportGenerator(BaseReportGenerator):
	def generate_report(self, years: list[int], dest_path: str, pseudonyms: dict = None):
		"""
		Generates a multi-page PDF report for all UCodes in the specified years.
			Generates report using WeasyPrint and jinja2. Writes PDF file to file path.

			Note: Rendering from HTML/CSS to PDF may take up to 3 minutes for larger datasets (e.g., if six years of
			data are selected).

		Args:
			years (list[int]): List of years to filter data by (e.g., [2022, 2023]).
			dest_path (str): Destination folder where the PDF will be saved.
			pseudonyms (dict[str, str], optional): Mapping of `Aerztl_Stelle` to pseudonyms. If None, no
				pseudonymization is applied.

		Returns:
			None

		Raises:
			ValueError: If the filtered data is empty after applying year filter.
			FileNotFoundError: If logo or template resources are missing.

		Example:
			>>> reportGenerator = PdfReportGenerator(data=my_data)
			>>> reportGenerator.generate_report(years=[2022, 2023], dest_path="dest_path/reports/")
		"""
		data_years = self.data.filter(pl.col("Jahr").is_in(years))
		if data_years.is_empty():
			get_logger().warning("No data available for the selected years.")
			return
		data_years = data_years.sort("UCode")  # to order pages in report dependent on ucode
		if pseudonyms:
			data_years = self._pseudonymize_aerztl_stelle(df=data_years, pseudonyms=pseudonyms)

		# create report page data per ucode
		report_data_df = data_years.group_by("UCode", maintain_order=True).map_groups(self._process_ucode)
		report_data_list = report_data_df.to_dicts()

		# load logos as base64
		logo_bfs = self._load_logo_base64("Logo_BfS_DE.png")
		logo_ki_lab = self._load_logo_base64("ki-lab-logo.png")

		# Render HTML for all ucodes with Jinja2
		jinja_template = self._load_jinja2_template()
		rendered_html = jinja_template.render(ucode_list=report_data_list, logo_bfs=logo_bfs, logo_ki_lab=logo_ki_lab)

		# Convert HTML to Multi-Page PDF using WeasyPrint
		suffix = "_pseudonyms" if pseudonyms else ""
		pdf_title = f"report_{'-'.join(map(str, years))}{suffix}.pdf"
		output_pdf = os.path.join(dest_path, pdf_title)
		HTML(string=rendered_html).write_pdf(output_pdf)

		get_logger().info(f" Multi-page weasyprint/jinja2 PDF successfully created: {output_pdf}")

	def _process_ucode(self, ucode_data: pl.DataFrame) -> pl.DataFrame:
		# Creates input data for report page template for one ucode.

		violin1 = plot_violin(ucode_data, "Aerztl_Stelle", self.value_column, legend=True)
		violin2 = plot_violin(ucode_data, "Jahr", self.value_column)
		df_descr = create_descr_statistics(ucode_data, value_column=self.value_column)
		df_country = create_country_table(ucode_data.row(0, named=True), value_text=self.value_column)

		return pl.DataFrame(
			{
				"label": [self.available_ucode_labels.get(ucode_data["UCode"].item(0))],
				"img_base64": [self._plotly_to_base64(violin1)],
				"img_base64_2": [self._plotly_to_base64(violin2)],
				"table_descr_html": [self._pl_dataframe_to_html(df_descr)],
				"table_country_html": [self._pl_dataframe_to_html(df_country)],
			}
		)

	@staticmethod
	def _load_jinja2_template(template_name: str = "report_template.html") -> jinja2.environment.Template:
		with importlib.resources.files(templates).joinpath(template_name).open("r") as f:
			source = f.read()
		template_env = jinja2.Environment(loader=jinja2.BaseLoader())
		return template_env.from_string(source)

	@staticmethod
	def _plotly_to_base64(fig: plotly.graph_objects.Figure) -> str:
		fig.update_traces(hoverinfo="skip")  # reduce size
		return base64.b64encode(fig.to_image(format="svg")).decode("utf-8")

	@staticmethod
	def _pl_dataframe_to_html(df: pl.DataFrame) -> str:
		return df.to_pandas().to_html(index=False)

	@staticmethod
	def _load_logo_base64(filename: str):
		# Logos are stored in assets folder
		with importlib.resources.files(assets).joinpath(filename).open("rb") as f:
			return base64.b64encode(f.read()).decode("utf-8")

	@staticmethod
	def _pseudonymize_aerztl_stelle(df: pl.DataFrame, pseudonyms: dict) -> pl.DataFrame:
		# Replaces unique group_by values with as_01, as_02, ..., in random order.
		# One aerztl_stelle has same pseudonym for each ucode.
		pseudonym_col = "Aerztl_Stelle"
		return df.with_columns(pl.col(pseudonym_col).replace_strict(pseudonyms))


class DashReportGenerator(BaseReportGenerator):
	def __init__(self, db_manager: DataManager):
		super().__init__(db_manager)
		self.available_years = self.data["Jahr"].unique().to_list()

	def generate_report(
		self, ucode: int, selected_years: list[int]
	) -> tuple[go.Figure, go.Figure, list[dict], list[dict], list[dict], list[dict]]:
		"""Filters required ucode data and generates visualization and tables (with column description)
		for a given UCode and selected years. Use this only for plotly dash content.

		Args:
			ucode (int): Untersuchungscode to create the report/filter the data
			selected_years (list[int]): List of years to filter the dataset.

		Returns:
			tuple: Two Violin plots (grouped by aerztliche_stelle and years), descriptive statistics table,
			country comparison table and table column definitions required by plotly dash app. Returns empty Figure
			with text hint and empty lists if selected_years is empty.
		"""
		if not selected_years:
			return (empty_figure_with_text(), go.Figure(), [], [], [], [])

		# filter data
		filtered_data = self.data.filter(pl.col("UCode") == ucode, pl.col("Jahr").is_in(selected_years))

		# Generate plots
		fig_violin1 = plot_violin(filtered_data, "Aerztl_Stelle", self.value_column, True)
		fig_violin2 = plot_violin(filtered_data, "Jahr", self.value_column)

		fig_violin1.update_layout(height=800, width=filtered_data["Aerztl_Stelle"].n_unique() * 150 or 1000)
		fig_violin2.update_layout(height=800, width=len(selected_years) * 250)

		# Generate tables
		df_descr = create_descr_statistics(filtered_data, value_column=self.value_column)
		df_country = create_country_table(filtered_data.row(0, named=True), value_text=self.value_column)

		# Create header information for plotly dash
		descr_columns = self._create_dash_table_header(df_descr)
		country_columns = self._create_dash_table_header(df_country)

		return fig_violin1, fig_violin2, df_descr.to_dicts(), df_country.to_dicts(), descr_columns, country_columns

	@staticmethod
	def _create_dash_table_header(df: pl.DataFrame) -> list[dict]:
		"""Generates column definitions for Dash AgGrid from a Polars DataFrame containing the table data."""
		return [{"headerName": col, "field": col} for col in df.columns] if not df.is_empty() else []

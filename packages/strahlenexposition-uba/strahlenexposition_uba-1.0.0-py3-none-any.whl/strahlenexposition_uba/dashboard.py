import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import strahlenexposition_uba.database as db
from strahlenexposition_uba.report import DashReportGenerator


class DashboardApp:
	"""Simple Dash web application for visualizing radiation exposure reports interactively."""

	def __init__(self, db_manager: db.DataManager):
		"""Initializes the DashboardApp with a database manager.
		Uses ReportGenerator to obtain data from database, and create data components shown in Dashboard
		(plotly Figure, data tables as list/column descriptions).
		Style details are defined in style.css

		Args:
			db_manager (db.DataManager): The database manager instance with connection to sqlite database.
		"""
		self.db_manager = db_manager
		agg_data = self.db_manager.get_agg_dosis_with_ucode_data()
		self.report_generator = DashReportGenerator(agg_data)
		self.app = dash.Dash(
			__name__,
			external_stylesheets=[
				dbc.themes.FLATLY,
				"https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-grid.css",
				"https://cdn.jsdelivr.net/npm/ag-grid-community/styles/ag-theme-alpine.css",
			],
		)
		self._setup_layout()
		self._setup_callbacks()

	def _setup_layout(self):
		"""Define the app layout."""
		self.app.layout = html.Div(
			[
				html.H1("Strahlenexposition Report Dashboard"),
				html.Div(
					[
						html.Label("Auswahl Untersuchungscode:"),
						dcc.Dropdown(
							id="ucode-dropdown",
							options=[
								{"label": ucode_label, "value": ucode}
								for ucode, ucode_label in self.report_generator.available_ucode_labels.items()
							],
							value=self.report_generator.available_ucodes[0],
							clearable=False,
						),
					],
					className="dropdown-container",
				),
				html.Div(
					[
						html.Label("Auswahl Jahr(e):"),
						dcc.Checklist(
							id="year-checklist",
							options=[
								{"label": str(year), "value": year} for year in self.report_generator.available_years
							],
							value=[],
							inline=True,
							className="dash-checklist",
						),
					],
					className="checklist-container",
				),
				html.Div(
					[
						html.Div(dcc.Graph(id="violin-plot1"), className="graph-container"),
					],
					className="scrollable-graph-container",
				),
				html.Div(
					[
						html.Div(dcc.Graph(id="violin-plot2"), className="graph-container"),
					],
					className="scrollable-graph-container",
				),
				html.Div(
					[
						dag.AgGrid(
							id="table-descr",
							columnDefs=[],
							rowData=[],
							defaultColDef={
								"sortable": True,
								"filter": True,
								"resizable": True,
								"cellStyle": {"textAlign": "center"},
								"flex": 1,
							},
							columnSize="sizeToFit",
							dashGridOptions={"domLayout": "autoHeight"},
							style={"maxHeight": 500, "overflow": "auto"},
							className="ag-theme-alpine grid-container",
						),
						dag.AgGrid(
							id="table-country",
							columnDefs=[],
							rowData=[],
							defaultColDef={
								"sortable": True,
								"filter": True,
								"resizable": True,
								"cellStyle": {"textAlign": "center"},
								"flex": 1,
							},
							columnSize="sizeToFit",
							dashGridOptions={"domLayout": "autoHeight"},
							style={"maxHeight": 420, "overflow": "auto"},
							className="ag-theme-alpine grid-container",
						),
					],
					className="table-container",
				),
			],
			className="main-container",
		)

	def _setup_callbacks(self):
		"""Define Dash callback triggered by change of Untersuchungscode dropdown or year checklist.
		Can be extended by further callbacks."""

		@self.app.callback(
			[
				Output("violin-plot1", "figure"),
				Output("violin-plot2", "figure"),
				Output("table-descr", "rowData"),
				Output("table-country", "rowData"),
				Output("table-descr", "columnDefs"),
				Output("table-country", "columnDefs"),
			],
			[Input("ucode-dropdown", "value"), Input("year-checklist", "value")],
		)
		def update_output(ucode, selected_years):
			return self.report_generator.generate_report(ucode=ucode, selected_years=selected_years)

	def run(self, debug: bool = True):
		"""Start the Dash app."""
		self.app.run_server(debug=debug)

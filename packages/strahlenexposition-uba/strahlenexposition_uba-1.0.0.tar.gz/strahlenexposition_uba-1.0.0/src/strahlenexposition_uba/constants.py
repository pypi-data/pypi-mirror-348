"""Global constants used across the package."""

import polars as pl

FILE_ENDINGS = (".xls", ".xlsx", ".XLSX", ".XLS")
"""tuple[str]: Tuple of all valid excel file endings."""

BAYERN_PATTERN = r"(?:Bayern|BY).*[\\/]"
"""str: Regex of the pattern which corresponds to files in the old Bayern format"""

COLUMNS_UCODES = [
	"Ucode",
	"Bezeichnung",
	"Unit_Dosiswert",
	"Unit_DLP",
	"DRW_aktuell",
	"DRW_Vorschlag",
	"DRW_DLP_aktuell",
	"EUCLID_DRW",
	"EU_DRW",
	"US_DRW",
	"Schweiz_DRW",
	"Österreich_DRW",
	"EUCLID_DRW_DLP",
	"EU_DRW_DLP",
	"US_DRW_DLP",
	"Schweiz_DLP",
	"Österreich_DLP",
	"Deff",
]
"""list[str]: List of columns in the DRW master excel"""

COLUMNS_EINZELWERTE = [
	"ID_der_RX",
	"UCode_id",
	"Arbeitsblatt_id",
	"DFP",
	"AGD",
	"CTDI",
	"Dosiswert",
]

COLUMNS_DOSISWERTE_AGG = ["ID_der_RX", "UCode_id", "Aerztl_Stelle", "Dosiswert", "Anzahl_Werte", "Jahr"]

COLUMNS_OPTIONALWERTE = ["Einzelwert_id", "Spaltenname", "Wert"]

COLUMNS_BLACKLIST = [r"alter\s*(\n)?monat", r"altersklass"]
"""list[str]: Regex of columns to exclude in order to maintain uniqueness of columns"""

UCODE_TO_DOSISWERT_MAPPING = {r"^(1|7)": "CTDI", r"^3": "AGD"}
"""dict: Maps UCode beginnings to type of measurement, e.g. `1*** -> CTDI` """

COLUMN_METADATA = {
	r"id": {"standard_name": "ID_der_RX", "dtype": pl.String, "category": "id"},
	r"code": {"standard_name": "Untersuchungscode", "dtype": pl.String, "category": "id"},
	r"dfp": {"standard_name": "DFP", "dtype": pl.Float64, "category": "mandatory"},
	r"agd": {"standard_name": "AGD", "dtype": pl.Float64, "category": "mandatory"},
	r"ctdi[\-_\s\n]?($|vol|\(mgy\)|1)": {
		"standard_name": "CTDI",
		"dtype": pl.Float64,
		"category": "mandatory",
	},
	# Optional columns
	r"dlp": {"standard_name": "DLP", "dtype": pl.Float64, "category": "optional"},
	r"(?:phantom|prüfkörper)": {"standard_name": "CTDI-Phantom", "dtype": pl.String, "category": "optional"},
	r"gewicht": {"standard_name": "Gewicht", "dtype": pl.Float64, "category": "optional"},
	r"alter": {"standard_name": "Alter", "dtype": pl.Float64, "category": "optional"},
	r"(?:meldungsart|mw oder ew)": {"standard_name": "Meldungsart", "dtype": pl.String, "category": "optional"},
	r"(an)?zahl": {"standard_name": "Anzahl", "dtype": pl.Float64, "category": "optional"},
	r"studien(-)?beschreibung": {"standard_name": "Studienbeschreibung", "dtype": pl.String, "category": "optional"},
	r"serien(-)?beschreibung": {"standard_name": "Serienbeschreibung", "dtype": pl.String, "category": "optional"},
	r"protokollname": {"standard_name": "Protokollname", "dtype": pl.String, "category": "optional"},
	r"gerätebezeichnung": {"standard_name": "Gerätebezeichnung", "dtype": pl.String, "category": "optional"},
	r"betreiber": {"standard_name": "Betreiber", "dtype": pl.String, "category": "optional"},
}
"""dict: Nested dictionary. Maps a regex which identifies a column in the excel file to a dictionary with keys 
`standard_name`, `dtype` and `category`"""

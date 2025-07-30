CREATE TABLE IF NOT EXISTS 'Untersuchungscodes' (
    -- generiert
    'id'              INTEGER PRIMARY KEY AUTOINCREMENT,
    'UCode'           INTEGER NOT NULL UNIQUE,
    'Bezeichnung'     TEXT    NOT NULL,
    'Unit_Dosiswert'  TEXT    NULL,
    'Unit_DLP'        TEXT    NULL    ,
    'DRW_aktuell'     REAL    NULL     DEFAULT NULL,
    'DRW_Vorschlag'   REAL    NULL     DEFAULT NULL,
    'DRW_DLP_aktuell' REAL    NULL     DEFAULT NULL,
    'EUCLID_DRW'      REAL    NULL     DEFAULT NULL,
    'EU_DRW'          REAL    NULL     DEFAULT NULL,
    'US_DRW'          REAL    NULL     DEFAULT NULL,
    'Schweiz_DRW'     REAL    NULL     DEFAULT NULL,
    'Österreich_DRW'  REAL    NULL     DEFAULT NULL,
    'EUCLID_DRW_DLP'  REAL    NULL     DEFAULT NULL,
    'EU_DRW_DLP'      REAL    NULL     DEFAULT NULL,
    'US_DRW_DLP'      REAL    NULL     DEFAULT NULL,
    'Schweiz_DLP'     REAL    NULL     DEFAULT NULL,
    'Österreich_DLP'  REAL    NULL     DEFAULT NULL,
    'Deff'            REAL    NULL     DEFAULT Null,
    -- generated, YYYY-MM-DD HH:MM:SS
    'Erstellungsdatum' TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- aggregiert
CREATE TABLE IF NOT EXISTS 'Dosiswerte_AGG' (
    -- generiert
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Einrichtung oder Geraetetyp
    'ID_der_RX' TEXT NOT NULL,
    'UCode_id' INTEGER NOT NULL,
    'Aerztl_Stelle' TEXT NOT NULL,
    -- aggregiert
    'Dosiswert' REAL NOT NULL,
    'Anzahl_Werte' INTEGER NOT NULL,
    -- Erhebungsjahr
    'Jahr' INTEGER NOT NULL,
    -- generated, YYYY-MM-DD HH:MM:SS
    'Erstellungsdatum' TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (
        'ID_der_RX',
        'UCode_id',
        'Aerztl_Stelle',
        'Jahr'
    ),
    FOREIGN KEY ('UCode_id') REFERENCES 'Untersuchungscodes' ('id')
);

-- UNIQUE(Dateiname, Arbeitsblatt)
CREATE TABLE IF NOT EXISTS 'eingelesene_dateien'
(
  -- generiert
  'id'               INTEGER PRIMARY KEY AUTOINCREMENT,
  'Dateiname'        TEXT    NOT NULL,
  -- excel sheet
  'Arbeitsblatt'     TEXT    NOT NULL,
  -- Erhebungsjahr
  'Jahr'             INTEGER NOT NULL,
  'Aerztl_Stelle'    TEXT,
  -- generiert YYYY-MM-DD HH:MM:SS
  'eingelesen_datum' TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- 0 -> Fehler, 1 -> erfolgreich
  'erfolgreich'      INTEGER NULL    ,
  UNIQUE (
        'Dateiname',
        'Arbeitsblatt',
        'Jahr'
    )
);

-- (bereinigte Werte, Jahr und Aerztl_Stelle siehe Arbeitsblatt_id)
CREATE TABLE IF NOT EXISTS 'Einzelwerte' (
    -- generiert
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Einrichtung oder Geraetetyp
    'ID_der_RX' TEXT NOT NULL,
    'UCode_id' INTEGER NOT NULL,
    -- Referenz zu Datei und Arbeitsblatt
    'Arbeitsblatt_id' INTEGER NOT NULL,
    -- Dosisflaechenprodukt, forrmatiert
    'DFP' REAL NULL,
    -- Average Glandular Dose, formatiert
    'AGD' REAL NULL,
    -- Computed Tomography Dose Index, formatiert
    'CTDI' REAL NULL,
    -- formatiert
    'Dosiswert' REAL NULL,
    -- generated, YYYY-MM-DD HH:MM:SS
    'Erstellungsdatum' TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ('UCode_id') REFERENCES 'Untersuchungscodes' ('id'),
    FOREIGN KEY ('Arbeitsblatt_id') REFERENCES 'eingelesene_dateien' ('id')
);

CREATE TABLE IF NOT EXISTS 'Optionalwerte' (
    -- generiert
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    -- Referenz zu Datei und Arbeitsblatt
    'Einzelwert_id' INTEGER NOT NULL,
    -- Dosisflaechenprodukt, forrmatiert
    'Spaltenname' TEXT NULL,
    -- Average Glandular Dose, formatiert
    'Wert' TEXT NULL,
    FOREIGN KEY ('Einzelwert_id') REFERENCES 'Einzelwerte' ('id')
);

CREATE VIEW einzelwerte_details AS 
    SELECT ewt."Dosiswert", ewt."ID_der_RX", ewt."UCode_id", u."UCode", edt."Aerztl_Stelle", edt."Jahr"  FROM "Einzelwerte" as ewt  
    JOIN eingelesene_dateien as edt  on ewt."Arbeitsblatt_id" = edt.id 
    JOIN "Untersuchungscodes" as u on ewt."UCode_id" = u.id
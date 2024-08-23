get_uom = """
SELECT "ItemUOM_Key" 
FROM "ItemUOM" 
WHERE "ItemUOM_Descr" = %s AND "ItemUOM_ItemTyp_Key" = %s;
"""

create_uom = """
INSERT INTO "ItemUOM" 
("ItemUOM_Descr", "itemUOM_StockUOM_Key", "ItemUOK_ConvUnits", "ItemUOM_CreatedBy", "ItemUOM_CreatedDtTm", "ItemUOM_LastModifiedBy", "ItemUOM_LastModifiedDtTm", "ItemUOM_Client_ID", "ItemUOM_ItemTyp_Key", "ItemUOM_UOMTyp_Key")
VALUES (%s, NULL, NULL, %s, %s, NULL, NULL, %s, %s, NULL)
RETURNING "ItemUOM_Key";
"""

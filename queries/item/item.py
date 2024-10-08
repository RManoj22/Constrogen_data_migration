get_item = """SELECT "Item_Key"
FROM "Item"
WHERE "Item_Descr" = %s AND "Item_ItemTyp_Key" = %s AND "Item_SubType_Key" = %s;
"""

get_item_with_descr = """SELECT "Item_Key"
FROM "Item"
WHERE "Item_Descr" = %s;
"""

create_item = """
INSERT INTO "Item"
("Item_Descr", "Item_Model_Number", "Item_StockType", "Item_Gst", "Item_Amount", "Item_CreatedBy", "Item_CreatedDtTm", "Item_LastModifiedBy", "Item_LastModifiedDtTm", "Item_Client_ID", "Item_ItemTyp_Key", "Item_SubType_Key")
VALUES (%s, NULL, %s, %s, NULL, %s, %s, NULL, NULL, %s, %s, %s)
RETURNING "Item_Key";
"""

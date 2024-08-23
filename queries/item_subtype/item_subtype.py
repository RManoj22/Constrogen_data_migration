get_item_subtype = """
SELECT "ItemSubTyp_Key" 
FROM "ItemSubType" 
WHERE "ItemSubTyp_Descr" = %s AND "ItemSubTyp_Gst" = %s AND "ItemSubTyp_ItemTyp_Key" = %s;
"""

create_item_subtype = """
INSERT INTO "ItemSubType" 
("ItemSubTyp_Descr", "ItemSubTyp_Gst", "ItemSubTyp_CreatedBy", "ItemSubTyp_CreatedDtTm", "ItemSubTyp_LastModifiedBy", "ItemSubTyp_LastModifiedDtTm", "ItemSubTyp_Client_ID", "ItemSubTyp_ItemTyp_Key")
VALUES (%s, %s, %s, %s, NULL, NULL, %s, %s)
RETURNING "ItemSubTyp_Key";
"""

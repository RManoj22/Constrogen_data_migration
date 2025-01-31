get_item_type = """
SELECT "ItemTyp_Key" 
FROM "ItemType" 
WHERE "ItemTyp_Descr" = %s AND "ItemTyp_Client_ID" = %s;
"""

create_item_type = """
INSERT INTO "ItemType" 
("ItemTyp_Descr", "ItemTyp_CreatedBy", "ItemTyp_CreatedDtTm", "ItemTyp_LastModifiedBy", "ItemTyp_LastModifiedDtTm", "ItemTyp_Client_ID")
VALUES (%s, %s, %s, NULL, NULL, %s)
RETURNING "ItemTyp_Key";
"""

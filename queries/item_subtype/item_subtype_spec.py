get_item_subtype_spec = """
SELECT "ItemSubtypeSpec_Key" 
FROM "ItemSubtypeSpecification"
WHERE "ItemSubtypeSpec_Descr" = %s AND "ItemSubtypeSpec_ItemSubtype_Key" = %s;
"""

create_item_subtype_spec = """
INSERT INTO "ItemSubtypeSpecification"
("ItemSubtypeSpec_Descr", "ItemSubtypeSpec_CreatedBy", "ItemSubtypeSpec_CreatedDtTm", "ItemSubtypeSpec_LastModifiedBy", "ItemSubtypeSpec_LastModifiedDtTm", "ItemSubtypeSpec_Client_ID", "ItemSubtypeSpec_ItemSubtype_Key")
VALUES (%s, %s, %s, NULL, NULL, %s, %s)
RETURNING "ItemSubtypeSpec_Key";
"""

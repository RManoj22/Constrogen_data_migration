get_item_spec = """
SELECT "ItemSpec_Key"
FROM "ItemSpecification"
WHERE "ItemSpec_Value" = %s AND "ItemSpec_Item_key" = %s AND "ItemSpec_ItemSubtypeSpec_ID" = %s;
"""

create_item_spec = """
INSERT INTO "ItemSpecification"
("ItemSpec_Value", "ItemSpec_CreatedBy", "ItemSpec_CreatedDtTm", "ItemSpec_LastModifiedBy", "ItemSpec_LastModifiedDtTm", "ItemSpec_Client_ID", "ItemSpec_Item_key", "ItemSpec_ItemSubtypeSpec_ID")
VALUES (%s, %s, %s, NULL, NULL, %s, %s, %s)
RETURNING "ItemSpec_Key";
"""

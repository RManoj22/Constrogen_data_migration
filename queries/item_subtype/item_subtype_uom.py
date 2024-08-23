get_item_subtype_uom = """
SELECT "ItemSubtypeUOM_Key"
FROM "ItemSubtype_ItemUOM"
WHERE "ItemSubtypeUOM_ItemSubtype_Key" = %s AND "ItemSubtypeUOM_ItemUOM_Key" = %s;
"""

create_item_subtype_uom = """
INSERT INTO "ItemSubtype_ItemUOM"
("ItemSubtypeUOM_CreatedBy", "ItemSubtypeUOM_CreatedDtTm", "ItemSubtypeUOM_LastModifiedBy", "ItemSubtypeUOM_LastModifiedDtTm", "ItemSubtypeUOM_Client_ID", "ItemSubtypeUOM_ItemSubtype_Key", "ItemSubtypeUOM_ItemUOM_Key")
VALUES (%s, %s, NULL, NULL, %s, %s, %s)
RETURNING "ItemSubtypeUOM_Key";
"""

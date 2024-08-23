get_item_uom = """
SELECT "ItemItemUOM_Key"
FROM "Item_ItemUOM"
WHERE "ItemItemUOM_Item_Key" = %s AND "ItemItemUOM_ItemUOM_Key" = %s;
"""

create_item_uom = """
INSERT INTO "Item_ItemUOM"
("ItemItemUOM_CreatedBy", "ItemItemUOM_CreatedDtTm", "ItemItemUOM_LastModifiedBy", "ItemItemUOM_LastModifiedDtTm", "ItemItemUOM_Client_ID", "ItemItemUOM_Item_Key", "ItemItemUOM_ItemUOM_Key")
VALUES (%s, %s, NULL, NULL, %s, %s, %s)
RETURNING "ItemItemUOM_Key";
"""
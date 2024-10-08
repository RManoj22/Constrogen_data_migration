get_item_purpose = """
SELECT "ItemPurpose_Key" 
FROM "ItemPurpose" 
WHERE "ItemPurpose_ItemKey" = %s AND "ItemPurpose_PurposeKey" = %s AND "ItemPurpose_ClientID" = %s ;
"""

create_item_purpose = """
INSERT INTO "ItemPurpose"
("ItemPurpose_ItemKey", "ItemPurpose_PurposeKey", "ItemPurpose_ClientID")
VALUES (%s, %s, %s)
RETURNING "ItemPurpose_Key";
"""

get_vendor_item_type = """
SELECT "VendItemType_Key" 
FROM "VendorItemType" 
WHERE "VendItemType_Vend_Key" = %s
AND  "VendItemType_Item_Type_Key" = %s;
"""

create_vendor_item_type = """
INSERT INTO "VendorItemType" 
("VendItemType_Vend_Key", "VendItemType_Item_Type_Key", "VendItemType_Client_ID", "VendItemType_Company_ID")
VALUES (%s, %s, %s, %s)
RETURNING "VendItemType_Key";
"""

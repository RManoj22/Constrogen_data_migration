get_vendor_po_desc = """
SELECT "PO_Desc" FROM "PurchaseOrder"
"""

get_vendor_po_details= """
SELECT 
"PO_Date", 
"PO_NetAmt", 
"PO_Client_ID", 
"PO_Company_ID", 
"PO_Proj_Key", 
"PO_Vend_Key", 
"PO_GstAmt", 
"PO_Key"
FROM "PurchaseOrder"
WHERE "PO_Desc" = %s;
"""

update_vendor_po_status = """
UPDATE "PurchaseOrder"
SET "PO_Status" = 'I'
WHERE "PO_Key" = %s;
"""

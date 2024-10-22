get_last_vendor_po_number = """      
SELECT "PO_Number" FROM "PurchaseOrder"
WHERE "PO_Company_ID" = %s AND "PO_Client_ID" = %s
ORDER BY "PO_Key" DESC LIMIT 1
"""

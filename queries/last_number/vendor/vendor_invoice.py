get_last_vendor_invoice_number = """
SELECT "VendInv_InvoiceNo" FROM "VendorInvoice"
WHERE "VendInv_Company_ID" = %s AND "VendInv_Client_ID" = %s
ORDER BY "VendInv_Key" DESC LIMIT 1
"""

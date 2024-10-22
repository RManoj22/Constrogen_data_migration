get_vendor_invoice = """
SELECT "VendInv_Key"
FROM "VendorInvoice"
WHERE 
    "VendInv_InvoiceDate" = %s AND
    "VendInv_InvAmt" = %s AND
    "VendInv_Client_ID" = %s AND
    "VendInv_Company_ID" = %s AND
    "VendInv_Proj_Key" = %s AND
    "VendInv_Vend_Key" = %s AND
    "VendInv_GstAmt" = %s AND
    "VendInv_PO_Key" = %s;
"""

create_vendor_invoice = """
INSERT INTO "VendorInvoice" (
    "VendInv_InvoiceNo", 
    "VendInv_InvoiceDate", 
    "VendInv_InvNotes", 
    "VendInv_InvAmt", 
    "VendInv_BalAmt", 
    "VendInv_CreatedBy", 
    "VendInv_CreatedDtTm", 
    "VendInv_LastModifiedBy", 
    "VendInv_LastModifiedDtTm", 
    "VendInv_Client_ID", 
    "VendInv_Company_ID", 
    "VendInv_Proj_Key", 
    "VendInv_Vend_Key", 
    "VendInv_GstAmt", 
    "VendInv_Method", 
    "VendInv_TdsAmt", 
    "VendInv_PO_Key", 
    "VendorInv_InvoiceStatus", 
    "VendorInv_PaidAmount"
) VALUES (
    %s, %s, NULL, %s, %s, %s, %s,
    NULL, NULL, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s
) RETURNING "VendInv_Key";
"""

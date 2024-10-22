get_vendor_voucher_hdr = """
SELECT "VendorPaymentVoucherHdr_Key"
FROM "VendorPaymentVoucherHdr"
WHERE "VendorPaymentVoucherHdr_VendorVoucherDate" = %s 
  AND "VendorPaymentVoucherHdr_TotalAmount" = %s 
  AND "VendorPaymentVoucherHdr_ClientID" = %s 
  AND "VendorPaymentVoucherHdr_CompanyID" = %s 
  AND "VendorPaymentVoucherHdr_VendorID" = %s 
  AND "VendorPaymentVoucherHdr_PaymentModeID" = %s;
"""

create_vendor_voucher_hdr = """
INSERT INTO "VendorPaymentVoucherHdr"
("VendorPaymentVoucherHdr_VoucherNumber", "VendorPaymentVoucherHdr_VendorVoucherDate", "VendorPaymentVoucherHdr_TransactionDetail", 
"VendorPaymentVoucherHdr_Notes", "VendorPaymentVoucherHdr_TotalAmount", "VendorPaymentVoucherHdr_AccountID", 
"VendorPaymentVoucherHdr_ClientID", "VendorPaymentVoucherHdr_CompanyID", "VendorPaymentVoucherHdr_PaymentModeID", 
"VendorPaymentVoucherHdr_VendorID")
VALUES (%s, %s, NULL, NULL, %s, NULL, %s, %s, %s, %s)
RETURNING "VendorPaymentVoucherHdr_Key";
"""

get_vendor_voucher_dtl = """
SELECT "VendorPaymentVoucherDtl_Key"
FROM "VendorPaymentVoucherDtl"
WHERE "VendorPaymentVoucherDtl_InvoiceID" = %s
  AND "VendorPaymentVoucherDtl_PaidAmount" = %s
  AND "VendorPaymentVoucherDtl_ClientID" = %s
  AND "VendorPaymentVoucherDtl_VendorPaymentVoucherHdrKey" = %s;
"""


create_vendor_voucher_dtl = """
INSERT INTO "VendorPaymentVoucherDtl"
("VendorPaymentVoucherDtl_PaidAmount", "VendorPaymentVoucherDtl_ClientID", "VendorPaymentVoucherDtl_InvoiceID", 
"VendorPaymentVoucherDtl_VendorPaymentVoucherHdrKey")
VALUES (%s, %s, %s, %s)
RETURNING "VendorPaymentVoucherDtl_Key";
"""

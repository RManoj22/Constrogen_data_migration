get_contractor_voucher_hdr = """
SELECT "ContractVoucherHdr_Key"
FROM "ContractVoucherHdr"
WHERE "ContractVoucherHdr_ContractVoucherDate" = %s 
  AND "ContractVoucherHdr_TotalAmount" = %s 
  AND "ContractVoucherHdr_ClientID" = %s 
  AND "ContractVoucherHdr_CompanyID" = %s 
  AND "ContractVoucherHdr_ContractorID" = %s 
  AND "ContractVoucherHdr_PaymentModeID" = %s;
"""

create_contractor_voucher_hdr = """
INSERT INTO "ContractVoucherHdr"
("ContractVoucherHdr_VoucherNumber", "ContractVoucherHdr_ContractVoucherDate", "ContractVoucherHdr_TransactionDetail", 
"ContractVoucherHdr_Notes", "ContractVoucherHdr_TotalAmount", "ContractVoucherHdr_AccountID", 
"ContractVoucherHdr_ClientID", "ContractVoucherHdr_CompanyID", "ContractVoucherHdr_PaymentModeID", 
"ContractVoucherHdr_ContractorID")
VALUES (%s, %s, NULL, NULL, %s, NULL, %s, %s, %s, %s)
RETURNING "ContractVoucherHdr_Key";
"""

get_contractor_voucher_dtl = """
SELECT "ContractVoucherDtl_Key"
FROM "ContractVoucherDtl"
WHERE "ContractVoucherDtl_InvoiceID" = %s 
  AND "ContractVoucherDtl_PaidAmount" = %s 
  AND "ContractVoucherDtl_ClientID" = %s 
  AND "ContractVoucherDtl_ContractVoucherHdrKey" = %s;
"""

create_contractor_voucher_dtl = """
INSERT INTO "ContractVoucherDtl"
("ContractVoucherDtl_PaidAmount", "ContractVoucherDtl_ContractVoucherHdrKey", "ContractVoucherDtl_InvoiceID", "ContractVoucherDtl_ClientID")
VALUES (%s, %s, %s, %s)
RETURNING "ContractVoucherDtl_Key";
"""

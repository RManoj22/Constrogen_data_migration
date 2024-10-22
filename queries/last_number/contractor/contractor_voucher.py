get_last_contractor_voucher_number = """
SELECT "ContractVoucherHdr_VoucherNumber" FROM "ContractVoucherHdr"
WHERE "ContractVoucherHdr_CompanyID" = %s AND "ContractVoucherHdr_ClientID" = %s
ORDER BY "ContractVoucherHdr_Key" DESC LIMIT 1
"""

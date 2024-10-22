get_last_vendor_voucher_number = """
SELECT "VendorPaymentVoucherHdr_VoucherNumber" FROM "VendorPaymentVoucherHdr"
WHERE "VendorPaymentVoucherHdr_CompanyID" = %s AND "VendorPaymentVoucherHdr_ClientID" = %s
ORDER BY "VendorPaymentVoucherHdr_Key" DESC LIMIT 1
"""

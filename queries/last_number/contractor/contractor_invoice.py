get_last_contractor_invoice_number = """
SELECT "ContractorInvoice_InvoiceID" FROM "ContractorInvoice"
WHERE "ContractorInvoice_CompanyID" = %s AND "ContractorInvoice_ClientID" = %s
ORDER BY "ContractorInvoiceKey" DESC LIMIT 1
"""

get_contractor_invoice = """
SELECT "ContractorInvoiceKey"
FROM "ContractorInvoice"
WHERE 
    "ContractorInvoice_InvoiceDate" = %s AND
    "ContractorInvoice_InvoiceAmount" = %s AND
    "ContractorInvoice_TDSAmount" = %s AND
    "ContractorInvoice_ClientID" = %s AND
    "ContractorInvoice_CompanyID" = %s AND
    "ContractorInvoice_ProjectID" = %s AND
    "ContractorInvoice_ContractorID" = %s;
"""


create_contractor_invoice = """
INSERT INTO "ContractorInvoice" (
    "ContractorInvoice_InvoiceID", 
    "ContractorInvoice_InvoiceDate", 
    "ContractorInvoice_InvoiceAmount", 
    "ContractorInvoice_TDSAmount", 
    "ContractorInvoice_InvoiceType", 
    "ContractorInvoice_InvoiceDesc", 
    "ContractorInvoice_AgreementID", 
    "ContractorInvoice_ClientID", 
    "ContractorInvoice_CompanyID", 
    "ContractorInvoice_PaymentScheldueID", 
    "ContractorInvoice_ProjectID", 
    "ContractorInvoice_PaidAmount", 
    "ContractorInvoice_ContractorID", 
    "ContractorInvoice_InvoiceStatus"
) VALUES (
    %s, %s, %s, %s, %s, NULL, NULL, 
    %s, %s, NULL, %s, %s, %s, %s
) RETURNING "ContractorInvoiceKey";
"""


update_contractor_invoice_status = """
UPDATE "ContractorInvoice"
SET "ContractorInvoice_InvoiceStatus" = 'P'
WHERE "ContractorInvoiceKey" = %s;
"""

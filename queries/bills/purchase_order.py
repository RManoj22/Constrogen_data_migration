get_purchase_order = """
SELECT "PO_Key" FROM "PurchaseOrder" WHERE "PO_Desc" = %s AND "PO_Date" = %s AND "PO_NetAmt" = %s AND "PO_GstAmt" = %s AND "PO_Vend_Key" = %s AND "PO_Proj_Key" = %s AND "PO_Client_ID" = %s AND "PO_Company_ID" = %s;
"""

create_purchase_order = """
INSERT INTO "PurchaseOrder" (
    "PO_Number", "PO_Desc", "PO_Date", "PO_CreatedBy", "PO_CreatedDtTm", "PO_Client_ID", "PO_Company_ID", "PO_Proj_Key", "PO_Vend_Key", "PO_GstAmt",
    "PO_NetAmt", "PO_Status", "PO_TdsAmt"
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
RETURNING "PO_Key";
"""

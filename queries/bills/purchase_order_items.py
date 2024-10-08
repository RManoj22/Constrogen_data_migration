get_purchase_order_item = """
SELECT "POItm_Key" FROM "PurchaseOrder_Items" WHERE "POItm_PO_Key" = %s AND "POItm_Item_Key" = %s AND "POItm_NetAmt" = %s AND "POItm_Qty" = %s AND "POItm_Client_ID" = %s AND "POItm_Company_ID" = %s;
"""

create_purchase_order_item = """
INSERT INTO "PurchaseOrder_Items" (
    "POItm_NetAmt", "POItm_PO_Key", "POItm_CreatedBy", "POItm_CreatedDtTm", "POItm_Client_ID", "POItm_Company_ID", "POItm_Item_Key",
    "POItm_Qty"
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s 
    )
RETURNING "POItm_Key";
"""

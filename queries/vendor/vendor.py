get_vendor = """
SELECT "Vend_Key" 
FROM "Vendor" 
WHERE "Vend_Name" = %s AND "Vend_Client_ID" = %s AND "Vend_Company_ID" = %s;
"""

create_vendor = """
INSERT INTO "Vendor" 
("Vend_Name", "Vend_Addr1", "Vend_Addr2", "Vend_BriefDescr", "Vend_ModeOfPay", "Vend_GSTNumber", "Vend_CreatedBy", "Vend_CreatedDtTm", "Vend_LastModifiedBy", "Vend_LastModifiedDtTm", "Vend_ContactName", "Vend_ContactPhoneNo", "Vend_APTerm_Key", "Vend_City_Key", "Vend_Client_ID", "Vend_Company_ID", "Vend_State_Key", "Vend_ContactLandlineNo", "Vend_PinCode","Vend_InActive")
VALUES (%s, NULL, NULL, NULL, NULL, NULL, %s, %s, NULL, NULL, NULL, NULL, NULL, %s, %s, %s, %s, NULL, NULL, 'N')
RETURNING "Vend_Key";
"""

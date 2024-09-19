get_vendor_type = """
SELECT "VendTyp_Key" 
FROM "VendorType" 
WHERE "VendTyp_Descr" = %s AND "VendTyp_Company_ID" = %s;
"""

create_vendor_type = """
INSERT INTO "builder-iq"."VendorType" 
("VendTyp_Descr", "VendTyp_CreatedBy", "VendTyp_CreatedDtTm", "VendTyp_LastModifiedBy", "VendTyp_LastModifiedDtTm", "VendTyp_Client_ID", "VendTyp_Company_ID")
VALUES (%s, %s, %s, NULL, NULL, %s, %s)
RETURNING "VendTyp_Key";
"""

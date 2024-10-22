get_simple_contractor = """
SELECT "Contractor_Key"
FROM "Contractor"
WHERE "Contractor_Name" = %s
AND "Contractor_Client_ID" = %s
AND "Contractor_Company_ID" = %s;
"""

get_contractor = """
SELECT "Contractor_Key"
FROM "Contractor"
WHERE "Contractor_Name" = %s
AND "Contractor_ContractorTyp_Key" = %s
AND "Contractor_Client_ID" = %s
AND "Contractor_Company_ID" = %s;
"""

create_contractor = """
INSERT INTO "Contractor"
(
    "Contractor_Name", "Contractor_CreatedBy", "Contractor_CreatedDtTm", "Contractor_Client_ID", "Contractor_Company_ID", "Contractor_ContractorTyp_Key", "Contractor_InActive", "Contractor_InHouse"
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
RETURNING "Contractor_Key";
"""

# create_contractor = """
# INSERT INTO "Contractor"
# (
#     "Contractor_Name", "Contractor_Addr1", "Contractor_Addr2", "Contractor_PinCode", 
#     "Contractor_GSTNumber", "Contractor_ContactPhoneNo", "Contractor_ContactLandlineNo", 
#     "Contractor_ContactEmailID", "Contractor_InActive", "Contractor_InHouse", 
#     "Contractor_CreatedBy", "Contractor_CreatedDtTm", "Contractor_City_Key", 
#     "Contractor_Client_ID", "Contractor_Company_ID", "Contractor_ContractorTyp_Key", 
#     "Contractor_State_Key"
# )
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# RETURNING "Contractor_Key";
# """
get_contractor_type = """
SELECT "ContractorTyp_Key" 
FROM "ContractorType" 
WHERE "ContractorTyp_Descr" = %s
AND "ContractorTyp_Client_ID" = %s
AND "ContractorTyp_Company_ID" = %s;
"""

create_contractor_type = """
INSERT INTO "ContractorType" 
("ContractorTyp_Descr", "ContractorTyp_CreatedBy", "ContractorTyp_CreatedDtTm", 
"ContractorTyp_LastModifiedBy", "ContractorTyp_LastModifiedDtTm", "ContractorTyp_Client_ID", "ContractorTyp_Company_ID")
VALUES (%s, %s, %s, NULL, NULL, %s, %s)
RETURNING "ContractorTyp_Key";
"""

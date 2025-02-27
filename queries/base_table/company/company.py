get_company = """
SELECT "Company_ID" 
FROM "Company"
WHERE "Company_Name" = %s AND "Company_Client_ID" = %s;
"""

create_company = """
INSERT INTO "Company" 
("Company_Name", "Company_Client_ID")
VALUES (%s, %s)
RETURNING "Company_ID";
"""

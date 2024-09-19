get_city = """
SELECT "City_Key" 
FROM "City" 
WHERE "City_Name" = %s AND "City_Company_ID" = %s AND "City_State_Key" = %s;
"""

create_city = """
INSERT INTO "City" 
("City_Name", "City_CreatedBy", "City_CreatedDtTm", "City_LastModifiedBy", "City_LastModifiedDtTm", "City_Client_ID", "City_Company_ID", "City_State_Key")
VALUES (%s, %s, %s, NULL, NULL, %s, %s, %s)
RETURNING "City_Key";
"""

get_project = """
SELECT "Proj_Key" 
FROM "Project" 
WHERE "Proj_Name" = %s
"""

create_project = """
INSERT INTO "Project"
("Proj_ID", "Proj_Name", "Proj_Addr1", "Proj_No_Of_Units", "Proj_CreatedBy", "Proj_CreatedDtTm", "Proj_City_Key", "Proj_Client_ID", "Proj_Company_ID", "Proj_ProjStatus_Key", "Proj_ProjTyp_Key", "Proj_State_Key")
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
RETURNING "Proj_Key";
"""

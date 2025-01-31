get_project_type = """
SELECT "ProjTyp_Key" 
FROM "ProjectType" 
WHERE "ProjTyp_Descr" = %s AND "ProjTyp_Company_ID" = %s AND "ProjTyp_Client_ID" = %s;
"""

create_project_type = """
INSERT INTO "ProjectType" 
("ProjTyp_Descr", "ProjTyp_CreatedBy", "ProjTyp_CreatedDtTm", "ProjTyp_LastModifiedBy", "ProjTyp_LastModifiedDtTm", "ProjTyp_Client_ID", "ProjTyp_Company_ID")
VALUES (%s, %s, %s, NULL, NULL, %s, %s)
RETURNING "ProjTyp_Key";
"""

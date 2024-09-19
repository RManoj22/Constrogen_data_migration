get_project_status = """
SELECT "ProjStatus_Key" 
FROM "ProjectStatus" 
WHERE "ProjStatus_Descr" = %s AND "ProjStatus_Company_ID" = %s;
"""

create_project_status = """
INSERT INTO "ProjectStatus" 
("ProjStatus_Descr", "ProjStatus_Is_Active_State", "ProjStatus_Client_ID", "ProjStatus_Company_ID")
VALUES (%s, true, %s, %s)
RETURNING "ProjStatus_Key";
"""

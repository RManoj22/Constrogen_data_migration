get_purpose = """
SELECT "Purpose_Key" 
FROM "Purpose"
WHERE "Purpose_Name" = %s AND "Purpose_ItemTyp_Key" = %s;
"""

create_purpose = """
INSERT INTO "Purpose"
("Purpose_Name", "Purpose_CreatedBy", "Purpose_CreatedDtTm", "Purpose_LastModifiedBy", "Purpose_LastModifiedDtTm", "Purpose_Client_ID", "Purpose_ItemTyp_Key")
VALUES (%s, %s, %s, NULL, NULL, %s, %s)
RETURNING "Purpose_Key";
"""

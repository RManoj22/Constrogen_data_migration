get_state = """
SELECT "State_Key" 
FROM "State" 
WHERE "State_Name" = %s;
"""

create_state = """
INSERT INTO "State" 
("State_ID", "State_Name")
VALUES (%s, %s)
RETURNING "State_Key";
"""

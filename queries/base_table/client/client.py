get_client = """
SELECT "Client_ID" 
FROM "ClientBase"
WHERE "Client_Name" = %s;
"""

create_client = """
INSERT INTO "ClientBase" 
("Client_Name")
VALUES (%s)
RETURNING "Client_ID";
"""

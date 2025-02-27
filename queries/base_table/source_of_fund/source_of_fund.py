get_source_of_fund = """
SELECT "SourceOfFund_Key" 
FROM "SourceOfFund"
WHERE "SourceOfFund_Name" = %s;
"""

create_source_of_fund = """
INSERT INTO "SourceOfFund" 
("SourceOfFund_Name")
VALUES (%s)
RETURNING "SourceOfFund_Key";
"""

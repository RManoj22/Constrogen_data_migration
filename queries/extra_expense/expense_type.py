get_expense_type = """
SELECT "ExpenseType_Key" 
FROM "ExpenseType" 
WHERE "ExpenseType_Descr" = %s AND "ExpenseType_Company_ID" = %s;
"""

create_expense_type = """
INSERT INTO "ExpenseType" 
("ExpenseType_Descr", "ExpenseType_Client_ID", "ExpenseType_Company_ID")
VALUES (%s, %s, %s)
RETURNING "ExpenseType_Key";
"""

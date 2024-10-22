get_extra_expense = """
SELECT "PaidExpenses_Key" 
FROM "PaidExpenses"
WHERE "PaidExpenses_Date" = %s AND "PaidExpenses_Amount" = %s AND "PaidExpenses_ExpenseType" = %s AND "PaidExpenses_ProjectKey" = %s;
"""

create_extra_expense = """
INSERT INTO "PaidExpenses" 
("PaidExpenses_Date", "PaidExpenses_Amount", "PaidExpenses_Payment_Desc", "PaidExpenses_ClientID", "PaidExpenses_CompanyID", "PaidExpenses_PaymentModeKey", "PaidExpenses_ProjectKey", "PaidExpenses_AccountID", "PaidExpenses_Notes", "PaidExpenses_ExpenseType")
VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NULL, %s)
RETURNING "PaidExpenses_Key";
"""

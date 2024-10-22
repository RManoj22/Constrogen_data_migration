
get_mode_of_pay_query = """
SELECT "ModeOfPay" 
FROM "ModeOfPay" 
WHERE "ModeOfPay_Descr" = %s
"""

create_mode_of_pay_query = """
INSERT INTO "ModeOfPay"
("ModeOfPay", "ModeOfPay_Descr")
VALUES (%s, %s)
RETURNING "ModeOfPay";
"""

get_mode_of_pay = """
SELECT "ModeOfPay" 
FROM "ModeOfPay"
WHERE "ModeOfPay_Descr" = %s;
"""

create_mode_of_pay = """
INSERT INTO "ModeOfPay" 
("ModeOfPay","ModeOfPay_Descr")
VALUES (%s, %s)
RETURNING "ModeOfPay";
"""

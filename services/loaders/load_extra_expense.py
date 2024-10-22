from utils.logger import logger
from services.get_or_create.project.project import get_or_create_project
from utils.excel_readers.read_extra_expense_data import read_extra_expense_data
from services.get_or_create.extra_expense.expense_type import get_or_create_expense_type
from services.get_or_create.extra_expense.extra_expense import get_or_create_extra_expense
from services.get_or_create.payment.mode_of_pay.mode_of_pay import get_or_create_mode_of_pay
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT, MODE_OF_PAYMENT


client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT
mode_of_pay = MODE_OF_PAYMENT


def load_extra_expense(conn):
    extra_expenses = read_extra_expense_data()
    logger.info(f"Data read from Excel: {extra_expenses}")

    counters = {
        "expense type": {"created": 0, "existing": 0},
        "extra expense": {"created": 0, "existing": 0},
        "mode of pay": {"created": 0, "existing": 0},
        "project": {"created": 0, "existing": 0}
    }

    for date, bill_no, material_type, vendor, amount, project, item in extra_expenses:
        if material_type == 'Extra Expense':
            material_type = 'Miscellaneous Expenses'
        elif material_type in ['Printer Toner Refill', 'System Purchase and Repair', 'Electronics']:
            material_type = 'System Maintenance and Repair'

        expense_type_key, created = get_or_create_expense_type(
            conn, material_type)
        if created:
            counters["expense type"]["created"] += 1
        else:
            counters["expense type"]["existing"] += 1
        logger.info(
            f"The key of the expense_type {material_type} is: {expense_type_key}")

        mode_of_pay_key, created = get_or_create_mode_of_pay(conn, mode_of_pay)
        if created:
            counters["mode of pay"]["created"] += 1
        else:
            counters["mode of pay"]["existing"] += 1
        logger.info(
            f"The key of the mode of pay {mode_of_pay} is: {mode_of_pay_key}")

        project_key, created = get_or_create_project(conn, project)
        if created:
            counters["project"]["created"] += 1
        else:
            counters["project"]["existing"] += 1
        logger.info(f"The key of the project {project} is: {project_key}")

        payment_desc = f'BillNo: {bill_no}, Vendor: {vendor} and Item details: {item} '

        print('type(date):: ',type(date))
        extra_expense_key, created = get_or_create_extra_expense(
            conn, date, amount, payment_desc, mode_of_pay_key, project_key, expense_type_key
        )
        if created:
            counters["extra expense"]["created"] += 1
        else:
            counters["extra expense"]["existing"] += 1
        logger.info(
            f"The key of the extra expense with date {date}, amount {amount} and expense type {material_type} is:{extra_expense_key}")

    conn.commit()
    logger.info("All operations completed successfully. Transaction committed.")

    for service, count in counters.items():
        logger.info(
            f"{service.capitalize()} - Created: {count['created']}, Existing: {count['existing']}"
        )

    return counters

import config
from utils.logger import logger
from database.db_connection import get_db_connection
from services.loaders.load_bills import load_bills
from services.loaders.load_items import load_items
from services.loaders.load_vendors import load_vendors
from services.loaders.load_projects import load_projects
from services.loaders.load_base_tables import load_base_table
from services.loaders.load_contractors import load_contractors
from services.loaders.load_extra_expense import load_extra_expense
from services.loaders.load_vendor_invoice_and_voucher import load_vendor_invoice_and_voucher
from services.loaders.load_contractor_invoice_and_voucher import load_contractor_invoice_and_voucher

if __name__ == "__main__":
    logger.info("Starting the application")

    conn = get_db_connection()
    if conn:
        try:
            logger.info("Successfully connected to the database")
            conn.autocommit = False

            # Define tasks that need to be loaded
            load_tasks = {
                "Projects": config.LOAD_PROJECTS,
                "Items": config.LOAD_ITEMS,
                "Vendors": config.LOAD_VENDORS,
                "Purchase Orders": config.LOAD_BILLS,
                "Vendor Invoices and Vouchers": config.LOAD_VENDOR_INVOICE_AND_VOUCHER,
                "Extra Expenses": config.LOAD_EXTRA_EXPENSE,
                "Contractors": config.LOAD_CONTRACTORS,
                "Contractor Invoices and Vouchers": config.LOAD_CONTRACTOR_INVOICE_AND_VOUCHER,
                "Base Table Data": config.LOAD_BASE_TABLE_DATA
            }

            # Filter only tasks that are enabled (True in config)
            enabled_tasks = [task for task, enabled in load_tasks.items() if enabled]

            if not enabled_tasks:
                logger.info("No tasks are enabled for loading. Exiting.")
                print("No data loading tasks are enabled in the configuration. Exiting.")
            else:
                # Show the user the tasks that will be loaded
                print("\nThe following data will be loaded:")
                for task in enabled_tasks:
                    print(f" - {task}")

                # Prompt the user for confirmation
                confirmation = input("\nDo you want to proceed? (yes/no): ").strip().lower()

                if confirmation not in ["y", "yes"]:
                    logger.info("User canceled the operation.")
                    print("Operation canceled. Exiting.")
                else:
                    logger.info("User confirmed data loading.")
                    counters = {}

                    if config.LOAD_PROJECTS:
                        counters["projects"] = load_projects(conn)

                    if config.LOAD_ITEMS:
                        counters["items"] = load_items(conn)

                    if config.LOAD_VENDORS:
                        counters["vendors"] = load_vendors(conn)

                    if config.LOAD_BILLS:
                        counters["purchase order"] = load_bills(conn)

                    if config.LOAD_VENDOR_INVOICE_AND_VOUCHER:
                        counters["vendor invoice and voucher"] = load_vendor_invoice_and_voucher(conn)

                    if config.LOAD_EXTRA_EXPENSE:
                        counters["extra expense"] = load_extra_expense(conn)

                    if config.LOAD_CONTRACTORS:
                        counters["contractors"] = load_contractors(conn)

                    if config.LOAD_CONTRACTOR_INVOICE_AND_VOUCHER:
                        counters["contractor invoice and voucher"] = load_contractor_invoice_and_voucher(conn)

                    if config.LOAD_BASE_TABLE_DATA:
                        counters["base table"] = load_base_table(conn)

                    logger.info(f"Counters: {counters}")
                    print("\nData loading completed successfully.")

        except Exception as e:
            conn.rollback()
            logger.error(f"An error occurred during operations: {e}")
            print(f"Error: {e}")
            raise

        finally:
            conn.close()
            logger.info("Database connection closed")
            print("Database connection closed.")

# Constrogen_data_migration

## Setup Instructions

**To get started, follow these steps:**

### 1. Create a Python Virtual Environment

Make sure you have Python installed. Then, create a virtual environment to manage the dependencies.

`python -m venv venv`

### 2. Activate the Virtual Environment

Activate the virtual environment. The activation command depends on your operating system:

On Windows:
`venv\Scripts\activate`

On macOS/Linux:
`source venv/bin/activate`

### 3. Install Dependencies

With the virtual environment activated, install the required packages listed in requirements.txt.

`pip install -r requirements.txt`

### 4. Configure Settings

Update the configuration settings as needed. Open config.py and modify the necessary details according to your requirements. The excel file path is set to the current root directory, change the file_name as needed.

### 5: Create a `.env` File

**In the root directory of the project, create a file named `.env`.**

**Add the following variables to the file, and replace the placeholder values with your actual database configuration:**

`DB_NAME=your_database_name_here`
`DB_USER=your_database_username_here`
`DB_PWD=your_database_password_here`
`DB_HOST=your_database_host_here`
`DB_PORT=your_database_port_here`
`DB_SCHEMA=your_database_schema_here`

### 6. Run the Script

Finally, execute the main script.
`python main.py`

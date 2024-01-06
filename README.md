School-Group repository created for the development of a Three-tier application, project assigned by the lecturer in the course DATA WAREHOUSE AND DATA MINING 
## Name of Contributors 
### 1) KAMCHE YANN ARNAUD 
### 2) METAGNE KAMGA MAIVA
### 3) NKWI CYRIL AKINIMBON
### 4) AMABO JOSHUA

# Personal Expense Tracker Web App

This Flask web application helps you track your personal expenses and visualizes your spending patterns. It uses Snowflake as the backend database for storing expense data.

## Snowflake Credentials Setup

Before running the application, you need to set up your Snowflake credentials. Follow these steps to create a `snowflake_credentials.json` file:

### Prerequisites

- Snowflake account credentials (account name, username, password)
- Information about the Snowflake database and warehouse

### Steps to Create snowflake_credentials.json

1. Open a text editor (e.g., Notepad, VS Code, etc.).

2. Create a new JSON file and copy the following template:

   ```json
   {
       "SNOWFLAKE_ACCOUNT": "your_account_name",
       "SNOWFLAKE_USER": "your_username",
       "SNOWFLAKE_PASSWORD": "your_password",
       "SNOWFLAKE_DATABASE": "your_database_name",
       "SNOWFLAKE_WAREHOUSE": "your_warehouse_name_or_null"
   }
   Replace the placeholder values (your_account_name, your_username, your_password, your_database_name, your_warehouse_name_or_null) with your actual Snowflake credentials. The SNOWFLAKE_WAREHOUSE can be set to null if not applicable.

Save the file with the name snowflake_credentials.json. Ensure that the file extension is .json.

Usage in Flask Application
The snowflake_credentials.json file will be used by the Flask application to establish a connection to Snowflake. Make sure to place this file in the root directory of your Flask application.

In your Flask application code, the connection is established using the following function:

def get_snowflake_connection():
    with open('snowflake_credentials.json') as credentials_file:
        credentials = json.load(credentials_file)

    connection = snowflake.connector.connect(
        account=credentials['SNOWFLAKE_ACCOUNT'],
        user=credentials['SNOWFLAKE_USER'],
        password=credentials['SNOWFLAKE_PASSWORD'],
        database=credentials['SNOWFLAKE_DATABASE'],
        warehouse=credentials['SNOWFLAKE_WAREHOUSE'],
    )
    return connection

Running the Application
### 1. Install dependencies:
pip install -r requirements.txt

### 2. Activate your virtual environment:
source venv/bin/activate  # for Linux or macOS
# or
.\venv\Scripts\activate   # for Windows

### 3. Run the Flask application:
python app.py

### 4. Alternatively, you can use the following command:
   python -m flask run
   
The application will be accessible at http://localhost:5000. Open this URL in your web browser to start tracking your expenses.

Additional Information
Feel free to customize the application according to your needs.
If you encounter any issues or have further questions, please reach out.
Happy expense tracking!

This modification includes information about activating a virtual environment and running the Flask application using `python -m flask run`. Adjust the instructions as needed based on your specific virtual environment setup.


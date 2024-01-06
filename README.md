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

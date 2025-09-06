# Budget App
A simple Python application for budgeting, built with Streamlit and SQLite.

## Requirements / Installation
Before running the project, make sure you have the following installed:

### Requirements:
- **Python 3.12+**
- **pip**
- **Streamlit**
- **SQLite3**
- **Docker** (optional)

### Installation:

Navigate to the desired directory via ```cd``` command and
use
```bash 
git clone https://github.com/pMaciek1/Budget.git
```
This will clone the project into your local repository.

To install the required Python packages, run:
```bash
pip install -r requirements.txt
```

After cloning the repository you can run the application with:
```bash
streamlit run app.py
```

Alternatively, you can build and run a Docker image:

In project directory, build the image: 
```bash
docker build -t budgetapp .
```
Then run the container: 
```bash
docker run -p 8501:8501 budgetapp
```
The Streamlit app will be available on port **8501**.

You can access the page on http://localhost:8501/


## Usage
### 1. Main page

The main page displays:
- The five most recent incomes and expenses
- The total sum of incomes and expenses for the current month
- The balance between them

### 2. Add Transaction

TThis section has two pages: **Income** and **Expense**.

- **Income**: Add a new income record to the database  
- **Expense**: Add a new expense record to the database

When adding a transaction, you can specify:
- Title
- Date
- Amount
- Category (for expenses only)

### 3. History of transaction

This page allows you to view all transactions stored in the database.  
You can filter data by:
- Year (then month)
- Type (Income or Expense)
- Category (for expenses only)

### 4. Analyze Data

This page provides useful data visualizations:
- **Bar Chart**: Displays transactions by month with filtering options
- **Pie Chart**: Shows the percentage share of each expense category per month
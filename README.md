# Employee Management Dashboard

A Streamlit-based dashboard application that displays employee, salary, and department information from a SQLite database.

## Features

- 👥 **Employee Management**: View and search employee information
- 💰 **Salary Analysis**: Analyze salary data with filters and visualizations
- 🏢 **Department Overview**: View department statistics and employee distribution
- 📈 **Analytics**: Interactive charts and insights about compensation trends

## Project Structure

```
.
├── app.py              # Main Streamlit dashboard application
├── database.py         # Database connection and query functions
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sumalata13/skills-getting-started-with-github-copilot.git
cd skills-getting-started-with-github-copilot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database with sample data:
```bash
python init_db.py
```

This will create an `employee_database.db` file with three tables:
- **department**: Department information (id, name, location)
- **employee**: Employee information (id, name, email, hire date, department)
- **salary**: Salary information (id, employee_id, base_salary, bonus, effective_date)

### Running the Application

Start the Streamlit dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Dashboard Pages

### 1. Overview
- Key metrics (total employees, departments, average compensation, total payroll)
- Employee distribution by department
- Salary distribution histogram

### 2. Employees
- Complete employee list with department information
- Search functionality by name or email
- Sortable and filterable data table

### 3. Salaries
- Detailed salary information for all employees
- Filter by compensation range
- Stacked bar chart showing base salary and bonus breakdown

### 4. Departments
- Department overview with employee counts
- Salary statistics by department (min, max, average, total)
- Average compensation visualization

### 5. Analytics
- Department compensation comparison (min, average, max)
- Total payroll distribution by department
- Top 5 earners

## Database Schema

### Department Table
- `department_id`: Integer (Primary Key)
- `department_name`: Text
- `location`: Text

### Employee Table
- `employee_id`: Integer (Primary Key)
- `first_name`: Text
- `last_name`: Text
- `email`: Text
- `hire_date`: Text
- `department_id`: Integer (Foreign Key)

### Salary Table
- `salary_id`: Integer (Primary Key)
- `employee_id`: Integer (Foreign Key)
- `base_salary`: Real
- `bonus`: Real
- `effective_date`: Text

## Sample Data

The initialization script creates:
- 5 departments (Engineering, HR, Marketing, Sales, Finance)
- 10 employees across different departments
- 10 salary records with base salary and bonus information

## Technologies Used

- **Streamlit**: Web application framework for creating the dashboard
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations and charts
- **SQLite**: Lightweight database for storing employee data

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is created as an exercise for getting started with GitHub Copilot.

"""
Database initialization script for Employee Management System.
Creates tables for departments, employees, and salaries with sample data.
"""

import sqlite3
import os

DB_PATH = "employee_database.db"


def init_database():
    """Initialize the database with tables and sample data."""
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    # Create new database connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create Department table
    cursor.execute("""
        CREATE TABLE department (
            department_id INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)
    
    # Create Employee table
    cursor.execute("""
        CREATE TABLE employee (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            hire_date TEXT NOT NULL,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES department(department_id)
        )
    """)
    
    # Create Salary table
    cursor.execute("""
        CREATE TABLE salary (
            salary_id INTEGER PRIMARY KEY,
            employee_id INTEGER NOT NULL,
            base_salary REAL NOT NULL,
            bonus REAL DEFAULT 0,
            effective_date TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
        )
    """)
    
    # Insert sample departments
    departments = [
        (1, "Engineering", "New York"),
        (2, "Human Resources", "Boston"),
        (3, "Marketing", "San Francisco"),
        (4, "Sales", "Chicago"),
        (5, "Finance", "New York")
    ]
    cursor.executemany("INSERT INTO department VALUES (?, ?, ?)", departments)
    
    # Insert sample employees
    employees = [
        (1, "John", "Doe", "john.doe@company.com", "2020-01-15", 1),
        (2, "Jane", "Smith", "jane.smith@company.com", "2019-03-22", 1),
        (3, "Michael", "Johnson", "michael.j@company.com", "2021-06-10", 2),
        (4, "Emily", "Williams", "emily.w@company.com", "2020-11-05", 3),
        (5, "David", "Brown", "david.b@company.com", "2018-09-12", 4),
        (6, "Sarah", "Davis", "sarah.d@company.com", "2022-02-28", 1),
        (7, "Robert", "Miller", "robert.m@company.com", "2019-07-19", 5),
        (8, "Lisa", "Wilson", "lisa.w@company.com", "2021-04-03", 3),
        (9, "James", "Moore", "james.m@company.com", "2020-08-17", 4),
        (10, "Maria", "Taylor", "maria.t@company.com", "2022-01-10", 2)
    ]
    cursor.executemany("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?)", employees)
    
    # Insert sample salaries
    salaries = [
        (1, 1, 95000, 5000, "2020-01-15"),
        (2, 2, 105000, 7000, "2019-03-22"),
        (3, 3, 65000, 3000, "2021-06-10"),
        (4, 4, 78000, 4000, "2020-11-05"),
        (5, 5, 88000, 6000, "2018-09-12"),
        (6, 6, 92000, 4500, "2022-02-28"),
        (7, 7, 110000, 8000, "2019-07-19"),
        (8, 8, 72000, 3500, "2021-04-03"),
        (9, 9, 85000, 5500, "2020-08-17"),
        (10, 10, 68000, 3200, "2022-01-10")
    ]
    cursor.executemany("INSERT INTO salary VALUES (?, ?, ?, ?, ?)", salaries)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database '{DB_PATH}' initialized successfully!")
    print("Tables created: department, employee, salary")
    print("Sample data inserted for 5 departments, 10 employees, and 10 salary records")


if __name__ == "__main__":
    init_database()

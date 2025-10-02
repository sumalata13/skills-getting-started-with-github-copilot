"""
Database connection and query functions for Employee Management System.
"""

import sqlite3
import pandas as pd

DB_PATH = "employee_database.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def get_all_employees():
    """Get all employees with their department information."""
    conn = get_connection()
    query = """
        SELECT 
            e.employee_id,
            e.first_name,
            e.last_name,
            e.email,
            e.hire_date,
            d.department_name,
            d.location
        FROM employee e
        LEFT JOIN department d ON e.department_id = d.department_id
        ORDER BY e.employee_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_all_salaries():
    """Get all salary information with employee details."""
    conn = get_connection()
    query = """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name AS employee_name,
            s.base_salary,
            s.bonus,
            s.base_salary + s.bonus AS total_compensation,
            s.effective_date,
            d.department_name
        FROM salary s
        JOIN employee e ON s.employee_id = e.employee_id
        LEFT JOIN department d ON e.department_id = d.department_id
        ORDER BY total_compensation DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_all_departments():
    """Get all departments with employee count."""
    conn = get_connection()
    query = """
        SELECT 
            d.department_id,
            d.department_name,
            d.location,
            COUNT(e.employee_id) AS employee_count
        FROM department d
        LEFT JOIN employee e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name, d.location
        ORDER BY employee_count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_department_salary_stats():
    """Get salary statistics by department."""
    conn = get_connection()
    query = """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) AS employee_count,
            ROUND(AVG(s.base_salary + s.bonus), 2) AS avg_total_compensation,
            ROUND(SUM(s.base_salary + s.bonus), 2) AS total_compensation,
            ROUND(MIN(s.base_salary + s.bonus), 2) AS min_compensation,
            ROUND(MAX(s.base_salary + s.bonus), 2) AS max_compensation
        FROM department d
        LEFT JOIN employee e ON d.department_id = e.department_id
        LEFT JOIN salary s ON e.employee_id = s.employee_id
        GROUP BY d.department_name
        ORDER BY avg_total_compensation DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_employee_by_id(employee_id):
    """Get detailed information for a specific employee."""
    conn = get_connection()
    query = """
        SELECT 
            e.employee_id,
            e.first_name,
            e.last_name,
            e.email,
            e.hire_date,
            d.department_name,
            d.location,
            s.base_salary,
            s.bonus,
            s.base_salary + s.bonus AS total_compensation
        FROM employee e
        LEFT JOIN department d ON e.department_id = d.department_id
        LEFT JOIN salary s ON e.employee_id = s.employee_id
        WHERE e.employee_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(employee_id,))
    conn.close()
    return df

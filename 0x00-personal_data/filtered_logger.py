#!/usr/bin/env python3
"""
This module provides a function that returns the log message obfuscated
"""
import re
import logging
from typing import List, Tuple
import mysql.connector
from mysql.connector.connection import MySQLConnection
import os
import logging

# Define a list of fields considered PII (Personally Identifiable Information)
PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """
    REDACTION = '***'
    FORMAT = '[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s'
    SEPARATOR = ';'

    def __init__(self, fields: List[str]):
        """Constructor method

        Args:
            fields (List[str]): a list of fields
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format method

        Args:
            record (logging.LogRecord): a record object

        Returns:
            str: a formatted string
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated

    Args:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field will be
                        obfuscated
        message (str): a string representing the log line
        separator (str): a string representing by which character is separating
                    all fields
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Get logger method

    Returns:
        logging.Logger: a logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create and configure stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    # Add stream handler to logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Get a connection object to the database

    Returns:
        mysql.connector.connection.MySQLConnection: A connection to the
        MySQL database

    """
    # Retrieve environment variables for database connection
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database using the retrieved credentials
    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    Obtains a database connection using get_db(), retrieves all rows
    in the users table, and displays each row under a filtered format
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='[HOLBERTON] user_data INFO %(asctime)s: %(message)s'
        )
    logger = logging.getLogger('user_data')

    # Get database connection
    db_conn = get_db()
    cursor = db_conn.cursor(dictionary=True)

    # Execute query to fetch all rows from users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Log each row in the users table
    for row in rows:
        filtered_data = {field: "***" if field in PII_FIELDS else
                         row[field] for field in row}
        log_message = "; ".join([f"{key}={value}" for
                                 key, value in filtered_data.items()])
        logger.info(log_message)

    # Clean up
    cursor.close()
    db_conn.close()


if __name__ == '__main__':
    main()

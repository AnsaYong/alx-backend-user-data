#!/usr/bin/env python3
"""
This module provides a function that returns the log message obfuscated
"""
import re


def filter_datum(fields: list[str], redaction: str, message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message

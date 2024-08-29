#!/usr/bin/env python3
"""Module that handles filtering of log"""
from typing import List
import re
import logging
import os
import mysql.connector


regexPattrn = {
        'extract': lambda fld, sep: fr"(?P<field>{'|'.join(fld)})=[^{sep}]*",
        'replace': lambda redact: fr"\g<field>={redact}"
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Getting and return log message obfuscated"""
    extract, replace = (regexPattrn["extract"], regexPattrn["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializing class for RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a LogRecord and conceals designated fields"""
        mssgeFmt = super(RedactingFormatter, self).format(record)
        mssgeRedact = filter_datum(self.fields,  self.REDACTION,
                                   mssgeFmt, self.SEPARATOR)
        return mssgeRedact


def get_logger() -> logging.Logger:
    """Creating and configure user data's logger specifically"""
    loggerUserData = logging.getLogger("user_data")
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    loggerUserData.setLevel(logging.INFO)
    loggerUserData.propagate = False
    loggerUserData.addHandler(streamHandler)
    return loggerUserData


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Getting and return database connector"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pword = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    conct = mysql.connector.connection.MySQLConnection(
            user=db_user,
            password=db_pword,
            host=db_host,
            database=db_name
    )
    return connct

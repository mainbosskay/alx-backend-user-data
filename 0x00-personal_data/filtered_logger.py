#!/usr/bin/env python3
"""Module that handles filtering of log"""
from typing import List
import re


regexPattrn = {
        'extract': lambda fld, sep: fr"(?P<field>{'|'.join(fld)})=[^{sep}]",
        'replace': lambda redact: fr"\g<field>={redact}"
}


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Getting and return log message obfuscated"""
    extract, replace = (regexPattrn["extract"], regexPattrn["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)

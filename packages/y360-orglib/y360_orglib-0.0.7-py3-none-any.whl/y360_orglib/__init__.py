
"""
    Y360 Org Library - Library for interacting with Y360 APIs.
"""

__version__ = "0.1.0"

from y360_orglib.logging.config import configure_logger
from y360_orglib.service_app import ServiceAppClient
from y360_orglib.common.exceptions import ServiceAppError, DirectoryClientError, DiskClientError, MailAuditError
from y360_orglib.directory.directory_client import DirectoryClient
from y360_orglib.disk.disk_client import DiskClient
from y360_orglib.audit.audit_mail import AuditMail


__all__ = [
    'DirectoryClient',
    'ServiceAppClient',
    'DirectoryClientError',
    'ServiceAppError',
    'DiskClientError',
    'MailAuditError',
    'DiskClient',
    'AuditMail',
    'configure_logger'
    ]

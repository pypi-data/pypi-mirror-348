__all__ = [
    "add_secret",
    "remove_secret",
    "UseLoggingRedactor",
    "LogRedactorMessage",
]
import contextlib
import logging

__SECRETS__ = set()

_called_from_test = False


def add_secret(secret: str) -> None:
    """Adds a secret that should not be logged

    :param secret: Secret to be added
    """
    global __SECRETS__
    __SECRETS__.add(secret)


def remove_secret(secret: str) -> None:
    """Removes a secret that can now be logged

    :param secret: Secret to be removed
    """
    global __SECRETS__
    with contextlib.suppress(KeyError):
        __SECRETS__.remove(secret)


def reset_secrets() -> None:
    if _called_from_test:
        __SECRETS__.clear()
    else:
        raise RuntimeError("Secret reset not called")


class UseLoggingRedactor:
    """Context manager that generates loggers that utilize redaction"""

    def __enter__(self):
        self.previous_log_default = logging.getLoggerClass()
        logging.setLoggerClass(LoggingRedactor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLoggerClass(self.previous_log_default)
        return True


class LogRedactorMessage:
    """Context manager that forces redacted messages"""

    def __enter__(self):
        self.previous_logrecord_default = logging.getLogRecordFactory()
        logging.setLogRecordFactory(LoggingRedactorRecord)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.setLogRecordFactory(self.previous_logrecord_default)
        return True


class LoggingRedactor(logging.Logger):
    """Removes secrets from the logs"""

    def makeRecord(self, *args, **kwargs) -> logging.LogRecord:
        with LogRedactorMessage():
            return super().makeRecord(*args, **kwargs)


class LoggingRedactorRecord(logging.LogRecord):
    """Filters out secrets"""

    def getMessage(self):
        msg = super().getMessage()
        global __SECRETS__
        for secret in __SECRETS__:
            if len(secret) < 10:
                replacement = "*****"
            else:
                replacement = f"{secret[0:2]}***{secret[-2:]}"
            msg = msg.replace(secret, replacement)
        return msg

import logging

import pytest

from securelogging import (
    LogRedactorMessage,
    UseLoggingRedactor,
    add_secret,
    remove_secret,
    reset_secrets,
)


@pytest.fixture(scope="function", autouse=True)
def test_cleanup(request):
    reset_secrets()
    yield
    reset_secrets()


@pytest.mark.parametrize(
    "secret, log_msg, expected_msg",
    [
        (
            "",
            "Whoa, that's a pretty cool redactor!",
            "Whoa, that's a pretty cool redactor!",
        ),
        (
            "cool",
            "Whoa, that's a pretty cool redactor!",
            "Whoa, that's a pretty ***** redactor!",
        ),
        (
            "need-a-longer-secret-to-hide",
            "thats a need-a-longer-secret-to-hide",
            "thats a ne***de",
        ),
    ],
)
def test_LogRedactorMessage(secret, log_msg, expected_msg, caplog):
    logger = logging.getLogger()
    if secret:
        add_secret(secret)
    with LogRedactorMessage():
        logger.warning(log_msg)
    assert expected_msg in caplog.text


def test_remove_secret(caplog):
    logger = logging.getLogger()
    add_secret("secret")
    with LogRedactorMessage():
        logger.warning("secret")
    assert "*****" in caplog.text
    remove_secret("secret")
    caplog.clear()
    with LogRedactorMessage():
        logger.warning("secret")
    assert "secret" in caplog.text


def test_remove_secret_outofscope():
    import securelogging

    securelogging._called_from_test = False
    with pytest.raises(RuntimeError):
        reset_secrets()
    securelogging._called_from_test = True


def test_UseLoggingRedactor(caplog, capsys):
    key = "JHKLASDJKQWEBBNMASDHJK:LGHJKWQE"
    add_secret(key)
    with UseLoggingRedactor():
        logger_bb = logging.getLogger("beans.beans")

    sh_bb = logging.StreamHandler()
    sh_bb.setFormatter(logging.Formatter("beanbean - %(message)s"))
    logger_bb.addHandler(sh_bb)

    logger_b = logging.getLogger("beans")
    sh_b = logging.StreamHandler()
    sh_b.setFormatter(logging.Formatter("bean - %(message)s"))
    logger_b.addHandler(sh_b)

    logger_bb.warning("Assigned key: %s", key)
    assert key not in caplog.text
    msgs = [x for x in capsys.readouterr().err.splitlines()]
    assert "beanbean - Assigned key: JH***QE" in msgs
    assert "bean - Assigned key: JH***QE" in msgs

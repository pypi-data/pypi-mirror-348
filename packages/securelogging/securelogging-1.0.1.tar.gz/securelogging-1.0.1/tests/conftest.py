import securelogging


def pytest_configure(config):
    securelogging._called_from_test = True

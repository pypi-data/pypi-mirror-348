.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/Expl0dingBanana/securelogging.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/Expl0dingBanana/securelogging
    .. image:: https://readthedocs.org/projects/securelogging/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://securelogging.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/Expl0dingBanana/securelogging/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/Expl0dingBanana/securelogging
    .. image:: https://img.shields.io/pypi/v/securelogging.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/securelogging/
    .. image:: https://img.shields.io/conda/vn/conda-forge/securelogging.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/securelogging
    .. image:: https://pepy.tech/badge/securelogging/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/securelogging
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/securelogging

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=============
securelogging
=============


    Remove secrets from logging


This project enables redaction in logs based on a global set of secrets. These
secrets are managed by `add_secret` and `remove_secret`.

In this example, we have a key that we want to have a key redacted from the log.
To accomplish this, we need to define the key and add it to secret. When
we generate our logger, we do it within ``UseLoggingRedactor``. When
the message is logged, it will appear as `beanbean - Assigned key: JH***QE`

.. code-block::python

   from securelogging import add_secret, UseLoggingRedactor
   import logging


   key = "JHKLASDJKQWEBBNMASDHJK:LGHJKWQE"
   add_secret(key)
   with UseLoggingRedactor():
       logger_bb = logging.getLogger("beans.beans")

   sh_bb = logging.StreamHandler()
   sh_bb.setFormatter(logging.Formatter("beanbean - %(message)s"))
   logger_bb.addHandler(sh_bb)

   logger_bb.warning("Assigned key: %s", key)


Since the log record is modified, propagation still occurs as expected,
but will do so with the redacted message. The output of this will be

.. code-block::

   beanbean - Assigned key: JH***QE
   bean - Assigned key: JH***QE


.. code-block::python

   from securelogging import add_secret, UseLoggingRedactor
   import logging


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


You can also redact a single message. This could be useful if you normally
do not want something redacted, but in specific use-cases you need it to be
redacted. The output of this will be

.. code-block::

   Assigned non-redacted key: JHKLASDJKQWEBBNMASDHJK:LGHJKWQE
   Assigned non-redacted key: JH***QE


.. code-block::python

   from securelogging import add_secret, LogRedactorMessage
   import logging

   key = "JHKLASDJKQWEBBNMASDHJK:LGHJKWQE"
   add_secret(key)
   logger_bb = logging.getLogger("beans.beans")
   logger_bb.warning("Assigned non-redacted key: %s", key)

   with LogRedactorMessage():
       logger_bb.warning("Assigned non-redacted key: %s", key)



.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.

# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

try:
    from trytond.modules.electronic_signature.tests.test_module import suite
except ImportError:
    from .test_module import suite

__all__ = ['suite']

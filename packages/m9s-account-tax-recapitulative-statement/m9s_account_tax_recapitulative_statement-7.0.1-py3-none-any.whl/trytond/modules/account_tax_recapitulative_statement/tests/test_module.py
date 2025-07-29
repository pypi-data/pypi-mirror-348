# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.tests.test_tryton import ModuleTestCase


class AccountTaxRecapitulativeStatementTestCase(ModuleTestCase):
    "Test Account Tax Recapitulative Statement module"
    module = 'account_tax_recapitulative_statement'


del ModuleTestCase

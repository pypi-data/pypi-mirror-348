# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.i18n import gettext
from trytond.pool import PoolMeta

from .exceptions import CodeMissingError


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def _compute_taxes(self):
        tax_lines = super(InvoiceLine, self)._compute_taxes()
        for line in tax_lines:
            if line.tax.vat_code_required:
                party = self.party or self.invoice.party
                tax_identifier = party.tax_identifier
                if not tax_identifier:
                    raise CodeMissingError(gettext(
                            'account_tax_recapitulative_statement.'
                            'missing_party_vat_code',
                            party=party.rec_name))
                line.vat_code = tax_identifier.code
        return tax_lines


class InvoiceTax(metaclass=PoolMeta):
    __name__ = 'account.invoice.tax'

    def get_move_line(self):
        line = super(InvoiceTax, self).get_move_line()
        if self.tax_code and self.tax.vat_code_required:
            tax_line = line[0].tax_lines[0]
            party = self.invoice.party
            tax_identifier = party.tax_identifier
            if not tax_identifier:
                raise CodeMissingError(gettext(
                        'account_tax_recapitulative_statement.'
                        'missing_party_vat_code',
                        party=party.rec_name))
            tax_line.vat_code = tax_identifier.code
        return line

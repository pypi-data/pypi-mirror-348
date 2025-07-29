# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.exceptions import UserError
from trytond.model.exceptions import ValidationError


class CodeMissingError(UserError):
    pass


class PartyMissingError(UserError):
    pass


class CodeValidationError(ValidationError):
    pass

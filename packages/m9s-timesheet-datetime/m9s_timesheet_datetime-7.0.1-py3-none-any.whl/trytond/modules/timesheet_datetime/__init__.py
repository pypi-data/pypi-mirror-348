# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import timesheet

__all__ = ['register']


def register():
    Pool.register(
        timesheet.Line,
        module='timesheet_datetime', type_='model')

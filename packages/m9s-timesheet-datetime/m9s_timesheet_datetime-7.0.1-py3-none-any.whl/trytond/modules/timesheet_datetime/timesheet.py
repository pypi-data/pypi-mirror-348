# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class Line(metaclass=PoolMeta):
    __name__ = 'timesheet.line'

    start_time = fields.DateTime('Start Date', format='%H:%M')
    end_time = fields.DateTime('End Date', format='%H:%M')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        #  we want to order primarily by start_time and id
        #  timesheet passes [('date', 'DESC'), ('id', 'DESC')]
        cls._order.insert(0, ('start_time', 'DESC NULLS LAST'))

    @staticmethod
    def default_start_time():
        now = datetime.datetime.now()
        return now.replace(second=0, microsecond=0)

    @staticmethod
    def default_end_time():
        now = datetime.datetime.now()
        return now.replace(second=0, microsecond=0)

    @fields.depends('duration', 'start_time', 'end_time')
    def on_change_with_duration(self, name=None):
        if not self.duration and (self.start_time and self.end_time):
            td = self.end_time - self.start_time
            # format as minutes without seconds
            minutes = round(td.total_seconds() / 60)
            return datetime.timedelta(minutes=minutes)
        else:
            return self.duration

    @fields.depends('start_time')
    def on_change_with_date(self, name=None):
        Date = Pool().get('ir.date')
        if self.start_time:
            return self.start_time.date()
        return Transaction().context.get('date') or Date.today()

    @fields.depends('start_time', 'end_time', 'duration')
    def on_change_duration(self):
        if self.end_time and self.duration:
            self.start_time = self.end_time - self.duration
        elif self.start_time and self.duration:
            self.end_time = self.start_time + self.duration

    @fields.depends('start_time', 'end_time')
    def update_duration(self):
        if self.start_time and self.end_time:
            if self.end_time < self.start_time:
                self.end_time = self.start_time
            self.duration = self.end_time - self.start_time

    @fields.depends(methods=['update_duration'])
    def on_change_start_time(self):
        self.update_duration()

    @fields.depends(methods=['update_duration'])
    def on_change_end_time(self):
        self.update_duration()

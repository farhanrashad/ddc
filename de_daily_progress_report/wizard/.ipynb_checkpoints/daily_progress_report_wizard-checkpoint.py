# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class ProgressReportWizard(models.TransientModel):
    _name = 'progress.report.wizard'

    date = fields.Date(string="Set Date")

    def progress_report(self):
        data = {}
        data['form'] = self.read(['date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date',])[0])
        return self.env.ref('de_daily_progress_report.daily_progress_report_id').with_context(landscape=True).report_action(
            self, data=data, config=False)
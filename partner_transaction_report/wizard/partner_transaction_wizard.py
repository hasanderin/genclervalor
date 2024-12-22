from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PartnerTransactionWizard(models.TransientModel): 
    _name = "partner.transaction.wizard"
    _description = "Partner Transaction Report Wizard"

    partner_ids = fields.Many2many('res.partner', string='Cariler')

    def _prepare_report_data(self):
        self.ensure_one()
        query = """
            SELECT
                p.id as partner_id,
                p.name as partner_name,
                COALESCE(p.mobile, p.phone) as partner_phone,
                to_timestamp(SUM(EXTRACT(EPOCH FROM aml.date) * aml.debit) / NULLIF(SUM(aml.debit), 0))::date as avg_debit_date,
                to_timestamp(SUM(EXTRACT(EPOCH FROM aml.date) * aml.credit) /NULLIF(SUM(aml.credit), 0))::date as avg_credit_date,
                CURRENT_DATE - to_timestamp(
                        (
                            SUM(EXTRACT(EPOCH FROM aml.date) * aml.debit) -
                            SUM(EXTRACT(EPOCH FROM aml.date) * aml.credit)
                        ) / NULLIF(SUM(aml.balance), 0))::date as days_since_avg_transaction,
                SUM(aml.debit) as net_debit,
                SUM(aml.credit) as net_credit,
                SUM(aml.balance) as net_balance
            FROM account_move_line aml
            JOIN res_partner p ON p.id = aml.partner_id
            JOIN account_account a ON a.id = aml.account_id
            JOIN account_move am ON am.id = aml.move_id
            WHERE aml.parent_state = 'posted'
                AND aml.balance != 0
                AND a.internal_type in ('receivable', 'payable')
                AND am.closing_type not in ('opening', 'closing')
        """

        params = []
        if self.partner_ids:
            query += " AND p.id IN %s"
            params.append(tuple(self.partner_ids.ids))

        query += """
            GROUP BY p.id, p.name, p.mobile, p.phone
            HAVING SUM(ABS(aml.balance)) != 0
        """

        self.env.cr.execute(query, params)
        return self.env.cr.dictfetchall()

    def print_xlsx_report(self):
        self.ensure_one()
        data = {
            'report_data': self._prepare_report_data(),
            'partner_ids': self.partner_ids.ids if self.partner_ids else [],
            'report_title': 'Seçili Cariler' if self.partner_ids else 'Tüm Cariler',
        }
        return self.env.ref('partner_transaction_report.partner_transaction_xlsx').report_action(self, data=data)

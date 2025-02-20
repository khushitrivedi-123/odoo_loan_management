from odoo import models, api, fields
from odoo.exceptions import ValidationError


class LoanInstallment(models.Model):
    _name = 'loan.installment'
    _description = 'Loan Installment'

    loan_id = fields.Many2one('loan.loan', string="Loan Reference", ondelete='cascade')
    principle_amount = fields.Float(string="Principle Amount")
    interest_amount = fields.Float(string="Interest Amount")
    amount = fields.Float(string="Amount")
    remaining_amount = fields.Float(string="Remaining Amount")
    due_date = fields.Date(string="Due Date")
    amount_paid = fields.Float(string="Amount Paid")
    payment_ref = fields.Char(string="Payment Ref")
    payment_date = fields.Date(string="Payment Date")
    status = fields.Selection(
            [("paid", "Paid"), ("unpaid", "Unpaid")],
            default="unpaid"
        )

    def action_open_payment_form(self):
        existing_payment = self.env['account.payment'].search([
            ('ref', '=', self.payment_ref)
        ], limit=1)

        if self.status == 'paid':
            return {
                'type': 'ir.actions.act_window',
                'name': 'Account Payment',
                'res_model': 'account.payment',
                'res_id': existing_payment.id,
                'view_mode': 'form',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Account Payment',
                'res_model': 'account.payment',
                'view_mode': 'form',
                'context': {
                    'default_partner_id': self.loan_id.inquiry_id.partner_id.id,
                    'default_amount': self.amount,
                    'default_loan_installment_id': self.id,
                    'default_installment_amount':self.amount
                }
            }

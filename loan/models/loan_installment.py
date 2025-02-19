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

    def action_open_payment_form(self):
        partner = self.env['res.partner'].search([('customer_rank', '>', 0)], limit=1)

        if not partner:
            raise ValidationError("No valid customer found. Please create a customer first.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Account Payment',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.loan_id.inquiry_id.partner_id.id,
                'default_amount': self.remaining_amount,
                'default_loan_installment_id': self.id,
                'default_installment_amount':self.amount
            }
        }

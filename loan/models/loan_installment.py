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
            'name': 'Loan Payment',
            'res_model': 'loan.payment',
            'view_mode': 'form',
            'view_id': self.env.ref('your_module.view_loan_payment_form').id,
            'target': 'new',
            'context': {
                'default_partner_id': partner.id,
                'default_installment_id': self.id,
                'default_amount': self.remaining_amount,
            }
        }

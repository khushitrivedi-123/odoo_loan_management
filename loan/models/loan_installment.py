from odoo import models, api, fields

class LoanInstallment(models.Model):
    _name = "loan.installment"
    _description = "Installment"

    s_no = fields.Char("S No.", required=True)
    principle_amount = fields.Float("Principle Amount", required=True)
    interest_amount = fields.Float("Interest Amount")
    amount_due = fields.Float("Amount Due")
    remaining_amount = fields.Float("Remaining Amount")
    payment_date = fields.Date("Payment Date")
    loan_id = fields.Many2one('loan.loan', 'Loan')
from odoo import models, fields, api
from odoo.exceptions import UserError

class CustomAccountPayment(models.Model):
    _inherit = "account.payment"

    loan_installment_id = fields.Many2one('loan.installment', string="Loan Installment")
    installment_amount = fields.Float()

    @api.model
    def create(self, vals):
        loan_installment_id = self.env.context.get('default_loan_installment_id')

        if not loan_installment_id:
            print("loan_installment_id is missing in vals and context!")

        else:
            loan_installment = self.env['loan.installment'].browse(loan_installment_id)
            client_id = loan_installment.loan_id.loan_id
            sequence = self.env['ir.sequence'].next_by_code('account.payment.ref') or 'new'
            vals['ref'] = f'{client_id}{sequence}'

        payment = super(CustomAccountPayment, self).create(vals)
        if payment.installment_amount > 0.00:
            amount = payment.amount
            installment_amount = payment.installment_amount
            if installment_amount != amount:
                raise UserError(
                    f"Invalid amount!\n"
                    f"Exact remaining amount for this installment is {installment_amount}.\n"
                    "To make a custom payment, please click on the Custom Payments button on the loan form."
                )

            if payment.loan_installment_id:
                payment.loan_installment_id.payment_ref = payment.ref
                payment.loan_installment_id.amount_paid = payment.amount
                payment.loan_installment_id.payment_date = payment.date
                payment.loan_installment_id.status = 'paid'
        return payment

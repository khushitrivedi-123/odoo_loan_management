from odoo import models, fields, api
from odoo.exceptions import UserError

class CustomAccountPayment(models.Model):
    _inherit = "account.payment"

    loan_installment_id = fields.Many2one('loan.installment', string="Loan Installment")
    installment_amount = fields.Float()

    @api.model
    def create(self, vals):
        payment = super(CustomAccountPayment, self).create(vals)
        amount = payment.amount
        installment_amount = payment.installment_amount
        if installment_amount != amount:
            print("--------------------",payment.installment_amount,"----------------------",amount)

            raise UserError(
                f"Invalid amount!\n"
                f"Exact remaining amount for this installment is {installment_amount}.\n"
                "To make a custom payment, please click on the Custom Payments button on the loan form."
            )

        if payment.loan_installment_id:
            payment.loan_installment_id.payment_ref = payment.ref
            payment.loan_installment_id.payment_date = payment.date
        return payment



        #loan_id = vals.get(" self.loan_id.inquiry_id.partner_id.id,")

        # loan_prefix = f"{loan_id}/INSTLMT"
        # if "ref" not in vals or not vals["ref"]:  # Set ref only if it's empty
        #     sequence_number = self.env["ir.sequence"].next_by_code("memo.sequence.data") or "New"
        #     vals["ref"] = f"{loan_prefix}{sequence_number}"
        # return super(CustomAccountPayment, self).create(vals)




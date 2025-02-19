import re
from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import models, api, fields
from odoo.exceptions import ValidationError


class LoanLoan(models.Model):
    _name = "loan.loan"
    _description = "Loan"


    loan_id = fields.Char("Loan ID", requied=True, readonly=True)
    inquiry_id = fields.Many2one("loan.inquiry", "Name", required=True)
    email = fields.Char("Email", compute="_compute_email", required=True)
    mobile_no = fields.Char("Mobile No.", required=True)
    city = fields.Char("City", required=True)
    state = fields.Selection([("gujarat","Gujarat"),("maharashtra","Maharashtra"),("delhi", "Delhi")], string="State", required=True)
    pincode = fields.Char(string="Pincode", required=True)
    status = fields.Selection(
        [("running", "Running"), ("closed", "Closed")],
        default="running",
        tracking=True
    )
    principle_amount = fields.Float("Principle Amount", required=True)
    rate = fields.Float("Rate", required=True)
    interest_amount = fields.Float("Interest Amount", compute="_compute_interest_amount", required=True, readonly=True)
    loan_amount = fields.Float("Loan Amount", required=False, readonly=True)
    no_of_installments = fields.Integer("No. of Installments",required=True)
    gap = fields.Integer("Gap (In months)")
    custom_payments = fields.Boolean("Custom Payments?")
    starting_date = fields.Date("Starting date",default=lambda *a: date.today(), required=True)
    closing_date = fields.Date("Closing Date", compute="_compute_closing_date", readonly=True)
    loan_description = fields.Char("Loan Description")
    principle_entries = fields.Boolean("Need Interest/Principle Entries?")

    journal_id = fields.Many2one('account.journal', string="Journal")
    asset_account_id = fields.Many2one('account.account', string="Asset Account (Current)")
    interest_expense_account_id = fields.Many2one('account.account', string="Interest Account (Expense)")
    interest_payable_account_id = fields.Many2one('account.account', string="Interest Account (Payable)")

    installment_ids = fields.One2many('loan.installment', 'loan_id', string="Installments")
    computed_message = fields.Text(string="Info Message", default="Click on Compute Installments to create installment lines.", readonly= True)

    @api.constrains("mobile_no", "email")
    def validate_constraints(self):

        # Validate mobile number
        pattern_mobile = r"^\d{10}$"
        if not re.match(pattern_mobile, self.mobile_no):
            raise ValidationError("Invalid mobile number. Please enter a 10-digit number.")

        # Validate email
        pattern_email = r'^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,4}$'
        if not re.match(pattern_email, self.email):
            raise ValidationError("Invalid email. Please enter a correct email address.")

    @api.model
    def create(self, vals):
        if not vals.get("loan_id"):
            vals["loan_id"] = self.env["ir.sequence"].next_by_code("loan.sequence.data") or "New"
        return super(LoanLoan, self).create(vals)

    @api.depends("inquiry_id")
    def _compute_email(self):
        for record in self:
            record.email = record.inquiry_id.email
            record.city = record.inquiry_id.city
            record.mobile_no = record.inquiry_id.phone_number
            record.state = record.inquiry_id.state
            record.pincode = record.inquiry_id.pincode

    @api.depends("starting_date", "no_of_installments", "gap")
    def _compute_closing_date(self):
        for record in self:
            if record.starting_date and record.no_of_installments and record.gap:
                record.closing_date = record.starting_date + relativedelta(
                    months=(record.no_of_installments * record.gap)+1)
            else:
                record.closing_date = False

    @api.depends("principle_amount", "rate")
    def _compute_interest_amount(self):
        for record in self:
            if record.principle_amount and record.rate:
                record.interest_amount = (record.principle_amount * record.rate) / 100
                record.loan_amount = record.principle_amount + record.interest_amount
            else:
                record.interest_amount = 0.0  # Default to zero if values are missing

    def action_custom_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Custom Payment',
            'res_model': 'custom.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_loan_id': self.id},
        }

    def action_principle_entries(self):
        # Your logic for Principle Entries
        pass

    def action_interest_entries(self):
        # Your logic for Interest Entries
        pass

    def action_compute_installments(self):
        for record in self:
            record.computed_message = "Installments computed successfully!"

    def action_closed(self):
        for record in self:
            record.status = 'closed'

    def action_running(self):
        for record in self:
            record.status = 'running'

        def action_submit(self):
        print("action submit")

        self.env['loan.installment'].search([('loan_id', '=', self.id)]).unlink()  # Remove existing installments

        principle_per_installment = self.principle_amount / self.no_of_installments
        interest_per_installment = (self.principle_amount * self.rate / 100) / self.no_of_installments
        total_per_installment = principle_per_installment + interest_per_installment
        remaining_amount = self.loan_amount
        current_due_date = self.starting_date

        for i in range(1, self.no_of_installments + 1):
            remaining_amount -= total_per_installment
            self.env['loan.installment'].create({
                'loan_id': self.id,
                'sr_no': i,
                'principle_amount': principle_per_installment,
                'interest_amount': interest_per_installment,
                'amount': total_per_installment,
                'remaining_amount': remaining_amount,
                'due_date': current_due_date,
            })
            current_due_date += timedelta(days=30 * self.gap)  # Move to next due date


    def action_get_document(self):
        print("print documents")

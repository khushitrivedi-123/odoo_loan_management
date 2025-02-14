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
    status = fields.Selection(
        [("running", "Running"), ("closed", "Closed")],
        default="running",
        tracking=True
    )
    principle_amount = fields.Float("Principle Amount", required=True)
    rate = fields.Float("Rate", required=True)
    interest_amount = fields.Float("Interest Amount", compute="_compute_interest_amount", required=True, readonly=True)
    loan_amount = fields.Float("Loan Amount", required=True, readonly=True)
    no_of_installments = fields.Integer("No. of Installments",required=True)
    gap = fields.Integer("Gap (In months)")
    custom_payments = fields.Boolean("Custom Payments?")
    starting_date = fields.Date("Starting date",default=lambda *a: date.today(), required=True)
    closing_date = fields.Date("Closing Date", compute="_compute_closing_date", readonly=True)
    loan_description = fields.Char("Loan Description")
    principle_entries = fields.Boolean("Need Interest/Principle Entries?")

    journal = fields.Char("Journal")
    asset_account = fields.Char("Asset Account")
    interest_account = fields.Char("Interest Account")

    installment_ids = fields.One2many("loan.installment", "loan_id", string="Child Installmemt")
    computed_message = fields.Text(string="Info Message", default="Click on Compute Installments to create installment lines.", readonly= True)

    @api.constrains("name", "mobile_no", "email")
    def validate_constraints(self):
        # Validate name
        pattern_name = r"^[a-zA-Z ]{2,}$"
        if not re.match(pattern_name, self.name):
            raise ValidationError("Invalid name. Name should not contain numbers or special characters.")

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
        vals["loan_id"] = (
                self.env["ir.sequence"].sudo().next_by_code("loan.sequence.data") or "New"
        )
        return super(LoanLoan, self).create(vals)

    @api.depends("inquiry_id")
    def _compute_email(self):
        for record in self:
            record.email = record.inquiry_id.email
            record.city = record.inquiry_id.city
            record.mobile_no = record.inquiry_id.phone_number


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

    def action_get_document(self):
        print("print documents")
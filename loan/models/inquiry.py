import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LoanInquiry(models.Model):
    _name = "loan.inquiry"
    _description = "Loan Inquiry"
    _rec_name = "client_name"
    _inherits = {"res.users": "u_id"}

    u_id = fields.Many2one(
        "res.users", required=True, ondelete="restrict", auto_join=True
    )
    client_name = fields.Char(string="Client Name", required=True)
    email = fields.Char(string="Email", required=True)
    phone_number = fields.Char(string="Phone Number", required=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender", required=True)
    city = fields.Selection([("ahmedabad","Ahmedabad"),("mumbai", "Mumbai"),("delhi", "Delhi")], string="City", required=True)
    state = fields.Selection([("gujarat","Gujarat"),("maharashtra","Maharashtra"),("delhi", "Delhi")], string="State", required=True)
    pincode = fields.Char(string="Pincode", required=True)
    status = fields.Selection(
        [("draft", "Draft"), ("approve", "approve"), ("reject", "Reject")],
        default="draft",
        tracking=True
    )

    @api.constrains("email")
    def _check_email_format(self):
        for client in self:
            if client.email:
                email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if not re.match(email_regex, client.email):
                    raise (ValidationError("The email address is not in a valid format."))

    @api.constrains("phone_number")
    def _check_phone_number(self):
        for client in self:
            if client.phone_number:
                phone_regex = r"^\d{10}$"
                if not re.match(phone_regex, client.phone_number):
                    raise ValidationError("Phone number must contain exactly 10 digits.")

    @api.constrains("pincode")
    def _check_pincode(self):
        for client in self:
            if client.pincode:
                pincode_regex = r"^\d{6}$"  # Ensures exactly 6 digits
                if not re.match(pincode_regex, client.pincode):
                    raise ValidationError("Pincode must contain exactly 6 digits.")
    @api.model
    def create(self, vals):
        vals['name'] = vals.get("client_name")
        vals['login'] = vals.get("email")
        user = super(LoanInquiry, self).create(vals)
        return user

    def action_approve(self):
        for record in self:
            record.status = 'approve'

    def action_reject(self):
        for record in self:
            record.status = 'reject'

    def action_draft(self):
        for record in self:
            record.status = 'draft'


import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LoanInquiry(models.Model):
    _name = "loan.inquiry"
    _description = "Loan Inquiry"
    _rec_name = "client_name"

    client_name = fields.Char(string="Client Name", required=True)
    email = fields.Char(string="Email", required=True)
    phone_number = fields.Char(string="Phone Number", required=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender", required=True)
    city = fields.Selection([("ahmedabad","Ahmedabad"),("mumbai", "Mumbai"),("delhi", "Delhi")], string="City", required=True)

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

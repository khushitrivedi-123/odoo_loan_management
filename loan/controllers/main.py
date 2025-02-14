from odoo import http
from odoo.http import request

class LoanInquiryController(http.Controller):

    @http.route('/loan/inquiry', type='http', auth="public", website=True)
    def loan_inquiry_form(self):
        return request.render("loan_management.loan_inquiry_template", {})

    @http.route('/loan/inquiry/submit', type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def submit_loan_inquiry(self, **post):
        if post:
            inquiry = request.env['loan.inquiry'].sudo().create({
                'client_name': post.get('client_name'),
                'email': post.get('email'),
                'phone_number': post.get('phone_number'),
                'gender': post.get('gender'),
                'city': post.get('city'),
            })

            template = request.env.ref('loan_management.email_template_loan_inquiry')
            if template:
                template.sudo().send_mail(inquiry.id, force_send=True)
        return request.render("loan_management.inquiry_success", {})

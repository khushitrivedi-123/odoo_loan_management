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
                'state': post.get('state'),
                'pincode': post.get('pincode'),
            })

            template = request.env.ref('loan_management.email_template_loan_inquiry')
            if template:
                template.sudo().send_mail(inquiry.id, force_send=True)
        return request.render("loan_management.inquiry_success", {})
        
     @http.route('/loan/select/<int:inquiry_id>', type='http', auth="public", website=True)
     def select_loan_type_page(self, inquiry_id):
         inquiry = request.env['loan.inquiry'].sudo().browse(inquiry_id)
         if not inquiry.exists():
             return request.render("website.404")
            return request.render("loan_management.loan_type_selection", {'inquiry_id': inquiry_id})

     @http.route('/loan/select/<int:inquiry_id>/confirm', type='http', auth="public", website=True)
     def confirm_loan_type(self, inquiry_id, **post):
        loan_type = post.get('loan_type')
        inquiry = request.env['loan.inquiry'].sudo().browse(inquiry_id)

        if inquiry.exists() and loan_type in ['personal', 'home', 'vehicle']:
            inquiry.sudo().write({'loan_type': loan_type})
            return request.render("loan_management.loan_selected_success", {})

        return request.render("website.404")

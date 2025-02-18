{
    "name": "Loan Management System",
    "version": "1.0",
    "category": "Accounting",
    "author": "Khushi Trivedi",
    "description": """
    Loan Management System
    This module works for both 'Enterprise' and 'Community'.
    """,
    "license": "LGPL-3",
    "depends": ["base","website","mail","account"],
    "data": [
        "security/ir.model.access.csv",
        "views/loan_menu.xml",
        "views/inquiry_views.xml",
        "views/inquiry_templates.xml",
        "data/templates_email.xml",
        "views/loan_type_selection.xml",
        "views/loan_selected_success.xml",
        "data/ir_sequence_data.xml",
        "views/loan_loan_views.xml",
        "views/loan_installment_views.xml",
        "wizard/custom_payment_views.xml",
    ],
    "installable": True,
    "application": True,

}

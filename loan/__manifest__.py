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
    "depends": ["base","website","mail"],
    "data": [
        "security/loan_security.xml",
        "security/ir.model.access.csv",

        "data/ir_sequence_data.xml",
        "data/templates_email.xml",

        "views/loan_loan_views.xml",
        "views/loan_menu_views.xml",
        "views/inquiry_views.xml",
        "views/inquiry_templates.xml",
        "views/loan_menu_views.xml"

    ],
    "installable": True,
    "application": True,

}
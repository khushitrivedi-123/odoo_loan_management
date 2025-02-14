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
        "security/ir.model.access.csv",
        "views/loan_menu.xml",
        "views/inquiry_views.xml",
        "views/inquiry_templates.xml",
        "data/templates_email.xml",
    ],
    "installable": True,
    "application": True,

}
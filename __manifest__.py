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
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/loan_views.xml",
    ],
    "installable": True,
    "application": True,

}
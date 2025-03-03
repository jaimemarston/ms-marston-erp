{
    "name": """Plan Operativo Anual (POA)""",
    "description": """This module aims to manage the Annual Operating Plan (POA) within
        Odoo 18, allowing:
        ● Define strategic objectives.
        ● Create activities with assigned budgets.
        ● Relate activities to funding sources.
        ● Associate activities with entities (schools, institutions, etc.).
        ● Manage expenses through Analytical Accounts and Accounting Entries.
        ● Generate budget vs. executed expense reports.
    """,
    "version": "1.0",
    'category': 'Accounting/Accounting',
    "depends": [
        'base',
        'web',
        'account',
        'analytic',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/poa_activity.xml',
        'views/poa_budget.xml',
        'views/poa_entity.xml',
        'views/poa_objective.xml',
        'views/poa_plan.xml',
        'views/menu.xml',
    ],
    'license': 'LGPL-3',
}

{
    "name": """ms_render_account_management""",
    "version": "1.0",
    'category': '',
    "depends": ['base','l10n_latam_invoice_document', 'account'],
    'data': [
        "security/ir.model.access.csv",
        'views/requests_management_views.xml',
        'views/request_settings_views.xml',
        'views/menus_views.xml',
    ],
    'license': 'OPL-1',
}

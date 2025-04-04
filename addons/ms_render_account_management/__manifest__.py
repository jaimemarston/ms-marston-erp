{
    "name": """ms_render_account_management""",
    "version": "1.0",
    'category': '',
    "depends": ['web','base','l10n_latam_invoice_document', 'account','ms_account_system'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menus_views.xml',
        'views/requests_management_views.xml',
        'views/requests_contracts_views.xml',
        'views/requests_os_views.xml',
        'views/requests_oc_views.xml',
        'views/requests_to_render_views.xml',
        'views/requests_surrenders_views.xml',
        'views/account_move_views.xml',
        'views/treasury_views.xml',
         'data/product_data.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ms_render_account_management/static/src/js/**/*.*',
        ],
    },
    
    'license': 'OPL-1',
}

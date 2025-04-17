{
    "name": """ms_render_account_management""",
    "version": "1.0",
    'category': '',
    "depends": ['web','base','l10n_latam_invoice_document', 'account', 'om_account_accountant','ms_account_system'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/views_users/group_vb_solicitante_view/ir.model.access.csv',
        'data/product_data.xml',
        'data/ms_request_management_actions.xml',
        'views/requests_management_views.xml',
        'views/requests_contracts_views.xml',
        'views/requests_os_views.xml',
        'views/requests_oc_views.xml',
        'views/requests_to_render_views.xml',
        'views/requests_surrenders_views.xml',
        'views/account_move_views.xml',
        'views/treasury_views.xml',
        'views/travel_request.xml',
        'views/menus_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ms_render_account_management/static/src/js/**/*.*',
        ],
    },
    
    'license': 'OPL-1',
}

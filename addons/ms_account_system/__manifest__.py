{
    'name': 'ms_account_system',
    'version': '2.1',
    'category': 'Tools',
    'summary': 'Modulo Contable',
    'description': """Modulo de Contabilidad Empresarial.
    Incluye todos los modulos necesarios.""",
    'author': 'Marston Software',
    'depends': [
        'base',
        'web',
        'account',
        'contacts',
        'l10n_latam_invoice_document',
        'hr_expense',
        'om_account_accountant'
    ],
    'data': [
        'security/ir.model.access.csv',  # Primero los permisos
        'views/project_plan_views.xml',
        'views/business_plan_views.xml',
        'views/activity_plan_views.xml',
        'views/area_plan_settings_views.xml',
        'views/menu.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}

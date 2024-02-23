{
    "name" : 'Odoo crm custom widget',
    'summery':'Odoo crm custom widget',
    'category':'CRM',
    'sequence':1,
    "version":  "1.0.0",
    'depends' :['crm'] , 
    'data'  :[
        'security/ir.model.access.csv',
        'data/stage_data.xml',
        'views/crm_lead_views.xml',
            ],
    'application' :True,
    "assets": {
        'web.assets_backend': [
            "wk_crm_custom_widget/static/src/**/*",
        ]
    }
}


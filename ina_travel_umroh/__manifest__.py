# -*- coding: utf-8 -*-
{
    "name": "ina_travel_umroh",
    "summary": """
        Module untuk melakukan manajemen travel Umroh
    """,
    "description": """
        Travel Umrah Management
    """,
    "author": "Rifqi Ammar Ramadhan",
    "website": "https://rifqiammarramadhan.xyz/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "product", "sale", "mrp", "mail", "report_xlsx", "stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "report/report_action_view.xml",
        "views/sequence_data_view.xml",
        "views/scheduler_data_view.xml",
        "security/security.xml",
        "views/views.xml",
        "views/partner_view.xml",
        "report/stock_picking_report_view.xml",
        "views/stock_picking_view.xml",
        "views/sale_order_view.xml",
        "views/menuitems_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "aplication": True,
    "installable": True,
}

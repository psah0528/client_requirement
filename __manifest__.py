{
    "name": "Client Requirement",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Manage Client Requirements",
    "author": "Puja",
    "license": "LGPL-3",
    "depends": ["base", "mail","web"],
    "data": [
        "security/ir.model.access.csv",
        "views/client_project_views.xml",
        'report/client_project_export.xml',
    ],
    "application": True,
    "installable": True,
}
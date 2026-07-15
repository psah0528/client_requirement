from odoo import fields, models


class ClientRequirementLine(models.Model):
    _name = "client.requirement.line"
    _description = "Client Requirement Line"
    _order = "sequence,id"

    sequence = fields.Integer(default=10)

    project_id = fields.Many2one(
        "client.project",
        string="Project",
        ondelete="cascade",
        required=True,
    )

    requirement_name = fields.Char(
        string="Requirement",
        required=True,
    )

    module_name = fields.Selection(
        [
            ("sales", "Sales"),
            ("purchase", "Purchase"),
            ("inventory", "Inventory"),
            ("accounting", "Accounting"),
            ("manufacturing", "Manufacturing"),
            ("hr", "HR"),
            ("crm", "CRM"),
            ("project", "Project"),
            ("website", "Website"),
            ("other", "Other"),
        ],
        string="Module",
    )

    priority = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("critical", "Critical"),
        ],
        default="medium",
        string="Priority",
    )

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("analysis", "Analysis"),
            ("development", "Development"),
            ("testing", "Testing"),
            ("done", "Done"),
        ],
        default="draft",
        string="Status",
    )

    assigned_to = fields.Char(
        string="Assigned To"
    )

    description = fields.Text(
        string="Description"
    )
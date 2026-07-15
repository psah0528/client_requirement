from odoo import fields, models


class ClientWorkflowLine(models.Model):
    _name = "client.workflow.line"
    _description = "Client Workflow Line"
    _order = "sequence,id"

    sequence = fields.Integer(default=10)

    project_id = fields.Many2one(
        "client.project",
        string="Project",
        required=True,
        ondelete="cascade",
    )

    step_name = fields.Char(
        string="Step Name",
        required=True,
    )

    responsible = fields.Selection(
        [
            ("sales", "Sales"),
            ("manager", "Manager"),
            ("purchase", "Purchase"),
            ("inventory", "Inventory"),
            ("production", "Production"),
            ("accounts", "Accounts"),
            ("hr", "HR"),
            ("other", "Other"),
        ],
        string="Responsible",
    )

    next_step = fields.Char(
        string="Next Step"
    )

    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("progress", "In Progress"),
            ("done", "Done"),
        ],
        default="pending",
        string="Status",
    )

    notes = fields.Text(
        string="Notes"
    )
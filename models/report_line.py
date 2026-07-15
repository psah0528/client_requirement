from odoo import fields, models


class ClientReportLine(models.Model):
    _name = "client.report.line"
    _description = "Client Report Line"
    _order = "sequence,id"

    sequence = fields.Integer(default=10)

    project_id = fields.Many2one(
        "client.project",
        string="Project",
        required=True,
        ondelete="cascade",
    )

    report_name = fields.Char(
        string="Report Name",
        required=True,
    )

    format = fields.Selection(
        [
            ("pdf", "PDF"),
            ("excel", "Excel"),
            ("csv", "CSV"),
            ("other", "Other"),
        ],
        string="Format",
    )

    priority = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="medium",
        string="Priority",
    )

    required = fields.Boolean(
        string="Required",
        default=True,
    )

    remarks = fields.Text(
        string="Remarks",
    )
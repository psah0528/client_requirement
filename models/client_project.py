from odoo import fields, models


class ClientProject(models.Model):
    _name = "client.project"
    _description = "Client Requirement Project"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "project_name"

    project_name = fields.Char(
        string="Project Name",
        required=True,
        tracking=True,
    )

    client_name = fields.Char(
        string="Client Name",
        tracking=True,
    )

    meeting_date = fields.Date(
        string="Meeting Date"
    )

    developer = fields.Char(
        string="Developer"
    )

    business_type = fields.Selection(
        [
            ("manufacturing", "Manufacturing"),
            ("retail", "Retail"),
            ("restaurant", "Restaurant"),
            ("hospital", "Hospital"),
            ("education", "Education"),
            ("service", "Service"),
            ("other", "Other"),
        ],
        string="Business Type",
    )

    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("discussion", "Discussion"),
            ("analysis", "Analysis"),
            ("development", "Development"),
            ("done", "Done"),
        ],
        default="draft",
        tracking=True,
        string="Status",
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

    current_process = fields.Selection([
    ("excel", "Excel"),
    ("manual", "Manual"),
    ("odoo", "Odoo"),
    ("sap", "SAP"),
    ("other", "Other"),
    ], string="Current Process")

    string="Current Business Process"
    process_description = fields.Text(
    )

    current_problems = fields.Text(
    string="Current Problems"
    )

    expected_solution = fields.Text(
    string="Expected Solution"
    )

    special_rules = fields.Text(
    string="Special Business Rules"
    )

    open_questions = fields.Text(
    string="Open Questions"
    )

    requirement_line_ids = fields.One2many(
    "client.requirement.line",
    "project_id",
    string="Requirements",
    )

    workflow_line_ids = fields.One2many(
    "client.workflow.line",
    "project_id",
    string="Workflow",
    )

    report_line_ids = fields.One2many(
    "client.report.line",
    "project_id",
    string="Reports",
    )

    # reports 
    def action_export_excel(self):
          self.ensure_one()

          return {
        "type": "ir.actions.act_url",
        "url": "/client_requirement/export/%s" % self.id,
        "target": "self",
    }


    # PDF ######################################
    def action_export_pdf(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "/client_requirement/pdf/%s" % self.id,
            "target": "new",
        }
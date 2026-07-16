from odoo import http
from odoo.http import request
import io
import xlsxwriter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch

class ClientRequirementExport(http.Controller):

    @http.route("/client_requirement/export/<int:project_id>", type="http", auth="user")
    def export_excel(self, project_id, **kw):
        project = request.env["client.project"].browse(project_id)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        title = workbook.add_format({"bold": True, "font_size": 14, "align": "center"})
        header = workbook.add_format({"bold": True, "bg_color": "#4472C4", "font_color": "white", "border": 1})
        label = workbook.add_format({"bold": True, "bg_color": "#D9EAD3", "border": 1})
        cell = workbook.add_format({"border": 1})
        wrap = workbook.add_format({"border": 1, "text_wrap": True})

        # Project
        sheet = workbook.add_worksheet("Project")
        sheet.set_column("A:A", 25)
        sheet.set_column("B:B", 45)
        sheet.merge_range("A1:B1", "CLIENT REQUIREMENT", title)
        fields = [
            ("Project Name", project.project_name or ""),
            ("Client Name", project.client_name or ""),
            ("Developer", project.developer or ""),
            ("Meeting Date", str(project.meeting_date or "")),
            ("Business Type", dict(project._fields["business_type"].selection).get(project.business_type, "")),
            ("Priority", project.priority or ""),
            ("Status", project.status or ""),
        ]
        row = 2
        for k,v in fields:
            sheet.write(row,0,k,label)
            sheet.write(row,1,v,cell)
            row += 1

        # Business Process
        sheet = workbook.add_worksheet("Business Process")
        sheet.set_column("A:A",30)
        sheet.set_column("B:B",80)
        sheet.write(0,0,"Field",header)
        sheet.write(0,1,"Value",header)
        sheet.write(1,0,"Current Process",label)
        sheet.write(1,1,dict(project._fields["current_process"].selection).get(project.current_process,""),wrap)
        sheet.write(2,0,"Description",label)
        sheet.write(2,1,project.process_description or "",wrap)

        # Current Problems
        sheet = workbook.add_worksheet("Current Problems")
        sheet.set_column("A:A",120)
        sheet.write(0,0,"Current Problems",header)
        sheet.write(1,0,project.current_problems or "",wrap)

        # Requirements
        sheet = workbook.add_worksheet("Requirements")
        heads=["Requirement","Module","Priority","Status","Assigned To","Description"]
        for c,h in enumerate(heads):
            sheet.write(0,c,h,header)
        row=1
        for rec in project.requirement_line_ids:
            sheet.write(row,0,rec.requirement_name or "",wrap)
            sheet.write(row,1,rec.module_name or "",cell)
            sheet.write(row,2,rec.priority or "",cell)
            sheet.write(row,3,rec.status or "",cell)
            sheet.write(row,4,rec.assigned_to or "",cell)
            sheet.write(row,5,rec.description or "",wrap)
            row+=1

        # Workflow
        sheet=workbook.add_worksheet("Workflow")
        heads=["Step","Responsible","Next Step","Status","Notes"]
        for c,h in enumerate(heads):
            sheet.write(0,c,h,header)
        row=1
        for rec in project.workflow_line_ids:
            sheet.write(row,0,rec.step_name or "",wrap)
            sheet.write(row,1,rec.responsible or "",cell)
            sheet.write(row,2,rec.next_step or "",wrap)
            sheet.write(row,3,rec.status or "",cell)
            sheet.write(row,4,rec.notes or "",wrap)
            row+=1

        # Reports
        sheet=workbook.add_worksheet("Reports")
        heads=["Report","Format","Priority","Required","Remarks"]
        for c,h in enumerate(heads):
            sheet.write(0,c,h,header)
        row=1
        for rec in project.report_line_ids:
            sheet.write(row,0,rec.report_name or "",cell)
            sheet.write(row,1,rec.format or "",cell)
            sheet.write(row,2,rec.priority or "",cell)
            sheet.write(row,3,"Yes" if rec.required else "No",cell)
            sheet.write(row,4,rec.remarks or "",wrap)
            row+=1

        sheet=workbook.add_worksheet("Special Rules")
        sheet.write(0,0,"Special Rules",header)
        sheet.write(1,0,project.special_rules or "",wrap)

        sheet=workbook.add_worksheet("Open Questions")
        sheet.write(0,0,"Open Questions",header)
        sheet.write(1,0,project.open_questions or "",wrap)

        workbook.close()
        output.seek(0)
        return request.make_response(
            output.read(),
            headers=[
                ("Content-Type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                ("Content-Disposition",'attachment; filename="Client_Requirement.xlsx"')
            ]
        )
   


    # PDF ############################################################
    @http.route(
        "/client_requirement/pdf/<int:project_id>",
        type="http",
        auth="user",
    )

    def export_pdf(self, project_id, **kw):

        project = request.env["client.project"].browse(project_id)

        output = io.BytesIO()

        pdf = SimpleDocTemplate(output)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "CLIENT REQUIREMENT DOCUMENT",
                styles["Title"]
            )
        )

        data = [
            ["Project Name", project.project_name or ""],
            ["Client Name", project.client_name or ""],
            ["Developer", project.developer or ""],
            ["Meeting Date", str(project.meeting_date or "")],
            ["Priority", project.priority or ""],
            ["Status", project.status or ""],
        ]

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0,0), (-1,-1), 1, colors.black),
                    ("VALIGN", (0,0), (-1,-1), "TOP"),
                ]
            )
        )

        elements.append(table)

        elements.append(
            Paragraph(
                "Business Process",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                project.process_description or "",
                styles["BodyText"]
            )
        )


        elements.append(
            Paragraph(
                "Current Problems",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                project.current_problems or "",
                styles["BodyText"]
            )
        )

        # ================= Requirements =================

        if project.requirement_line_ids:

         elements.append(Paragraph("<br/><b>Requirements</b>", styles["Heading2"]))

        data = [["Requirement", "Module", "Priority", "Status"]]

        for rec in project.requirement_line_ids:
         data.append([
            rec.requirement_name or "",
            rec.module_name or "",
            rec.priority or "",
            rec.status or "",
        ])

        table = Table(data)

        table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

        elements.append(table)




        pdf.build(elements)

        output.seek(0)

        return request.make_response(
            output.read(),
            headers=[
                (
                    "Content-Type",
                    "application/pdf",
                ),
                (
                    "Content-Disposition",
                    'attachment; filename="Client_Requirement.pdf"',
                ),
            ],
        )    
# from odoo import api, models
#
#
# class SalesReport(models.AbstractModel):
#     _name = 'report.weekly_monthly_sale_report.sales_report_template'
#     _description = 'Weekly monthly report'
#
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['sale.order'].browse(docids)
#         print(docs)
#         return {
#             'doc_ids': docids,
#             'doc_model': 'sale.order',
#             'docs': docs,
#             'data': data,
#         }
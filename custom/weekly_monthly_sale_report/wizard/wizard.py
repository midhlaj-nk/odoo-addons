from odoo import fields, models, api
import base64


class SaleMonthlyWeeklyReport(models.TransientModel):
    _name = 'sale.monthly.weekly.reporting'
    _description = 'Reporting wizard'

    customer_ids = fields.Many2many('res.partner')
    sales_team_id = fields.Many2one('crm.team', 'Sales Team')
    week_month = fields.Selection([('week', 'Week'),
                                   ('month', 'Month')
                                   ])

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def print_report(self):

        email_ids = []
        for rec in self.customer_ids:
            email_ids.append(rec.email)

        if self.week_month =="month":
            qy = ("""select date_trunc('month',sale_order.date_order) as month,
                                 sum(amount_total) as  total_amount,
                                 sale_order.name as sale_order_ref,
                                 res_partner.name as cust,
                                 sale_order.state as state,
                                 crm_team.name  as sales_team



                                 from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                 join crm_team on crm_team.id = sale_order.team_id

                                 group by date_trunc('month',sale_order.date_order),res_partner.name,sale_order.name,sale_order.state,crm_team.name

                       """ )

            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }

            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()

            # print(data)
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )
        if self.week_month=="week":
            cust_val = tuple(self.customer_ids.mapped('id'))
            qy = ("""select date_trunc('week',sale_order.date_order) as Week,
                                sum(amount_total) as  total_amount,
                                sale_order.name as sale_order_ref,
                                res_partner.name as cust,
                                sale_order.state as state,
                                crm_team.name  as sales_team



                                from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                join crm_team on crm_team.id = sale_order.team_id

                                 
                                          group by date_trunc('week',sale_order.date_order),res_partner.name,sale_order.name,sale_order.state,crm_team.name
                                 """ )


            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "Your Sales report",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(self.read()[0])
            # print(data)
            return self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                self, data=data)

        if self.customer_ids and self.sales_team_id and self.date_from and self.date_to and self.week_month == "week":
            print("week")
            # customer,sales team,from,to
            cust_val = tuple(self.customer_ids.mapped('id'))
            qy = ("""select date_trunc('week',sale_order.date_order) as Week,
                    sum(amount_total) as  total_amount,
                    sale_order.name as sale_order_ref,
                    res_partner.name as cust,
                    sale_order.state as state,
                    crm_team.name  as sales_team
                    
                    
                    
                    from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                    join crm_team on crm_team.id = sale_order.team_id
                    
                     where sale_order.date_order > '%s' and
                              sale_order.date_order < '%s' and
                              sale_order.partner_id in %s and
                              sale_order.team_id = '%s'
                              group by date_trunc('week',sale_order.date_order),res_partner.name,sale_order.name,sale_order.state,crm_team.name
                     """ % (
                self.date_from,
                self.date_to,
                cust_val,
                self.sales_team_id.id

            ))
            if len(cust_val) == 1:
                print("heyyiuhwic")
                qy = ("""select date_trunc('week',sale_order.date_order) as Week,
                         sum(amount_total) as  total_amount,
                         sale_order.name as sale_order_ref,
                         res_partner.name as cust,
                         sale_order.state as state,
                         crm_team.name  as sales_team



                         from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                         join crm_team on crm_team.id = sale_order.team_id

                          where sale_order.date_order > '%s' and
                                   sale_order.date_order < '%s' and
                                   sale_order.partner_id = '%s' and
                                   sale_order.team_id = '%s'
                                   group by date_trunc('week',sale_order.date_order),res_partner.name,sale_order.name,sale_order.state,crm_team.name
                          """ % (
                    self.date_from,
                    self.date_to,
                    self.customer_ids.id,
                    self.sales_team_id.id

                ))

            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "Your Sales report",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(self.read()[0])
            # print(data)
            return self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                self, data=data)

        elif self.customer_ids and self.sales_team_id and self.date_from and self.date_to and self.week_month == "month":
            print("month")
            # customer,sales team,from,to
            cust_val = tuple(self.customer_ids.mapped('id'))
            qy = ("""select date_trunc('month',sale_order.date_order) as month,
                      sum(amount_total) as  total_amount,
                      sale_order.name as sale_order_ref,
                      res_partner.name as cust,
                      sale_order.state as state,
                      crm_team.name  as sales_team



                      from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                      join crm_team on crm_team.id = sale_order.team_id
                                      where sale_order.date_order > '%s' and
                              sale_order.date_order < '%s' and
                              sale_order.partner_id in %s and
                              sale_order.team_id = '%s'
                      group by date_trunc('month',sale_order.date_order),res_partner.name,sale_order.name,sale_order.state,crm_team.name

            """ % (
                self.date_from,
                self.date_to,
                cust_val,
                self.sales_team_id.id

            ))
            if len(cust_val) == 1:
                print("hemonthy")
                qy = ("""select date_trunc('month',sale_order.date_order) as month,
                                      sum(amount_total) as  total_amount,
                                      sale_order.name as sale_order_ref,
                                      res_partner.name as cust,
                                      sale_order.state as state,
                                      crm_team.name  as sales_team



                                      from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                      join crm_team on crm_team.id = sale_order.team_id
                                                      where sale_order.date_order > '%s' and
                                              sale_order.date_order < '%s' and
                                              sale_order.partner_id = '%s' and
                                              sale_order.team_id = '%s'
                                      group by date_trunc('month',sale_order.date_order),res_partner.name,sale_order.name,sale_order.state,crm_team.name

                            """ % (
                    self.date_from,
                    self.date_to,
                    self.customer_ids.id,
                    self.sales_team_id.id

                ))

            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }

            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()

            # print(data)
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )

        elif self.customer_ids and self.sales_team_id and self.date_from and self.date_to:

            print("1")
            # customer,sales team,from,to
            cust_val = tuple(self.customer_ids.mapped('id'))
            qy = ("""select res_partner.name as customer,
                        sale_order.name as sale_order_ref,
                        crm_team.name  as sales_team,
                        amount_total as total_amount,
                        sale_order.state as state
    
                        from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                        join crm_team on crm_team.id = sale_order.team_id
                        where sale_order.date_order > '%s' and
                              sale_order.date_order < '%s' and
                              sale_order.partner_id in %s and
                              sale_order.team_id = '%s'
                     """ % (
                self.date_from,
                self.date_to,
                cust_val,
                self.sales_team_id.id

            ))
            if len(cust_val) == 1:
                qy = ("""select res_partner.name as customer,
                                        sale_order.name as sale_order_ref,
                                        crm_team.name  as sales_team,
                                        amount_total as total_amount,
                                        sale_order.state as state

                                        from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                        join crm_team on crm_team.id = sale_order.team_id
                                        where sale_order.date_order > '%s' and
                                              sale_order.date_order < '%s' and
                                              sale_order.partner_id = %s and
                                              sale_order.team_id = '%s'
                                     """ % (
                    self.date_from,
                    self.date_to,
                    self.customer_ids.id,
                    self.sales_team_id.id

                ))

            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(data['form_data'])
            # print(self.read()[0])
            print("Query", qdata)
            print("form_data", self.read()[0])
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )

        elif self.customer_ids:
            # customer multiple
            print("2")
            cust_val = tuple(self.customer_ids.mapped('id'))
            qy = ("""select res_partner.name as customer,
                                    sale_order.name as sale_order_ref,
                                    crm_team.name  as sales_team,
                                    amount_total as total_amount,
                                    sale_order.state as state
    
                                    from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                    join crm_team on crm_team.id = sale_order.team_id
                                    where sale_order.partner_id in %s
                                          
                                 """ % (

                cust_val,

            ))
            if len(cust_val)==1:
                qy = ("""select res_partner.name as customer,
                                                   sale_order.name as sale_order_ref,
                                                   crm_team.name  as sales_team,
                                                   amount_total as total_amount,
                                                   sale_order.state as state

                                                   from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                                   join crm_team on crm_team.id = sale_order.team_id
                                                   where sale_order.partner_id = '%s'

                                                """ % (

                    self.customer_ids.id,

                ))

            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(self.read()[0])
            # print(data)
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )

        elif self.sales_team_id:
            # sales team
            print("3")
            qy = ("""select res_partner.name as customer,
                                    sale_order.name as sale_order_ref,
                                    crm_team.name  as sales_team,
                                    amount_total as total_amount,
                                    sale_order.state as state
    
                                    from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                    join crm_team on crm_team.id = sale_order.team_id
                                    where 
                                          sale_order.team_id = '%s'
                                 """ % (
                self.sales_team_id.id

            ))
            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(self.read()[0])
            # print(data)
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )
        elif self.date_from:
            # from date
            print("from date")
            qy = ("""select res_partner.name as customer,
                                    sale_order.name as sale_order_ref,
                                    crm_team.name  as sales_team,
                                    amount_total as total_amount,
                                    sale_order.state as state
    
                                    from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                    join crm_team on crm_team.id = sale_order.team_id
                                    where sale_order.date_order > '%s'
    
                                 """ % (
                self.date_from

            ))
            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(self.read()[0])
            # print(data)
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )
        elif self.date_to:
            print("date to")
            cust_val = tuple(self.customer_ids.mapped('id'))
            qy = ("""select res_partner.name as customer,
                                    sale_order.name as sale_order_ref,
                                    crm_team.name  as sales_team,
                                    amount_total as total_amount,
                                    sale_order.state as state
    
                                    from sale_order join res_partner on res_partner.id = sale_order.partner_id
                                                    join crm_team on crm_team.id = sale_order.team_id
                                    where 
                                          sale_order.date_order < '%s' 
    
                                 """ % (

                self.date_to,

            ))
            self.env.cr.execute(qy)
            qdata = self.env.cr.dictfetchall()
            # print(self.read()[0])
            list = []
            for rec in self.customer_ids:
                list.append(rec.name)
                # print(list)
            data = {
                'form_data': self.read()[0],
                'query': qdata,
                'customer': list
            }
            pdf = self.env.ref(
                'weekly_monthly_sale_report.monthly_weekly_report_pdf_action')._render_qweb_pdf(
                self, data=data)

            print(pdf)

            data_record = base64.b64encode(pdf[0])
            attachment = self.env['ir.attachment'].create({
                'name': 'report.pdf',
                'type': 'binary',
                'datas': data_record,
                'store_fname': data_record,
                'mimetype': 'application/x-pdf',
            })

            for res in email_ids:
                main_content = {
                    'subject': ('sales report'),
                    'body_html': "hey",
                    'email_to': res,
                    'attachment_ids': attachment

                }

                self.env['mail.mail'].create(main_content).send()
            print(self.read()[0])
            # print(data)
            return \
                self.env.ref(
                    'weekly_monthly_sale_report.monthly_weekly_report_pdf_action').report_action(
                    self, data=data
                )

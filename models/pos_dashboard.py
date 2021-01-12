import pytz
from odoo import models, fields, api, _
from datetime import timedelta, datetime, date, time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError
from odoo.http import request

menit = datetime.now().strftime("%H")
menit = int(menit) - 1

jam = datetime.now().strftime("%H")
jam = int(jam) + 7

tgl = datetime.now().strftime("%d")
tgl = int(tgl) - 1

bln = datetime.now().strftime("%m")
bln = int(bln) - 1

name_bulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def get_session(self, pos, date1, date2):
        self._cr.execute("SELECT name FROM pos_session WHERE state = 'opened' ORDER BY name;")
        result = self._cr.dictfetchall()
        order = len(result)
        a = "{:,}".format(order)
        return a

class PosDashboard(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_categ_chart(self, option,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        order = []
        today = []
        product = []
        count = 0
        hitung = 0
        jamku = []
        if option == 'pos_dayly_sales':
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state IN ('sale','done') AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += int(x.get('qty'))
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += int(x.get('qty'))
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_monthly_sales':
            name = "monthly"
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state IN ('sale','done') AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += int(x.get('qty'))
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += int(x.get('qty'))
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_year_sales':
            name = "yearly"
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state IN ('sale','done') AND sale_order.date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += int(x.get('qty'))
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += int(x.get('qty'))
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        if date2:
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state IN ('sale','done') AND sale_order.date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY product_category.id ORDER BY qty DESC")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += int(x.get('qty'))
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += int(x.get('qty'))
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif date1:
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state IN ('sale','done') AND sale_order.date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += int(x.get('qty'))
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += int(x.get('qty'))
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        final = [order[:5], today[:5], name]
        return final

    @api.model
    def get_categ_chart2(self):
        order = []
        today = []
        product = []
        count = 0
        hitung = 0
        jamku = []
        name = "monthly"
        self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state IN ('sale','done') AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC")
        result = self._cr.dictfetchall()
        name = "dayly"
        for x in result: 
            get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
            if x.get('name') not in jamku:
                if count != 0:
                    order.append(count)
                    count = 0
                today.append(str(str(get_name.categ_id.display_name)))
                jamku.append(x.get('name'))
                count += int(x.get('qty'))
                hitung += 1
                if hitung == len(result):
                     order.append(count)
            else:
                count += int(x.get('qty'))
                hitung +=1
                if hitung == len(result):
                     order.append(count)
        final = [order[:5], today[:5], name]
        return final

    @api.model
    def get_order(self, pos, date1, date2):
        list_lokasi = []
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                list_lokasi.append(x.get('id'))
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        elif pos != "": 
            list_lokasi.append(pos)
        if not date2:
            self._cr.execute("SELECT pos_order.id FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND amount_total < 0 AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"';")
            result = self._cr.dictfetchall()
            record = request.env.ref('dashboard_pos.action_pos_pos_form2')
            record.write({
                    'domain' : [('session_id.config_id.id', 'in', list_lokasi),("amount_total","<", 0),("date_order",">=",str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit))),("date_order","<",str(datetime.now() + timedelta(hours=7)))],
                    'context': {}
                })
            a = len(result)
            b = "{:,}".format(a)
        elif date2:             
            self._cr.execute("SELECT pos_order.id FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND amount_total < 0 AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"';")
            result = self._cr.dictfetchall()
            record = request.env.ref('dashboard_pos.action_pos_pos_form2')
            record.write({
                    'domain' : [('session_id.config_id.id', 'in', list_lokasi),("amount_total","<", 0),("date_order",">=",str(date1)),("date_order","<",str(date2))],
                    'context': {}
                })
            a = len(result)
            b = "{:,}".format(a)
        return b

    @api.model
    def o_today_order(self, pos, date1, date2):
        list_lokasi = []
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                list_lokasi.append(x.get('id'))
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        elif pos != "": 
            list_lokasi.append(pos)
        if not date2:            
            self._cr.execute("SELECT pos_order.id FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"';")
            result = self._cr.dictfetchall()
            record = request.env.ref('dashboard_pos.action_pos_pos_form3')
            record.write({
                    'domain' : [('session_id.config_id.id', 'in', list_lokasi),("date_order",">=",str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit))),("date_order","<",str(datetime.now() + timedelta(hours=7)))],
                    'context': {}
                })
            a = len(result)
            b = "{:,}".format(a)
        if date2:
            self._cr.execute("SELECT pos_order.id FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"';")
            result = self._cr.dictfetchall()
            record = request.env.ref('dashboard_pos.action_pos_pos_form3')
            record.write({
                    'domain' : [('session_id.config_id.id', 'in', list_lokasi),("date_order",">=",str(date1)),("date_order","<",str(date2))],
                    'context': {}
                })
            a = len(result)
            b = "{:,}".format(a)
        return b

    @api.model
    def get_order_today(self, pos, date1, date2):
        list_lokasi = []
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                list_lokasi.append(x.get('id'))
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        elif pos != "": 
            list_lokasi.append(pos)
        if not date2:
            self._cr.execute("SELECT stock_picking.name , pos_order.date_order,pos_order.state, pos_order_line.qty FROM pos_order INNER JOIN pos_order_line ON pos_order.id=pos_order_line.order_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id JOIN stock_picking on stock_picking.id = pos_order.picking_id WHERE pos_order.amount_total > 0 AND pos_config.id IN ("+pos+") AND  date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"';")
            result = self._cr.dictfetchall()
            list_reference = []
            user_ids= 0
            for ids in result:
                user_ids += ids.get('qty')
                list_reference.append(ids.get("name"))
            a = int(user_ids)
            b = "{:,}".format(a)
            record = request.env.ref('dashboard_pos.stock_move_line_action2')
            record.write({
                        'domain' : [('reference','in',list_reference),("date",">=", str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit))),("date","<", str(datetime.now() + timedelta(hours=7)))],
                        'context': {}
                    })
        if date2:
            self._cr.execute("SELECT stock_picking.name , pos_order.date_order,pos_order.state, pos_order_line.qty FROM pos_order INNER JOIN pos_order_line ON pos_order.id=pos_order_line.order_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id JOIN stock_picking on stock_picking.id = pos_order.picking_id WHERE pos_order.amount_total > 0 AND pos_config.id IN ("+pos+") AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"';")
            result = self._cr.dictfetchall()
            record = request.env.ref('dashboard_pos.stock_move_line_action2')
            list_reference = []
            user_ids= 0
            for ids in result:
                user_ids += ids.get('qty')
                list_reference.append(ids.get("name"))
            a = int(user_ids)
            b = "{:,}".format(a)
            record = request.env.ref('dashboard_pos.stock_move_line_action2')
            record.write({
                        'domain' : [('reference','in',list_reference),("date",">=", str(date1)),("date","<", str(date2))],
                        'context': {}
                    })
        return b

    @api.model
    def get_product_chart(self, option, pos, date1, date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')    + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        order = []
        name = []
        no = 0
        product = []
        if option == "pos_dayly_categ_product":
            self._cr.execute("SELECT product_category.name as nama,product_category.id as id, SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND pos_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('nama'))
                order.append(x.get('qty'))
        elif option == "pos_monthly_categ_product":
            self._cr.execute("SELECT product_category.name as nama,product_category.id as id, SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('nama'))
                order.append(x.get('qty'))
        elif option == "pos_year_categ_product":
            self._cr.execute("SELECT product_category.name as nama,product_category.id as id, SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('nama'))
                order.append(x.get('qty'))
        if date2:
            self._cr.execute("SELECT product_category.name as nama,product_category.id as id, SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('nama'))
                order.append(x.get('qty'))
        elif date1:
            self._cr.execute("SELECT product_category.name as nama,product_category.id as id, SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('nama'))
                order.append(x.get('qty'))
        

        # raise result
        # raise AccessError(str(result))
        final = [order, name, ""]
        return final
    
    @api.model
    def get_pos_chart(self, option, pos, date1, date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)    
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')    + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        name = []
        order = []
        total = []

        if option == "pos_dayly_sales":
            self._cr.execute("SELECT pos_config.name,count(pos_order.id) as order,sum(pos_order.amount_total) as total FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id where pos_config.id IN ("+pos+") AND date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY pos_config.id")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('name'))
                order.append(x.get('order'))
                total.append(x.get('total'))

        elif option == "pos_monthly_sales":
            self._cr.execute("SELECT pos_config.name,count(pos_order.id) as order,sum(pos_order.amount_total) as total FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id where pos_config.id IN ("+pos+") AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY pos_config.id")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('name'))
                order.append(x.get('order'))
                total.append(x.get('total'))

        elif option == "pos_year_sales":
            self._cr.execute("SELECT pos_config.name,count(pos_order.id) as order,sum(pos_order.amount_total) as total FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id where pos_config.id IN ("+pos+") AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY pos_config.id")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('name'))
                order.append(x.get('order'))
                total.append(x.get('total'))

        if date2:
            self._cr.execute("SELECT pos_config.name,count(pos_order.id) as order,sum(pos_order.amount_total) as total FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id where pos_config.id IN ("+pos+") AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY pos_config.id")
            result = self._cr.dictfetchall()
            for x in result:
                name.append(x.get('name'))
                order.append(x.get('order'))
                total.append(x.get('total'))
        
        final = [order, name, total]
        return final

    @api.model
    def get_orders_chart(self, option, pos, date1, date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        count = 0
        hitung = 0
        order = []
        order1 = [] 
        name = []
        today = []
        name = 'Jumlah Order'
        name2 = 'Rata - rata'
        jamku   = []
        if option == 'pos_hourly_sales' and date2:
            self._cr.execute("SELECT extract(hour from date_order) as jam_pos, count(pos_order.id) as jml FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY extract(hour from date_order) ORDER BY jam_pos")
            docs1 = self._cr.dictfetchall()
            for x in range(0,24):
                a = x + 1
                b = x
                if x < 10:
                    b = str(0)+str(x)
                if x < 9: 
                    a =  str(0)+str(x+1)
                for record in docs1:
                    var_ung = int(record.get('jam_pos')) + 7
                    if var_ung > 24:
                        var_ung - 24
                    if int(x) == var_ung:
                        count = record.get('jml')
                delta = date2 - date1
                Jumlah_hari = str(delta.days)
                count = count / int(Jumlah_hari)
                c = round(count,2)
                order.append(c)
                today.append(str(b)+"-"+str(a))
                count = 0
        elif option == 'pos_hourly_sales' and date1:
            self._cr.execute("SELECT extract(hour from date_order) as jam_pos, count(pos_order.id) as jml FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY extract(hour from date_order) ORDER BY jam_pos")
            docs1 = self._cr.dictfetchall()
            for x in range(0,24):
                a = x + 1
                b = x
                if x < 10:
                    b = str(0)+str(x)
                if x < 9: 
                    a =  str(0)+str(x+1)
                for record in docs1:
                    var_ung = int(record.get('jam_pos')) + 7
                    if var_ung > 24:
                        var_ung - 24
                    if int(x) == var_ung:
                        count = record.get('jml')
                delta = datetime.now() + timedelta(hours=7) - date1
                Jumlah_hari = str(delta.days)
                count = count / int(Jumlah_hari)
                c = round(count,2)
                order.append(c)
                today.append(str(b)+"-"+str(a))
                count = 0
        elif option == 'pos_hourly_sales':
            self._cr.execute("SELECT extract(hour from date_order) as jam_pos, count(pos_order.id) as jml FROM pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY extract(hour from date_order) ORDER BY jam_pos")
            docs1 = self._cr.dictfetchall()
            for x in range(0,24):
                a = x + 1
                b = x
                if x < 10:
                    b = str(0)+str(x)
                if x < 9: 
                    a =  str(0)+str(x+1)
                for record in docs1:
                    var_ung = int(record.get('jam_pos')) + 7
                    if var_ung > 24:
                        var_ung - 24
                    if int(x) == var_ung:
                        count = record.get('jml')
                order.append(count)
                today.append(str(b)+"-"+str(a))
                count = 0

        elif option == 'pos_dayly_sales':
            self._cr.execute("SELECT date_order, extract(day from date_order) as date_orders from pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY date_order ASC;")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('date_order').strftime("%d/%m/%Y") not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(x.get('date_order').strftime("%d/%m/%Y"))
                    jamku.append(x.get('date_order').strftime("%d/%m/%Y"))
                    count += 1
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)   
                else:
                    count +=1
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_monthly_sales' and date2:
            self._cr.execute("SELECT extract(month from date_order) as date_order ,extract(year from date_order) as year from pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' ORDER BY date_order DESC;")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('date_order') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    bulan = name_bulan[int(x.get('date_order')-1)]
                    today.append(str(bulan)+ " - " +str(int(x.get("year"))))
                    jamku.append(x.get('date_order'))
                    count += 1
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)   
                else:
                    count +=1
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_monthly_sales':
            self._cr.execute("SELECT extract(month from date_order) as date_order from pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY date_order ASC;")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('date_order') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    bulan = name_bulan[int(x.get('date_order')-1)]
                    today.append(str(bulan))
                    jamku.append(x.get('date_order'))
                    count += 1
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)   
                else:
                    count +=1
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_year_sales':
            self._cr.execute("SELECT extract(year from date_order) as date_order from pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced')  ORDER BY date_order ASC;")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('date_order') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(x.get('date_order'))
                    jamku.append(x.get('date_order'))
                    count += 1
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)   
                else:
                    count +=1
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)
        if date2 and not option:
            self._cr.execute("SELECT date_order, extract(day from date_order) as date_orders from pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' ORDER BY date_order ASC;")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('date_order').strftime("%d/%m/%Y") not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(x.get('date_order').strftime("%d/%m/%Y"))
                    jamku.append(x.get('date_order').strftime("%d/%m/%Y"))
                    count += 1
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)   
                else:
                    count +=1
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)
        elif date1 and not option:
            self._cr.execute("SELECT date_order, extract(day from date_order) as date_orders from pos_order JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY date_order ASC;")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('date_order').strftime("%d/%m/%Y") not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(x.get('date_order').strftime("%d/%m/%Y"))
                    jamku.append(x.get('date_order').strftime("%d/%m/%Y"))
                    count += 1
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)   
                else:
                    count +=1
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)
        final = [order, today, name]
        return final

    @api.model
    def get_sale_by_salesman(self,option, pos, date1, date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        order = ""
        no = 0
        customer = []
        if option == "pos_dayly_customer":
            self._cr.execute("SELECT res_partner.display_name, res_partner.id as id ,res_partner.name, COUNT(res_partner.name) as haha FROM pos_order INNER JOIN res_partner ON pos_order.partner_id = res_partner.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.display_name , res_partner.id, res_partner.name ORDER BY haha DESC LIMIT 5;")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/customer/filter?customer="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('haha'))+"</td></tr>"
        elif option == "pos_monthly_customer":
            self._cr.execute("SELECT res_partner.display_name , res_partner.id as id ,res_partner.name, COUNT(res_partner.name) as haha FROM pos_order INNER JOIN res_partner ON pos_order.partner_id = res_partner.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.display_name ,res_partner.id , res_partner.name ORDER BY haha DESC LIMIT 5;")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/customer/filter?customer="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('haha'))+"</td></tr>"
        elif option == "pos_year_customer":
            self._cr.execute("SELECT res_partner.display_name , res_partner.id as id ,res_partner.name, COUNT(res_partner.name) as haha FROM pos_order INNER JOIN res_partner ON pos_order.partner_id = res_partner.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.display_name , res_partner.id , res_partner.name ORDER BY haha DESC LIMIT 5;")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/customer/filter?customer="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('haha'))+"</td></tr>"
        if date2:
            self._cr.execute("SELECT res_partner.display_name , res_partner.id as id ,res_partner.name, COUNT(res_partner.name) as haha FROM pos_order INNER JOIN res_partner ON pos_order.partner_id = res_partner.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY res_partner.display_name , res_partner.id , res_partner.name ORDER BY haha DESC LIMIT 5;")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/customer/filter?customer="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+str(x.get('haha'))  +"</td></tr>"
        elif date1:
            self._cr.execute("SELECT res_partner.display_name , res_partner.id as id ,res_partner.name, COUNT(res_partner.name) as haha FROM pos_order INNER JOIN res_partner ON pos_order.partner_id = res_partner.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.display_name , res_partner.id , res_partner.name ORDER BY haha DESC LIMIT 5;")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/customer/filter?customer="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+str(x.get('haha'))  +"</td></tr>"
        return order

    @api.model
    def get_top_sales(self, option, pos, date1, date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=-jam, minutes=-menit)
        if not pos:
            self._cr.execute("SELECT id FROM pos_config ORDER BY name ASC;")
            result = self._cr.dictfetchall()
            hitungs = 0
            pos = ""
            for x in result:
                pos = pos + "'"+str(x.get('id')) + "'"
                hitungs += 1
                if hitungs != len(result):
                    pos = pos + ","
        order = ""
        today = []
        no = 0
        product = []
        if option == 'pos_dayly_product':
            self._cr.execute("SELECT product_template.id as id,product_template.list_price * SUM(pos_order_line.qty) as value, product_template.name , SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_template.id ,product_template.name ORDER BY value DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                # value = x.get('list_price') * x.get('qty')
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/product2/filter?product2="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('qty'))+"</td><td>"+"{:,}".format(x.get('value'))+"</td></tr>"
        elif option == 'pos_monthly_product':
            self._cr.execute("SELECT product_template.id as id,product_template.list_price * SUM(pos_order_line.qty) as value, product_template.name , SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_template.id ,product_template.name ORDER BY value DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                # value = x.get('list_price') * x.get('qty')
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/product2/filter?product2="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('qty'))+"</td><td>"+"{:,}".format(x.get('value'))+"</td></tr>"
        elif option == 'pos_year_product':
            self._cr.execute("SELECT product_template.id as id,product_template.list_price * SUM(pos_order_line.qty) as value, product_template.name , SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_template.id ,product_template.name ORDER BY value DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                # value = x.get('list_price') * x.get('qty')
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/product2/filter?product2="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('qty'))+"</td><td>"+"{:,}".format(x.get('value'))+"</td></tr>"
        if date2:
            self._cr.execute("SELECT product_template.id as id,product_template.list_price * SUM(pos_order_line.qty) as value, product_template.name , SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY product_template.id ,product_template.name ORDER BY value DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                # value = x.get('list_price') * x.get('qty')
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/product2/filter?product2="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('qty'))+"</td><td>"+"{:,}".format(x.get('value'))+"</td></tr>"
        elif date1:
            self._cr.execute("SELECT product_template.id as id,product_template.list_price * SUM(pos_order_line.qty) as value, product_template.name , SUM(pos_order_line.qty) as qty FROM pos_order_line JOIN pos_order ON pos_order_line.order_id = pos_order.id JOIN product_product ON pos_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN pos_session ON pos_session.id = pos_order.session_id JOIN pos_config ON pos_session.config_id = pos_config.id WHERE pos_config.id IN ("+pos+") AND pos_order.state IN ('paid','done','invoiced') AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_template.id ,product_template.name ORDER BY value DESC LIMIT 10")
            result = self._cr.dictfetchall()
            for x in result:
                no += 1
                # value = x.get('list_price') * x.get('qty')
                order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/point_of_sale/product2/filter?product2="+str(x.get('id'))+"'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('qty'))+"</td><td>"+"{:,}".format(x.get('value'))+"</td></tr>"
        return order

    @api.model
    def get_name_pos(self):
        name = ""
        self._cr.execute("SELECT id, name FROM pos_config ORDER BY name ASC;")
        result = self._cr.dictfetchall()
        for x in result:
            name = name + "<option value='"+str(x.get("id"))+"'>"+str(x.get("name"))+"</option>"
        return name

    @api.model
    def get_date_now(self):
        first_date = (datetime.now() + timedelta(days=-tgl + 1, hours=-jam, minutes=-menit)).strftime('%Y-%m-%d')
        last_date = (datetime.now() + relativedelta(months=1) + timedelta(days=-tgl, hours=-jam, minutes=-menit)).strftime('%Y-%m-%d')
        return [first_date, last_date]
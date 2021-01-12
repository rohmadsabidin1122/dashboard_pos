# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import werkzeug.utils
from odoo.addons.sale.controllers.onboarding import OnboardingController  
from datetime import timedelta, datetime, date, time

menit = datetime.now().strftime("%H")
menit = int(menit) - 1

jam = datetime.now().strftime("%H")
jam = int(jam) - 7

date = datetime.now() + timedelta(hours=-jam, minutes=-menit) 
date1 = datetime.now() + timedelta(hours=7)
class CustomOnboardingController(OnboardingController): 

    @http.route('/dashboard_pos/dashboard_form_view', auth='user', type='json')
    def pos_dashboard(self):
       
        company = request.env.user.company_id
        
        return {
            'html': request.env.ref('dashboard_pos.pos_quotation_notify').render({
                'company': company if company else True,
                'state': True
            })
        }

    # @http.route('/point_of_sale/anjing/filter', auth='user', type='http')
    # def sale_quotation_filter1(self,**kw):
    #     record = request.env.ref('dashboard_pos.action_pos_pos_form2')
    #     key = kw.get('kerek')
    #     record.write({
    #                 'context': {}
    #                 })
    #     return werkzeug.utils.redirect('/web#action={0}&amp;model=pos.order&amp;view_type=list&amp;'.format(record.id))
    
   

    @http.route('/point_of_sale/today_order/filter', auth='user', type='http')
    def sale_quotation_filter_today(self,**kw):
        record = request.env.ref('dashboard_pos.action_pos_pos_form2')
        key = kw.get('today')
        # record.write({
        #                 'domain' : [("amount_total","<", 0)],
        #                 'context': {}
        #             })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=pos.order&amp;view_type=list&amp;'.format(record.id))

    @http.route('/point_of_sale/data/filter', auth='user', type='http')
    def sale_quotation_filter2(self,**kw):
        record = request.env.ref('dashboard_pos.action_pos_pos_form3')
        key = kw.get('data')
        # record.write({
        #                 'domain' : [],
        #                 'context': {}
        #             })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=pos.order&amp;view_type=list&amp;'.format(record.id))    
   
    @http.route('/point_of_sale/active_session/filter', auth='user', type='http')
    def sale_quotation_filter3(self,**kw):
        record = request.env.ref('point_of_sale.action_pos_config_kanban')
        key = kw.get('active')
        record.write({
                        # 'domain' : [('pos_session_state', '=', 'opened')], 
                        'domain' : [], 
                        'context': {}
                    })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=pos.config&amp;view_type=list&amp;'.format(record.id))


    @http.route('/point_of_sale/Sessions/filter', auth='user', type='http')
    def sale_quotation_filter3(self,**kw):
        record = request.env.ref('point_of_sale.action_pos_session')
        key = kw.get('active')
        record.write({
                        'domain' : [('state', '=', 'opened')], 
                        'context': {}
                    })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=pos.config&amp;view_type=list&amp;'.format(record.id))


    @http.route('/point_of_sale/product/filter', auth='user', type='http')
    def sale_quotation_filter4(self,**kw):
        record = request.env.ref('dashboard_pos.stock_move_line_action2')
        key = kw.get('product')
        # record.write({
        #                 'domain' : [("date",">=", str(date.strftime("%Y-%m-%d %H:%M:%S"))),("date","<", str(date1.strftime("%Y-%m-%d %H:%M:%S")))],
        #                 'context': {}
        #             })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=stock.move.line&amp;view_type=list&amp;'.format(record.id))

    @http.route('/point_of_sale/customer/filter', auth='user', type='http')
    def sale_quotation_filter5(self,**kw):
        record = request.env.ref('dashboard_pos.action_partner_customer_form2')
        key = kw.get('customer')
        record.write({
                        'domain' : [("id","=",key)],
                        'context': {}
                    })
        return werkzeug.utils.redirect("/web#id="+key+"&action={0}&model=res.partner&view_type=form&menu_id=".format(record.id))

    @http.route('/point_of_sale/product2/filter', auth='user', type='http')
    def sale_quotation_filter6(self,**kw):
        record = request.env.ref('dashboard_pos.product_template_action_pos_product2')
        key = kw.get('product2')
        record.write({
                        'domain' : [("id","=",key)],
                        'context': {}
                    })
        return werkzeug.utils.redirect("/web#id="+key+"&action={0}&model=product.template&view_type=form&menu_id=".format(record.id))

    @http.route('/point_of_sale/categ_id/filter', auth='user', type='http')
    def sale_quotation_filter7(self,**kw):
        record = request.env.ref('product.product_category_action_form')
        key = kw.get('categ_id')
        record.write({
                        'domain' : [("id","=",key)],
                        'context': {}
                    })
        return werkzeug.utils.redirect("/web#id="+key+"&action={0}&model=product.template&view_type=form&menu_id=".format(record.id))

   
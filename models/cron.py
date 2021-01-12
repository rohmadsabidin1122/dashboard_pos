# class ClassName(models.Model):
# 	_name = "dashboard_pos.reset_order"
	
#     def sale_order_filter_reset(self,**kw):
#         record = request.env.ref('point_of_sale.action_pos_pos_form')
#         record.write({
#                         'domain' : [], 
#                         'context': {}
#                     })
#         record = request.env.ref('point_of_sale.action_pos_config_kanban')
#         record.write({
#                         'domain' : [], 
#                         'context': {}
#                     })
#         record = request.env.ref('point_of_sale.product_template_action_pos_product')
#         record.write({
#                         'domain' : [], 
#                         'context': {}
#                     })
#         return werkzeug.utils.redirect('/web#action={0}&amp;model=product.template&amp;view_type=list&amp;'.format(record.id))
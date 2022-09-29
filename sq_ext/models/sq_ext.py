
from odoo import models, api, fields, _
from odoo.exceptions import UserError
# from odoo.addons.sale.models.sale import SaleOrder as OriginalSaleOrder 

class Name_Dropdown(models.Model):
    _name = "project.name"
    name  =  fields.Char(string="Name")

class Size_Dropdown(models.Model):
    _name = "plot.size"
    name  = fields.Char(string="Size")

class Internal_Dropdown(models.Model):
    _name = "internal.ref"
    name  = fields.Char(string="Size")

class SQExtension(models.Model):
    _inherit = 'sale.order'

    project_name      =   fields.Many2one("project.name","Project Name")
    plot_size         =   fields.Many2one("plot.size","Plot Size")
    internal_ref      =   fields.Many2one("internal.ref","Internal Reference")
    price             =   fields.Integer(string="Sales Price")
    cost              =   fields.Integer(string="Actual Cost")
    additional_price  =   fields.Integer(string="Additional Price")
    discount_builder  =   fields.Integer(string="Discount by Builder")
    # gross_amount     =   fields.Char(string="Gross Amount",compute="get_gross_amount", store=True)  
    gross_amount     =   fields.Integer(string="Gross Amount",compute="get_gross_amount") 
    gross_amount_final= fields.Integer(string="Gross Amount ") 

    def get_gross_amount(self):

        self.gross_amount = (self.price + self.additional_price) - self.cost
        self.gross_amount_final=self.gross_amount
        
    @api.onchange('gross_amount')
    def _amount_all(self):
      
        for order in self:
            amount_tax = discount = 0.0
            for line in order.order_line:

                discount += line.price_subtotal
                amount_tax += line.price_tax

            order.update({
                'amount_untaxed': discount,
                'amount_tax': amount_tax,
                'amount_total': (self.gross_amount + amount_tax) - discount,
            })



class SALEExtension(models.Model):
    _inherit = 'sale.report'
    project_name   =   fields.Many2one("project.name","Project Name")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['project_name'] = ", s.project_name as project_name"
        groupby+=", s.project_name"
        return super(SALEExtension, self)._query(with_clause, fields, groupby, from_clause)
    
    
class SALEExtension1(models.Model):
    _inherit = 'sale.report'
    plot_size  =   fields.Many2one("plot.size","Plot Size")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['plot_size'] = ", s.plot_size as plot_size"
        groupby+=", s.plot_size"
        return super(SALEExtension1, self)._query(with_clause, fields, groupby, from_clause)
    
    
class SALEExtension2(models.Model):
    _inherit = 'sale.report'
    internal_ref =   fields.Many2one("internal.ref","Internal Reference")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['internal_ref'] = ", s.internal_ref as internal_ref"
        groupby+=", s.internal_ref"
        return super(SALEExtension2, self)._query(with_clause, fields, groupby, from_clause)
    
    
class SALEExtension3(models.Model):
    _inherit = 'sale.report'   
    price= fields.Integer(string="Sales Price")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['price'] = ", s.price as price"
        return super(SALEExtension3, self)._query(with_clause, fields, groupby, from_clause)
    
    
    
class SALEExtension4(models.Model):
    _inherit = 'sale.report'     
    cost= fields.Integer(string="Actual Cost")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['cost'] = ", s.cost as cost "
        return super(SALEExtension4, self)._query(with_clause, fields, groupby, from_clause)
    


class SALEExtension5(models.Model):
    _inherit = 'sale.report'     
    additional_price  =   fields.Integer(string="Additional Price")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['additional_price'] = ", s.additional_price as additional_price"
        groupby+=", s.additional_price"
        return super(SALEExtension5, self)._query(with_clause, fields, groupby, from_clause)
    
    
 
class SALEExtension6(models.Model):
    _inherit = 'sale.report'      
    discount_builder  =   fields.Integer(string="Discount by Builder")
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['discount_builder'] = ", s.discount_builder as discount_builder"
        groupby+=", s.discount_builder"
        return super(SALEExtension6, self)._query(with_clause, fields, groupby, from_clause)
    
    
    
    
class SALEExtension7(models.Model):
    _inherit = 'sale.report'      
    gross_amount_final= fields.Integer(string="Gross Amount ") 
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['gross_amount_final'] = ", s.gross_amount_final as gross_amount_final"
        groupby+=", s.gross_amount_final"
        return super(SALEExtension7, self)._query(with_clause, fields, groupby, from_clause)
    
# class SALEExtension7(models.Model):
#     _inherit = 'sale.report' 
#     gross_amount  =  fields.Char(string="Gross Amount")
#     # def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
#     #     fields['gross_amount'] = ", s.gross_amount as gross_amount"
#     #     groupby+=", s.gross_amount"
#     #     return super(SALEExtension7, self)._query(with_clause, fields, groupby, from_clause)
#     def _query(self, with_clause='', fields=None, groupby='', from_clause=''):
#         if fields is None:
#             fields = {}
#         fields['gross_amount '] = ", s.gross_amount  as gross_amount "
#         return super(SALEExtension7, self)._query(with_clause, fields, groupby, from_clause)
 
 
 
 
 
 
 
    
    # def _prepare_invoice_values(self, order, name, amount, so_line):
    #     res = super()._prepare_invoice_values(order, name, amount, so_line)
    #     res.update({'_default_project_name':order.project_name.id})
    #     return res


    # class PivotInheritReport(models.Model):
    #     _inherit = 'sale.report'
    #     new_name = fields.Char('New Name')
    #     def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
    #         fields['new_name'] = ", s.new_name as new_name"
    #         return super(PivotInheritReport, self)._query(with_clause, fields, groupby, from_clause)
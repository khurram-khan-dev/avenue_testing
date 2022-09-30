from odoo import models, api, fields, _
from odoo.exceptions import UserError


class INExtension(models.Model):
    _inherit = 'account.move'

    project_name        =   fields.Char('Project Name', compute='get_sale_order_reference')
    # project_name        =   fields.Char(string='Project Name',related='order_id.project_name.name')
    # project_name = fields.Many2one('project.name', string='Project Name')

    plot_size           =   fields.Char(string="Plot size",compute="get_plot")
    internal_ref        =   fields.Char(string="Internal Reference",compute="get_internal")
    price               =   fields.Integer(string="Sale Price",compute="get_price")
    cost                =   fields.Integer(string="Actual Cost",compute="get_cost_name")
    additional_price    =   fields.Integer(string="Additional price",compute="get_additional")
    discount_builder    =   fields.Integer(string="Discount by Builder",compute="get_dis_builder")
    gross_amount        =   fields.Integer(string="Gross Amount",compute="get_gross_amount")

    employee_name       =   fields.Char(string="Employee Name")
    unit_type           =   fields.Char(string="Unit Type")
    total_payable       =   fields.Integer(string="Total Payable")

    token_amount        =   fields.Integer(string="Amount Due")
    token_date          =   fields.Date(string="Due Date")

    f_deposit_amount        =   fields.Integer(string="Amount Due")
    f_deposit_date          =   fields.Date(string="Due Date")

    s_deposit_amount        =   fields.Integer(string="Amount Due")
    s_deposit_date          =   fields.Date(string="Due Date")

    t_deposit_amount        =   fields.Integer(string="Amount Due")
    t_deposit_date          =   fields.Date(string="Due Date")
    

    


    def get_sale_order_reference(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.project_name = res.project_name.name
    
    def get_plot(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.plot_size = res.plot_size.name

    def get_internal(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.internal_ref = res.internal_ref.name

    def get_price(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.price = res.price

    def get_cost_name(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.cost = res.cost
    
    def get_additional(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.additional_price = res.additional_price

    def get_dis_builder(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.discount_builder = res.discount_builder
    
    def get_gross_amount(self):

        for rec in self:
            res = rec.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            rec.gross_amount = res.gross_amount

    def action_post(self):
        result = super(INExtension, self).action_post()
        for inv in self:
            amount_tax = discount = 0.0
            for line in inv.invoice_line_ids:

                discount += line.price_subtotal
                # amount_tax += line.price_tax

            inv.update({
                'amount_untaxed': discount,
                # 'amount_tax': amount_tax,
                'amount_total': (self.gross_amount + self.amount_tax) - discount,
                'amount_residual': (self.gross_amount + self.amount_tax) - discount,
                'amount_total_signed':  (self.gross_amount + self.amount_tax) - discount,
            })

            # inv.amount_total_signed = abs(total) if move.move_type == 'entry' else -total

    # def action_check(self):
    #     for inv in self:
    #         amount_tax = discount = 0.0
    #         for line in inv.invoice_line_ids:

    #             discount += line.price_subtotal
    #             # amount_tax += line.price_tax

    #         inv.update({
    #             'amount_untaxed': discount,
    #             # 'amount_tax': amount_tax,
    #             'amount_total': (self.gross_amount + self.amount_tax) - discount,
    #         })

    
        
    # @api.onchange('gross_amount')
    def _amount_all(self):
        raise UserError(amount_untaxed)
        for inv in self:
            amount_tax = discount = 0.0
            for line in inv.invoice_line_ids:

                discount += line.price_subtotal
                amount_tax += line.price_tax

            inv.update({
                'amount_untaxed': discount,
                'amount_tax': amount_tax,
                'amount_total': (self.gross_amount + self.amount_tax) - discount,
            })

    


    #method:

    #   search order whose name is match wiht invoice origin
    #  get all value from that order and assign it

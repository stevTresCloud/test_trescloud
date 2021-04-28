# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        if self.is_new_enrollment and not self.partner_id.is_student:
            raise ValidationError('Debe seleccionar un Cliente que sea estudiante. Si quiere convertir a este cliente en estudiante, seleccione el campo "Es estudiante", en la configuracion del cliente %s.' % self.partner_id.name)
        # enrollment_object = 
        res = super(SaleOrder, self).action_confirm()
        return res
    
    # Columns
    is_new_enrollment = fields.Boolean(
        string=u'Is Enrollemnt transaction',
        help=u'With this field, we validate that the sale order is for a new Enrollment transaction.',
        default=False
    )
    enrollment_ids = fields.Many2many(
        'enrollment',
        string='Enrollment',
        help='Enrollment of the student, if this transaction is a new enrollment.',
        readonly=True,
        store=True
        )

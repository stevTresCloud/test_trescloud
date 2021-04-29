# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        # Con este método realizamos algunas validaciones y también creamos la matrícula
        if self.is_new_enrollment and not self.partner_id.is_student:
            raise ValidationError('Debe seleccionar un Cliente que sea estudiante. Si quiere convertir a este cliente en estudiante, seleccione el campo "Es estudiante", en la configuracion del cliente %s.' % self.partner_id.name)
        if len(self.order_line) > 1 and self.is_new_enrollment:
            raise ValidationError('La transacción se puede realizar un producto(curso) por matrícula. Si desea realizar otra matriculación, realice otra cotizzación.')
        if not self.order_line and self.is_new_enrollment:
            raise ValidationError('Seleccione un producto (curso) para realizar la matriculación.')
        res = super(SaleOrder, self).action_confirm()
        if self.is_new_enrollment:
            enrollment_object = self.env['enrollment']
            enrollment_dict = [{
                'student_partner_id': self.partner_id.id,
                'course_code': self.order_line.product_id.course_code,
                'sale_order_id': self.id
                }]
            # enrollment_list = [(0,0,enrollment_dict)]
            enrollment_id = enrollment_object.create(enrollment_dict)
            self.write({
                'enrollment_id': enrollment_id.id
                })
            self.partner_id.write({
                'enrollment_id': enrollment_id.id
                })
            return {
                'name': self.enrollment_id.name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': self.enrollment_id._name,
                'res_id': self.enrollment_id.id,
                # 'target': 'new',
                }
        return res
    
    # Columns
    is_new_enrollment = fields.Boolean(
        string=u'Is Enrollemnt transaction',
        help=u'With this field, we validate that the sale order is for a new Enrollment transaction.',
        default=False
    )
    enrollment_id = fields.Many2one(
        'enrollment',
        string='Enrollment',
        help='Enrollment of the student, if this transaction is a new enrollment.',
        readonly=True,
        store=True
        )

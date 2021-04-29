# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _enrollment_validations(self):
        # Se realiza varias validaciones antes de crear la matrícula
        for enrollment in self:
            if enrollment.is_new_enrollment and not enrollment.partner_id.is_student:
                raise ValidationError('Debe seleccionar un Cliente que sea estudiante. Si quiere convertir a este cliente en estudiante, seleccione el campo "Es estudiante", en la configuracion del cliente %s.' % self.partner_id.name)
            if len(enrollment.order_line) > 1 and enrollment.is_new_enrollment:
                raise ValidationError('La transacción se puede realizar, un producto(curso) por matrícula. Si desea realizar otra matriculación, realice otra cotización.')
            if not enrollment.order_line and enrollment.is_new_enrollment:
                raise ValidationError('Seleccione un producto (curso) para realizar la matriculación.')
            if enrollment.partner_id.enrollment_id and enrollment.partner_id.is_student:
                raise ValidationError('El cliente %s elegido ya tiene una matrícula asignada. No puede asignar más de dos matrículas a un cliente.' % self.partner_id.name)
            if not enrollment.is_new_enrollment and enrollment.enrollment_id and enrollment.enrollment_id.state == 'matriculate':
                raise ValidationError('El cliente %s elegido tiene una matrícula asignada. No puede quitar el check porque tiene una matrícula en estado "Matriculado".')
    
    def action_open_enrollment_form(self):
        # Abrimos el formulario de matrícula de esta cotización
        self.ensure_one()
        if self.is_new_enrollment and self.enrollment_id:
            return {
                'name': self.enrollment_id.name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': self.enrollment_id._name,
                'res_id': self.enrollment_id.id,
                # 'target': 'new',
                }
    
    def action_confirm(self):
        # Con este método creamos la matrícula e invocamos el método _enrollment_validations antes de crearlo
        for enrollment in self:
            enrollment._enrollment_validations()
        res = super(SaleOrder, self).action_confirm()
        for enrollment in self:
            if enrollment.is_new_enrollment:
                enrollment_object = enrollment.env['enrollment']
                enrollment_dict = [{
                    'student_partner_id': enrollment.partner_id.id,
                    'course_code': enrollment.order_line.product_id.course_code,
                    'sale_order_id': enrollment.id
                    }]
                # enrollment_list = [(0,0,enrollment_dict)]
                enrollment_id = enrollment_object.create(enrollment_dict)
                self.write({
                    'enrollment_id': enrollment_id.id
                    })
                self.partner_id.write({
                    'enrollment_id': enrollment_id.id
                    })
                if len(self) == 1:
                    enrollment.action_open_enrollment_form()
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

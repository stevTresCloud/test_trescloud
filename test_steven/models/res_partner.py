# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    def action_open_enrollment_form(self):
        # Abrimos el formulario de matrícula de esta cotización
        self.ensure_one()
        if self.is_student and self.enrollment_id:
            return {
                'name': self.enrollment_id.name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': self.enrollment_id._name,
                'res_id': self.enrollment_id.id,
                # 'target': 'new',
                }
    
    # Columns
    is_student = fields.Boolean(
        string='Is Student',
        help='With this field, we validate that the user is a student.',
        )
    enrollment_id = fields.Many2one(
        'enrollment',
        string='Enrollment',
        help='Enrollment of the student, if the user is a student.',
        readonly=True,
        store=True
        )

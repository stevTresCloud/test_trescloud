# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Enrollment(models.Model):
    _name = 'enrollment'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Enrollment of the student.'
    
    def action_matriculate_button(self):
        self.state = 'matriculate'
    
    def action_cancel(self):
        pass
    
    @api.model
    def create(self, vals):
        # Utilizamos el secuencial para el nombre de la matrícula
        if 'name' not in vals or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('enrollment.sequence') or _('New')
        return super(Enrollment, self).create(vals)
    
    # Columns
    name = fields.Char(
        string=u'Enrollment',
        help=u'Name of the enrollment.',
        readonly=True,
        store=True,
        default='New'
        )
    state = fields.Selection(
        [('draft', 'Draft'),
        ('matriculate', 'Matriculate'),
        ('cancel', 'Cancel')],
        default='draft'
        )
    student_partner_id = fields.Many2one(
        'res.partner',
        string='Student',
        help='Student of this enrollment.',
        required=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    day_trip = fields.Selection(
        [('morning', 'Morning'),
        ('evening', 'Evening')],
        help='Day trip in which the student will study.',
        default='morning',
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    start_date = fields.Date(
        string='Start Date',
        help='Starting day the career begins.',
        default=fields.Date.context_today,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    end_date = fields.Date(
        string='End Date',
        help='Ending day the career finish.',
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    course_code = fields.Char(
        string='Course Code',
        help='Course Code for the enrollment in the partner student.',
        required=True,
        readonly=True,
        store=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    career_enrollment_id = fields.Many2one(
        'career.enrollment',
        string='Career',
        help='Career that the student will follow.',
        required=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Transaction',
        help='Reference transaction where enrollment was created.',
        required=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )

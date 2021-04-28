# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Enrollment(models.Model):
    _name = 'enrollment'
    _description = 'Enrollment of the student.'
    
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
        [('draft', 'New'),
        ('approved', 'Approved'),
        ('matriculate', 'Matriculate')],
        required=True,
        default='draft'
        )
    student_partner_id = fields.Many2one(
        'res.partner',
        string='Student',
        help='Student of this enrollment.',
        required=True,
        states={'draft': [('readonly', False)]}
        )
    day_trip = fields.Selection(
        [('morning', 'Morning'),
        ('evening', 'Evening')],
        help='Day trip in which the student will study.',
        required=True,
        default='morning'
        )
    start_date = fields.Date(
        string='Start Date',
        help='Starting day the career begins.',
        required=True,
        default=fields.Date.context_today
        )
    end_date = fields.Date(
        string='End Date',
        help='Ending day the career finish.',
        required=True
        )
    course_level = fields.Selection(
        [('first', 'Course A'),
        ('second', 'Course B'),
        ('third', 'Course C')],
        required=True
        )
    career_enrollment_id = fields.Many2one(
        'career.enrollment',
        string='Career',
        help='Career that the student will follow.',
        required=True,
        states={'draft': [('readonly', False)]}
        )

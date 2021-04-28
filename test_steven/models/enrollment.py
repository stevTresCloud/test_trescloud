# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Enrollment(models.Model):
    _name = 'enrollment'
    _description = 'Enrollment of the student.'

    name = fields.Char(
        string=u'Enrollment',
        help=u'Name of the enrollment.',
        readonly=True,
        required=True,
        store=True
        )
    state = fields.Selection(
        [('draft', 'New'),
        ('approved', 'Approved'),
        ('matriculate', 'Matriculate')],
        store=True,
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
        help='',
        store=True,
        required=True,
        default='morning'
        )
    course_level = fields.Selection(
        [('first', 'Course A'),
        ('second', 'Course B'),
        ('third', 'Course C')],
        store=True,
        required=True
        )
    career_enrollment_id = fields.Many2one(
        'career.enrollment',
        string='Career',
        help='Career that the student will follow.',
        required=True,
        states={'draft': [('readonly', False)]}
        )

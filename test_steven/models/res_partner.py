# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Columns
    is_student = fields.Boolean(
        string='Is Student',
        help='With this field, we validate that the user is a student.',
    )
    enrollment_id = fields.Many2one(
        'enrollment',
        string='Enrollment',
        help='Enrollment of the student, if the user is a student.'
        )
    student_subject_id = fields.One2many(
        'student.subject',
        'student_id',
        string='Subjects',
        help='Subjects of the student',
        readonly=True,
        store=True
        )

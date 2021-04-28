# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class CareerEnrollment(models.Model):
    _name = 'career.enrollment'
    _description = 'Career that the student will follow.'
    
    # Columns
    name = fields.Char(
        string=u'Career',
        help=u'Name of the career.',
        required=True
        )
    description = fields.Char(
        string=u'Description',
        help=u'Description of the career.'
        )
    subjects_ids = fields.Many2many(
        'subject',
        string='Subjects',
        help='Subjects of the level',
        readonly=True
        )

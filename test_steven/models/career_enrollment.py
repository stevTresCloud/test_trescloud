# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class CareerEnrollment(models.Model):
    _name = 'career.enrollment'
    _description = 'Career that the student will follow.'
    
    name = fields.Char(
        string=u'Career',
        help=u'Name of the career.',
        required=True
        )
    description = fields.Char(
        string=u'Description',
        help=u'Description of the career.'
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
    levels_line_ids = depreciation_move_ids = fields.One2many(
        'career.enrollment.levels',
        'career_enrollment_id',
        string='Levels',
        help='Levels of the career',
        readonly=True
        )

    
class CareerEnrollmentLevels(models.Model):
    _name = 'career.enrollment.levels'
    _description = 'Levels of the career that the student will follow. By default there are three levels.'
    
    name = fields.Char(
        string=u'Career',
        help=u'Name of the career.',
        required=True
        )
    observation = fields.Char(
        string=u'Observation',
        help=u'Observation of the level.'
        )
    career_enrollment_id = fields.Many2one(
        'career.enrollment',
        string='Asset',
        help='Reference to the career.',
        ondelete='cascade',
        required=True
        )
    subjects_ids = fields.One2many(
        'subject',
        'level_id',
        string='Subjects',
        help='Subjects of the level',
        readonly=True
        )
    average_level = fields.Float(
        string="Average Level",
        help='Average of the level.',
        readonly=True
        )

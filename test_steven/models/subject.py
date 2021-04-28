# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Subject(models.Model):
    _name = 'subject'
    _description = 'Career Subject'
    
    # Columns
    name = fields.Char(
        string=u'Name subject',
        help=u'Name of the subject.',
        required=True
        )
    description = fields.Char(
        string=u'Description',
        help=u'Description of the subject. You can put any observation too.'
        )
    teacher_employee_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        help='Teacher who teaching the subject.',
        required=True
        )
    max_score = fields.Float(
        string="Max Score",
        help='Max Score of the subject',
        readonly=True
        )
    min_score = fields.Float(
        string="Min Score",
        help='Min Score of the subject',
        readonly=True
        )
    average = fields.Float(
        string="Average",
        help='Average of the three levels.',
        readonly=True
        )
    is_approved = fields.Selection(
        [('approved', 'Approved'),
        ('disapproved', 'Disapproved')],
        store=True,
        required=True,
        readonly=True
        )
    level_id = fields.Many2one(
        'career.enrollment.levels',
        string='Level Id',
        help='Reference to the level.',
        required=True
        )
    subject_syllabus_ids = fields.One2many(
        'subject.syllabus',
        'subject_id',
        string='Subjects Syllabus',
        help='Subjects syllabus',
        readonly=True
        )
    subject_scores_ids = fields.One2many(
        'subject.scores',
        'subject_id',
        string='Subjects Syllabus',
        help='Subjects syllabus',
        readonly=True
        )

    
class SubjectSyllabus(models.Model):
    _name = 'subject.syllabus'
    _description = 'Subject syllabus'
    
    # Columns
    name = fields.Char(
        string=u'Name syllabus',
        help=u'Name of the syllabus.',
        required=True
        )
    description = fields.Char(
        string=u'Description',
        help=u'Description of the syllabus. You can put any observation too.'
        )
    syllabus_hours = fields.Integer(
        string=u'Hours',
        help=u'Number of hours of the syllabus.',
        required=True 
        )
    subject_id = fields.Many2one(
        'subject',
        string='Subject',
        help='Reference of the subject.',
        required=True
        )


class SubjectScores(models.Model):
    _name = 'subject.scores'
    _description = 'Subject scores'
    
    # Columns
    name = fields.Char(
        string=u'Name Score',
        help=u'Name of the score.',
        required=True
        )
    score = fields.Float(
        string="Score",
        help='Score of the subject'
        )
    subject_id = fields.Many2one(
        'subject',
        string='Subject',
        help='Reference of the subject.',
        required=True
        )
    

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class StudentSubject(models.Model):
    _name = 'student.subject'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Student Subjects'
    
    # Columns
    name = fields.Many2one(
        'subject',
        string='Name Subject',
        help='Reference of the Subject.',
        required=True
        )
    subject_scores_ids = fields.One2many(
        'student.subject.scores',
        'student_subject_id',
        string='Subjects Syllabus',
        help='Subjects syllabus',
        readonly=True
        )
    min_score = fields.Float(
        string="Min Score",
        help='Min Score of the subject',
        readonly=True,
        store=True
        )
    max_score = fields.Float(
        string="Max Score",
        help='Max Score of the subject',
        readonly=True,
        store=True
        )
    average = fields.Float(
        string="Average",
        help='Average of the three levels.',
        readonly=True,
        store=True
        )
    is_approved = fields.Selection(
        [('approved', 'Approved'),
        ('disapproved', 'Disapproved')],
        required=True,
        readonly=True,
        store=True,
        )
    total_hours = fields.Integer(
        related="name.total_hours",
        string=u'Total Hours',
        help=u'Total of hours of the subject.',
        readonly=True,
        store=True
        )
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        help='Reference of the Student.',
        required=True
        )


class StudentSubjectScores(models.Model):
    _name = 'student.subject.scores'
    _description = 'Student subject scores'
    
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
    student_subject_id = fields.Many2one(
        'student.subject',
        string='Subject',
        help='Reference of the subject.',
        required=True
        )

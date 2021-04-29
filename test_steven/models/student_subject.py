# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class StudentSubject(models.Model):
    _name = 'student.subject'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Student Subjects'
    
    @api.onchange('subject_scores_ids')
    def _onchange_subject_scores_ids(self):
        for subject in self:
            if subject.subject_scores_ids:
                subject._compute_scores()
    
    @api.depends('min_score', 'max_score', 'average')
    def _compute_scores(self):
        for subject in self:
            subject.min_score = 0.0
            subject.max_score = 0.0
            subject.average = 0.0
            if subject.subject_scores_ids:
                subject.min_score = min(subj.score for subj in subject.subject_scores_ids)
                subject.max_score = max(subj.score for subj in subject.subject_scores_ids)
                subject.average = sum(subj.score for subj in subject.subject_scores_ids) / len(subject.subject_scores_ids)
                if subject.average > 7:
                    subject.is_approved = 'approved'
                else:
                    subject.is_approved = 'disapproved'
    
    # Columns
    name = fields.Many2one(
        'subject',
        string='Name Subject',
        help='Reference of the Subject.',
        required=True,
        readonly=True,
        store=True
        )
    subject_scores_ids = fields.One2many(
        'student.subject.scores',
        'student_subject_id',
        string='Subjects Syllabus',
        help='Subjects syllabus'
        )
    min_score = fields.Float(
        string="Min Score",
        help='Min Score of the subject',
        compute='_compute_scores'
        )
    max_score = fields.Float(
        string="Max Score",
        help='Max Score of the subject',
        compute='_compute_scores'
        )
    average = fields.Float(
        string="Average",
        help='Average of the three levels.',
        compute='_compute_scores',
        readonly=True,
        store=True
        )
    is_approved = fields.Selection(
        [('approved', 'Approved'),
        ('disapproved', 'Disapproved')]
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
        required=True,
        readonly=True,
        store=True
        )
    enrollment_student_id = fields.Many2one(
        'enrollment',
        string='Enrollment',
        help='Reference of the Student enrollment.'
        )


class StudentSubjectScores(models.Model):
    _name = 'student.subject.scores'
    _description = 'Student subject scores'
    
    @api.onchange('score')
    def onchange_score(self):
        for subject_score in self:
            subject_score._check_score()
    
    @api.constrains('score')
    def _check_score(self):
        for subject_score in self:
            if 0 > subject_score.score or subject_score.score > 10:
                subject_score.score = 0.0
                raise ValidationError('La nota no puede ser mayor que 10 o menor que 0') 
    
    # Columns
    name = fields.Char(
        string=u'Name Score',
        help=u'Name of the score.',
        required=True
        )
    score = fields.Float(
        string="Score",
        help='Score of the subject',
        required=True
        )
    student_subject_id = fields.Many2one(
        'student.subject',
        string='Subject',
        help='Reference of the subject.',
        required=True
        )

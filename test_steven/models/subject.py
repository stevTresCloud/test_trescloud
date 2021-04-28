# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Subject(models.Model):
    _name = 'subject'
    _description = 'Career Subject'
    
    @api.onchange('subject_syllabus_ids')
    def _onchange_subject_syllabus_ids(self):
        self._compute_total_subject_hours()
        
    @api.depends('total_hours')
    def _compute_total_subject_hours(self):
        total = 0
        if self.subject_syllabus_ids:
            total = sum(syllabus.syllabus_hours for syllabus in self.subject_syllabus_ids)
        self.total_hours = total
    
    # Columns
    name = fields.Char(
        string=u'Subject',
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
        readonly=True,
        store=True
        )
    total_hours = fields.Integer(
        string=u'Total Hours',
        compute='_compute_total_subject_hours',
        help=u'Total of hours of the subject.',
        readonly=True,
        store=True
        )
    career_id = fields.Many2one(
        'career.enrollment',
        string='Career',
        help='Reference to the career.',
        required=True
        )
    subject_syllabus_ids = fields.One2many(
        'subject.syllabus',
        'subject_id',
        string='Subjects Syllabus',
        help='Subjects syllabus'
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
    

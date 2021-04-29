# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Subject(models.Model):
    _name = 'subject'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Career Subject'
    
    @api.onchange('subject_syllabus_ids')
    def _onchange_subject_syllabus_ids(self):
        # Si hay un cambio en las líneas del temario, lanza el método _compute_total_subject_hours para recomputar
        for subject in self:
            subject._compute_total_subject_hours()
        
    @api.depends('total_hours')
    def _compute_total_subject_hours(self):
        # Con este método computamos el campo total_hours según las líneas subject_syllabus_ids
        # :return: Cero si no hay líneas subject_syllabus_ids, y devuelve la suma de las horas desde las líneas subject_syllabus_ids
        for subject in self:
            total = 0
            if subject.subject_syllabus_ids:
                total = sum(syllabus.syllabus_hours for syllabus in subject.subject_syllabus_ids)
            subject.total_hours = total
    
    @api.model    
    def create(self, vals):
        # Realizamos un super para evitar que se guarde el total de horas con horas negativas o cero
        if int(vals.get('total_hours', False)) <= 0 or not vals.get('subject_syllabus_ids'):
            raise ValidationError('La materia debe tener más de 0 horas totales, para guardar.')
        return super(Subject, self).create(vals)
    
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
    total_hours = fields.Integer(
        string=u'Total Hours',
        compute='_compute_total_subject_hours',
        help=u'Total of hours of the subject.'
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
    

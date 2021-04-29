# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime


class Enrollment(models.Model):
    _name = 'enrollment'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Enrollment of the student.'
    
    def action_button_to_student_subject(self):
        pass
    
    def action_matriculate_button(self):
        # Realizamos varias validaciones antes de matricular al estudiante
        for enrollment in self:
            if not enrollment.end_date or not enrollment.start_date:
                raise ValidationError('Ingrese una fecha de inicio o finalización de la carrera para la matricula del estudiante %s.' % enrollment.student_partner_id.name)
            if not enrollment.career_enrollment_id:
                raise ValidationError('Ingrese una carrera para la matricula del estudiante %s.' % enrollment.student_partner_id.name)
            if not enrollment.day_trip:
                raise ValidationError('Ingrese una jornada para la matricula del estudiante %s.' % enrollment.student_partner_id.name)
            student_subj_obj = enrollment.env['student.subject']
            student_subj_list = []
            for subject in enrollment.career_enrollment_id.subjects_ids:
                student_subj_dict = {
                    'student_id': enrollment.student_partner_id.id,
                    'name' : subject.id
                    }
                student_subj_list.append((0,0,student_subj_dict))
            # subjects_create = student_subj_obj.create(student_subj_list)
            enrollment.write({
                'student_subjects_ids' : student_subj_list
                })
            enrollment.state = 'matriculate'
    
    def action_cancel(self):
        pass
    
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
        [('draft', 'Draft'),
        ('matriculate', 'Matriculate'),
        ('cancel', 'Cancel')],
        default='draft'
        )
    student_partner_id = fields.Many2one(
        'res.partner',
        string='Student',
        help='Student of this enrollment.',
        required=True,
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    day_trip = fields.Selection(
        [('morning', 'Morning'),
        ('evening', 'Evening')],
        help='Day trip in which the student will study.',
        default='morning',
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    start_date = fields.Date(
        string='Start Date',
        help='Starting day the career begins.',
        default=datetime.today(),
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    end_date = fields.Date(
        string='End Date',
        help='Ending day the career finish.',
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    course_code = fields.Char(
        string='Course Code',
        help='Course Code for the enrollment in the partner student.',
        readonly=True,
        store=True,
        states={'draft': [('readonly', True)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    career_enrollment_id = fields.Many2one(
        'career.enrollment',
        string='Career',
        help='Career that the student will follow.',
        states={'draft': [('readonly', False)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Transaction',
        help='Reference transaction where enrollment was created.',
        states={'draft': [('readonly', True)], 'matriculate': [('readonly', True)],'cancel': [('readonly', True)]}
        )
    student_subjects_ids = fields.One2many(
        'student.subject',
        'enrollment_student_id',
        string='Subjects',
        help='Subjects of the student'
        )

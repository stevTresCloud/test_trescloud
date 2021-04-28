# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Columns
    is_course = fields.Boolean(
        string=u'Is curse',
        help=u'With this field, we validate that the product is for a course.',
    )
    course_code = fields.Char(
        string=u'Course Code',
        help=u'With this field, the teacher can filtered by course code in the search of products'
    )

# -*- coding: utf-8 -*-
# from odoo import http


# class TestSteven(http.Controller):
#     @http.route('/test_steven/test_steven/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_steven/test_steven/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_steven.listing', {
#             'root': '/test_steven/test_steven',
#             'objects': http.request.env['test_steven.test_steven'].search([]),
#         })

#     @http.route('/test_steven/test_steven/objects/<model("test_steven.test_steven"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_steven.object', {
#             'object': obj
#         })

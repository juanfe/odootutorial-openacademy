# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import fields, osv

class Course(osv.Model):
    _name = 'openacademy.course'
    _columns = {
        'name' : fields.char('Title'),
        'description' : fields.text('Description'),
    }

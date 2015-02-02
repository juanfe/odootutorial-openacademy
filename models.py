# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import fields, osv

class Course(osv.Model):
    _name = 'openacademy.course'
    _columns = {
        'name' : fields.char('Title'),
        'description' : fields.text('Description'),
    }

class Session(osv.Model):
    _name = 'openacademy.session'
    _columns = {
        'name' : fields.char(required=True),
        'start_date' : fields.date(default=fields.date.today),
        'duration' : fields.float(digits=(6,2), help="Duration in days"),
        'seats' : fields.integer(string="Number of seats"),
    }

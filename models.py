# -*- coding: utf-8 -*-

from openerp import api
from openerp.osv import fields, osv

class Course(osv.Model):
    _name = 'openacademy.course'
    _columns = {
        'name' : fields.char('Title'),
        'description' : fields.text('Description'),

        'responsible_id' : fields.many2one('res.users',
                on_delete="set null", string="Responsible", index=True),
        'session_ids' : fields.one2many('openacademy.session', 'course_id',
                        string='Sessions'),
    }

class Session(osv.Model):
    _name = 'openacademy.session'
    _columns = {
        'name' : fields.char('Name', required=True),
        'start_date' : fields.date('Start date', default=fields.date.today),
        'duration' : fields.float('Duration', digits=(6,2), help="Duration in days"),
        'seats' : fields.integer(string="Number of seats"),

        'instructor_id' : fields.many2one('res.partner', string="Instructor"),
        'course_id' : fields.many2one('openacademy.course',
                ondelete = "cascade", string = "Course", required = True),
    }

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
        'active' : fields.boolean('Active', default=True),

        'instructor_id' : fields.many2one('res.partner', string="Instructor",
                domain=['|', ('instructor', '=', True),
                             ('category_id.name', 'ilike', "Teacher")]),
        'course_id' : fields.many2one('openacademy.course',
                ondelete = "cascade", string = "Course", required = True),
        'attendee_ids' : fields.many2many('res.partner', string='Attendees'),

        'taken_seats' : fields.float(string="Taken seats", compute='_taken_seats'),
    }

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len (self.attendee_ids) / self.seats

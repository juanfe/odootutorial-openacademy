# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from openerp import api, exceptions
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

    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
            ('name_description_check',
             'CHECK(name != description)',
             "The title of teh course should not be teh description"),

            ('name_unique',
             'UNIQUE(name)',
             "The course title must be unique"),
            ]

class Session(osv.Model):
    _name = 'openacademy.session'
    _columns = {
        'name' : fields.char('Name', required=True),
        'start_date' : fields.date('Start date', default=fields.date.today),
        'duration' : fields.float('Duration', digits=(6,2), help="Duration in days"),
        'seats' : fields.integer(string="Number of seats"),
        'active' : fields.boolean('Active', default=True),
        'color' : fields.integer(),

        'instructor_id' : fields.many2one('res.partner', string="Instructor",
                domain=['|', ('instructor', '=', True),
                             ('category_id.name', 'ilike', "Teacher")]),
        'course_id' : fields.many2one('openacademy.course',
                ondelete = "cascade", string = "Course", required = True),
        'attendee_ids' : fields.many2many('res.partner', string='Attendees'),

        'taken_seats' : fields.float(string="Taken seats", compute='_taken_seats'),
        'end_date' : fields.date(string="End Date", store=True,
                        compute='_get_end_date', inverse='_set_end_date'),

        'hours' : fields.float('Duration in hours', compute='_get_hours', inverse='_set_hours'),

        'attendees_count' : fields.integer(
                        string="Attendess count", compute='_get_attendees_count', store=True),

        'state' : fields.selection([
                    ('draft', "Draft"),
                    ('confirmed', "Confirmed"),
                    ('done', "Done"),
                ], default='draft'),
    }

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.taken_seats = 0.0
        else:
            self.taken_seats = 100.0 * len (self.attendee_ids) / self.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }

    @api.one
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        if not (self.start_date and self.duration):
            self.end_date = self.start_date
            return

        # Add duration to start_date, but: Monday + 5 days = Saturday, so
        # subtract one second to get on Friday instead
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        duration = timedelta(days=self.duration, seconds=-1)
        self.end_date = start + duration

    @api.one
    def _set_end_date(self):
        if not (self.start_date and self.end_date):
            return

        # Compute the difference between dates, bu: Friday = 4 days,
        # so add one day to get 5 days instead
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d")
        self.duration = (end_date - start_date).days + 1

    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24

    @api.one
    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError("A session's instructor can't be an attendee")

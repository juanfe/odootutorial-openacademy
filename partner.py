# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class Partner(osv.Model):
    _inherit = 'res.partner'

    _columns = {
        'instructor' : fields.boolean("Instructor", default=False),

        'session_ids' : fields.many2many('openacademy.session',
            string="Attended Sessions", readonly=True),
    }

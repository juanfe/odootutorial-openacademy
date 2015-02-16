from openerp.tests.common import TransactionCase

class TestSession(TransactionCase):
    """Test for Session"""

    def test_session(self):
        # This test must be fail because is course_id is required
        record = self.env['openacademy.session'].create({'name': 'Nueva session'})
        self.assertEqual(record.name, 'Nueva session')

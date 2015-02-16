from openerp.tests.common import TransactionCase

class TestCourse(TransactionCase):
    """Test for Course"""

    def test_course(self):
        record = self.env['openacademy.course'].create({'name': 'Curso nuevo',
                'description': 'None description'})
        self.assertEqual(record.name, 'Curso nuevo')

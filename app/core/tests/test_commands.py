"""
Test custom django management commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# mocking the check method to simulate the response from the db
# patch adds a new arg to our test calls as patched_check


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test commands
    """

    def test_wait_for_db_ready(self, patched_check):
        """
        test waiting for dsatabase if ready
        """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Tests waiting for db when getting operational error
        """
        # what patched_check.side_effect says is that\
        #  it'll check the db a total of 6 times,
        # two of which it'll return a Psycopg2Error error,\
        #  three an OperationalError
        # and the last time it'll return true, indicatiing\
        #  successful connection of the test db
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

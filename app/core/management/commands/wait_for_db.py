"""
Django command to wait for the DB to be
available
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django command to wait for DB
    """

    def handle(self, *args, **kwargs):
        """
        Entry point for command
        """
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2OpError, OperationalError):
                self.stSdout.write('Database unavailable, \
                    waiting for 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))

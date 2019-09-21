from datetime import datetime

from django.test import TestCase

from condottieri_events.management.commands.clean_events import Command

class CommandTestCase(TestCase):

    def test_handle_noargs(self):
        command = Command()
        self.assertIsNone(command.handle_noargs())
    

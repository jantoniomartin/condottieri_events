from django.test import TestCase #, override_settings
from django.contrib.auth.models import User

from condottieri_events.models import *
from machiavelli.models import Game
from condottieri_scenarios.models import Area

class BaseTestCase(TestCase):

    fixtures = ['users.yaml',
            'settings.yaml',
            'scenarios.yaml',
            'games.yaml',
            ]

    def setUp(self):
        self.game = Game.objects.get(id=1)
        self.area_1 = Area.objects.create(setting=self.game.scenario.setting,
                name_en = "Albacete",
                code = "ALB")
        self.event_1 = StandoffEvent.objects.create(game=self.game, year=0, season=0,
                phase=0, classname="StandoffEvent", area=self.area_1)

    def test_get_concrete(self):
        self.assertIn("Albacete", str(self.event_1.get_concrete()))

    def test_unit_string(self):
        self.assertEqual(self.event_1.unit_string("A", self.area_1), "the army in Albacete")
        self.assertEqual(self.event_1.unit_string("F", self.area_1), "the fleet in Albacete")
        self.assertEqual(self.event_1.unit_string("G", self.area_1), "the garrison in Albacete")

    def test_season_class(self):
        self.assertEqual(self.event_1.season_class(), "season_0")

    def test_event_class(self):
        self.assertEqual(self.event_1.event_class(), "standoff-event")

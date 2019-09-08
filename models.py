## Copyright (c) 2010 by Jose Antonio Martin <jantonio.martin AT gmail DOT com>
## This program is free software: you can redistribute it and/or modify it
## under the terms of the GNU Affero General Public License as published by the
## Free Software Foundation, either version 3 of the License, or (at your option
## any later version.
##
## This program is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
## for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/agpl.txt>.
##
## This license is also included in the file COPYING
##
## AUTHOR: Jose Antonio Martin <jantonio.martin AT gmail DOT com>

""" This application manages the log of events during a Condottieri game.

"""

## django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import capfirst

## machiavelli
import machiavelli.models as machiavelli
import machiavelli.signals as signals

import condottieri_scenarios.models as scenarios

class BaseEvent(models.Model):
	"""
BaseEvent is the parent class for all kind of game events.
	"""
	game = models.ForeignKey(machiavelli.Game)
	year = models.PositiveIntegerField()
	season = models.PositiveIntegerField(choices=machiavelli.SEASONS)
	phase = models.PositiveIntegerField(choices=machiavelli.GAME_PHASES)
	classname = models.CharField(max_length=32, editable=False)
	
	def get_concrete(self):
		""" Gets the name of the child class of this BaseEvent """
		return self.__getattribute__(self.classname.lower())

	def unit_string(self, type, area):
		""" Returns a string like **the garrison in Naples** """
		if type == 'A':
			return _("the army in %s") % area.name
		elif type == 'F':
			return _("the fleet in %s") % area.name
		elif type == 'G':
			return _("the garrison in %s") % area.name

	def season_class(self):
		""" Returns a css class name for the game season """
		return "season_%s" % self.season

	def event_class(self):
		""" Returns a css class name depending on the type of event """
		return self.get_concrete().event_class()

	def country_class(self):
		""" Returns a css class name if the event is related to a country """
		try:
			country = self.get_concrete().country.static_name
		except:
			country = ''
		return country
	
	def color_output(self):
		""" Returns a html list item with season and event styles """
		return "<li class=\"%(season_class)s %(event_class)s\"><span class=\"%(country_class)s\">%(log)s</span></li>" % {
							'season_class': self.season_class(),
							'event_class': self.event_class(),
							'country_class': self.country_class(),
							'log': capfirst(self)
							}

	def __unicode__(self):
		return str(self.get_concrete())
	
	class Meta:
		abstract = False
		ordering = ['-year', '-season', '-id']

def log_event(event_class, game, **kwargs):
	""" Creates a new BaseEvent and its child event. """
	try:
		event = event_class(game=game, year=game.year, season=game.season, phase=game.phase, **kwargs)
		event.save()
	except:
		pass

class NewUnitEvent(BaseEvent):
	""" Event triggered when a new unit is placed in the map. """

	country = models.ForeignKey(scenarios.Country)
	type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	area = models.ForeignKey(scenarios.Area)
	
	def event_class(self):
		return "new-unit-event"

	def __unicode__(self):
		return _("New %(type)s in %(area)s.") % {
						'country': self.country,
						'type': self.get_type_display(),
						'area': self.area.name
						}

def log_new_unit(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(NewUnitEvent, sender.player.game,
					classname="NewUnitEvent",
					country=sender.player.contender.country,
					type=sender.type,
					area=sender.area.board_area)

signals.unit_placed.connect(log_new_unit)

class DisbandEvent(BaseEvent):
	""" Event triggered when a unit is disbanded. """
	country = models.ForeignKey(scenarios.Country, blank=True, null=True)
	type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	area = models.ForeignKey(scenarios.Area)

	def event_class(self):
		return "disband-event"

	def __unicode__(self):
		if self.country:
			return _("%(type)s in %(area)s is disbanded.") % {
						'country': self.country,
						'type': self.get_type_display(),
						'area': self.area.name
						}
		else:
			return _("Autonomous %(type)s in %(area)s is disbanded.") % {
						'type': self.get_type_display(),
						'area': self.area.name}
			
def log_disband(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(DisbandEvent, sender.player.game,
					classname="DisbandEvent",
					country=sender.player.contender.country,
					type=sender.type,
					area=sender.area.board_area)

signals.unit_disbanded.connect(log_disband)

class OrderEvent(BaseEvent):
	""" Event triggered when an order is confirmed. """
	country = models.ForeignKey(scenarios.Country)
	type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	origin = models.ForeignKey(scenarios.Area, related_name='event_origin')
	code = models.CharField(max_length=1, choices=machiavelli.ORDER_CODES)
	destination = models.ForeignKey(scenarios.Area, blank=True, null=True, related_name='event_destination')
	conversion = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES, blank=True, null=True)
	subtype = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES, blank=True, null=True)
	suborigin = models.ForeignKey(scenarios.Area, related_name='event_suborigin', blank=True, null=True)
	subcode = models.CharField(max_length=1, choices=machiavelli.ORDER_CODES, blank=True, null=True)
	subdestination = models.ForeignKey(scenarios.Area, blank=True, null=True, related_name='event_subdestination')
	subconversion = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES, blank=True, null=True)

	def event_class(self):
		return "order-event"

	def __unicode__(self):
		return self.get_message()
		#country_info = "<small>(%s)</small>" % (unicode(self.country),)
		#msg = self.get_message()
		#return "%s %s" % (country_info, msg)
	
	def get_message(self):
		unit = self.unit_string(self.type, self.origin)
		if self.code == '-':
			msg = _("%(unit)s tries to go to %(area)s.") % {
							'unit': unit,
							'area': self.destination.name
							}
		elif self.code == 'B':
			msg = _("%(unit)s besieges the city.") % {'unit': unit}
		elif self.code == '=':
			msg = _("%(unit)s tries to convert into %(type)s.") % {
							'unit': unit,
							'type': self.get_conversion_display()
							}
		elif self.code == 'C':
			msg = _("%(unit)s must convoy %(subunit)s to %(area)s.") % {
							'unit': unit,
							'subunit': self.unit_string(self.subtype,
														self.suborigin),
							'area': self.subdestination.name
							}
		elif self.code == 'S':
			if self.subcode == 'H':
				msg=_("%(unit)s supports %(subunit)s to hold its position.") % {
							'unit': unit,
							'subunit': self.unit_string(self.subtype,
														self.suborigin)
							}
			elif self.subcode == '-':
				msg = _("%(unit)s supports %(subunit)s to go to %(area)s.") % {
							'unit': unit,
							'subunit': self.unit_string(self.subtype,
														self.suborigin),
							'area': self.subdestination.name
							}
			elif self.subcode == '=':
				msg = _("%(unit)s supports %(subunit)s to convert into %(type)s.") % {
							'unit': unit,
							'subunit': self.unit_string(self.subtype,
														self.suborigin),
							'type': self.get_subconversion_display()
							}
		return msg

def log_order(sender, **kwargs):
	assert isinstance(sender, machiavelli.Order), "sender must be an Order"
	try:
		destination = sender.destination.board_area
	except:
		destination = None
	if isinstance(sender.subunit, machiavelli.Unit):
		subtype = sender.subunit.type
		suborigin = sender.subunit.area.board_area
	else:
		subtype = None
		suborigin = None
	try:
		subdestination = sender.subdestination.board_area
	except:
		subdestination = None
	log_event(OrderEvent, sender.unit.player.game,
					classname="OrderEvent",
					country = sender.player.contender.country,
					type = sender.unit.type,
					origin = sender.unit.area.board_area,
					code = sender.code,
					destination = destination,
					conversion = sender.type,
					subtype = subtype,
					suborigin = suborigin,
					subcode = sender.subcode,
					subdestination = subdestination,
					subconversion = sender.subtype)

signals.order_placed.connect(log_order)

class StandoffEvent(BaseEvent):
	""" Event triggered when a standoff happens. """
	area = models.ForeignKey(scenarios.Area)

	def event_class(self):
		return "standoff-event"

	def __unicode__(self):
		return _("Conflicts in %(area)s result in a standoff.") % {
						'area': self.area.name,
						}

def log_standoff(sender, **kwargs):
	assert isinstance(sender, machiavelli.GameArea), "sender must be a GameArea"
	log_event(StandoffEvent, sender.game,
					classname="StandoffEvent",
					area = sender.board_area)

signals.standoff_happened.connect(log_standoff)

class ConversionEvent(BaseEvent):
	""" Event triggered when a unit changes its type. """

	country = models.ForeignKey(scenarios.Country, null=True, blank=True)
	area = models.ForeignKey(scenarios.Area)
	before = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	after = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)

	def event_class(self):
		return "conversion-event"

	def __unicode__(self):
		return _("%(unit)s converts into %(type)s.") % {
						'unit': self.unit_string(self.before, self.area),
						'type': self.get_after_display()
						}

def log_conversion(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(ConversionEvent, sender.player.game,
					classname="ConversionEvent",
					country=sender.player.contender.country,
					area=sender.area.board_area,
					before=kwargs["before"],
					after=kwargs["after"])

signals.unit_converted.connect(log_conversion)

class ControlEvent(BaseEvent):
	""" Event triggered when a player gets the control of a province. """
	country = models.ForeignKey(scenarios.Country)
	area = models.ForeignKey(scenarios.Area)
	new_home = models.BooleanField(default=False)

	def event_class(self):
		return "control-event"

	def __unicode__(self):
		if self.new_home:
			return _("%(area)s is now home of %(country)s.") % {
						'country': self.country,
						'area': self.area.name
						}
		else:
			return _("%(country)s gets control of %(area)s.") % {
						'country': self.country,
						'area': self.area.name
						}

def log_control(sender, **kwargs):
	assert isinstance(sender, machiavelli.GameArea), "sender must be a GameArea"
	log_event(ControlEvent, sender.player.game,
					classname="ControlEvent",
					country=sender.player.contender.country,
					area=sender.board_area,
					new_home=kwargs["new_home"])

signals.area_controlled.connect(log_control)

class MovementEvent(BaseEvent):
	""" Event triggered when a unit moves to a different province. """

	country = models.ForeignKey(scenarios.Country, null=True, blank=True)
	type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	origin = models.ForeignKey(scenarios.Area, related_name="movement_origin")
	destination = models.ForeignKey(scenarios.Area, related_name="movement_destination")

	def event_class(self):
		return "movement-event"

	def __unicode__(self):
		return _("%(unit)s advances into %(destination)s.") % {
				'unit': self.unit_string(self.type,	self.origin),
				'destination': self.destination.name
				}

def log_movement(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(MovementEvent, sender.player.game,
					classname="MovementEvent",
					country = sender.player.contender.country,
					type=sender.type,
					origin=sender.area.board_area,
					destination=kwargs['destination'].board_area)

signals.unit_moved.connect(log_movement)

class RetreatEvent(BaseEvent):
	""" Event triggered when a unit retreats. """

	country = models.ForeignKey(scenarios.Country, null=True, blank=True)
	type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	origin = models.ForeignKey(scenarios.Area, related_name="retreat_origin")
	destination = models.ForeignKey(scenarios.Area, related_name="retreat_destination")

	def event_class(self):
		return "movement-event"

	def __unicode__(self):
		if self.origin == self.destination:
			return _("%(unit)s garrisons in the city.") % {
					'unit': self.unit_string(self.type,	self.origin),
					'destination': self.destination.name
					}
		else:
			return _("%(unit)s retreats to %(destination)s.") % {
					'unit': self.unit_string(self.type,	self.origin),
					'destination': self.destination.name
					}

def log_retreat(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(RetreatEvent, sender.player.game,
					classname="RetreatEvent",
					country = sender.player.contender.country,
					type=sender.type,
					origin=sender.area.board_area,
					destination=kwargs['destination'].board_area)

signals.unit_retreated.connect(log_retreat)

UNIT_EVENTS = (
	(0, _('cannot carry out its support order.')),
	(1, _('must retreat.')),
	(2, _('surrenders.')),
	(3, _('is now besieging.')),
	(4, _('changes of country.')),
	(5, _('becomes autonomous.')),
)

class UnitEvent(BaseEvent):
	""" Event triggered when a unit is subject to some conditions.

	Currently, the conditions are:
	
	* The unit cannot carry out its support order.
	
	* The unit must retreat.
	
	* The unit surrenders (because of a siege).
	
	* The unit starts a siege.

	* The unit changes of country because of a bribe.

	* The unit becomes autonomous because of a bribe.
	
	Each condition must have its own signal.
	"""

	country = models.ForeignKey(scenarios.Country, null=True, blank=True)
	type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES)
	area = models.ForeignKey(scenarios.Area)
	message = models.PositiveIntegerField(choices=UNIT_EVENTS)
	
	def event_class(self):
		if self.message == 0:
			return 'broken-support-event'
		elif self.message == 1:
			return 'retreat-event'
		elif self.message == 2:
			return 'surrender-event'
		elif self.message == 3:
			return 'besieging-event'
		elif self.message == 4 or self.message == 5:
			return 'bribe-event'

	def __unicode__(self):
		return "%(unit)s %(message)s" % {
						'unit': self.unit_string(self.type, self.area),
						'message': self.get_message_display()
						}

def log_broken_support(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(UnitEvent, sender.player.game,
					classname="UnitEvent",
					country = sender.player.contender.country,
					type=sender.type,
					area=sender.area.board_area,
					message=0)

signals.support_broken.connect(log_broken_support)

def log_forced_retreat(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(UnitEvent, sender.player.game,
				classname="UnitEvent",
				country = sender.player.contender.country,
				type=sender.type,
				area=sender.area.board_area,
				message=1)

signals.forced_to_retreat.connect(log_forced_retreat)

def log_unit_surrender(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(UnitEvent, sender.player.game,
				classname="UnitEvent",
				country = sender.player.contender.country,
				type=sender.type,
				area=sender.area.board_area,
				message=2)

signals.unit_surrendered.connect(log_unit_surrender)

def log_siege_start(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(UnitEvent, sender.player.game,
				classname="UnitEvent",
				country = sender.player.contender.country,
				type=sender.type,
				area=sender.area.board_area,
				message=3)

signals.siege_started.connect(log_siege_start)
	
def log_change_country(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(UnitEvent, sender.player.game,
				classname="UnitEvent",
				country = sender.player.contender.country,
				type=sender.type,
				area=sender.area.board_area,
				message=4)

signals.unit_changed_country.connect(log_change_country)

def log_to_autonomous(sender, **kwargs):
	assert isinstance(sender, machiavelli.Unit), "sender must be a Unit"
	log_event(UnitEvent, sender.player.game,
				classname="UnitEvent",
				country = sender.player.contender.country,
				type=sender.type,
				area=sender.area.board_area,
				message=5)

signals.unit_to_autonomous.connect(log_to_autonomous)

COUNTRY_EVENTS = (
	(0, _('Government has been overthrown')),
	(1, _('Has been conquered')),
	(2, _('Has been declared enemy of Christendom')),
	(3, _('Has been eliminated')),
	(4, _('Leader has been assassinated')),
	(5, _('Excommunication has been lifted')),
	(6, _('Leader suffered an assassination attempt')),
)

class CountryEvent(BaseEvent):
	""" Event triggered when a country is subject to some conditions.

	Currently, the conditions are:
	
	* A new player (not playing) takes the control of the country.
	
	* The country has been conquered.
	
	* The country has been excommunicated.

	* The country has been eliminated.

	* The leader has been assassinated.

	* An excommunication has been lifted.

	* An assassination has been attempted.
	
	Each condition must have its own signal.
	"""
	country = models.ForeignKey(scenarios.Country)
	message = models.PositiveIntegerField(choices=COUNTRY_EVENTS)

	def __unicode__(self):
		return "%(country)s: %(message)s" % {
									'country': self.country.name,
									'message': self.get_message_display()
									}
	
	def event_class(self):
		return "season_%(season)s" % {'season': self.season}

def log_overthrow(sender, **kwargs):
	assert isinstance(sender, machiavelli.Revolution), "sender must be a Revolution"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = sender.country,
					message = 0)

signals.government_overthrown.connect(log_overthrow)

def log_conquering(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = kwargs['country'],
					message = 1)

signals.country_conquered.connect(log_conquering)

def log_excommunication(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = sender.contender.country,
					message = 2)

signals.country_excommunicated.connect(log_excommunication)

def log_elimination(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = kwargs['country'],
					message = 3)

signals.country_eliminated.connect(log_elimination)

def log_assassination(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = sender.contender.country,
					message = 4)

signals.player_assassinated.connect(log_assassination)

def log_lifted_excommunication(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = sender.contender.country,
					message = 5)

signals.country_forgiven.connect(log_lifted_excommunication)

def log_assassination_attempt(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(CountryEvent, sender.game,
					classname="CountryEvent",
					country = sender.contender.country,
					message = 6)

signals.assassination_attempted.connect(log_assassination_attempt)

DISASTER_EVENTS = (
	(0, _('%(area)s is affected by famine.')),
	(1, _('%(area)s has been affected by plague.')),
	(2, _('A rebellion has broken out in %(area)s.')),
	(3, _('%(area)s is affected by a storm.')),
)

class DisasterEvent(BaseEvent):
	""" Event triggered when a province is affected by a disaster.

	Currently, the conditions are:
	
	* The province is affected by famine.
	
	* The province is affected by plague.

	* The province is affected by a rebellion.

	* The sea is affected by a storm
	
	Each condition must have its own signal.
	"""
	area = models.ForeignKey(scenarios.Area)
	message = models.PositiveIntegerField(choices=DISASTER_EVENTS)

	def __unicode__(self):
		msg = self.get_message_display()
		return msg % {'area': self.area.name,}
	
	def event_class(self):
		if self.message == 0:
			return "famine-event"
		elif self.message == 1:
			return "plague-event"
		elif self.message == 2:
			return "rebellion-event"
		elif self.message == 3:
			return "storm-event"
		else:
			return ""

def log_famine_marker(sender, **kwargs):
	assert isinstance(sender, machiavelli.GameArea), "sender must be a GameArea"
	log_event(DisasterEvent, sender.game,
					classname="DisasterEvent",
					area = sender.board_area,
					message = 0)

signals.famine_marker_placed.connect(log_famine_marker)

def log_plague(sender, **kwargs):
	assert isinstance(sender, machiavelli.GameArea), "sender must be a GameArea"
	log_event(DisasterEvent, sender.game,
					classname="DisasterEvent",
					area = sender.board_area,
					message = 1)

signals.plague_placed.connect(log_plague)

def log_rebellion(sender, **kwargs):
	assert isinstance(sender, machiavelli.GameArea), "sender must be a GameArea"
	log_event(DisasterEvent, sender.game,
					classname="DisasterEvent",
					area = sender.board_area,
					message = 2)

signals.rebellion_started.connect(log_rebellion)

def log_storm_marker(sender, **kwargs):
	assert isinstance(sender, machiavelli.GameArea), "sender must be a GameArea"
	log_event(DisasterEvent, sender.game,
					classname="DisasterEvent",
					area = sender.board_area,
					message = 3)

signals.storm_marker_placed.connect(log_storm_marker)

class IncomeEvent(BaseEvent):
	""" Event triggered when a country receives income """
	country = models.ForeignKey(scenarios.Country)
	ducats = models.PositiveIntegerField()

	def event_class(self):
		return "income-event"

	def __unicode__(self):
		return _("%(country)s raises %(ducats)s ducats.") % {
						'country': self.country,
						'ducats': self.ducats,
						}

def log_income(sender, **kwargs):
	assert isinstance(sender, machiavelli.Player), "sender must be a Player"
	log_event(IncomeEvent, sender.game,
					classname="IncomeEvent",
					country=sender.contender.country,
					ducats=kwargs['ducats'])

signals.income_raised.connect(log_income)

class ExpenseEvent(BaseEvent):
	country = models.ForeignKey(scenarios.Country)
	ducats = models.PositiveIntegerField(default=0)
	type = models.PositiveIntegerField(choices=machiavelli.EXPENSE_TYPES)
	area = models.ForeignKey(scenarios.Area, null=True, blank=True)
	unit_type = models.CharField(max_length=1, choices=machiavelli.UNIT_TYPES, null=True, blank=True)

	def event_class(self):
		return "expense-event"

	def __unicode__(self):
		data = {
			'country': self.country,
			'ducats' : self.ducats,
			'area'   : self.area,
			'unit'   : self.unit_string(self.unit_type, self.area),
		}

		if self.type == 0:
			msg = _("%(country)s pays %(ducats)sd to relief famine in %(area)s")
		elif self.type == 1:
			msg = _("%(country)s pays %(ducats)sd to pacify the rebellion in %(area)s")
		elif self.type in (2, 3):
			msg = _("%(country)s pays %(ducats)sd to cause a rebellion in %(area)s")
		elif self.type == 4:
			msg = _("%(country)s pays %(ducats)sd to protect %(unit)s from bribes")
		elif self.type in (5, 8):
			msg = _("%(country)s pays %(ducats)sd to disband %(unit)s")
		elif self.type in (6, 9):
			msg = _("%(country)s pays %(ducats)sd to buy %(unit)s")
		elif self.type == 7:
			msg = _("%(country)s pays %(ducats)sd to turn %(unit)s into an autonomous garrison")
		else:
			msg = _("Unknown expense")
		return msg % data

def log_expense(sender, **kwargs):
	assert isinstance(sender, machiavelli.Expense), "sender must be an Expense"
	if sender.unit:
		_area = sender.unit.area.board_area
		_unit_type = sender.unit.type
	else:
		_area = sender.area.board_area
		_unit_type = ""
	log_event(ExpenseEvent, sender.player.game,
					classname="ExpenseEvent",
					country=sender.player.contender.country,
					ducats=sender.ducats,
					type=sender.type,
					area=_area,
					unit_type=_unit_type)

signals.expense_paid.connect(log_expense)

class UncoverEvent(BaseEvent):
	""" Event triggered when a diplomat is uncovered. """
	country = models.ForeignKey(scenarios.Country, blank=True, null=True)
	area = models.ForeignKey(scenarios.Area)

	def event_class(self):
		return "uncover-event"

	def __unicode__(self):
		return _("A spy from %(country)s is uncovered in %(area)s.") % {
					'country': self.country,
					'area': self.area.name
					}
			
def log_uncover(sender, **kwargs):
	assert isinstance(sender, machiavelli.Diplomat), "sender must be a Diplomat"
	log_event(UncoverEvent, sender.player.game,
					classname="UncoverEvent",
					country=sender.player.contender.country,
					area=sender.area.board_area)

signals.diplomat_uncovered.connect(log_uncover)


import condottieri_events.models as events
from django.contrib import admin

class BaseEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase')

class NewUnitEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year')
	list_filter = ('game', 'year')

class DisbandEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase')

class OrderEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', 'country', '__str__', 'year', 'season')
	list_filter = ('game', 'country', 'year', 'season')

class StandoffEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season')
	list_filter = ('game', 'year', 'season')

class ConversionEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase')

class ControlEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year')
	list_filter = ('game', 'year')

class MovementEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase')

class RetreatEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase')

class UnitEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase', 'message')

class CountryEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase', 'message')

class DisasterEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year', 'season', 'phase')
	list_filter = ('game', 'year', 'season', 'phase', 'message')

class IncomeEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year')
	list_filter = ('game', 'year')

class ExpenseEventAdmin(admin.ModelAdmin):
	ordering = ['-year']
	list_per_page = 20
	list_display = ('game', '__str__', 'year')
	list_filter = ('game', 'year')

admin.site.register(events.BaseEvent, BaseEventAdmin)
admin.site.register(events.NewUnitEvent, NewUnitEventAdmin)
admin.site.register(events.DisbandEvent, DisbandEventAdmin)
admin.site.register(events.OrderEvent, OrderEventAdmin)
admin.site.register(events.StandoffEvent, StandoffEventAdmin)
admin.site.register(events.ConversionEvent, ConversionEventAdmin)
admin.site.register(events.ControlEvent, ControlEventAdmin)
admin.site.register(events.MovementEvent, MovementEventAdmin)
admin.site.register(events.RetreatEvent, RetreatEventAdmin)
admin.site.register(events.UnitEvent, UnitEventAdmin)
admin.site.register(events.CountryEvent, CountryEventAdmin)
admin.site.register(events.DisasterEvent, DisasterEventAdmin)
admin.site.register(events.IncomeEvent, IncomeEventAdmin)
admin.site.register(events.ExpenseEvent, ExpenseEventAdmin)

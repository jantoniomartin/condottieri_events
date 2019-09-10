# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('machiavelli', '__first__'),
        ('condottieri_scenarios', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('season', models.PositiveIntegerField(choices=[(1, 'Spring'), (2, 'Summer'), (3, 'Fall')])),
                ('phase', models.PositiveIntegerField(choices=[(0, 'Inactive game'), (1, 'Military adjustments'), (2, 'Order writing'), (3, 'Retreats'), (4, 'Strategic movement')])),
                ('classname', models.CharField(max_length=32, editable=False)),
            ],
            options={
                'ordering': ['-year', '-season', '-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ControlEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('new_home', models.BooleanField(default=False)),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('country', models.ForeignKey(to='condottieri_scenarios.Country', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='ConversionEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('before', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('after', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('country', models.ForeignKey(blank=True, to='condottieri_scenarios.Country', null=True, on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='CountryEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('message', models.PositiveIntegerField(choices=[(0, 'Government has been overthrown'), (1, 'Has been conquered'), (2, 'Has been declared enemy of Christendom'), (3, 'Has been eliminated'), (4, 'Leader has been assassinated'), (5, 'Excommunication has been lifted'), (6, 'Leader suffered an assassination attempt')])),
                ('country', models.ForeignKey(to='condottieri_scenarios.Country', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='DisasterEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('message', models.PositiveIntegerField(choices=[(0, '%(area)s is affected by famine.'), (1, '%(area)s has been affected by plague.'), (2, 'A rebellion has broken out in %(area)s.'), (3, '%(area)s is affected by a storm.')])),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='DisbandEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('country', models.ForeignKey(blank=True, to='condottieri_scenarios.Country', null=True, on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='ExpenseEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('ducats', models.PositiveIntegerField(default=0)),
                ('type', models.PositiveIntegerField(choices=[(0, 'Famine relief'), (1, 'Pacify rebellion'), (2, 'Conquered province to rebel'), (3, 'Home province to rebel'), (4, 'Counter bribe'), (5, 'Disband autonomous garrison'), (6, 'Buy autonomous garrison'), (7, 'Convert garrison unit'), (8, 'Disband enemy unit'), (9, 'Buy enemy unit'), (10, 'Hire a diplomat in own area'), (11, 'Hire a diplomat in foreign area')])),
                ('unit_type', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('area', models.ForeignKey(blank=True, to='condottieri_scenarios.Area', null=True, on_delete=models.CASCADE)),
                ('country', models.ForeignKey(to='condottieri_scenarios.Country', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='IncomeEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('ducats', models.PositiveIntegerField()),
                ('country', models.ForeignKey(to='condottieri_scenarios.Country', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='MovementEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('country', models.ForeignKey(blank=True, to='condottieri_scenarios.Country', null=True, on_delete=models.CASCADE)),
                ('destination', models.ForeignKey(related_name='movement_destination', to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('origin', models.ForeignKey(related_name='movement_origin', to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='NewUnitEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('country', models.ForeignKey(to='condottieri_scenarios.Country', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='OrderEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('code', models.CharField(max_length=1, choices=[(b'H', 'Hold'), (b'B', 'Besiege'), (b'-', 'Advance'), (b'=', 'Conversion'), (b'C', 'Convoy'), (b'S', 'Support')])),
                ('conversion', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('subtype', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('subcode', models.CharField(blank=True, max_length=1, null=True, choices=[(b'H', 'Hold'), (b'B', 'Besiege'), (b'-', 'Advance'), (b'=', 'Conversion'), (b'C', 'Convoy'), (b'S', 'Support')])),
                ('subconversion', models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('country', models.ForeignKey(to='condottieri_scenarios.Country', on_delete=models.CASCADE)),
                ('destination', models.ForeignKey(related_name='event_destination', blank=True, to='condottieri_scenarios.Area', null=True, on_delete=models.CASCADE)),
                ('origin', models.ForeignKey(related_name='event_origin', to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('subdestination', models.ForeignKey(related_name='event_subdestination', blank=True, to='condottieri_scenarios.Area', null=True, on_delete=models.CASCADE)),
                ('suborigin', models.ForeignKey(related_name='event_suborigin', blank=True, to='condottieri_scenarios.Area', null=True, on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='RetreatEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('country', models.ForeignKey(blank=True, to='condottieri_scenarios.Country', null=True, on_delete=models.CASCADE)),
                ('destination', models.ForeignKey(related_name='retreat_destination', to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('origin', models.ForeignKey(related_name='retreat_origin', to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='StandoffEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='UncoverEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('country', models.ForeignKey(blank=True, to='condottieri_scenarios.Country', null=True, on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.CreateModel(
            name='UnitEvent',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='condottieri_events.BaseEvent', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=1, choices=[(b'A', 'Army'), (b'F', 'Fleet'), (b'G', 'Garrison')])),
                ('message', models.PositiveIntegerField(choices=[(0, 'cannot carry out its support order.'), (1, 'must retreat.'), (2, 'surrenders.'), (3, 'is now besieging.'), (4, 'changes of country.'), (5, 'becomes autonomous.')])),
                ('area', models.ForeignKey(to='condottieri_scenarios.Area', on_delete=models.CASCADE)),
                ('country', models.ForeignKey(blank=True, to='condottieri_scenarios.Country', null=True, on_delete=models.CASCADE)),
            ],
            bases=('condottieri_events.baseevent',),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='game',
            field=models.ForeignKey(to='machiavelli.Game', on_delete=models.CASCADE),
        ),
    ]

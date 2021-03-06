# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-20 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CentralMI', '0017_tblleaverecord_tblleavetype_uatdetail_uatstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblAppreciation',
            fields=[
                ('appreciationid', models.AutoField(db_column='Appreciationid', primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('appreciated_by', models.CharField(blank=True, db_column='Appreciated_by', max_length=100, null=True)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_Appreciation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblRawActivityDetail',
            fields=[
                ('raw_activity_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('raw_activity', models.CharField(blank=True, max_length=50, null=True)),
                ('raw_activity_description', models.TextField(blank=True, null=True)),
                ('raw_activity_img', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_activity_scheduled', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tbl_raw_activity_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblRawScore',
            fields=[
                ('raw_score_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('score', models.IntegerField(blank=True, null=True)),
                ('winner', models.CharField(blank=True, db_column='Winner', max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_raw_score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblRawTeamMaster',
            fields=[
                ('raw_team_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('raw_team', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_team_icon', models.CharField(blank=True, max_length=255, null=True)),
                ('raw_team_slogan', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_raw_team_master',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblRawTeamMemberMaster',
            fields=[
                ('raw_team_member_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'tbl_raw_team_member_master',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblTeamMetrics',
            fields=[
                ('metrics_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('metrics_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tbl_team_metrics',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeamMetrics',
            fields=[
                ('metrics_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'team_metrics',
                'managed': False,
            },
        ),
    ]

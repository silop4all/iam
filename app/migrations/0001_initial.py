# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=255)),
                ('client_access_token', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=255)),
                ('callback_url', models.CharField(max_length=500)),
                ('callback_url2', models.CharField(max_length=500, null=True)),
            ],
            options={
                'db_table': 'iam_application',
            },
        ),
        migrations.CreateModel(
            name='ApplicationMemberHasRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'iam_application_member_hasrole',
            },
        ),
        migrations.CreateModel(
            name='ApplicationMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application', models.ForeignKey(to='app.Application')),
            ],
            options={
                'ordering': ['application'],
                'db_table': 'iam_application_membership',
            },
        ),
        migrations.CreateModel(
            name='ApplicationOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application', models.ForeignKey(to='app.Application')),
            ],
            options={
                'db_table': 'iam_application_ownership',
            },
        ),
        migrations.CreateModel(
            name='ApplicationRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application', models.ForeignKey(to='app.Application')),
            ],
            options={
                'ordering': ['application'],
                'db_table': 'iam_application_role',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=64)),
                ('password', models.CharField(unique=True, max_length=128)),
                ('token', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'iam_manager',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127, null=True, blank=True)),
                ('surname', models.CharField(max_length=127, null=True, blank=True)),
                ('gender', models.CharField(default=b'M', max_length=1, choices=[(b'M', b'sir'), (b'W', b'madam')])),
                ('username', models.CharField(unique=True, max_length=255)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('postcode', models.CharField(max_length=20, null=True, blank=True)),
                ('mail', models.EmailField(max_length=255)),
                ('phone', models.CharField(default=b'00000000000000', max_length=20, null=True, blank=True)),
                ('skills', models.CharField(default=b'low', max_length=10)),
                ('activation', models.BooleanField(default=False)),
                ('crowd_fund_participation', models.BooleanField(default=False)),
                ('crowd_fund_notification', models.BooleanField(default=False)),
                ('logo', models.ImageField(null=True, upload_to=b'app/users/logos', blank=True)),
            ],
            options={
                'ordering': ['username'],
                'db_table': 'iam_profile',
            },
        ),
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail', models.EmailField(max_length=255)),
                ('uuid', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['mail'],
                'db_table': 'iam_registration_request',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(unique=True, max_length=64)),
                ('description', models.CharField(max_length=255, null=True)),
            ],
            options={
                'ordering': ['type'],
                'db_table': 'iam_role',
            },
        ),
        migrations.AddField(
            model_name='applicationrole',
            name='role',
            field=models.ForeignKey(to='app.Role'),
        ),
        migrations.AddField(
            model_name='applicationowner',
            name='user',
            field=models.ForeignKey(to='app.Profile'),
        ),
        migrations.AddField(
            model_name='applicationmembership',
            name='member',
            field=models.ForeignKey(to='app.Profile'),
        ),
        migrations.AddField(
            model_name='applicationmemberhasrole',
            name='application_member',
            field=models.ForeignKey(related_name='member_roles', to='app.ApplicationMembership'),
        ),
        migrations.AddField(
            model_name='applicationmemberhasrole',
            name='application_role',
            field=models.ForeignKey(to='app.ApplicationRole'),
        ),
        migrations.AlterUniqueTogether(
            name='applicationmembership',
            unique_together=set([('application', 'member')]),
        ),
    ]

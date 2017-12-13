# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default=b'U', max_length=1, choices=[(b'U', b'Not available'), (b'M', b'sir'), (b'W', b'madam')]),
        ),
    ]

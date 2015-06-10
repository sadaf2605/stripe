# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20150529_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='Article',
            name='draft',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='Article',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

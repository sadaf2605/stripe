# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20150530_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='Article',
            name='category',
        ),
        migrations.AddField(
            model_name='Article',
            name='categories',
            field=models.ManyToManyField(to='news.Category'),
            preserve_default=True,
        ),
    ]

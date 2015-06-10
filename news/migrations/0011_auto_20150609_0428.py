# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20150607_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Article',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]

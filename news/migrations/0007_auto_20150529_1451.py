# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20150529_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Article',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'news_covers/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]

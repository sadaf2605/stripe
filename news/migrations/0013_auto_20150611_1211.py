# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_auto_20150611_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='populararticle',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'news_covers/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='populararticle',
            name='synopsis',
            field=models.TextField(max_length=220, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sliderarticle',
            name='synopsis',
            field=models.TextField(max_length=220, null=True, blank=True),
            preserve_default=True,
        ),
    ]

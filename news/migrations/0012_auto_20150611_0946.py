# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_auto_20150609_0428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='populararticle',
            old_name='Article',
            new_name='article',
        ),
        migrations.RenameField(
            model_name='sliderarticle',
            old_name='Article',
            new_name='article',
        ),
        migrations.AlterField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(to='news.Category', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'news_covers/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]

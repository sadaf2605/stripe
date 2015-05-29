# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20150528_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField()),
                ('article', models.ForeignKey(to='news.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

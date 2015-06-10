# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20150529_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField()),
                ('Article', models.ForeignKey(to='news.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='scrollerarticle',
            name='Article',
        ),
        migrations.DeleteModel(
            name='ScrollerArticle',
        ),
    ]

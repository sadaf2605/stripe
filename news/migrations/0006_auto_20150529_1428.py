# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_populararticle'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrollerArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField()),
                ('article', models.ForeignKey(to='news.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.ImageField(upload_to=b'news_covers/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]

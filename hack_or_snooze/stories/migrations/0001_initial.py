# Generated by Django 5.0 on 2023-12-14 10:20

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='stories', to=settings.AUTH_USER_MODEL, verbose_name='User who posted')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

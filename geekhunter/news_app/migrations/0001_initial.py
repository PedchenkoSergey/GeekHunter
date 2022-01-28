# Generated by Django 4.0.1 on 2022-01-27 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('text', models.CharField(max_length=1000, verbose_name='text')),
                ('topic', models.CharField(blank=True, max_length=100, verbose_name='topic')),
                ('status', models.CharField(choices=[('DRAFT', 'draft'), ('APPROVED', 'approved')], default='DRAFT', max_length=10, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

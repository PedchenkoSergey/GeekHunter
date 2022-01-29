# Generated by Django 4.0.1 on 2022-01-27 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('about', models.CharField(max_length=500, verbose_name='about')),
                ('awards', models.CharField(blank=True, max_length=500, verbose_name='awards')),
                ('priorities', models.CharField(blank=True, max_length=500, verbose_name='priorities')),
                ('status', models.CharField(choices=[('DRAFT', 'draft'), ('ACTIVE', 'active')], default='DRAFT', max_length=10, verbose_name='status')),
                ('moderation_status', models.CharField(choices=[('UNDER_REVIEW', 'under_review'), ('APPROVED', 'approved'), ('NOT_APPROVED', 'not_approved')], default='UNDER_REVIEW', max_length=20, verbose_name='moderation_status')),
                ('error_text', models.CharField(blank=True, max_length=400, verbose_name='error_text')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('specialization', models.CharField(blank=True, max_length=300, verbose_name='specialization')),
                ('short_description', models.CharField(blank=True, max_length=500, verbose_name='short_description')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteResume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HrManager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('status', models.CharField(choices=[('SENT', 'sent'), ('ACCEPTED', 'accepted'), ('NOT_ACCEPTED', 'not_accepted')], default='SENT', max_length=20, verbose_name='status')),
                ('text', models.CharField(max_length=500, verbose_name='text')),
                ('feedback', models.CharField(blank=True, max_length=500, verbose_name='feedback')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=1000, verbose_name='description')),
                ('salary', models.CharField(blank=True, max_length=400, verbose_name='salary')),
                ('location', models.CharField(blank=True, max_length=400, verbose_name='location')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('DRAFT', 'draft'), ('ACTIVE', 'active')], default='DRAFT', max_length=10, verbose_name='status')),
                ('moderation_status', models.CharField(choices=[('UNDER_REVIEW', 'under_review'), ('APPROVED', 'approved'), ('NOT_APPROVED', 'not_approved')], default='UNDER_REVIEW', max_length=20, verbose_name='moderation_status')),
                ('error_text', models.CharField(blank=True, max_length=400, verbose_name='error_text')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='company_app.company')),
            ],
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-23 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('status', models.CharField(choices=[('SENT', 'sent'), ('ACCEPTED', 'accepted'), ('NOT_ACCEPTED', 'not_accepted')], default='SENT', max_length=20, verbose_name='status')),
                ('text', models.CharField(max_length=500, verbose_name='text')),
                ('feedback', models.CharField(blank=True, max_length=500, verbose_name='feedback')),
                ('resume', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='employee_app.resume')),
                ('vacancy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='company_app.vacancy')),
            ],
        ),
        migrations.CreateModel(
            name='HrManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='first_name')),
                ('last_name', models.CharField(max_length=200, verbose_name='last_name')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='company_app.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hr_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteResume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hr_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hr_managers', to='company_app.hrmanager')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='employee_app.resume')),
            ],
        ),
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
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='company_app.company')),
            ],
        ),
    ]
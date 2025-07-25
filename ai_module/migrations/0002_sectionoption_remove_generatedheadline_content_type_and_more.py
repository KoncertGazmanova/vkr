# Generated by Django 5.1.4 on 2025-06-07 17:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(choices=[('pain', 'Боль'), ('benefit', 'Выгода'), ('solution', 'Решение'), ('cta', 'Призыв'), ('proof', 'Подтверждение')], max_length=20)),
                ('text', models.TextField()),
                ('ctr', models.FloatField(default=0.0)),
                ('cr', models.FloatField(default=0.0)),
                ('success_score', models.FloatField(default=0.0)),
                ('is_successful', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='generatedheadline',
            name='content_type',
        ),
        migrations.AddField(
            model_name='generatedheadline',
            name='benefit_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headlines_as_benefit', to='ai_module.sectionoption'),
        ),
        migrations.AddField(
            model_name='generatedheadline',
            name='cta_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headlines_as_cta', to='ai_module.sectionoption'),
        ),
        migrations.AddField(
            model_name='generatedheadline',
            name='pain_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headlines_as_pain', to='ai_module.sectionoption'),
        ),
        migrations.AddField(
            model_name='generatedheadline',
            name='proof_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headlines_as_proof', to='ai_module.sectionoption'),
        ),
        migrations.AddField(
            model_name='generatedheadline',
            name='solution_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headlines_as_solution', to='ai_module.sectionoption'),
        ),
    ]

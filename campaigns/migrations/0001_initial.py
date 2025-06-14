# Generated by Django 5.1.4 on 2025-06-08 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ai_module', '0002_sectionoption_remove_generatedheadline_content_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('country', models.CharField(blank=True, max_length=64)),
                ('category', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('active', 'Active'), ('paused', 'Paused'), ('stopped', 'Stopped')], default='active', max_length=20)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('stopped_at', models.DateTimeField(blank=True, null=True)),
                ('total_clicks', models.PositiveIntegerField(default=0)),
                ('total_conversions', models.PositiveIntegerField(default=0)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_revenue', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignHeadline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('ctr', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headlines', to='campaigns.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('last_edited', models.DateTimeField(auto_now=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='campaigns.campaign')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='campaigns', to='campaigns.tag'),
        ),
        migrations.CreateModel(
            name='CampaignStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('hour', models.PositiveSmallIntegerField(default=0)),
                ('clicks', models.PositiveIntegerField(default=0)),
                ('conversions', models.PositiveIntegerField(default=0)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('revenue', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='campaigns.campaign')),
            ],
            options={
                'indexes': [models.Index(fields=['campaign', 'date'], name='campaigns_c_campaig_1783e5_idx'), models.Index(fields=['campaign', 'date', 'hour'], name='campaigns_c_campaig_65197b_idx')],
                'unique_together': {('campaign', 'date', 'hour')},
            },
        ),
        migrations.CreateModel(
            name='CampaignVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview_image_url', models.URLField(blank=True)),
                ('leads', models.PositiveIntegerField(default=0)),
                ('approvals', models.PositiveIntegerField(default=0)),
                ('payout', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('weight', models.PositiveSmallIntegerField(default=1)),
                ('clicks', models.PositiveIntegerField(default=0)),
                ('conversions', models.PositiveIntegerField(default=0)),
                ('revenue', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='campaigns.campaign')),
                ('headline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ai_module.generatedheadline')),
                ('landing_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.landingpage')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.offer')),
            ],
            options={
                'unique_together': {('campaign', 'landing_page', 'offer', 'headline')},
            },
        ),
        migrations.CreateModel(
            name='TrafficPath',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('clicks', models.PositiveIntegerField(default=0)),
                ('conversions', models.PositiveIntegerField(default=0)),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('revenue', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('leads', models.PositiveIntegerField(default=0)),
                ('approvals', models.PositiveIntegerField(default=0)),
                ('payout', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paths', to='campaigns.campaign')),
            ],
            options={
                'unique_together': {('campaign', 'name')},
            },
        ),
    ]

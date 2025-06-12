from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_teasermetric'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allow_countries', models.JSONField(blank=True, default=list)),
                ('block_ip_list', models.JSONField(blank=True, default=list)),
                ('block_bots', models.BooleanField(default=True)),
                ('ip_rate_limit', models.PositiveIntegerField(default=60)),
                ('campaign', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='traffic_filter', to='campaigns.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='BlockedTrafficEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('country', models.CharField(blank=True, max_length=8)),
                ('user_agent', models.TextField(blank=True)),
                ('reason', models.CharField(choices=[('BOT', 'BOT'), ('GEO', 'GEO'), ('IP', 'IP'), ('RATE', 'RATE')], max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_events', to='campaigns.campaign')),
            ],
        ),
    ]

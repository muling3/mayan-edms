from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='EventSubscription',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'event_type', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subscriptions', to='events.EventType',
                        verbose_name='Event type'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL, verbose_name='User'
                    )
                )
            ],
            options={
                'verbose_name': 'Event subscription',
                'verbose_name_plural': 'Event subscriptions'
            }
        )
    ]

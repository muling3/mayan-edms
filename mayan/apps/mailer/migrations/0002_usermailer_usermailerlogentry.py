from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('mailer', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='UserMailer',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        max_length=32, unique=True, verbose_name='Label'
                    )
                ),
                (
                    'default', models.BooleanField(
                        default=True, verbose_name='Default'
                    )
                ),
                (
                    'backend_path', models.CharField(
                        help_text='The dotted Python path to the backend '
                        'class.', max_length=128, verbose_name='Backend path'
                    )
                ),
                (
                    'backend_data', models.TextField(
                        blank=True, verbose_name='Backend data'
                    )
                )
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'User mailer',
                'verbose_name_plural': 'User mailers'
            }
        ),
        migrations.CreateModel(
            name='UserMailerLogEntry',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'datetime', models.DateTimeField(
                        auto_now_add=True, verbose_name='Date time'
                    )
                ),
                (
                    'message', models.TextField(
                        blank=True, editable=False, verbose_name='Message'
                    )
                ),
                (
                    'user_mailer', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='mailer.UserMailer', verbose_name='User mailer'
                    )
                )
            ],
            options={
                'ordering': ('-datetime',),
                'get_latest_by': 'datetime',
                'verbose_name': 'User mailer log entry',
                'verbose_name_plural': 'User mailer log entries'
            }
        )
    ]

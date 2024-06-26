from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=128, verbose_name='Internal name'
                    )
                )
            ],
            options={
                'verbose_name': 'Error log',
                'verbose_name_plural': 'Error logs',
                'ordering': ('name',)
            }
        ),
        migrations.CreateModel(
            name='ErrorLogPartition',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        db_index=True, max_length=128,
                        verbose_name='Internal name'
                    )
                ),
                (
                    'error_log', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='partitions', to='logging.ErrorLog',
                        verbose_name='Error log'
                    )
                )
            ],
            options={
                'verbose_name': 'Error log partition',
                'verbose_name_plural': 'Error log partitions',
                'unique_together': {
                    ('error_log', 'name')
                }
            }
        ),
        migrations.CreateModel(
            name='ErrorLogPartitionEntry',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'datetime', models.DateTimeField(
                        auto_now_add=True, db_index=True,
                        verbose_name='Date and time'
                    )
                ),
                (
                    'text', models.TextField(
                        blank=True, null=True, verbose_name='Text'
                    )
                ),
                (
                    'error_log_partition', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='entries',
                        to='logging.ErrorLogPartition',
                        verbose_name='Error log partition'
                    )
                )
            ],
            options={
                'verbose_name': 'Error log partition entry',
                'verbose_name_plural': 'Error log partition entries',
                'ordering': ('datetime',),
                'get_latest_by': 'datetime'
            }
        )
    ]

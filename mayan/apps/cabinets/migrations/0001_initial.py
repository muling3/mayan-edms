from django.db import migrations, models
import django.db.models.deletion

import mptt.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('documents', '0034_auto_20160509_2321')
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        max_length=128, verbose_name='Label'
                    )
                ),
                (
                    'lft', models.PositiveIntegerField(
                        db_index=True, editable=False
                    )
                ),
                (
                    'rght', models.PositiveIntegerField(
                        db_index=True, editable=False
                    )
                ),
                (
                    'tree_id', models.PositiveIntegerField(
                        db_index=True, editable=False
                    )
                ),
                (
                    'level', models.PositiveIntegerField(
                        db_index=True, editable=False
                    )
                ),
                (
                    'documents', models.ManyToManyField(
                        blank=True, related_name='cabinets',
                        to='documents.Document', verbose_name='Documents'
                    )
                ),
                (
                    'parent', mptt.fields.TreeForeignKey(
                        blank=True, null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='children', to='cabinets.Cabinet'
                    )
                )
            ],
            options={
                'ordering': ('parent__label', 'label'),
                'verbose_name': 'Cabinet',
                'verbose_name_plural': 'Cabinets'
            }
        ),
        migrations.CreateModel(
            name='DocumentCabinet',
            fields=[],
            options={
                'verbose_name': 'Document cabinet',
                'proxy': True,
                'verbose_name_plural': 'Document cabinets'
            },
            bases=('cabinets.cabinet',)
        ),
        migrations.AlterUniqueTogether(
            name='cabinet',
            unique_together={
                ('parent', 'label')
            }
        )
    ]

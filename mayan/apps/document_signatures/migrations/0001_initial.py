from django.core.files.storage import FileSystemStorage
from django.db import migrations, models

import mayan.apps.document_signatures.models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentVersionSignature',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'signature_file', models.FileField(
                        storage=FileSystemStorage(),
                        upload_to=mayan.apps.document_signatures.models.upload_to,
                        blank=True, editable=False, null=True,
                        verbose_name='Signature file'
                    )
                ),
                (
                    'has_embedded_signature', models.BooleanField(
                        default=False, verbose_name='Has embedded signature',
                        editable=False
                    )
                ),
                (
                    'document_version', models.ForeignKey(
                        editable=False, on_delete=models.CASCADE,
                        to='documents.DocumentVersion',
                        verbose_name='Document version'
                    )
                )
            ],
            options={
                'verbose_name': 'Document version signature',
                'verbose_name_plural': 'Document version signatures'
            },
            bases=(models.Model,),
        )
    ]

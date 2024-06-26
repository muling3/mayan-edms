from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0011_auto_20170524_0456')
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='slug',
            field=models.SlugField(
                help_text='This value will be used by other apps to reference '
                'this index.', max_length=128, unique=True, verbose_name='Slug'
            ),
        ),
        migrations.AlterField(
            model_name='indexinstancenode',
            name='documents',
            field=models.ManyToManyField(
                related_name='index_instance_nodes', to='documents.Document',
                verbose_name='Documents'
            ),
        ),
        migrations.AlterField(
            model_name='indexinstancenode',
            name='index_template_node',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='index_instance_nodes',
                to='document_indexing.IndexTemplateNode',
                verbose_name='Index template node'
            ),
        )
    ]

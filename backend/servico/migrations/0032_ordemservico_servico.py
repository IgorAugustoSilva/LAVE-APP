# Generated by Django 4.2.3 on 2024-08-24 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0031_alter_ordemservico_deliver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='servico',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='servico.servico'),
            preserve_default=False,
        ),
    ]
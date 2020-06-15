# Generated by Django 3.0.6 on 2020-06-01 10:16

import ModelsMaster.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ModelsMaster', '0005_auto_20200530_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccionMeta',
            fields=[
                ('Id', models.AutoField(db_column='AT_Id_AccMeta', primary_key=True, serialize=False)),
                ('Nombre', models.CharField(db_column='AT_Nombre', max_length=256)),
                ('Estado', models.CharField(db_column='AT_Estado_Avance', max_length=256, null=True)),
                ('Plazo', models.CharField(db_column='AT_Plazo', max_length=256)),
            ],
            options={
                'db_table': 'T_Acciones_Meta',
            },
        ),
        migrations.CreateModel(
            name='DocumentosSistema',
            fields=[
                ('Id', models.AutoField(db_column='DC_Id_Documento_Sistema', primary_key=True, serialize=False)),
                ('Nombre', models.CharField(db_column='DC_Nombre', max_length=256)),
                ('Codificacion', models.CharField(db_column='DC_Codificacion', max_length=256)),
                ('IdPc', models.ForeignKey(db_column='DC_Id_Puntos_Capitulo', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.PuntosCapitulo')),
            ],
            options={
                'db_table': 'T_Documento_Sistema',
            },
        ),
        migrations.CreateModel(
            name='Estructura',
            fields=[
                ('Id', models.AutoField(db_column='ES_Id_Estructura', primary_key=True, serialize=False)),
                ('Nombre', models.CharField(db_column='ES_Nombre', max_length=256)),
                ('Eliminado', models.BooleanField(db_column='ES_Eliminado', default=False)),
            ],
            options={
                'db_table': 'T_Estructura',
            },
        ),
        migrations.CreateModel(
            name='IndicadorAccionProceso',
            fields=[
                ('Id', models.AutoField(db_column='IA_Id_Indicador_Accion', primary_key=True, serialize=False)),
                ('Nombre', models.CharField(db_column='IA_Nombre', max_length=256)),
                ('Descripcion', models.CharField(blank=True, db_column='IA_Descripcion', max_length=256, null=True)),
                ('Periodo', models.CharField(db_column='IA_Periodo', max_length=256)),
                ('Estado', models.CharField(blank=True, db_column='IA_Estado', max_length=256, null=True)),
                ('ValorObjetivo', models.CharField(db_column='IA_Valor_Objetivo', max_length=256)),
                ('ValorConseguido', models.CharField(db_column='IA_Valor_conseguido', max_length=256)),
                ('Plazo', models.CharField(db_column='IA_Plazo_Seguimiento', max_length=256, validators=[ModelsMaster.validators.plazo_filtro])),
                ('IdAcc', models.ForeignKey(db_column='IA_Id_Accion_Meta', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.AccionMeta')),
            ],
            options={
                'db_table': 'T_Indicador_Accion_proceso',
            },
        ),
        migrations.CreateModel(
            name='SeguimientoIndicadores',
            fields=[
                ('Id', models.AutoField(db_column='IS_Id_Indicador', primary_key=True, serialize=False)),
                ('Fecha', models.DateField(db_column='Is_Fecha_Seguimiento', validators=[ModelsMaster.validators.fecha_filtro])),
                ('Seguimiento', models.IntegerField(db_column='IS_Valor_Seguimiento')),
                ('IdAccMeta', models.ForeignKey(db_column='IS_Id_Indicador_Accion', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.IndicadorAccionProceso')),
                ('IdDoc', models.ForeignKey(blank=True, db_column='IS_Id_Documento', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.DocumentosSistema')),
            ],
            options={
                'db_table': 'T_Seguimiento_Indicador',
            },
        ),
        migrations.CreateModel(
            name='proceso',
            fields=[
                ('Id', models.AutoField(db_column='PR_Id_Proceso', primary_key=True, serialize=False)),
                ('Nombre', models.CharField(db_column='PR_Nombre', max_length=256)),
                ('Descripcion', models.CharField(blank=True, db_column='PR_Descripcion', max_length=256, null=True)),
                ('Codificacion', models.CharField(db_column='PR_Codificacion', max_length=256)),
                ('IdEst', models.ForeignKey(db_column='PR_Id_Estructura', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.Estructura')),
                ('IdPc', models.ForeignKey(db_column='PR_Id_Punto_Capitulo', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.PuntosCapitulo')),
            ],
            options={
                'db_table': 'T_Proceso',
            },
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('Id', models.AutoField(db_column='MT_Id_Meta', primary_key=True, serialize=False)),
                ('Codificacion', models.CharField(db_column='MT_Codificacion', max_length=256)),
                ('Nombre', models.CharField(db_column='MT_Nombre', max_length=256)),
                ('Descripcion', models.TextField(blank=True, db_column='MT_Descripcion', max_length=256, null=True)),
                ('IdObj', models.ForeignKey(db_column='MT_Id_Objetivo', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.Objetivo')),
                ('IdParent', models.ForeignKey(db_column='MT_Id_Padre', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.Meta')),
            ],
            options={
                'db_table': 'T_Meta',
            },
        ),
        migrations.AddField(
            model_name='indicadoraccionproceso',
            name='IdProc',
            field=models.ForeignKey(blank=True, db_column='IA_Id_Proceso', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.proceso'),
        ),
        migrations.AddField(
            model_name='accionmeta',
            name='IdMeta',
            field=models.ForeignKey(db_column='AT_Id_Meta', on_delete=django.db.models.deletion.DO_NOTHING, to='ModelsMaster.Meta'),
        ),
    ]

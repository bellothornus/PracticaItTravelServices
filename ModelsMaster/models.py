from django.db import models
from ModelsMaster import validators
#from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Create your models here.
class Ambito(models.Model):
    Id=models.AutoField(primary_key=True,db_column="AM_Id_Ambito")
    Nombre=models.CharField(max_length=256, null=False, blank=False, db_column="AM_Nombre")
    Descripcion=models.CharField(max_length=256, null=True, blank=True, db_column="AM_Descripcion")
    Eliminado=models.BooleanField(default=False, db_column="AM_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Ambitos"

class TipoObjetivo(models.Model):
    Id=models.AutoField(primary_key=True, db_column="TO_Id_Tipo_Objetivo")
    Nombre=models.CharField(max_length=256, null=False, blank=False, db_column="TO_Nombre")
    Descripcion=models.CharField(max_length=256, null=True,blank=True, db_column="TO_Descripcion")
    Eliminado=models.BooleanField(default=False, db_column="TO_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Tipo_Objetivo"

class Estructura(models.Model):
    Id=models.AutoField(primary_key=True, db_column="ES_Id_Estructura")
    Nombre=models.CharField(max_length=256, db_column="ES_Nombre")
    Eliminado=models.BooleanField(default=False, db_column="ES_Eliminado")

    class Meta:
        db_table = "T_Estructura"

""" class Riesgo(models.Model):
    Id=models.AutoField(primary_key=True, db_column="RG_Id_Riesgo")
    Nombre=models.CharField(max_length=256,db_column="RG_Nombre")
    Eliminado=models.BooleanField(default=False, db_column="RG_Eliminado")

    class Meta:
        db_table = "riesgos" """

""" class TipoInterviniente(models.Model):
    Id=models.AutoField(primary_key=True, db_column="id_Tipo_Interviniente")
    Nombre=models.CharField(max_length=256, db_column="Nombre")
    Eliminado=models.BooleanField(default=False, db_column="eliminado")

    class Meta:
        db_table = "tipo_intervinientes" """

class Sector(models.Model):
    Id=models.AutoField(primary_key=True, db_column="SC_Id_Sector")
    Nombre=models.CharField(max_length=256, db_column="SC_Nombre", null=False,blank=False)
    Descripcion=models.CharField(max_length=256, db_column="SC_Descripcion",null=True, blank=True)
    Eliminado=models.BooleanField(default=False, db_column="SC_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Sector"

class NivelAreaGeografica(models.Model):
    Id=models.AutoField(primary_key=True, db_column="NG_Id_Nivel_Area_Geo")
    Nivel=models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)],null=False,blank=False, db_column="NG_Nivel")
    Nombre=models.CharField(max_length=256,null=False,blank=False, db_column="NG_Nombre")
    Descripcion=models.CharField(max_length=256,null=True,blank=True, db_column="NG_Descripcion")
    Eliminado=models.BooleanField(default=False, db_column="NG_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Nivel_Area_Geografica"

class AreaGeografica(models.Model):
    #id_ag es el id del Area geográfica en sí, cada uno tiene el suyo ,es su identificador único
    Id=models.AutoField(primary_key=True, db_column="AG_Id_Area_Geo") 
    #id_ag_nag es el id del Nivel de Area Geografica que te indica esa Area geografica en que nivel está
    IdNag=models.ForeignKey(to=NivelAreaGeografica, db_column="AG_Id_Nivel", null=False, blank=False, on_delete=models.DO_NOTHING)
    #id_ag_parent es el id que indica si esta area depende de otra, por ejemplo Palma de mallorca pertenece a Baleares, no? pues pones aquí el ID único de Baleares
    IdParent=models.ForeignKey(to='self', on_delete=models.DO_NOTHING, db_column="AG_Id_Area_Padre", null=True, blank=True)
    #el nombre del registro
    Nombre=models.CharField(max_length=256, db_column="AG_Nombre", null=False,blank=False)
    #la descripcion del registro
    Descripcion=models.CharField(max_length=256, db_column="AG_Descripcion", null=True, blank=True)
    #columna que sirve para indicar si se ha eliminado o no
    Eliminado=models.BooleanField(default=False, db_column="AG_Eliminado")
        
    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Area_Geografica"
    
class Empresa(models.Model):
    Id=models.AutoField(primary_key=True, db_column="EM_Id_Empresa")
    IdSc=models.ForeignKey(to=Sector,on_delete=models.DO_NOTHING, null=False, blank=False, db_column="EM_Id_Sector")
    IdAg=models.ForeignKey(to=AreaGeografica, on_delete=models.DO_NOTHING, db_column="Em_Centro_Principal", null=False, blank=False)
    Nombre=models.CharField(max_length=256, db_column="EM_Nombre")
    Descripcion=models.CharField(max_length=256,db_column="EM_Descripcion", null=True, blank=True)
    Eliminado=models.BooleanField(default=False, db_column="EM_Eliminado")

    def __str__(self):
        #return "%s > %s" % (self.IdSc, self.IdAg)
        return self.Nombre

    class Meta:
        db_table = "T_Empresa"

class Modelo(models.Model):
    Id=models.AutoField(primary_key=True, db_column="MD_Id_Modelo")
    IdEmp=models.ForeignKey(to=Empresa, on_delete=models.DO_NOTHING, db_column="MD_Id_Empresa")
    Nombre=models.CharField(max_length=256, db_column="MD_Nombre")
    Descripcion=models.CharField(max_length=256, blank=True, null=True, db_column="MD_Descripcion")
    Eliminado=models.BooleanField(default=False, db_column="MD_Eliminado")
    
    def __str__(self):
        return self.Nombre 

    class Meta:
        db_table= "T_Modelo"
        
class Benchmarking(models.Model):
    Id=models.AutoField(primary_key=True, db_column="BH_Id_Bench")
    IdSc=models.ForeignKey(to=Sector, db_column="BH_Id_Sector", on_delete=models.DO_NOTHING)
    IdAg=models.ForeignKey(to=AreaGeografica, db_column="BH_Id_Area_Geo", on_delete=models.DO_NOTHING)
    Nombre=models.CharField(max_length=256, db_column="BH_Nombre")
    Descripcion=models.CharField(max_length=256, null=True, blank=True, db_column="BH_Descripcion")
    Valor=models.IntegerField(null=True, blank=True, db_column="BH_Valor")
    Anyo=models.IntegerField(null=True, blank=True, db_column="BH_Año")
    Ciclo=models.CharField(max_length=256,null=True, blank=True, db_column="BH_Ciclo")
    Eliminado=models.BooleanField(default=False, db_column="BH_Eliminado")
    
    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Benchmarkig"

class PuntosCapitulo(models.Model):
    Id=models.AutoField(primary_key=True, db_column="CP_Id_Capitulo")
    IdMd=models.ForeignKey(to=Modelo, db_column="CP_Id_Modelo", on_delete=models.DO_NOTHING)
    IdAm=models.ForeignKey(to=Ambito, to_field='Id', db_column="CP_Id_Ambito", on_delete=models.DO_NOTHING)
    Nombre=models.CharField(max_length=256, db_column="CP_Nombre")
    Descripcion=models.CharField(max_length=256, null=True, blank=True, db_column="CP_Descripcion")
    Eliminado=models.BooleanField(default=False, db_column="CP_Eliminado")

    def __str__(self):
        return self.Nombre
    
    def documentos(self):
        return DocumentosSistema.objects.filter(IdPc=self.Id)

    class Meta:
        db_table = "T_Puntos_Capitulo"

class Objetivo(models.Model):
    Id=models.AutoField(primary_key=True, db_column="OB_Id_Objetivo")
    IdPc=models.ForeignKey(to=PuntosCapitulo, db_column="OB_Id_Capitulo", on_delete=models.DO_NOTHING)
    IdTo=models.ForeignKey(to=TipoObjetivo, db_column="OB_Id_Tipo_Objetivo", on_delete=models.DO_NOTHING)
    IdParent=models.ForeignKey(to="self", default="", db_column="OB_Id_Objetivo_Padre", on_delete=models.DO_NOTHING, null=True, blank=True)
    Nombre=models.CharField(max_length=256, db_column="OB_Nombre")
    Descripcion=models.CharField(max_length=256, null=True, blank=True, db_column="OB_Descripcion")
    Codificacion=models.CharField(max_length=256, db_column="OB_Codificacion")
    Anyo=models.IntegerField(null=True, blank=True, db_column="OB_Año")
    Eliminado=models.BooleanField(default=False, db_column="OB_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Objetivo"

""" class ObjetivoRelacionado(models.Model):
    id_or=models.AutoField(primary_key=True, db_column="id_ObjetivoRelacionado")
    id_or_ob=models.ForeignKey(to=Objetivo, related_name="Id_Objetivo", db_column="id_Objetivo", on_delete=models.DO_NOTHING)
    id_or_ob_asociado=models.ForeignKey(to=Objetivo, related_name="Id_ObjetivoAsociado", db_column="id_Objetivo_Asociado", on_delete=models.DO_NOTHING)
    str_or_nombre=models.CharField(max_length=256, null=True, blank=True, db_column="Nombre")
    bool_or_eliminado=models.BooleanField(default=False, db_column="eliminado")

    class Meta:
        db_table = "objetivo_relacionado"
 """

class Meta(models.Model):
    Id=models.AutoField(primary_key=True, db_column="MT_Id_Meta")
    IdObj=models.ForeignKey(to=Objetivo, db_column="MT_Id_Objetivo", on_delete=models.DO_NOTHING)
    IdParent=models.ForeignKey(to='self', db_column="MT_Id_Padre", on_delete=models.DO_NOTHING, null=True, blank=True)
    Codificacion=models.CharField(max_length=256, db_column="MT_Codificacion")
    Nombre=models.CharField(max_length=256, db_column="MT_Nombre")
    Descripcion=models.TextField(max_length=256, db_column="MT_Descripcion", null=True, blank=True)
    Eliminado=models.BooleanField(default=False, db_column="MT_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Meta"

class AccionMeta(models.Model):
    Id=models.AutoField(primary_key=True, db_column="AT_Id_AccMeta")
    IdMeta=models.ForeignKey(to=Meta, db_column="AT_Id_Meta", on_delete=models.DO_NOTHING)
    Nombre=models.CharField(max_length=256, db_column="AT_Nombre")
    Estado=models.CharField(max_length=256, db_column="AT_Estado_Avance", null=True, blank=False)
    Plazo=models.CharField(max_length=256, db_column="AT_Plazo")
    Eliminado=models.BooleanField(default=False, db_column="AT_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Acciones_Meta"

class IndicadorAccionProceso(models.Model):
    Id=models.AutoField(primary_key=True, db_column="IA_Id_Indicador_Accion")
    IdAcc=models.ForeignKey(to=AccionMeta, db_column="IA_Id_Accion_Meta", on_delete=models.DO_NOTHING)
    IdProc=models.ForeignKey(to='Proceso', db_column="IA_Id_Proceso", null=True, blank=True, on_delete=models.DO_NOTHING)
    Nombre=models.CharField(max_length=256, db_column="IA_Nombre")
    Descripcion=models.CharField(max_length=256, db_column="IA_Descripcion", null=True, blank=True)
    Periodo=models.CharField(max_length=256, db_column="IA_Periodo")
    Estado=models.CharField(max_length=256, db_column="IA_Estado", null=True, blank=True)
    ValorObjetivo=models.CharField(max_length=256, db_column="IA_Valor_Objetivo")
    ValorConseguido=models.CharField(max_length=256, db_column="IA_Valor_conseguido", null=True, blank=True)
    plazos = [
        ("Semanal", "Semanal"), 
        ("Mensual","Mensual"), 
        ("Trimestral","Trimestral"), 
        ("Bimestral","Bimestral"),
        ("Cuatrimestral","Cuatrimestral"),
        ("Semestral","Semestral"),
        ("Anual","Anual")
    ]
    Plazo=models.CharField(max_length=256, choices=plazos, db_column="IA_Plazo_Seguimiento")
    Eliminado=models.BooleanField(default=False, db_column="IA_Eliminado")
    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Indicador_Accion_proceso"

class DocumentosSistema(models.Model):
    Id=models.AutoField(primary_key=True, db_column="DC_Id_Documento_Sistema")
    IdPc=models.ForeignKey(to=PuntosCapitulo, db_column="DC_Id_Puntos_Capitulo", on_delete=models.DO_NOTHING)
    #no lo intorducirá el usuario sino que será automático
    Nombre=models.CharField(max_length=256, db_column="DC_Nombre")
    Descripcion=models.CharField(max_length=256, db_column="DC_Descripcion", null=True,blank=True)
    Codificacion=models.CharField(max_length=256, db_column="DC_Codificacion")
    Eliminado=models.BooleanField(default=False, db_column="DC_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Documento_Sistema"

class SeguimientoIndicadores(models.Model):
    Id=models.AutoField(primary_key=True, db_column="IS_Id_Indicador")
    IdAccMeta=models.ForeignKey(to=IndicadorAccionProceso, db_column="IS_Id_Indicador_Accion", on_delete=models.DO_NOTHING)
    IdDoc=models.ForeignKey(to=DocumentosSistema, db_column="IS_Id_Documento", null=True, blank=True, on_delete=models.DO_NOTHING)
    Fecha=models.DateField(db_column="Is_Fecha_Seguimiento", validators=[validators.fecha_filtro])
    Seguimiento=models.IntegerField(db_column="IS_Valor_Seguimiento")
    Eliminado=models.BooleanField(default=False, db_column="IS_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Seguimiento_Indicador"

class Proceso(models.Model):
    Id=models.AutoField(primary_key=True, db_column="PR_Id_Proceso")
    IdPc=models.ForeignKey(to=PuntosCapitulo, db_column="PR_Id_Punto_Capitulo", on_delete=models.DO_NOTHING)
    IdEst=models.ForeignKey(to=Estructura, db_column="PR_Id_Estructura", on_delete=models.DO_NOTHING)
    Nombre=models.CharField(max_length=256, db_column="PR_Nombre")
    Descripcion=models.CharField(max_length=256, db_column="PR_Descripcion", null=True, blank=True)
    Codificacion=models.CharField(max_length=256, db_column="PR_Codificacion")
    Eliminado=models.BooleanField(default=False, db_column="PR_Eliminado")

    def __str__(self):
        return self.Nombre

    class Meta:
        db_table = "T_Proceso"

class UserEmpresa(models.Model):
    Id=models.AutoField(primary_key=True, db_column="UE_Id_UserEmpresa")
    IdEmp=models.ForeignKey(to=Empresa, db_column="UE_Id_Empresa", on_delete=models.DO_NOTHING)
    IdUser=models.ForeignKey(to=User, db_column="UE_Id_Usuario",on_delete=models.DO_NOTHING)
    Eliminado=models.BooleanField(default=False, db_column="UE_Eliminado")

    def __str__(self):
        #usuario = User.objects.get(id=self.Id)
        #empresa = Empresa.objects.get(Id=self.Id)
        return "%s de %s" % (self.IdUser, self.IdEmp)
    
    class Meta:
        db_table = "T_User_Empresa"

class GroupEmpresa(models.Model):
    Id=models.AutoField(primary_key=True, db_column="GE_Id_GroupEmpresa")
    IdEmp=models.ForeignKey(to=Empresa, db_column="GE_Id_Empresa", on_delete=models.DO_NOTHING)
    IdGroup=models.ForeignKey(to=Group, db_column="GE_Id_Group", on_delete=models.DO_NOTHING)
    Eliminado=models.BooleanField(default=False, db_column="GE_Eliminado")

    def __str__(self):
        return "%s de %s" % (self.IdGroup, self.IdEmp)

    class Meta:
        db_table = "T_Group_Empresa"

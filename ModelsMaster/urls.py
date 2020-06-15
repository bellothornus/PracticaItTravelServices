from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import  static
#from .views import *
from . import views

urlpatterns = [
    path('index/ambito/', views.AmbitoView.index),
    path('show/ambito/<int:id>', views.AmbitoView.show),
    path('create/ambito', views.AmbitoView.create),
    path('update/ambito/<int:id>', views.AmbitoView.update),
    path('delete/ambito/<int:id>', views.AmbitoView.delete),

    path('index/tipo_objetivo', views.TipoObjetivoView.index),
    path('show/tipo_objetivo/<int:id>', views.TipoObjetivoView.show),
    path('create/tipo_objetivo', views.TipoObjetivoView.create),
    path('update/tipo_objetivo/<int:id>', views.TipoObjetivoView.update),
    path('delete/tipo_objetivo/<int:id>', views.TipoObjetivoView.delete),

    path('index/estructura', views.EstructuraView.index),
    path('show/estructura/<int:id>', views.EstructuraView.show),
    path('create/estructura', views.EstructuraView.create),
    path('update/estructura/<int:id>', views.EstructuraView.update),
    path('delete/estructura/<int:id>', views.EstructuraView.delete),

    path('index/riesgo', views.RiesgoView.index), 
    path('show/riesgo/<int:id>', views.RiesgoView.show),
    path('create/riesgo', views.RiesgoView.create),
    path('update/riesgo/<int:id>', views.RiesgoView.update),
    path('delete/riesgo/<int:id>', views.RiesgoView.delete),

    path('index/tipo_interviniente', views.TipoIntervinienteView.index),
    path('show/tipo_interviniente/<int:id>', views.TipoIntervinienteView.show),
    path('create/tipo_interviniente', views.TipoIntervinienteView.create),
    path('update/tipo_interviniente/<int:id>', views.TipoIntervinienteView.update),
    path('delete/tipo_interviniente/<int:id>', views.TipoIntervinienteView.delete),

    path('index/sector', views.SectorView.index),
    path('show/sector/<int:id>', views.SectorView.show),
    path('create/sector', views.SectorView.create),
    path('update/sector/<int:id>', views.SectorView.update),
    path('delete/sector/<int:id>', views.SectorView.delete),

    path('index/nag', views.NivelAreaGeograficaView.index),
    path('show/nag/<int:id>', views.NivelAreaGeograficaView.show),
    path('create/nag', views.NivelAreaGeograficaView.create),
    path('update/nag/<int:id>', views.NivelAreaGeograficaView.update),
    path('delete/nag/<int:id>', views.NivelAreaGeograficaView.delete),

    path('index/area_geografica', views.AreaGeograficaView.index),
    path('show/area_geografica/<int:id>', views.AreaGeograficaView.show),
    path('create/area_geografica', views.AreaGeograficaView.create),
    path('update/area_geografica/<int:id>', views.AreaGeograficaView.update),
    path('delete/area_geografica/<int:id>', views.AreaGeograficaView.delete),

    path('index/empresa', views.EmpresaView.index),
    path('show/empresa/<int:id>', views.EmpresaView.show),
    path('create/empresa', views.EmpresaView.create),
    path('update/empresa/<int:id>', views.EmpresaView.update),
    path('delete/empresa/<int:id>', views.EmpresaView.delete),

    path('index/modelo', views.ModeloView.index),
    path('show/modelo/<int:id>', views.ModeloView.show),
    path('create/modelo', views.ModeloView.create),
    path('update/modelo/<int:id>', views.ModeloView.update),
    path('delete/modelo/<int:id>', views.ModeloView.delete),

    path('index/benchmarking', views.BenchmarkingView.index),
    path('show/benchmarking/<int:id>', views.BenchmarkingView.show),
    path('create/benchmarking', views.BenchmarkingView.create),
    path('update/benchmarking/<int:id>', views.BenchmarkingView.update),
    path('delete/benchmarking/<int:id>', views.BenchmarkingView.delete),

    path('index/puntoscap', views.PuntosCapituloView.index),
    path('show/puntoscap/<int:id>', views.PuntosCapituloView.show),
    path('create/puntoscap', views.PuntosCapituloView.create),
    path('update/puntoscap/<int:id>', views.PuntosCapituloView.update),
    path('delete/puntoscap/<int:id>', views.PuntosCapituloView.delete),

    path('index/objetivo', views.ObjetivoView.index),
    path('show/objetivo/<int:id>', views.ObjetivoView.show),
    path('create/objetivo', views.ObjetivoView.create),
    path('update/objetivo/<int:id>', views.ObjetivoView.update),
    path('delete/objetivo/<int:id>', views.ObjetivoView.delete),
    
    path('index/meta', views.MetaView.index),
    path('show/meta/<int:id>', views.MetaView.show),
    path('create/meta', views.MetaView.create),
    path('update/meta/<int:id>', views.MetaView.update),
    path('delete/meta/<int:id>', views.MetaView.delete),

    path('index/accionmeta', views.AccionMetaView.index),
    path('show/accionmeta/<int:id>', views.AccionMetaView.show),
    path('create/accionmeta', views.AccionMetaView.create),
    path('update/accionmeta/<int:id>', views.AccionMetaView.update),
    path('delete/accionmeta/<int:id>', views.AccionMetaView.delete),

    path('index/documentos_sistema', views.DocumentosSistemaView.index),
    path('show/documentos_sistema/<int:id>', views.DocumentosSistemaView.show),
    path('create/documentos_sistema', views.DocumentosSistemaView.create),
    path('update/documentos_sistema/<int:id>', views.DocumentosSistemaView.update),
    path('delete/documentos_sistema/<int:id>', views.DocumentosSistemaView.delete),

    path('index/indicador_accion_proceso', views.IndicadorAccionProcesoView.index),
    path('show/indicador_accion_proceso/<int:id>', views.IndicadorAccionProcesoView.show),
    path('create/indicador_accion_proceso', views.IndicadorAccionProcesoView.create),
    path('update/indicador_accion_proceso/<int:id>', views.IndicadorAccionProcesoView.update),
    path('delete/indicador_accion_proceso/<int:id>', views.IndicadorAccionProcesoView.delete),

    path('index/seguimiento_indicadores', views.SeguimientoIndicadoresView.index),
    path('show/seguimiento_indicadores/<int:id>', views.SeguimientoIndicadoresView.show),
    path('create/seguimiento_indicadores', views.SeguimientoIndicadoresView.create),
    path('update/seguimiento_indicadores/<int:id>', views.SeguimientoIndicadoresView.update),
    path('delete/seguimiento_indicadores/<int:id>', views.SeguimientoIndicadoresView.delete),

    path('index/proceso', views.ProcesoView.index),
    path('show/proceso/<int:id>', views.ProcesoView.show),
    path('create/proceso', views.ProcesoView.create),
    path('update/proceso/<int:id>', views.ProcesoView.update),
    path('delete/proceso/<int:id>', views.ProcesoView.delete),

    path('index/user', views.UserView.index),
    path('show/user/<int:id>', views.UserView.show),
    path('create/user', views.UserView.create),
    path('update/user/<int:id>', views.UserView.update),
    path('delete/user/<int:id>', views.UserView.delete),
    
    path('login', views.LogView.login, name='login'),
    path('logout', views.LogView.logout),

    path("index/user_empresa", views.UserEmpresaView.index),
    path("show/user_empresa/<int:id>", views.UserEmpresaView.show),
    path("create/user_empresa", views.UserEmpresaView.create),
    path("update/user_empresa/<int:id>", views.UserEmpresaView.update),
    path("delete/user_empresa/<int:id>", views.UserEmpresaView.delete),

    path("index/group_empresa", views.GroupEmpresaView.index),
    path("show/group_empresa/<int:id>", views.GroupEmpresaView.show),
    path("create/group_empresa", views.GroupEmpresaView.create),
    


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
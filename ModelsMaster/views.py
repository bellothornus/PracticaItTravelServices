from django.shortcuts import render, redirect
from django.views import View
from .forms import AmbitoForm, TipoObjetivoForm, SectorForm, NivelAreaGeograficaForm, AreaGeograficaForm, EmpresaForm, ModeloForm, BenchmarkingForm, PuntosCapituloForm, ObjetivoForm, EstructuraForm, MetaForm, ProcesoForm, DocumentosSistemaForm, IndicadorAccionProcesoForm, AccionMetaForm, SeguimientoIndicadoresForm, UserForm, UserEmpresaForm, GroupEmpresaForm
from .models import Ambito, TipoObjetivo, Sector, NivelAreaGeografica, AreaGeografica, Empresa, Modelo, Benchmarking, PuntosCapitulo, Objetivo, Estructura, Meta, Proceso, DocumentosSistema, IndicadorAccionProceso, AccionMeta, SeguimientoIndicadores, UserEmpresa, GroupEmpresa
from django.contrib.auth.models import User, Permission
from django.contrib.auth import logout as do_logout, login as do_login , authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
#para ver la lista de permisos de un usuairo
#perm_tuple = [(x.id, x.name) for x in Permission.objects.filter(user=2)]
# Create your views here.
class LogView(View):
    def login(request):
        #Creamos el formulario de autenticación vacío
        form = AuthenticationForm()
        if request.method == "POST":
            # Añadimos los datos recibidos al formulario
            form = AuthenticationForm(data=request.POST)
            # Si el formulario es válido->
            if form.is_valid():
                # Recuperamos las credenciales validadas
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Verificamos las credenciales del usuario
                user = authenticate(username=username, password=password)

                # Si existe un usuario con ese nombre y contraseña
                if user is not None:
                    # Hacemos el login manualmente
                    do_login(request, user)
                    # Y le redireccionamos a la portada
                    return redirect('/')

        # Si llegamos al final renderizamos el formulario
        arg={
            'form': form
        }
        return render(request, "log/login.html", arg)

    def logout(request):
        # Finalizamos la sesión
        do_logout(request)
        # Redireccionamos a la portada
        return redirect('/')

class UserView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_user'):
            all = User.objects.filter(is_active=1)
            args = {
                "querys":all,
                "titulo":"user",
                "titulo_view":"Usuario"
            }
            return render(request, 'User/index.html', args)
        else:
            error = "No tienes permiso para ver un usuario"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_user'):
            user = User.objects.get(id=id)
            form = UserForm(instance=user)
            args = {
                "form":form,
                "titulo":"user",
                "titulo_view":"Usuario"
            }
            return render(request, 'User/show.html', args)
        else:
            error = "No tienes permiso para ver este un usuario"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_user'):
            #Creamos el formulario de autenticación vacío
            form = UserForm()
            #permissions=Permission.objects.all()
            if request.method == "POST":
                # Añadimos los datos recibidos al formulario
                form = UserForm(data=request.POST)
                # Si el formulario es válido...
                if form.is_valid():
                    # Creamos la nueva cuenta de usuario
                    user = form.save()
                    #user.user_permissions.add(request.POST["id_permission"])
                    user.save()
                    # Si el usuario se crea correctamente 
                    if user is not None:
                        # Hacemos el login manualmente
                        do_login(request, user)
                        # Y le redireccionamos a la portada
                        return redirect('/login')
                else:
                    arg={
                    'form': form,
                    #'permissions':permissions,
                    "titulo":"user",    
                    "titulo_view":"Usuario"
                    }
                    # Si llegamos al final renderizamos el formulario
                    return render(request, "user/new.html", arg)
            else:
                form.fields['username'].help_text = None
                form.fields['password1'].help_text = None
                form.fields['password2'].help_text = None
                arg={
                    'form': form,
                    #'permissions':permissions,
                    "titulo":"user",    
                    "titulo_view":"Usuario"
                    }
                # Si llegamos al final renderizamos el formulario
                return render(request, "user/new.html", arg)
        else:
            error = "No tienes permiso para crear un usuario"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_user'):
            user = User.objects.get(id=id)
            form = UserForm(request.POST, instance=user)
            if request.method == "POST":
                if form.is_valid():
                    form.save()
                    args={
                        'form':form,
                        'user':user,
                        "titulo":"user",
                        "titulo_view":"Usuario"
                    }
            else:
                form = UserForm(instance=user)
                """form.fields['username'].help_text = None
                form.fields['password1'].help_text = None
                form.fields['password2'].help_text = None """
                args={
                        'form':form,
                        'user':user,
                        "titulo":"user",
                        "titulo_view":"Usuario"
                    }
            return render(request, 'User/update.html', args)
        else:
            error = "No tienes permiso para modificar un usuario"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    def delete(request,id):
        if request.user.has_perm('ModelsMaster.add_user'):
            user = User.objects.get(id=id)
            user.is_active = 0
            user.save()
            eliminado = "El usuario se ha eliminado"
            all = User.objects.filter(is_active=1)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"user",
                "titulo_view":"Usuario"
            }
            return render(request, 'User/index.html', args)
        else:
            error = "No tienes permiso para borrar un usuario"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

@login_required
def index(request):
    return render(request, 'index.html')

class AmbitoView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_ambito'):
            all = Ambito.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"ambito",
                "titulo_view":"Ambito"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un ambito"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_ambito'):
            ambito = Ambito.objects.get(Id=id)
            form = AmbitoForm(instance=ambito)
            args = {
                "form":form,
                "titulo":"ambito",
                "titulo_view":"Ambito"
            }
            return render(request, 'base_show.html', args)

        else:
            error = "No tienes permiso para ver ambitos"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_ambito'):
            form = AmbitoForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "El ambito se ha creado con éxito"
                all = Ambito.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"ambito",
                    "titulo_view":"Ambito"
                }
                return render(request, 'base_index.html', args )
            else:
                args = {
                    'form': form,
                    "titulo":"ambito",
                    "titulo_view":"Ambito"
                }
                return render (request, 'base_form.html', args )
        else:
            error = "No tienes permiso para crear un nuevo ambito"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_ambito'):
            ambito = Ambito.objects.get(Id=id)
            form = AmbitoForm(request.POST or None, instance=ambito)
            if form.is_valid():
                form.save()
                aviso = "Se han actualizado los datos"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"ambito",
                    "titulo_view":"Ambito"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"ambito",
                    "titulo_view":"Ambito"
                }
            return render(request, 'base_form.html',args)
        else:
            error = "No tienes permiso para modificar un ambito"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.add_ambito'):
            ambito = Ambito.objects.get(Id=id)
            all = Ambito.objects.filter(Eliminado=False)
            am_pc = PuntosCapitulo.objects.filter(IdAm=ambito.Id)
            if am_pc:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"ambito",
                    "titulo_view":"Ambito"
                }
            else:
                ambito.Eliminado = True
                ambito.save()
                eliminado = "El ambito se ha eliminado"
                all = Ambito.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"ambito",
                    "titulo_view":"Ambito"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un ambito"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class TipoObjetivoView(View):
    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_tipoobjetivo'):
            all = TipoObjetivo.objects.filter(Eliminado=False)
            args = {
                #"tipos_objetivos":all
                "querys":all,
                "titulo":"tipo_objetivo",
                "titulo_view":"Tipo Objetivo"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver tipo objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_tipoobjetivo'):
            tipo_objetivo = TipoObjetivo.objects.get(Id=id)
            form = TipoObjetivoForm(instance=tipo_objetivo)
            args = {
                "form":form,
                "titulo":"tipo_objetivo",
                "titulo_view":"Tipo Objetivo"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un tipo objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_tipoobjetivo'):
            form = TipoObjetivoForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "El tipo objetivo se ha creado con éxito"
                all = TipoObjetivo.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"tipo_objetivo",
                    "titulo_view":"Tipo Objetivo"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":form,
                    "titulo":"tipo_objetivo",
                    "titulo_view":"Tipo Objetivo"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un tipo objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_tipoobjetivo'):
            tipo_objetivo = TipoObjetivo.objects.get(Id=id)
            form = TipoObjetivoForm(request.POST or None, instance = tipo_objetivo)
            if form.is_valid():
                form.save()
                aviso = "Los datos se han actualizado!"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"tipo_objetivo",
                    "titulo_view":"Tipo Objetivo"
                }
                return render(request, 'base_form.html', args)
            else:
                args = {
                    "form":form,
                    "titulo":"tipo_objetivo",
                    "titulo_view":"Tipo Objetivo"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un tipo objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_tipoobjetivo'):
            #TODO:
            tipo_objetivo = TipoObjetivo.objects.get(Id=id)
            tipo_objetivo.Eliminado = True
            tipo_objetivo.save()
            eliminado = "El tipo objetivo se ha eliminado"
            all = TipoObjetivo.objects.filter(Eliminado=False)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"tipo_objetivo",
                "titulo_view":"Tipo Objetivo"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un tipo objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class EstructuraView(View):
    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_estructura'):
            all = Estructura.objects.filter(Eliminado=False)
            args = {
                #"estructuras":all
                "querys":all,
                "titulo":"estructura",
                "titulo_view":"Estructura"
            }
            #return render(request, 'Estructura/index.html', args)
            return render(request, 'base_index.html', args)
        else:
                error = "No tienes permiso para ver una estructura"
                args = {
                    "error":error
                }
                return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_estructura'):
            estructura = Estructura.objects.get(Id=id)
            form = EstructuraForm(instance=estructura)
            args = {
                "form":form,
                "titulo":"estructura",
                "titulo_view":"Estructura"
            }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para ver una estructura"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_estructura'):
            form = EstructuraForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "La estructura se ha creado con éxito"
                all = Estructura.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"estructura",
                    "titulo_view":"Estructuras"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":form,
                    "titulo":"estructura",
                    "titulo_view":"Estructuras"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear una estructura"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_estructura'):
            estructura = Estructura.objects.get(Id=id)
            form = EstructuraForm(request.POST or None, instance=estructura)
            if form.is_valid():
                form.save()
                aviso = "Los datos se han actualizado!"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"estructura",
                    "titulo_view":"Estructuras"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"estructura",
                    "titulo_view":"Estructuras"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar una estructura"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_estructura'):
            #TODO:
            all = Estructura.objects.filter(Eliminado=False)
            estructura = Estructura.objects.get(Id=id)
            proceso = Proceso.objects.filter(IdEst=estructura)
            if proceso:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, bórralos primero",
                    "querys":all,
                    "titulo":"estructura",
                    "titulo_view":"Estructura"
                }
            else:
                estructura.Eliminado = True
                estructura.save()
                eliminado = "El tipo objetivo se ha eliminado"
                all = Estructura.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"estructura",
                    "titulo_view":"Estructura"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar una estructura"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class RiesgoView(View):

    def index(request):
        if request.user.has_perm('ModelsMaster.add_ambito'):
            all = Riesgo.objects.filter(Eliminado=False)
            args = {
                #"riesgos":all
                "querys":all,
                "titulo":"riesgo",
                "titulo_view":"Riesgo"
            }
            #return render(request, 'Riesgo/index.html', args)
            return render(request, 'base_index.html', args)

    def show(request,id):
        riesgo = Riesgo.objects.get(Id=id)
        args = {
            "riesgo":riesgo
        }
        return render(request, 'Riesgo/show.html', args)

    def create(request):
        form = RiesgoForm(request.POST or None)
        if form.is_valid():
            form.save()
            aviso = "El riesgo se ha creado con éxito"
            all = Riesgo.objects.filter(Eliminado=False)
            args = {
                "aviso":aviso,
                "riesgos":all
            }
            return render(request, 'Riesgo/index.html', args)
        else:
            args = {
                "form":form
            }
            return render(request, 'Riesgo/new.html', args)

    def edit(request,id):
        riesgo = Riesgo.objects.get(Id=id)
        args = {
            "riesgo":riesgo
        }
        return render(request, 'Riesgo/edit.html', args)

    def update(request,id):
        riesgo = Riesgo.objects.get(Id=id)
        form = RiesgoForm(request.POST, instance=riesgo)
        if form.is_valid():
            form.save()
            aviso = "Los datos se han actualizado con éxito"
            args = {
                "aviso":aviso,
                "riesgo":riesgo
            }
            return render(request, 'Riesgo/edit.html', args)
        else:
            args = {
                "riesgo":riesgo,
                "form":form
            }
            return render(request, 'Riesgo/edit.html', args)

    def delete(request,id):
        riesgo = Riesgo.objects.get(Id=id)
        riesgo.Eliminado = True
        riesgo.save()
        all = Riesgo.objects.filter(Eliminado=False)
        eliminado = "El riesgo se ha eliminado"
        args = {
            "eliminado":eliminado,
            "querys":all,
            "titulo":"riesgo",
            "titulo_view":"Riesgo"
        }
        return render(request, 'base_indexindex.html', args)

class TipoIntervinienteView(View):

    def index(request):
        all = TipoInterviniente.objects.filter(Eliminado=False)
        args = {
            #"tipo_intervinientes":all
            "querys":all,
            "titulo":"tipo_interviniente",
            "titulo_view":"Tipo Interviniente"
        }
        #return render(request, 'TipoInterviniente/index.html', args)
        return render(request, 'base_index.html', args)

    def show(request,id):
        tipo_interviniente = TipoInterviniente.objects.get(Id=id)
        args = {
            "tipo_interviniente":tipo_interviniente
        }
        return render(request, 'TipoInterviniente/show.html', args)

    def new(request):
        return render(request, 'TipoInterviniente/new.html')

    def create(request):
        ModelForm_form = TipoIntervinienteForm(request.POST)
        if ModelForm_form.is_valid():
            ModelForm_form.save()
            aviso = "El tipo interviniente se ha creado con éxito!"
            all = TipoInterviniente.objects.filter(Eliminado=False)
            args ={
                "aviso":aviso,
                "tipo_intervinientes":all
            }
            return render(request, 'TipoInterviniente/index.html', args)
        else:
            args = {
                "form":ModelForm_form
            }
            return render(request, 'TipoInterviniente/new.html', args)

    def edit(request,id):
        tipo_interviniente = TipoInterviniente.objects.get(Id=id)
        args = {
            "tipo_interviniente":tipo_interviniente
        }
        return render(request, 'TipoInterviniente/edit.html', args)

    def update(request,id):
        tipo_interviniente = TipoInterviniente.objects.get(Id=id)
        ModelForm_form = TipoIntervinienteForm(request.POST, instance=tipo_interviniente)
        if ModelForm_form.is_valid():
            aviso = "Los datos se han actualizado con éxito"
            args = {
                "aviso":aviso,
                "tipo_interviniente":tipo_interviniente
            }
        else:
            args = {
                "form":ModelForm_form,
                "tipo_interviniente":tipo_interviniente
            }
        return render(request, 'TipoInterviniente/edit.html', args)

    def delete(request,id):
        tipo_interviniente = TipoInterviniente.objects.get(Id=id)
        tipo_interviniente.Eliminado = True
        tipo_interviniente.save()
        eliminado = "El tipo Interviniente se ha eliminado"
        all = TipoInterviniente.objects.filter(Eliminado=False)
        args = {
            "eliminado":eliminado,
            "querys":all,
            "titulo":"tipo_interviniente",
            "titulo_view":"Tipo Interviniente"
        }
        return render(request, 'base_index.html', args)

class SectorView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_sector'):
            all = Sector.objects.filter(Eliminado=False)
            args = {
                #"sectores":all
                "querys":all,
                "titulo":"sector",
                "titulo_view":"Sector"
            }
            #return render(request, 'Sector/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver sector"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_sector'):
            sector = Sector.objects.get(Id=id)
            form = SectorForm(instance=sector)
            args = {
                "form":form,
                "titulo":"sector",
                "titulo_view":"Sector"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un sector"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_sector'):
            ModelForm_form = SectorForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El sector se ha creado con éxito!"
                all = Sector.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"sector",
                    "titulo_view":"Sector"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"sector",
                    "titulo_view":"Sector"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un sector"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_sector'):
            sector = Sector.objects.get(Id=id)
            ModelForm_form = SectorForm(request.POST or None, instance=sector)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"sector",
                    "titulo_view":"Sector"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"sector",
                    "titulo_view":"Sector"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un sector"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_sector'):
            all = Sector.objects.filter(Eliminado=False)
            sector = Sector.objects.get(Id=id)
            sc_emp = Empresa.objects.filter(Id=sector.Id)
            sc_bench = Benchmarking.objects.filter(Id=sector.Id)
            if sc_emp or sc_bench:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"sector",
                    "titulo_view":"Sector"
                }
            else:
                sector.Eliminado = True
                sector.save()
                eliminado = "El sector se ha eliminado"
                all = Sector.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"sector",
                    "titulo_view":"Sector"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un sector"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class NivelAreaGeograficaView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_nivelareageografica'):
            all = NivelAreaGeografica.objects.filter(Eliminado=False)
            args = {
                #"nags":all
                "querys":all,
                "titulo":"nag",
                "titulo_view":"Nivel Área Geográfica"
            }
            #return render(request, 'Nag/index.html', args)
            return render(request, 'Nag/index.html', args)
        else:
            error = "No tienes permiso para ver un Nivel area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_nivelareageografica'):
            nag = NivelAreaGeografica.objects.get(Id=id)
            form = NivelAreaGeograficaForm(instance=nag)
            args = {
                "form":form,
                "titulo":"nag",
                "titulo_view":"Nivel Área Geográfica"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un nivel area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_nivelareageografica'):
            ModelForm_form = NivelAreaGeograficaForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El Nivel de Área geográfica se ha creado con éxito!"
                all = NivelAreaGeografica.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"nag",
                    "titulo_view":"Nivel Área Geográfica"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"nag",
                    "titulo_view":"Nivel Área Geográfica"
                }
                return render (request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un nivel area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_nivelareageografica'):
            nag = NivelAreaGeografica.objects.get(Id=id)
            ModelForm_form = NivelAreaGeograficaForm(request.POST or None, instance=nag)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"nag",
                    "titulo_view":"Nivel Área Geográfica"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"nag",
                    "titulo_view":"Nivel Área Geográfica"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un nivel area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_nivelareageografica'):
            all = NivelAreaGeografica.objects.filter(Eliminado=False)
            nag = NivelAreaGeografica.objects.get(Id=id)
            nag_ag = AreaGeografica.objects.filter(IdNag=nag.Id)
            if nag_ag:
                args = {
                    "eliminado":"No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"nag",
                    "titulo_view":"Nivel Área Geográfica"
                }
            else:
                nag.Eliminado = True
                nag.save()
                eliminado = "El Nivel de Área geográfica se ha eliminado"
                all = NivelAreaGeografica.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"nag",
                    "titulo_view":"Nivel Área Geográfica"
                }
            return render(request, 'Nag/index.html', args)
        else:
            error = "No tienes permiso para crear un nivel area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class AreaGeograficaView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_areageografica'):
            all = AreaGeografica.objects.filter(Eliminado=False)
            nags = NivelAreaGeografica.objects.filter(Eliminado=False)
            args = {
                #"ags":all
                "querys":all,
                "titulo":"area_geografica",
                "titulo_view":"Área Geográfica",
                "filtro":nags
            }
            #return render(request, 'AreaGeografica/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_areageografica'):
            ag = AreaGeografica.objects.get(Id=id)
            form = AreaGeograficaForm(instance=ag)
            nags = NivelAreaGeografica.objects.filter(Eliminado=False)
            hijos = AreaGeografica.objects.filter(IdParent=ag.Id)
            args = {
                "form":form,
                "titulo":"area_geografica",
                "titulo_view":"Área Geográfica",
                "nags":nags,
                "hijos":hijos
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_areageografica'):
            ModelForm_form = AreaGeograficaForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El Área geográfica se ha creado con éxito!"
                all = AreaGeografica.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"area_geografica",
                    "titulo_view":"Área Geográfica",
                }
                return render(request, 'base_index.html', args)
            else:
                all = AreaGeografica.objects.filter(Eliminado=False)
                args = {
                    "form":ModelForm_form,
                    "querys":all,
                    "titulo":"area_geografica",
                    "titulo_view":"Área Geográfica",
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_areageografica'):
            ag = AreaGeografica.objects.get(Id=id)
            ModelForm_form = AreaGeograficaForm(request.POST or None, instance=ag)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"area_geografica",
                    "titulo_view":"Área Geográfica",
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"area_geografica",
                    "titulo_view":"Área Geográfica",
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_areageografica'):
            all = AreaGeografica.objects.filter(Eliminado=False)
            ag = AreaGeografica.objects.get(Id=id)
            ag_parent = AreaGeografica.objects.filter(IdParent=ag.Id)
            bench_ag = Benchmarking.objects.filter(IdAg=ag.Id)
            emp_ag = Empresa.objects.filter(IdAg=ag.Id)
            if ag_parent or bench_ag or emp_ag:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"area_geografica",
                    "titulo_view":"Área Geográfica"
                }
            else:
                ag.Eliminado = True
                ag.save()
                eliminado = "El Área geográfica se ha eliminado"
                all = AreaGeografica.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"area_geografica",
                    "titulo_view":"Área Geográfica"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un area geografica"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class EmpresaView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_empresa'):
            all = Empresa.objects.filter(Eliminado=False)
            args = {
                #"emps":all
                "querys":all,
                "titulo":"empresa",
                "titulo_view":"Empresa"
            }
            #return render(request, 'Empresa/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver una empresa"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_empresa'):
            emp = Empresa.objects.get(Id=id)
            form = EmpresaForm(instance=emp)
            args = {
                "form":form,
                "titulo":"empresa",
                "titulo_view":"Empresa"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver una empresa"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_empresa'):
            ModelForm_form = EmpresaForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "La empresa se ha creado con éxito!"
                all = Empresa.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"empresa",
                    "titulo_view":"Empresa"
                }
                return render(request, 'base_index.html', args)
            else:
                emp_scs = Sector.objects.filter(Eliminado=False)
                emp_ags = AreaGeografica.objects.filter(Eliminado=False)
                args = {
                    "form":ModelForm_form,
                    "titulo":"empresa",
                    "titulo_view":"Empresa"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear una nueva empresa"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required 
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_empresa'):
            emp = Empresa.objects.get(Id=id)
            ModelForm_form = EmpresaForm(request.POST or None, instance=emp)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"empresa",
                    "titulo_view":"Empresa"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"empresa",
                    "titulo_view":"Empresa"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar una empresa"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_empresa'):
            all = Empresa.objects.filter(Eliminado=False)
            emp = Empresa.objects.get(Id=id)
            md_emp = Modelo.objects.filter(IdEmp=emp.Id)
            if md_emp:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"empresa",
                    "titulo_view":"Empresa"
                }
            else:
                emp.Eliminado = True
                emp.save()
                eliminado = "la empresa se ha eliminado"
                all = Empresa.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"empresa",
                    "titulo_view":"Empresa"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar una empresa"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class ModeloView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_modelo'):
            all=Modelo.objects.filter(Eliminado=False)
            args= {
                #"modelos":all
                "querys":all,
                "titulo":"modelo",
                "titulo_view":"Modelo"
            }
            #return render(request, 'Modelo/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un modelo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_modelo'):
            modelo = Modelo.objects.get(Id=id)
            form = ModeloForm(instance=modelo)
            args = {
                "form":form,
                "titulo":"modelo",
                "titulo_view":"Modelo"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un modelo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_modelo'):
            ModelForm_form = ModeloForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El Modelo se ha creado con éxito!"
                all = Modelo.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"modelo",
                    "titulo_view":"Modelo"
                }
                return render(request, 'base_index.html', args)
            else:
                modelo_emps = Empresa.objects.filter(Eliminado=False)
                args = {
                    "form":ModelForm_form,
                    "titulo":"modelo",
                    "titulo_view":"Modelo"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un nuevo modelo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_modelo'):
            modelo = Modelo.objects.get(Id=id)
            ModelForm_form = ModeloForm(request.POST or None, instance=modelo)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"modelo",
                    "titulo_view":"Modelo"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"modelo",
                    "titulo_view":"Modelo"
                    
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un modelo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_modelo'):
            all = Modelo.objects.filter(Eliminado=False)
            modelo = Modelo.objects.get(Id=id)
            pc_md = PuntosCapitulo.objects.filter(IdMd=modelo.Id)
            if pc_md:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"modelo",
                    "titulo_view":"Modelo"
                }
            else:
                modelo.Eliminado = True
                modelo.save()
                eliminado = "El Modelo se ha eliminado"
                all = Modelo.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"modelo",
                    "titulo_view":"Modelo"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un modelo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
            
class BenchmarkingView(View):
    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_benchmarking'):
            all = Benchmarking.objects.filter(Eliminado=False)
            args = {
                #"benchs":all
                "querys":all,
                "titulo":"benchmarking",
                "titulo_view":"Benchmarking"
            }
            #return render(request, 'Benchmarking/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un benchmarking"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_benchmarking'):
            bench = Benchmarking.objects.get(Id=id)
            form = BenchmarkingForm(instance=bench)
            args = {
                "form":form,
                "titulo":"benchmarking",
                "titulo_view":"Benchmarking"
            }
            return render(request, 'Benchmarking/show.html', args)
        else:
            error = "No tienes permiso para ver un benchmarking"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_benchmarking'):
            ModelForm_form = BenchmarkingForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El Benchmarking se ha creado con éxito!"
                all = Benchmarking.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"benchmarking",
                    "titulo_view":"Benchmarking"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"benchmarking",
                    "titulo_view":"Benchmarking"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un benchmarking"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_benchmarking'):
            bench = Benchmarking.objects.get(Id=id)
            ModelForm_form = BenchmarkingForm(request.POST or None, instance=bench)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "bench":bench,
                    "titulo":"benchmarking",
                    "titulo_view":"Benchmarking"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "bench":bench,
                    "titulo":"benchmarking",
                    "titulo_view":"Benchmarking"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un benchmarking"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_benchmarking'):
            bench = Benchmarking.objects.get(Id=id)
            bench.Eliminado = True
            bench.save()
            eliminado = "El benchmarking se ha eliminado"
            all = Benchmarking.objects.filter(Eliminado=False)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"benchmarking",
                "titulo_view":"Benchmarking"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un benchmarking"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class PuntosCapituloView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_puntoscapitulo'):
            all=PuntosCapitulo.objects.filter(Eliminado=False) 
            args = {
                #"pcs":all
                "querys":all,
                "titulo":"puntoscap",
                "titulo_view":"Puntos Capitulo"
            }
            #return render(request, 'PuntosCapitulo/index.html', args)
            return render(request, 'PuntosCapitulo/index.html', args)
        else:
            error = "No tienes permiso para ver un punto capitulo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_puntoscapitulo'):
            pc = PuntosCapitulo.objects.get(Id=id)
            form = PuntosCapituloForm(instance=pc)
            args = {
                "form":form,
                "titulo":"puntoscap",
                "titulo_view":"Puntos Capitulo"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un punto capitulo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_puntoscapitulo'):
            ModelForm_form = PuntosCapituloForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El PuntoCapitulo se ha creado con éxito!"
                all = PuntosCapitulo.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"puntoscap",
                    "titulo_view":"Puntos Capitulo"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"puntoscap",
                    "titulo_view":"Puntos Capitulo"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un punto capitulo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_puntoscapitulo'):
            pc = PuntosCapitulo.objects.get(Id=id)
            ModelForm_form = PuntosCapituloForm(request.POST or None, instance=pc)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"puntoscap",
                    "titulo_view":"Puntos Capitulo"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"puntoscap",
                    "titulo_view":"Puntos Capitulo"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar punto capitulo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_puntoscapitulo'):
            # TODO:
            #pendiente de Actulaizar
            all = PuntosCapitulo.objects.filter(Eliminado=False)
            pc = PuntosCapitulo.objects.get(Id=id)
            ob_pc = Objetivo.objects.filter(IdPc=pc.Id)
            if ob_pc:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"puntoscap",
                    "titulo_view":"Puntos Capitulo"
                }
            else:
                pc.Eliminado = True
                pc.save()
                eliminado = "El PuntoCapitulo se ha eliminado"
                all = PuntosCapitulo.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"puntoscap",
                    "titulo_view":"Puntos Capitulo"
                }
            return render(request, 'PuntosCapitulo/index.html', args)
        else:
            error = "No tienes permiso para borrar un punto capitulo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
        
class ObjetivoView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_objetivo'):
            all=Objetivo.objects.filter(Eliminado=False) 
            args = {
                #"objs":all
                "querys":all,
                "titulo":"objetivo",
                "titulo_view":"Objetivo"
            }
            #return render(request, 'Objetivo/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_objetivo'):
            obj = Objetivo.objects.get(Id=id)
            form = ObjetivoForm(instance=obj)
            hijos = Objetivo.objects.filter(IdParent=obj.Id)
            args = {
                "form":form,
                "titulo":"objetivo",
                "titulo_view":"Objetivo",
                "hijos":hijos
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para verr un objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_objetivo'):
            ModelForm_form = ObjetivoForm(request.POST or None)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "El Objetivo se ha creado con éxito!"
                all = Objetivo.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"objetivo",
                    "titulo_view":"Objetivo"    
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"objetivo",
                    "titulo_view":"Objetivo"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear un objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_objetivo'):
            obj = Objetivo.objects.get(Id=id)
            ModelForm_form = ObjetivoForm(request.POST or None, instance=obj)
            if ModelForm_form.is_valid():
                ModelForm_form.save()
                aviso = "Los datos se han actualizado con éxito"
                args = {
                    "aviso":aviso,
                    "form":ModelForm_form,
                    "titulo":"objetivo",
                    "titulo_view":"Objetivo"
                }
            else:
                args = {
                    "form":ModelForm_form,
                    "titulo":"objetivo",
                    "titulo_view":"Objetivo"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar un objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_objetivo'):
            # TODO:
            #pendiente de actualizar
            obj = Objetivo.objects.get(Id=id)
            obj.Eliminado = True
            obj.save()
            eliminado = "El Objetivo se ha eliminado"
            all = Objetivo.objects.filter(Eliminado=False)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"objetivo",
                "titulo_view":"Objetivo"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un objetivo"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class MetaView(View):
    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_meta'):
            all = Meta.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"meta",
                "titulo_view":"Meta"
            }
            return render(request,'base_index.html',args)
        else:
            error = "No tienes permiso para ver una meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_meta'):
            meta = Meta.objects.get(Id=id)
            form = MetaForm(instance=meta)
            hijos = Meta.objects.filter(IdParent=meta.Id)
            args = {
                "form":form,
                "titulo":"meta",
                "titulo_view":"Meta",
                "hijos":hijos
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver una meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_meta'):
            form = MetaForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "La meta se ha creado con éxito"
                all = Meta.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"meta",
                    "titulo_view":"Meta"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":form,
                    "titulo":"meta",
                    "titulo_view":"Meta"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear una nueva meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_meta'):
            meta = Meta.objects.get(Id=id)
            form = MetaForm(request.POST or None, instance=meta)
            if form.is_valid():
                form.save()
                aviso = "Se han actualizado los datos"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"meta",
                    "titulo_view":"Meta"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"meta",
                    "titulo_view":"Meta"
                }
            return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar una meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_meta'):
            meta = Meta.objects.get(Id=id)
            all = Meta.objects.filter(Eliminado=False)
            meta_accmeta=AccionMeta.objects.filter(IdMeta=meta.Id)
            if meta_accmeta:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"meta",
                    "titulo_view":"Meta"
                }
            else:
                meta.Eliminado = True
                meta.save()
                eliminado = "La meta se ha eliminado"
                all = Meta.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"meta",
                    "titulo_view":"Meta"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar una meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class AccionMetaView(View):
    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_accionmeta'):
            all = AccionMeta.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"accionmeta",
                "titulo_view":"Accion Meta"
            }
            return render(request, 'AccionMeta/index.html', args)
        else:
            error = "No tienes permiso para ver una nueva accion meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_accionmeta'):
            accion_meta = AccionMeta.objects.get(Id=id)
            form = AccionMetaForm(instance=accion_meta)
            args = {
                "form":form,
                "titulo":"accionmeta",
                "titulo_view":"Accion Meta"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver una nueva accion meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_accionmeta'):
            form = AccionMetaForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "La Accion Meta se ha creado con éxito"
                all = AccionMeta.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"accionmeta",
                    "titulo_view":"Accion Meta"
                }
                return render(request, 'base_index.html', args)
            else:
                args = {
                    "form":form,
                    "titulo":"accionmeta",
                    "titulo_view":"Accion Meta"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para crear una nueva accion meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_accionmeta'):
            accion_meta = AccionMeta.objects.get(Id=id)
            form = AccionMetaForm(request.POST or None, instance = accion_meta)
            if form.is_valid():
                form.save()
                aviso = "Los datos se han actualizado!"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"accionmeta",
                    "titulo_view":"Accion Meta"
                }
                return render(request, 'base_form.html', args)
            else:
                args = {
                    "form":form,
                    "titulo":"accionmeta",
                    "titulo_view":"Accion Meta"
                }
                return render(request, 'base_form.html', args)
        else:
            error = "No tienes permiso para modificar una accion meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_accionmeta'):
            accion_meta = AccionMeta.objects.get(Id=id)
            accion_meta.Eliminado = True
            accion_meta.save()
            eliminado = "La accion meta se ha eliminado"
            all = AccionMeta.objects.filter(Eliminado=False)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"accionmeta",
                "titulo_view":"Accion Meta"
            }
            return render(request, 'AccionMeta/index.html', args)
        else:
            error = "No tienes permiso para borrar una accion meta"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class IndicadorAccionProcesoView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_indicadoraccionproceso'):
            all = IndicadorAccionProceso.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"indicador_accion_proceso",
                "titulo_view":"Indicador Accion Proceso"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un indicador accion proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_indicadoraccionproceso'):
            indicador = IndicadorAccionProceso.objects.get(Id=id)
            form = IndicadorAccionProcesoForm(instance=indicador)
            args = {
                "form":form,
                "titulo":"indicador_accion_proceso",
                "titulo_view":"Indicador Accion Proceso"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un indicador accion proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_indicadoraccionproceso'):
            form = IndicadorAccionProcesoForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "El indicador Accion preoceso se ha creado con éxito"
                all = IndicadorAccionProceso.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"indicador_accion_proceso",
                    "titulo_view":"Indicador Accion Proceso"
                }
                return render(request, 'base_index.html', args )
            else:
                args = {
                    'form': form,
                    "titulo":"indicador_accion_proceso",
                    "titulo_view":"Indicador Accion Proceso"
                }
                return render (request, 'base_form.html', args )
        else:
            error = "No tienes permiso para crear un nuevo indicador accion proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required    
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_indicadoraccionproceso'):
            indicador = IndicadorAccionProceso.objects.get(Id=id)
            form = IndicadorAccionProcesoForm(request.POST or None, instance=indicador)
            if form.is_valid():
                form.save()
                aviso = "Se han actualizado los datos"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"indicador_accion_proceso",
                    "titulo_view":"Indicador Accion Proceso"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"indicador_accion_proceso",
                    "titulo_view":"Indicador Accion Proceso"
                }
            return render(request, 'base_form.html',args)
        else:
            error = "No tienes permiso para modificar un indicador accion proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_indicadoraccionproceso'):
            indicador = IndicadorAccionProceso.objects.get(Id=id)
            all = IndicadorAccionProceso.objects.filter(Eliminado=False)
            indicador_seguimiento = SeguimientoIndicadores.objects.filter(IdAccMeta=indicador.Id)
            if indicador_seguimiento:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"indicador_accion_proceso",
                    "titulo_view":"Indicador Accion Proceso"
                }
            else:
                indicador.Eliminado = True
                indicador.save()
                eliminado = "El indicador accion proceso se ha eliminado"
                all = IndicadorAccionProceso.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"indicador_accion_proceso",
                    "titulo_view":"Indicador Accion Proceso"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un indicador accion proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class DocumentosSistemaView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_documentossistema'):
            all = DocumentosSistema.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"documentos_sistema",
                "titulo_view":"Documentos Sistema"
            }
            #return render(request, 'Ambitos/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un documento sistema"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_documentossistema'):
            documento_sistema = DocumentosSistema.objects.get(Id=id)
            form = DocumentosSistemaForm(instance=documento_sistema)
            file = '/'+settings.MEDIA_URL+'files/DocumentosSistema/'+documento_sistema.Nombre
            args = {
                "form":form,
                "file":file,
                "titulo":"documentos_sistema",
                "titulo_view":"Documentos Sistema"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un documento sistema"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_documentossistema'):
            form = DocumentosSistemaForm(request.POST or None, request.FILES or None)
            if form.is_valid() and request.FILES['Archivo']:
                #request.FILES.get('Archivo',False)
                #aqui guardo el archivo en sí
                archivo = request.FILES['Archivo']
                #especifíco en que directorio se guarda
                directorio = settings.MEDIA_URL+'/files/DocumentosSistema/'
                #digo donde debe guardarse
                fs = FileSystemStorage(location=directorio, base_url=directorio)
                #guardo el archivo
                archivo_path = fs.save(archivo.name, archivo)
                #cojo la direccion dle archivo para poder presentarlo
                archivo_url = fs.url(archivo_path)
                #para poder operar con los campos del Modelo
                documento = form.save(commit=False)
                #guardo el nombre del archivo
                nombre = archivo_path
                #instancio manualmente el modelo con los datos personalizados
                guardar = DocumentosSistema(IdPc=documento.IdPc,Nombre=nombre,Codificacion=documento.Codificacion)
                #guardo el modelo con los datos perosnalizaods
                guardar.save()

                aviso = "El Documento Sistema se ha creado con éxito"
                all = DocumentosSistema.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"documentos_sistema",
                    "titulo_view":"Documentos Sistema"
                }
                return render(request, 'base_index.html', args )
            else:
                args = {
                    'form': form,
                    "titulo":"documentos_sistema",
                    "titulo_view":"Documentos Sistema"
                }
                return render (request, 'base_form.html', args )
        else:
            error = "No tienes permiso para crear un nuevo documento sistema"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.add_documentossistema'):
            documento_sistema = DocumentosSistema.objects.get(Id=id)
            form = DocumentosSistemaForm(request.POST or None, instance=documento_sistema)
            if form.is_valid():
                form.save()
                aviso = "Se han actualizado los datos"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"documentos_sistema",
                    "titulo_view":"Documentos Sistema"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"documentos_sistema",
                    "titulo_view":"Documentos Sistema"
                }
            return render(request, 'base_form.html',args)
        else:
            error = "No tienes permiso para modificar un documento sistema"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_documentossistema'):
            documento_sistema = DocumentosSistema.objects.get(Id=id)
            documento_sistema.Eliminado = True
            documento_sistema.save()
            #lo elimina del sistema, no se si imlpantarlo así o dejarlo
            #por si hay que recuperarlo en algún momento
            directorio = settings.MEDIA_URL+'/files/DocumentosSistema/'
            fs = FileSystemStorage(location=directorio, base_url=directorio)
            fs.delete(documento_sistema.Nombre)

            eliminado = "El Documento del Sistema se ha eliminado"
            
            all = DocumentosSistema.objects.filter(Eliminado=False)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"documentos_sistema",
                "titulo_view":"Documentos Sistema"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un documento sistema"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class SeguimientoIndicadoresView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_seguimientoindicadores'):
            all = SeguimientoIndicadores.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"seguimiento_indicadores",
                "titulo_view":"Seguimiento indicadores"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un seguimiento indicadores"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_seguimientoindicadores'):
            segin = SeguimientoIndicadores.objects.get(Id=id)
            form = SeguimientoIndicadoresForm(instance=segin)
            args = {
                "form":form,
                "titulo":"seguimiento_indicadores",
                "titulo_view":"Seguimiento indicadores"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un seguimiento indicadores"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_seguimientoindicadores'):
            form = SeguimientoIndicadoresForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "El Seguimiento indicador se ha creado con éxito"
                all = SeguimientoIndicadores.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"seguimiento_indicadores",
                    "titulo_view":"Seguimiento indicadores"
                }
                return render(request, 'base_index.html', args )
            else:
                args = {
                    'form': form,
                    "titulo":"seguimiento_indicadores",
                    "titulo_view":"Seguimiento indicadores"
                }
                return render (request, 'base_form.html', args )
        else:
            error = "No tienes permiso para crear un nuevo seguimiento indicadores"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_seguimientoindicadores'):
            segin = SeguimientoIndicadores.objects.get(Id=id)
            form = SeguimientoIndicadoresForm(request.POST or None, instance=segin)
            if form.is_valid():
                form.save()
                aviso = "Se han actualizado los datos"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"seguimiento_indicadores",
                    "titulo_view":"Seguimiento indicadores"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"seguimiento_indicadores",
                    "titulo_view":"Seguimiento indicadores"
                }
            return render(request, 'base_form.html',args)
        else:
            error = "No tienes permiso para modificar un seguimiento indicadores"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_seguimientoindicadores'):
            segin = SeguimientoIndicadores.objects.get(Id=id)
            segin.Eliminado = True
            segin.save()
            eliminado = "El Seguimiento indicador se ha eliminado"
            all = SeguimientoIndicadores.objects.filter(Eliminado=False)
            args = {
                "eliminado":eliminado,
                "querys":all,
                "titulo":"seguimiento_indicadores",
                "titulo_view":"Seguimiento indicadores"
            }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un seguimiento indicadores"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class ProcesoView(View):

    @login_required
    def index(request):
        if request.user.has_perm('ModelsMaster.view_proceso'):
            all = Proceso.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"proceso",
                "titulo_view":"Proceso"
            }
            #return render(request, 'Ambitos/index.html', args)
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para ver un proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

    @login_required
    def show(request,id):
        if request.user.has_perm('ModelsMaster.view_proceso'):
            proceso = Proceso.objects.get(Id=id)
            form = ProcesoForm(instance=proceso)
            args = {
                "form":form,
                "titulo":"proceso",
                "titulo_view":"Proceso"
            }
            return render(request, 'base_show.html', args)
        else:
            error = "No tienes permiso para ver un proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def create(request):
        if request.user.has_perm('ModelsMaster.add_proceso'):
            form = ProcesoForm(request.POST or None)
            if form.is_valid():
                form.save()
                aviso = "El Proceso se ha creado con éxito"
                all = Proceso.objects.filter(Eliminado=False)
                args = {
                    "aviso":aviso,
                    "querys":all,
                    "titulo":"proceso",
                    "titulo_view":"Proceso"
                }
                return render(request, 'base_index.html', args )
            else:
                args = {
                    'form': form,
                    "titulo":"proceso",
                    "titulo_view":"Proceso"
                }
                return render (request, 'base_form.html', args )
        else:
            error = "No tienes permiso para crear un nuevo proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    def update(request,id):
        if request.user.has_perm('ModelsMaster.change_proceso'):
            proceso = Proceso.objects.get(Id=id)
            form = ProcesoForm(request.POST or None, instance=proceso)
            if form.is_valid():
                form.save()
                aviso = "Se han actualizado los datos"
                args = {
                    "aviso":aviso,
                    "form":form,
                    "titulo":"proceso",
                    "titulo_view":"Proceso"
                }
            else:
                args = {
                    "form":form,
                    "titulo":"proceso",
                    "titulo_view":"Proceso"
                }
            return render(request, 'base_form.html',args)
        else:
            error = "No tienes permiso para modificar un proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)
    
    @login_required
    def delete(request,id):
        if request.user.has_perm('ModelsMaster.delete_proceso'):
            proceso = Proceso.objects.get(Id=id)
            all = Proceso.objects.filter(Eliminado=False)
            proceso_segin = IndicadorAccionProceso.objects.filter(IdProc=proceso.Id)
            if proceso_segin:
                args = {
                    "eliminado": "No puedes borrar este elemento porque otros dependen de él, borralos primero",
                    "querys":all,
                    "titulo":"proceso",
                    "titulo_view":"Proceso"
                }
            else:
                proceso.Eliminado = True
                proceso.save()
                eliminado = "El Proceso se ha eliminado"
                all = Proceso.objects.filter(Eliminado=False)
                args = {
                    "eliminado":eliminado,
                    "querys":all,
                    "titulo":"proceso",
                    "titulo_view":"Proceso"
                }
            return render(request, 'base_index.html', args)
        else:
            error = "No tienes permiso para borrar un proceso"
            args = {
                "error":error
            }
            return render(request, 'index.html', args)

class UserEmpresaView(View):

    def index(request):
            all = UserEmpresa.objects.filter(Eliminado=False)
            args = {
                "querys":all,
                "titulo":"user_empresa",
                "titulo_view":"Usuario de Empresa"
            }
            return render(request, "UserEmpresa/index.html", args)
    
    def show(request,id):
        user_empresa = UserEmpresa.objects.get(Id=id)
        form = UserEmpresaForm(instance=user_empresa)
        args = {
            "form":form,
            "titulo":"user_empresa",
            "titulo_view":"Usuario de Empresa"
        }
        return render(request, 'UserEmpresa/show.html', args)

    def create(request):
        form = UserEmpresaForm(request.POST or None)
        if form.is_valid():
            form.save()
            aviso="El Usuario de Empresa se ha creado con éxito"
            all = UserEmpresa.objects.filter(Eliminado=False)
            args = {
                "aviso":aviso,
                "querys":all,
                "titulo":"user_empresa",
                "titulo_view":"Usuario de Empresa"
            }
            return render(request, "UserEmpresa/index.html", args)
        else:
            args = {
                "form":form,
                "titulo":"user_empresa",
                "titulo_view":"Usuario de Empresa"
            }
            return render(request, "base_form.html", args)
    
    def update(request,id):
        user_empresa=UserEmpresa.objects.get(Id=id)
        form = UserEmpresaForm(request.POST or None, instance=user_empresa)
        if form.is_valid():
            form.save()
            aviso="Se han actualizado los datos"
            args={
                "aviso":aviso,
                "form":form,
                "titulo":"user_empresa",
                "titulo_view":"Usuario de Empresa"
            }
        else:
            args = {
                "form":form,
                "titulo":"user_empresa",
                "titulo_view":"Usuario de Empresa"
            }
        return render(request, "base_form.html", args)
    
    def delete(request,id):
        user_empresa=UserEmpresa.objects.get(Id=id)
        user_empresa.Eliminado = True
        user_empresa.save()
        eliminado = "El Usuario de Empresa se ha eliminado"
        all = UserEmpresa.objects.filter(Eliminado=False)
        args = {
            "eliminado":eliminado,
            "querys":all,
            "titulo":"user_empresa",
            "titulo_view":"Usuario de Empresa"
        }
        return render(request, "UserEmpresa/index.html", args)

class GroupEmpresaView(View):
    def index(request):
        all = GroupEmpresa.objects.filter(Eliminado=False)
        args = {
            "querys":all,
            "titulo":"group_empresa",
            "titulo_view":"Grupo de Empresa"
        }
        return render(request, "GroupEmpresa/index.html", args)
    
    def show(request,id):
        group_empresa = GroupEmpresa.objects.get(Id=id)
        form = GroupEmpresaForm(instance=group_empresa)
        args = {
            "form":form,
            "titulo":"group_empresa",
            "titulo_view":"Grupo de Empresa"
        }
        return render(request, "GroupEmpresa/show.html")
    
    def create(request):
        form = GroupEmpresaForm(request.POST or None)
        if form.is_valid():
            form.save()
            aviso = "El Grupo Empresa se ha creado con éxito"
            all = GroupEmpresa.objects.filter(Eliminado=False)
            args = {
                "aviso":aviso,
                "querys":all,
                "titulo":"group_empresa",
                "titulo_view":"Grupo de Empresa"
            }
            return render(request, "GroupEmpresa/index.html", args)
        else:
            args = {
                "form":form,
                "titulo":"group_empresa",
                "titulo_view":"Grupo de Empresa"
            }
            return render(request, "base_form.html", args)

    def update(request,id):
        group_empresa=GroupEmpresa.objects.get(Id=id)
        form = GroupEmpresaForm(request.POST or None, instance=group_empresa)
        if form.is_valid():
            form.save()
            aviso="Se han actualizado los datos"
            args={
                "aviso":aviso,
                "form":form,
                "titulo":"group_empresa",
                "titulo_view":"Grupo de Empresa"
            }
        else:
            args = {
                "form":form,
                "titulo":"group_empresa",
                "titulo_view":"Grupo de Empresa"
            }
        return render(request, "base_form.html", args)
    
    def delete(request,id):
        group_empresa=GroupEmpresa.objects.get(Id=id)
        group_empresa.Eliminado = True
        group_empresa.save()
        eliminado = "El Usuario de Empresa se ha eliminado"
        all = GroupEmpresa.objects.filter(Eliminado=False)
        args = {
            "eliminado":eliminado,
            "querys":all,
            "titulo":"group_empresa",
            "titulo_view":"Grupo de Empresa"
        }
        return render(request, "GroupEmpresa/index.html", args)
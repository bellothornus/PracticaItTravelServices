from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

def plazo_filtro(value):
    plazos = [
        "Semanal", 
        "Mensual", 
        "Trimestral", 
        "Bimestral",
        "Cuatrimestral",
        "Semastral",
        "Anual"
    ]
    if value not in plazos:
        raise ValidationError(
            _('%(value)s No se permite!'),
            params={'value': value},
        )

def fecha_filtro(value):
    if value > datetime.datetime.now():
        raise ValidationError(
            _('%(value)s No puedes poner una fecha mas tarde de la actual'),
            params={'value':value}
        )
import datetime

from accounts.models import User

def current_year(request) -> dict[str, int]:
    return {'current_year':datetime.date.today().year}

def user_groups(request):
    user:User = request.user
    return {
        'is_patient': (
            user.groups.filter(name='PATIENT').exists() if user.is_authenticated else False),
        'is_physio': (
            user.groups.filter(name='PHYSIO').exists() if user.is_authenticated else False),
        'is_physio_team': (
            user.groups.filter(name='PHYSIO_TEAM').exists() if user.is_authenticated else False),
    }
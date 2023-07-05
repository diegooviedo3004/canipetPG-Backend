import functools
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import UserInformation

def datos_ya_ingresados(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if UserInformation.objects.filter(user=request.user).count() == 1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/stepform/')
        return redirect('/stepform/')
    return wrapper

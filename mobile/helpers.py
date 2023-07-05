import functools
from django.contrib import messages
from django.shortcuts import redirect


def session_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
          if request.session.has_key('code'):
               return view_func(request, *args, **kwargs)
          else:
               return redirect(to="bienvenida")
    return wrapper
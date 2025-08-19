from django.shortcuts import redirect
from functools import wraps


def company_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not getattr(request.user, 'company', None):
            return redirect('dashboard:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

import django.dispatch

"""
Dispatched before rendering error template.
Must return name of template or None.
If name of template is returned it's used instead of the default error template.
"""
pre_error_rendering = django.dispatch.Signal(providing_args=["url_name", "params", "errors"])

"""
Dispatched before rendering a successful view execution.
Must return django.template.TemplateResponse or None.
If name of template is returned it's used instead of the default view template.
"""
pre_success_rendering = django.dispatch.Signal(providing_args=["url_name", "params", "data", "http_verb"])
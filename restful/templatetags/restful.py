import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django import template

register = template.Library()


@register.filter(name='jsonify')
def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)

@register.simple_tag(takes_context=True)
def query(context, *args, **kwargs):
    request = context.get('request')
    params = request.params.copy()
    added_params = {}

    for param_dict in args:
        added_params.update(param_dict)
    added_params.update(kwargs)

    for name, value in added_params.items():
        if params.get(name, None) is not None and value is None:
            del params[name]
        if value is not None:
            if isinstance(value, (list,tuple)):
                params.setlist(name, value)
            else:
                params[name] = value

    query_string = params.urlencode()

    return '' if not query_string else '?'+query_string

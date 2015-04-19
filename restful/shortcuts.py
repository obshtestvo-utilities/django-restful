import json

from django.contrib.messages.api import get_messages, constants


def errors(request):
    errors = {}
    for message in get_messages(request):
        if message.level == constants.ERROR:
            errors = dict(errors, **json.loads(message.message))
    return errors

def success(request):
    messages = {}
    for message in get_messages(request):
        if message.level == constants.SUCCESS:
            messages = dict(messages, **json.loads(message.message))
    return messages
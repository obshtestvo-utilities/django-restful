import json

from django.contrib.messages.api import get_messages, constants


def errors(request):
    errors_by_topic = {}
    for message in get_messages(request):
        if message.level == constants.ERROR:
            errors_by_topic = dict(errors_by_topic, **json.loads(message.message))

    return errors_by_topic

def success(request):
    messages = {}
    for message in get_messages(request):
        if message.level == constants.SUCCESS:
            messages = dict(messages, **json.loads(message.message))
    return messages

def last_input(request):
    for message in get_messages(request):
        if message.level == constants.INFO:
            data = json.loads(message.message)
            try:
                return data['input']
            except:
                continue

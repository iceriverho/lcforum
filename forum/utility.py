# -*- coding: utf-8 -*-
import uuid
import datetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    date = datetime.date.today().isocalendar()
    filename = "{2}/{3}/{4}/{0}.{1}".format(uuid.uuid4(), ext, *date)
    return filename
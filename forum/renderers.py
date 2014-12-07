# -*- coding: utf-8 -*-
from django.template import RequestContext

import rest_framework.renderers

class TemplateWithContextHTMLRenderer(rest_framework.renderers.TemplateHTMLRenderer):
    def resolve_context(self, data, request, response):
        if response.exception:
            data['status_code'] = response.status_code
        return RequestContext(request, {'context_data': data})
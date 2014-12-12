# -*- coding: utf-8 -*-

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'forum.renderers.TemplateWithContextHTMLRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}
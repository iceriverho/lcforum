# -*- coding: utf-8 -*-

class TemplatesMixin(object):
    def get_template_names(self):
        meta = self.get_queryset().model._meta
        app = meta.app_label
        name = meta.object_name.lower()

        templates = {
            'list': ["{0}/{1}/list.html".format(app, name), ],
            'retrieve': ["{0}/{1}/detail.html".format(app, name), ],
            'add': ["{0}/{1}/create.html".format(app, name), ],
            'edit': ["{0}/{1}/update.html".format(app, name), ],
            'delete': ["{0}/{1}/destroy.html".format(app, name), ],
        }

        if self.action in templates.keys():
            selected_templates = templates[self.action]
        else:
            selected_templates = ['rest_framework/api.html']

        return selected_templates
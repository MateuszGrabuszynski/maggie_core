from django.contrib import admin
from django.apps import apps

from maggie import models

all_models = apps.get_models()

for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


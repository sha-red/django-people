# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2016

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PeopleConfig(AppConfig):
    name = 'people'
    verbose_name = _("Personen")

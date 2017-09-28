# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2017

from django.conf.urls import url

from .views import PersonListView


urlpatterns = [
    url(r'^$',                      PersonListView.as_view(), name='person-list'),
    url(r'^(?P<letter>\w)/$',       PersonListView.as_view(), name='person-list-letter'),
]

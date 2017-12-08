# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2017


from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView

from .models import Person


class PersonListView(ListView):
    model = Person
    template_name = 'person/person_list.html'

    def get(self, request, *args, **kwargs):
        if 'letter' not in kwargs:
            return HttpResponsePermanentRedirect(reverse('person-list-letter', kwargs={'letter': 'a'}))
        else:
            return super(PersonListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(PersonListView, self).get_queryset()
        letter = self.kwargs.get('letter', 'a')
        return qs.filter(sort_name__istartswith=letter)

    def get_context_data(self, **kwargs):
        context = super(PersonListView, self).get_context_data(**kwargs)
        context['selected_letter'] = 'a'
        context['alphabet'] = 'abcdefghijklmnopqrstuvwxyz'
        return context


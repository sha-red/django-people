# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2016

from django.utils.translation import ugettext_lazy as _


class ArtPersonController(object):
    def get_lifetime_display(self):
        if self.birth_year and self.year_of_death:
            return u"%s–%s" % (self.birth_year, self.year_of_death)
        elif self.birth_year:
            return _("geb. %s") % self.birth_year
        else:
            return ""
    get_lifetime_display.short_description = _("Lebensdaten")


class PersonController(object):
    pass

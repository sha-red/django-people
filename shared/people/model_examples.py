from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from shared.utils.translation import get_translated_field

from .controllers import PersonController
from .models import PseudonymMixin, GroupMixin, BasePerson, PersonRoleBase, GenericParticipationRelBase


class Person(PersonController, PseudonymMixin, GroupMixin, BasePerson):
    class Meta(BasePerson.Meta):
        app_label = 'people'

    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'slug': self.slug})


class PersonRole(PersonRoleBase):
    class Meta(PersonRoleBase.Meta):
        verbose_name = _("Funktion")
        verbose_name_plural = _("Funktionen")
        ordering = ['order_index', 'name_de', 'name_en']

    def __str__(self):
        return self.name


class GenericParticipationRel(GenericParticipationRelBase):
    class Meta(GenericParticipationRelBase.Meta):
        app_label = 'people'

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2016


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel
from shared.utils.fields import AutoSlugField
from shared.utils.translation import get_translated_field

from .controllers import PersonController


@python_2_unicode_compatible
class ArtPersonMixin(models.Model):
    locations = models.CharField(_("Ort(e)"), max_length=100, blank=True, null=True)
    birth_year = models.PositiveIntegerField(_("Geburtsjahr"), blank=True, null=True)
    # TODO birthday statt birth_year verwenden für date_hierarchy und evtl. sortierung?
    year_of_death = models.PositiveIntegerField(_("Sterbejahr"), blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "%s%s" % (self.name, self.locations and " (%s)" % self.locations or "")


class GroupMixin(models.Model):
    is_group = models.BooleanField(_("Gruppe"), default=False, help_text=_("Bitte ankreuzen, wenn es sich um eine Gruppe handelt, und unten die Gruppenmitglieder auswählen"))
    members = models.ManyToManyField('self', verbose_name=_("Gruppenmitglieder"), blank=True, limit_choices_to={'is_group': False}, related_name='groups', symmetrical=False)

    class Meta:
        abstract = True


class PseudonymMixin(models.Model):
    main_person = models.ForeignKey('self', verbose_name=_("Haupteintrag"),
        null=True, blank=True, on_delete=models.PROTECT,
        related_name='pseudonym_set',
        help_text=_("Wenn es sich um eine alternative Schreibweise oder "
                    "ein Pseudonym handelt, hier den Hauptpersoneneintrag auswählen."))
    _is_main_person = models.BooleanField(_("Haupteintrag"), editable=False, default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self._is_main_person = not bool(self.main_person)
        super(PseudonymMixin, self).save(*args, **kwargs)

    def pseudonyms_and_self(self):
        return self.get_real_instance_class().objects.filter(models.Q(pk=self.pk) | models.Q(pk__in=self.pseudonym_set.all()))


@python_2_unicode_compatible
class BasePerson(PolymorphicModel):
    name = models.CharField(_("Name"), max_length=200, unique=True)
    slug = AutoSlugField(_("URL-Name"), max_length=200, populate_from='name', unique_slug=True)
    sort_name = models.CharField(_("Name sortierbar"), blank=True, max_length=200)

    class Meta:
        abstract = True
        verbose_name = _("Person")
        verbose_name_plural = _("Personen")
        ordering = ['sort_name', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sort_name:
            if " " in self.name:
                self.sort_name = ("%s, %s" % (self.name.split()[-1], " ".join(self.name.split()[:-1])))[:20]
            else:
                self.sort_name = self.name[:20]
        super(BasePerson, self).save(*args, **kwargs)


@python_2_unicode_compatible
class PersonRoleBase(models.Model):
    """
    Fixtures, non-deletable:
    author
    coauthor
    translator
    editor
    """
    id_text = models.CharField(_("Bezeichner (intern)"), max_length=20)
    name_de = models.CharField(_("Bezeichnung (de)"), max_length=50)
    name_en = models.CharField(_("Bezeichnung (en)"), null=True, blank=True, max_length=50)
    label_de = models.CharField(_("Ausgabetext (de)"), null=True, blank=True, max_length=200, help_text=_("In der Bibliografie"))
    label_en = models.CharField(_("Ausgabetext (en)"), null=True, blank=True, max_length=200)
    order_index = models.IntegerField(_("Sortierung"), default=0, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name = _("Funktion")
        verbose_name_plural = _("Funktionen")
        ordering = ['order_index', 'name_de', 'name_en']

    def __str__(self):
        return self.name

    @property
    def label(self):
        return get_translated_field(self, 'label')

    @property
    def name(self):
        return get_translated_field(self, 'name')


@python_2_unicode_compatible
class GenericParticipationRelBase(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    person = models.ForeignKey('Person', verbose_name=_("Person"), related_name='participations', related_query_name='participations')
    role = models.ForeignKey('PersonRole', verbose_name=_("Funktion"))
    order_index = models.IntegerField(_("Sortierung"), default=0, blank=False, null=False)
    label = models.CharField(_("Weitere Angaben"), null=True, blank=True, max_length=2000)
    # TODO Add label_en

    class Meta:
        abstract = True
        verbose_name = _("Rolle/Funktion")
        verbose_name_plural = _("Rollen/Funktionen")
        ordering = ['role', 'order_index', 'person__sort_name']

    def __str__(self):
        return _("%s als %s bei „%s“") % (self.person, self.role, self.content_object)

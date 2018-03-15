# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Erik Stein <code@classlibrary.net>, 2016

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

# django-admin-steroids is optional
try:
    from admin_steroids.options import ImproveRawIdFieldsFormTabularInline
except ModuleNotFoundError:
    class ImproveRawIdFieldsFormTabularInline(admin.TabularInline):
        pass


class PersonRoleAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'id_text', 'label_de', 'label_en']
    list_editable = ['id_text', 'label_de', 'label_en']
    search_fields = ['name_de', 'name_en']

    def get_name(self, obj):
        return obj.name_de or obj.name_en
    get_name.short_description = _("Bezeichnung")
    get_name.admin_order_field = 'name_de'


class PersonAdminBase(admin.ModelAdmin):
    list_display = ['name', 'sort_name', 'slug']
    list_display_links = ['name']
    list_editable = ['sort_name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class PersonAdmin(PersonAdminBase):
    class GroupMembershipListFilter(admin.SimpleListFilter):
        title = _("Gruppe")
        parameter_name = 'group'

        def lookups(self, request, model_admin):
            return model_admin.model.objects.filter(is_group=True).values_list('slug', 'name')

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(groups__slug=self.value())
            else:
                return queryset

    list_display = ('is_group', 'name', 'get_main_person', 'sort_name', 'slug')
    list_display_links = ('name',)
    list_editable = ('sort_name', 'slug')
    list_filter = (
        'is_group',
        GroupMembershipListFilter,
        '_is_main_person',
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('name', 'sort_name'),
                'slug',
                'main_person',
            )
        }),
        (_("Gruppe/Gruppenmitglieder"), {
            'classes': ('wide', 'collapse'),
            'fields': (
                'is_group',
                'members',
            )
        }),
    )
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['main_person']
    filter_horizontal = ('members',)

    def get_groups_display(self, obj):
        return ",".join(obj.groups.values_list('name', flat=True))
    get_groups_display.short_description = _("Gruppen")

    def get_main_person(self, obj):
        return getattr(obj.main_person, 'name', "–")
    get_main_person.short_description = _("Haupteintrag")


class GenericParticipationInline(ImproveRawIdFieldsFormTabularInline, GenericTabularInline):
    model = 'GenericParticipationRel'
    verbose_name = _("Teilnehmer/in")
    verbose_name_plural = _("Teilnehmer/innen")
    fields = ('role', 'person', 'label', 'order_index',)
    raw_id_fields = ('person',)
    related_search_fields = {
        'person': ('name',),
    }
    extra = 0


# from .models import PersonRole, Person, GenericParticipationRel
# admin.site.register(PersonRole, PersonRoleAdmin)
# admin.site.register(Person, PersonAdmin)

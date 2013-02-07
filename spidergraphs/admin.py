from spidergraphs.models import Institution, Program, ProgramOutcome, Course, CourseOutcome, CourseToProgram, UserProfile
from django.contrib import admin
from django.forms import TextInput, Textarea, ModelForm
from django.db import models
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from decimal import *

class ProgramOutcomeInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        total_weight = 0
        reallocate = False
        validFormCount = 0
        for form in self.forms:
            try:
                if not reallocate and form.cleaned_data.get('DELETE', True):
                    reallocate = True
                if form.cleaned_data and not form.cleaned_data.get('DELETE', True):
                    total_weight += form.cleaned_data['weight']
                    validFormCount += 1
            except AttributeError:
                if not reallocate:
                    realllocate = True
        if reallocate:
            re_weight = Decimal(1.0) - total_weight
            should_add = Decimal(round(re_weight / validFormCount,3))
            for form in self.forms:
                if not form.cleaned_data.get('DELETE', True):
                    ctp = form.cleaned_data['id']
                    ctp.weight = form.cleaned_data['weight'] + should_add
                    ctp.save()
            return
        if len(self.forms)>0 and (total_weight < .992 or total_weight > 1.008):
            raise forms.ValidationError(mark_safe('The weight of your outcomes must add up to one. Currently, they add to %s. <a href="#" class="equalizelink">Equalize them</a>' % total_weight))


class ProgramOutcomeInline(admin.TabularInline):
    model = ProgramOutcome
    extra = 0
    fields=("weight", "outcome", "applied", "specialized", "intellectual", "broad", "civic","comments")
    formfield_overrides = {
        models.DecimalField: {'widget': TextInput(attrs={'size':4})},
    }
    formset = ProgramOutcomeInlineFormset

class CourseToProgramInLineFormSet(forms.models.BaseInlineFormSet):
    def clean(self):
        total_weight = 0
        reallocate = False
        validFormCount = 0
        for form in self.forms:
            try:
                if not reallocate and form.cleaned_data.get('DELETE', True):
                    reallocate = True
                if form.cleaned_data and not form.cleaned_data.get('DELETE', True):
                    total_weight += form.cleaned_data['weight']
                    validFormCount += 1
            except AttributeError:
                if not reallocate:
                    realllocate = True
        if reallocate:
            re_weight = Decimal(1.0) - total_weight
            should_add = Decimal(round(re_weight / validFormCount,3))
            for form in self.forms:
                if not form.cleaned_data.get('DELETE', True):
                    ctp = form.cleaned_data['id']
                    ctp.weight = form.cleaned_data['weight'] + should_add
                    ctp.save()
            return
        if len(self.forms)>0 and (total_weight < .992 or total_weight > 1.008):
            raise forms.ValidationError(mark_safe('The weight of your outcomes must add up to one. Currently, they add to %s. <a href="#" class="equalizelink">Equalize them</a>' % total_weight))

class CourseToProgramInline(admin.TabularInline):
    model = CourseToProgram
    extra = 0
    formset = CourseToProgramInLineFormSet
    def formfield_for_dbfield(self, field, **kwargs):
        if field.name == 'course':
            # Note - get_object hasn't been defined yet
            program = self.get_object(kwargs['request'], Program)
            if kwargs['request'].user.is_superuser:
                allowed_courses = Course.objects.all()
            else:
                allowed_courses = Course.objects.filter(institution=kwargs['request'].user.get_profile().institution)
            return forms.ModelChoiceField(queryset=allowed_courses)
        return super(CourseToProgramInline, self).formfield_for_dbfield(field, **kwargs)

    def get_object(self, request, model):
        program_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
        try:
            program_id = int(program_id)
        except ValueError:
            return None
        return model.objects.get(pk=program_id)

class ProgramAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DecimalField: {'widget': TextInput(attrs={'size':4})},
    }
    ordering = ('name',)
    #Limit the Institutions you can add programs to to the one that's your foreign key
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "institution":
            if not request.user.is_superuser:
                kwargs["queryset"] = Institution.objects.filter(id=request.user.get_profile().institution.id)
        return super(ProgramAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #Override the default queryset for programs, limiting to ones at our institution
    def queryset(self, request):
        qs = super(ProgramAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(institution_id=request.user.get_profile().institution.id)

    inlines = [ProgramOutcomeInline, CourseToProgramInline]
    # These are removed becuase of difficulties in making them work with Django's add row javascript
    # they also provide very limited utility
    class Media:
#        css = {
#            'all':('jquery-ui-1.8.23.custom.css',)
#        }
        js = ('equalweight.js',)#'jquery-ui.js','adminsliders.js')

class CourseOutcomeInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        total_weight = 0
        reallocate = False
        validFormCount = 0
        for form in self.forms:
            try:
                if not reallocate and form.cleaned_data.get('DELETE', True):
                    reallocate = True
                if form.cleaned_data and not form.cleaned_data.get('DELETE', True):
                    total_weight += form.cleaned_data['weight']
                    validFormCount += 1
            except AttributeError:
                if not reallocate:
                    realllocate = True
        if reallocate:
            re_weight = Decimal(1.0) - total_weight
            should_add = Decimal(round(re_weight / validFormCount,3))
            for form in self.forms:
                if not form.cleaned_data.get('DELETE', True):
                    ctp = form.cleaned_data['id']
                    ctp.weight = form.cleaned_data['weight'] + should_add
                    ctp.save()
            return
        if len(self.forms)>0 and (total_weight < .992 or total_weight > 1.008):
            raise forms.ValidationError(mark_safe('The weight of your outcomes must add up to one. Currently, they add to %s. <a href="#" class="equalizelink">Equalize them</a>' % total_weight))

class CourseOutcomeInline(admin.TabularInline):
    fields=("weight", "outcome", "applied", "specialized", "intellectual", "broad", "civic","comments")
    model = CourseOutcome
    extra = 0
    formfield_overrides = {
        models.DecimalField: {'widget': TextInput(attrs={'size':4})},
    }
    formset = CourseOutcomeInlineFormset

class CourseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DecimalField: {'widget': TextInput(attrs={'size':4})},
    }
    ordering = ('course_number',)
    inlines = [CourseOutcomeInline]
    #Override the default queryset for courses
    def queryset(self, request):
        qs = super(CourseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(institution=request.user.get_profile().institution)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "institution":
            if not request.user.is_superuser:
                kwargs["queryset"] = Institution.objects.filter(id=request.user.get_profile().institution.id)
        return super(CourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    class Media:
#        css = {
#            'all':('jquery-ui-1.8.23.custom.css',)
#        }
        js = ('equalweight.js',)#'jquery-ui.js','adminsliders.js')

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

class InstitutionAdmin(admin.ModelAdmin):
    ordering = ('name',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)


from django.contrib import admin

from Venter.models import Category, File, Header, Organisation, Profile, Proposal, Domain, Keyword


class HeaderAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'header')
    list_filter = ['organisation_name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'category')
    list_filter = ['organisation_name']

class FileAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'uploaded_date', 'proposal')
    list_filter = ['uploaded_date']

class ProfileAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Employee Details'
    list_display = ('user', 'organisation_name', 'phone_number')
    list_filter = ['organisation_name']

class OrganisationAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Organisation Details'

class ProposalAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Proposal'

class DomainAdmin(admin.ModelAdmin):
    list_display = ('proposal_name', 'domain_name')
    list_filter = ['proposal_name']
    verbose_name_plural = 'Domains'

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('domain_name', 'keyword')
    list_filter = ['domain_name']
    verbose_name_plural = 'Keywords'


admin.site.register(Header, HeaderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Keyword, KeywordAdmin)

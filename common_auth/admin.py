from django.contrib import admin
from .models.token_auth import Token
from .models.ext_auth_cred import ExtAuthCred


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created', 'access_facta', 'access_geoserver', 'access_kaavapino')
    list_filter = ('created', 'access_facta', 'access_geoserver', 'access_kaavapino')
    search_fields = ('user__username', 'user__email', 'key')
    readonly_fields = ('key', 'created')
    raw_id_fields = ('user', 'access_facta', 'access_geoserver', 'access_kaavapino')


@admin.register(ExtAuthCred)
class ExtAuthCredAdmin(admin.ModelAdmin):
    list_display = ('id', 'system', 'cred_owner', 'username', 'host_spec')
    list_filter = ('system', 'cred_owner')
    search_fields = ('system', 'cred_owner', 'username', 'host_spec')
    fields = ('system', 'cred_owner', 'username', 'credential', 'host_spec')

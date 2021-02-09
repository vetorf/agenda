from django.contrib import admin
from .models import Categoria, Contato


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_per_page = 20
    list_editable = ('nome',)


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone',
                    'email', 'data_criacao', 'categoria', 'mostrar')
    list_filter = ('categoria',)
    # list_editable = ('nome', 'sobrenome', 'telefone', 'email', 'categoria')
    list_editable = ('mostrar',)
    # list_display_links = ('nome', 'sobrenome',
    #                       'telefone', 'email', 'categoria')
    list_per_page = 20
    search_fields = ('nome', 'sobrenome')


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Contato, ContatoAdmin)

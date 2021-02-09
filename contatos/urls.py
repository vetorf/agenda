from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('detalhes/<int:contato_id>', views.detalhes, name='detalhes'),
    path('busca/', views.busca, name='busca'),
    path('adicionar_contato/', views.adicionar_contato, name='adicionar_contato'),
    path('editar_contato/<int:contato_id>', views.editar_contato, name='editar_contato'),
    path('apagar_contato/<int:contato_id>', views.apagar_contato, name='apagar_contato'),
]

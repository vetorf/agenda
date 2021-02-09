from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Contato
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import auth, messages
from contatos.forms import ContatoForm
from django.contrib.auth.decorators import login_required


def index(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        raise Http404()

    # https://docs.djangoproject.com/en/3.1/topics/db/queries/
    lista_contatos = Contato.objects.filter(
        mostrar=True
    ).order_by('nome', 'sobrenome')  # - (decrescente)
    paginator = Paginator(lista_contatos, 20, orphans=5)

    # Paginação
    try:
        # Se for passado alguma página,
        pagina = request.GET.get('pagina', 1)
    except ValueError:
        # Se não for passado a página, envia a primeira
        pagina = 1

    try:
        contatos = paginator.page(pagina)
    except (InvalidPage, EmptyPage):
        contatos = paginator.page(paginator.num_pages)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    })


def detalhes(request: HttpRequest, contato_id: int) -> HttpResponse:
    if request.method == 'GET':
        contato = get_object_or_404(Contato, id=contato_id, mostrar=True)

        return render(request, 'contatos/detalhes.html', {
            'contato': contato
        })
    raise Http404()

    # # Outra forma de lançar erros 404
    # try:
    #     contato = Contato.objects.get(id=contato_id)
    #     return render(request, 'contatos/detalhes.html', {
    #         'contato': contato
    #     })
    # except Contato.DoesNotExist as err:
    #     raise Http404()


def busca(request: HttpRequest) -> HttpResponse:
    redirect_back_url = request.META.get('HTTP_REFERER') or 'index'
    if request.method != 'GET':
        raise Http404()

    termo = request.GET.get('termo')

    if termo is None or not termo:
        # raise Http404()
        messages.error(
            request,
            'Digite um termo para a busca.'
        )
        return redirect(redirect_back_url)

    campos = Concat('nome', Value(' '), 'sobrenome')
    lista_contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        # https://docs.djangoproject.com/en/3.1/topics/db/queries/
        # https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects
        Q(nome_completo__icontains=termo) | Q(telefone__icontains=termo),
        mostrar=True,
    ).order_by('nome', 'sobrenome')
    # print(lista_contatos.query)  # consulta que foi feita

    # Paginação
    paginator = Paginator(lista_contatos, 20, orphans=5)

    try:
        # Se for passado alguma página,
        pagina = request.GET.get('pagina', 1)
    except ValueError:
        # Se não for passado a página, envia a primeira
        pagina = 1

    try:
        contatos = paginator.page(pagina)
    except (InvalidPage, EmptyPage):
        contatos = paginator.page(paginator.num_pages)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })


@login_required(redirect_field_name='index')
def adicionar_contato(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = ContatoForm()

        return render(request, 'contatos/adicionar_contato.html', {
            'form': form
        })

    if request.method == 'POST':
        form = ContatoForm(request.POST)

        if form.is_valid():
            contato = form.save()
            messages.success(request, 'Contato criado com sucesso.')

            return redirect(resolve_url('editar_contato', contato.id))

        return render(request, 'contatos/editar_contato.html', {
            'form': form,
        })

    raise Http404()


@login_required(redirect_field_name='index')
def editar_contato(request: HttpRequest, contato_id) -> HttpResponse:
    redirect_back_url = request.META.get('HTTP_REFERER') or 'index'

    try:
        contato = Contato.objects.get(id=contato_id, mostrar=True)
    except Contato.DoesNotExist:
        messages.error(request, 'Contato inexistente.')
        return redirect(redirect_back_url)

    if request.method == 'GET':
        form = ContatoForm(instance=contato)

        return render(request, 'contatos/editar_contato.html', {
            'form': form,
        })

    if request.method == 'POST':
        form = ContatoForm(request.POST, instance=contato)

        if form.is_valid():
            form.save()

            messages.success(request, 'Contato salvo com sucesso.')
            return redirect(redirect_back_url)

        return render(request, 'contatos/editar_contato.html', {
            'form': form,
        })

    raise Http404()


@login_required(redirect_field_name='index')
def apagar_contato(request: HttpRequest, contato_id) -> HttpResponse:
    redirect_back_url = request.META.get('HTTP_REFERER') or 'index'
    try:
        contato = Contato.objects.get(id=contato_id)
        contato.delete()
        messages.success(
            request, f'Contato {contato.nome} apagado com sucesso!')
    except Contato.DoesNotExist:
        messages.error(request, 'Contato inexistente.')

    return redirect(redirect_back_url)

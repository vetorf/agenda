from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def not_login_required(redirect_field_name: str):
    def master(funcao):
        def slave(request: HttpRequest):
            if auth.get_user(request).is_authenticated:
                return redirect(redirect_field_name)
            return funcao(request)
        return slave
    return master


def login(request: HttpRequest):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha incorretos.')
    else:
        auth.login(request, user)

    return redirect('dashboard')


@login_required(redirect_field_name='login')
def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('index')


@not_login_required(redirect_field_name='index')
def register(request: HttpRequest):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')

    # constantes min/max de tamanho dos campos
    USUARIO_MIN_LEN = 4
    USUARIO_MAX_LEN = 40
    SENHA_MIN_LEN = 6
    SENHA_MAX_LEN = 40

    # validando nome
    if not nome:
        messages.error(request, 'Preencha o campo nome.')

    # validando sobrenome
    if not sobrenome:
        messages.error(request, 'Preencha o campo sobrenome.')

    # validando usuario
    usuario_valido = True
    if len(usuario) < USUARIO_MIN_LEN or len(usuario) > USUARIO_MAX_LEN:
        usuario_valido = False
        messages.error(request,
                       f'Usuário deve ter entre {USUARIO_MIN_LEN} e '
                       f'{USUARIO_MAX_LEN} caracteres.')

    if not usuario.isalnum():
        usuario_valido = False
        messages.error(request,
                       'Usuário deve conter apenas letras e/ou números.')

    if usuario_valido and User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já cadastrado.')

    # validando email
    try:
        validators.validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
    else:
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')

    # validando senhas
    if len(senha1) < SENHA_MIN_LEN or len(senha1) > SENHA_MAX_LEN:
        messages.error(request,
                       f'Senha deve ter entre {SENHA_MIN_LEN} e '
                       f'{SENHA_MAX_LEN} caracteres.')

    if senha1 != senha2:
        messages.error(request, 'As senhas devem ser iguais.')

    # se há alguma mensagem, mostra eles na tela
    if messages.get_messages(request):
        return render(request, 'accounts/register.html', {
            'form': request.POST
        })

    # registra o usuário
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha1, first_name=nome,
                                    last_name=sobrenome)
    user.save()

    messages.success(request, 'Registrado com sucesso. Faça login.')
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request: HttpRequest):
    return render(request, 'accounts/dashboard.html')

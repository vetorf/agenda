from django import forms
from django.core.exceptions import ValidationError
from contatos.models import Contato
from django.core.validators import validate_email

# Informações sobre criação de formulários
# https://django-portuguese.readthedocs.io/en/1.0/topics/forms/modelforms.html


class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('nome', 'sobrenome', 'telefone', 'email',
                  'categoria', 'descricao', 'foto')
        exclude = ('data_criacao', 'mostrar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configurando o id das tags
        # https://django-portuguese.readthedocs.io/en/1.0/ref/forms/api.html#configurando-tags-html-label
        self.auto_id = '%s'

        # Widgets e modificando atributos
        # https://docs.djangoproject.com/en/2.2/ref/forms/widgets/#styling-widget-instances

        # Informações sobre fields, templates e css
        # https://qastack.com.br/programming/5827590/css-styling-in-django-forms
        # https://docs.djangoproject.com/en/2.2/topics/forms/#working-with-form-templates

        # Fields
        # https://docs.djangoproject.com/en/3.1/ref/forms/fields/

        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Comentarios acima substituidos por
        # https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/

        self.fields['email'].label = 'E-mail'
        self.fields['descricao'].label = 'Descrição'

    # Validando formularios
    # https://django-portuguese.readthedocs.io/en/1.0/ref/forms/validation.html
    def clean_email(self):
        email = self.cleaned_data['email']

        # lança ValidationError
        validate_email(email)

        return email

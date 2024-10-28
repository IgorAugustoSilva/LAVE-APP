<<<<<<< HEAD
# Ordem de Serviço

## Este projeto foi feito com:

* [Django 4.2.3](https://www.djangoproject.com/)
* [Django-ninja](https://django-ninja.rest-framework.com/)
* [AlpineJS](https://alpinejs.dev/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/ordem-de-servico.git
# git clone https://gitlab.com/rg3915/ordem-de-servico.git
cd ordem-de-servico

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python contrib/env_gen.py

python manage.py migrate
python manage.py createsuperuser
```

=======
# LavanderiaCachoeira
>>>>>>> c2142a41cd85be42db3e6a59f2ce9a251ff6f56f

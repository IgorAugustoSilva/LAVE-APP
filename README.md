<<<<<<< HEAD

# Lavanderia Cachoeira

## Este projeto foi feito com:

* [Django 4.2.3]
* [Django-ninja]
* [AlpineJS]

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/IgorAugustoSilva/lavanderia-cachoeira.git
# git clone https://github.com/IgorAugustoSilva/lavanderia-cachoeira.git
cd ordem-de-servico

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python contrib/env_gen.py

python manage.py migrate
python manage.py createsuperuser
```


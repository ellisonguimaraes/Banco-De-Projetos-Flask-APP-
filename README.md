# Banco de Projetos  Interdisciplinares(Disciplina de Programação Web)

## Descrição

Repositório do projeto final do Tema 3 da disciplina CET1182 - Programação para Aplicações Web: Banco de Projetos Interdisciplinares do Colegiado.
Esta aplicação busca reunir as informações e atores relacionados aos projetos interdisciplinares do curso num só lugar, para facilitar a organização dos dados e acesso dos integrantes que desejam dar continuidade ou adquirir conhecimento sobre os mesmos. O sistema tornaria possível o cadastro e armazenamento do banco de projetos que poderiam ser pesquisados através da utilização de filtros associados ou não a disciplinas e acessados pelos usuários, junto a um sistema de usuários que iria garantir determinadas permissões de cadastro, edição e acesso.

## Objetivo

O objetivo dessa aplicação visa intermediar e compartilhar interesses em projetos interdisciplinares entre docentes e discentes do colegiado de Ciência da Computação da Universidade Estadual de Santa Cruz (UESC). Agrupando-os numa aplicação.

## Requisitos

[Python 3](https://www.python.org/downloads/)

## Clonando o Repositório 

`git clone https://github.com/ellisonguimaraes/Banco-De-Projetos-Flask-APP-.git`

## Instalação 

A instalação e execução pode ser feita automaticamente pelo arquivo ".bat" **install.bat** encontrado na raiz do diretório do projeto.

Ou pode ser feita manualmente através dos seguintes comandos:

```powershell
> pip install virtualenv 	# Instalando a ferramenta para criação de ambiente virtual
> python -m venv .venv 		# Criando um Ambiente Virtual
> .\venv\Scripts\activate	# Ativando o Ambiente Virtual
> pip install e .		    # Instalando dependências do projeto no Ambiente Virtual
```

## Execução

```powershell
> flask run                  # Executando o Projeto Flask em localhost:5000
```

## Usuários e Ações

Pode se criar um novo usuário através do formulário de registro e/ou acessar as contas de usuários já précriadas no banco de dados da Aplicação:

| Email           | Senha |
| --------------- | ----- |
| jhonata@uesc.br | 123   |
| ellison@uesc.br | 123   |
| felipe@uesc.br  | 123   |

Para realizar alterações nas informações armazenadas é necessário ter uma conta de usuário e estar logado.

As principais ações que podem ser feitas são:

**Em meus projetos**
- Criação e Edição de Projeto 
- Gerenciamento de membros em Projetos em que o usuário é orientador/líder
- Criação de atividades no Histórico

**Em Notificações**
- Visualizar, permitir ou recusar uma solicitação de participação

**Em Editar Perfil**
- Editar o próprio perfil do usuário

**Na Página do Projeto**
- Solicitar ou Cancelar uma solicitação de participação em projeto

## Lista de Páginas 

- Página Inicial
- Lista de Projetos
- Páginas de Cadastro, Edição e Visualização de Projeto
- Páginas de Histórico de Projeto
- Páginas de Login e Cadastro de Usuário
- Páginas de Edição e Visualização de Perfil de Usuário
- Páginas de Gerenciamento (Projetos, Membros de Projeto, Criação de Histórico de Projeto e Notificações)
- Página de Contato


## Implementação

### Front-End
- HTML5
- CSS3
- Python3
- Jinja2

### Back-END

- Flask

### Persistência de Dados: 

- SQLite


## Estrutura de Diretórios 
```
\---Banco-De-Projetos-Flask-APP-
    |   install.bat
    |   requirements.txt
    |   run.bat
    |   setup.py
    |
    +---app
    |   |   auth.py
    |   |   db.sqlite
    |   |   main.py
    |   |   manager.py
    |   |   __init__.py
    |   |
    |   +---models
    |   |   |   form_contact.py
    |   |   |   historico.py
    |   |   |   notificacao.py
    |   |   |   pessoa_projeto.py
    |   |   |   projeto.py
    |   |   |   tag.py
    |   |   |   tag_projeto.py
    |   |   |   user.py
    |   |   |
    |   |
    |   +---static
    |   |   +---css
    |   |   |       contact.css
    |   |   |       historic.css
    |   |   |       index.css
    |   |   |       login.css
    |   |   |       login_register.css
    |   |   |       manager.css
    |   |   |       profile.css
    |   |   |       projects.css
    |   |   |       proj_form.css
    |   |   |       proj_page.css
    |   |   |       styles.css
    |   |   |
    |   |   +---dist
    |   |   |   +---css
    |   |   |   |       bootstrap-grid.css
    |   |   |   |       bootstrap-grid.css.map
    |   |   |   |       bootstrap-grid.min.css
    |   |   |   |       bootstrap-grid.min.css.map
    |   |   |   |       bootstrap-reboot.css
    |   |   |   |       bootstrap-reboot.css.map
    |   |   |   |       bootstrap-reboot.min.css
    |   |   |   |       bootstrap-reboot.min.css.map
    |   |   |   |       bootstrap.css
    |   |   |   |       bootstrap.css.map
    |   |   |   |       bootstrap.min.css
    |   |   |   |       bootstrap.min.css.map
    |   |   |   |
    |   |   |   \---js
    |   |   |           bootstrap.bundle.js
    |   |   |           bootstrap.bundle.js.map
    |   |   |           bootstrap.bundle.min.js
    |   |   |           bootstrap.bundle.min.js.map
    |   |   |           bootstrap.js
    |   |   |           bootstrap.js.map
    |   |   |           bootstrap.min.js
    |   |   |           bootstrap.min.js.map
    |   |   |
    |   |   +---img
    |   |   |       local.png
    |   |   |       logo.png
    |   |   |       mail.png
    |   |   |       perfil_photo.png
    |   |   |       slide2.jpg
    |   |   |       slide3.jpg
    |   |   |       struct.png
    |   |   |       tel.png
    |   |   |       torre.jpg
    |   |   |
    |   |   \---upload
    |   |       +---pdf
    |   |       |       1.pdf
    |   |       |       4.pdf
    |   |       |       6.pdf
    |   |       |
    |   |       +---profile
    |   |       |       1
    |   |       |       2
    |   |       |       3
    |   |       |       32.png
    |   |       |       34
    |   |       |       wallhaven-ym133l.png
    |   |       |
    |   |       \---project
    |   |               1_0
    |   |               1_1
    |   |               3_0
    |   |               5_0
    |   |               6_0
    |   |               6_1
    |   |               6_2
    |   |               7_0
    |   |
    |   \---templates
    |       |   base1.html
    |       |   contact.html
    |       |   historic.html
    |       |   index.html
    |       |   profile.html
    |       |   projects.html
    |       |   project_page.html
    |       |
    |       +---auth
    |       |       login.html
    |       |       register.html
    |       |       update.html
    |       |
    |       \---manager
    |           |   base2.html
    |           |   historic.html
    |           |   members.html
    |           |   notify.html
    |           |
    |           \---project
    |                   add.html
    |                   delete.html
    |                   list.html
    |                   update.html
    |    
    |
    \---migrations
        |   alembic.ini
        |   env.py
        |   README
        |   script.py.mako
        |
        \---versions
            |   b1143a729f21_first_migrate.py
   
```

Os arquivos do bootstrap já estão incluídos no repositório: CSS e JS compilados (bootstrap. *), bem como CSS e JS compilados e minimizados (bootstrap.min. *), mapas de origem (bootstrap. *. map) e arquivos JS agrupados (bootstrap.bundle.js e bootstrap.bundle.min.js minificado).

## Dependências

```python
alembic
click
Flask
Flask-Login
Flask-Migrate
Flask-Script
Flask-SQLAlchemy
itsdangerous
Jinja2
Mako
MarkupSafe
python-dateutil
python-editor
six
SQLAlchemy
Werkzeug
```

## Limitações

Não foi desenvolvido o *super user* com o poder total da aplicação por questões de limitação de tempo e conhecimento, porém os tipos de usuários existentes (Orientador e Participante) servem como uma ideia de como funciona o sistema de permissões de usuário.

## Autores

Ellison William Medrado Guimaraes 

Felipe Gregue Chaves Pires 

Jhonata de Araújo Nascimento 
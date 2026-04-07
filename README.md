## 👤 Autor
- **Nome:** Railane Lopes dos Santos  
- **Email:** railanelopes11@outlook.com
- **GitHub:** https://github.com/railanelopes11
- **LinkedIn:** https://www.linkedin.com/in/railanelopes

---

# 🏢 Sistema de Vagas – Django

## 🎯 Objetivo do Projeto
Sistema de gerenciamento de vagas e candidatos desenvolvido em **Django**.  

- Cadastro de empresa e candidatos
- Empresas podem criar, editar e excluir vagas.
- Candidatos podem se candidatar a vagas disponíveis.
- Relatórios com gráficos interativos usando **Charts.js**.  

---

## 🛠 Tecnologias Utilizadas
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![SQLite](https://img.shields.io/badge/DB-SQLite-lightgrey?logo=sqlite)
![Charts.js](https://img.shields.io/badge/Charts.js-JS-yellow?logo=javascript)

---

## ⚙️ Instalação e Configuração
Siga os passos abaixo para configurar e executar o projeto localmente.

---

##  1. Clonar o repositório

Copie o link do repositório no GitHub e execute o comando abaixo no terminal:

git clone (colar o link do repositório)

---

## 2. Criar e ativar ambiente virtual

Crie um ambiente virtual para isolar as dependências do projeto:

python -m venv venv

Ative o ambiente virtual:

- No Windows:
venv\Scripts\activate

- No Linux/Mac:
source venv/bin/activate

---

##  3. Atualizar o pip 

pip install --upgrade pip

---

##  4. Instalar o Django

Instale o framework Django:

pip install django

---

##  5. Instalar dependências do projeto

Se o projeto possuir um arquivo requirements.txt, instale todas as dependências com:

pip install -r requirements.txt

Obs: Este arquivo normalmente já inclui o Django e outras bibliotecas utilizadas.

---

##  6. Aplicar as migrations

Execute o comando abaixo para criar as tabelas no banco de dados:

python manage.py makemigrations

python manage.py migrate

---

##  7. Criar superusuário (Se acahar necessário)

Para acessar o painel administrativo do Django:

python manage.py createsuperuser

Preencha os dados solicitados (email e senha).

---

## 8. Executar o servidor

Inicie o servidor local:

python manage.py runserver

---

##  9. Acessar o sistema

Abra o navegador e acesse:

http://127.0.0.1:8000/

Painel administrativo:

http://127.0.0.1:8000/admin/

---

## ⚠️ Observações importantes

- Certifique-se de que o ambiente virtual está ativado antes de rodar o projeto  
- Verifique se o Python está instalado corretamente  
- Caso ocorra erro de dependências, revise o requirements.txt  

---


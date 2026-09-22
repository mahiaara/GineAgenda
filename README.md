# GineAgenda

Sistema web desenvolvido para auxiliar no agendamento de consultas em uma clínica ginecológica.

## Sobre o projeto

O GineAgenda é uma aplicação web desenvolvida para facilitar o gerenciamento de consultas de uma clínica ginecológica.

Por meio do sistema, a paciente pode realizar seu cadastro, acessar sua área pessoal, consultar e editar seus dados, verificar horários disponíveis, realizar agendamentos, visualizar suas consultas e cancelar atendimentos.

O sistema também possui regras para evitar conflitos de horários e impedir agendamentos em datas não permitidas.

## Funcionalidades

- Cadastro de pacientes
- Login de pacientes
- Área da paciente
- Consulta de dados cadastrais
- Edição de dados
- Agendamento de consultas
- Exibição de horários disponíveis
- Bloqueio de horários já ocupados
- Bloqueio de datas passadas
- Bloqueio de sábados e domingos
- Bloqueio de feriados
- Bloqueio de mais de uma consulta ativa para a mesma paciente no mesmo dia
- Visualização das consultas
- Cancelamento de consultas
- Liberação do horário após cancelamento
- Atualização automática de consultas passadas
- Status de consulta: Agendada, Realizada e Cancelada
- Logout da paciente

## Tecnologias utilizadas

- Python
- Flask
- MySQL
- HTML
- CSS
- Bootstrap
- Werkzeug
- python-dotenv

## Estrutura do projeto

```text
GineAgenda/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── index.html
    ├── cadastro.html
    ├── login.html
    ├── paciente.html
    ├── agendar.html
    ├── consultas.html
    ├── dados.html
    └── editar_dados.html
```

## Configuração do banco de dados

O GineAgenda utiliza MySQL para armazenamento dos dados.

Para executar o projeto, deve ser criado um arquivo `.env` na pasta principal com as configurações de conexão com o banco de dados.

Exemplo:

```env
DB_HOST=127.0.0.1
DB_PORT=3307
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=gineagenda
SECRET_KEY=sua_chave_secreta
```

O arquivo `.env` contém informações sensíveis e não deve ser enviado para o GitHub.

## Como executar o projeto

### 1. Criar o ambiente virtual

```bash
python -m venv venv
```

### 2. Ativar o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o arquivo .env

Crie o arquivo `.env` na pasta principal do projeto e informe os dados de conexão com o MySQL.

### 5. Executar a aplicação

```bash
python app.py
```

### 6. Acessar o sistema

Abra o navegador e acesse:

```text
http://127.0.0.1:5000
```

## Segurança

As credenciais de acesso ao banco de dados e a chave secreta da aplicação são armazenadas no arquivo `.env`.

O arquivo `.gitignore` impede que o `.env`, o ambiente virtual e outros arquivos desnecessários sejam enviados para o repositório.

## Projeto acadêmico

Projeto desenvolvido como atividade acadêmica na área de Tecnologia da Informação.


## Banco de Dados

O GineAgenda utiliza MySQL para armazenamento e gerenciamento dos dados da aplicação.

O banco de dados possui duas entidades principais:

- **Pacientes:** armazena os dados cadastrais dos pacientes.
- **Agendamentos:** armazena as informações das consultas agendadas.

O relacionamento entre as entidades é do tipo **1:N**, no qual um paciente pode possuir vários agendamentos e cada agendamento pertence a um único paciente.

A integridade do relacionamento é garantida pela chave estrangeira `paciente_id`, presente na tabela `agendamentos`, que referencia o campo `id` da tabela `pacientes`.

### Operações SQL

Durante o desenvolvimento foram realizadas operações de:

- `INSERT` — inserção de registros;
- `SELECT` — consulta de dados;
- `UPDATE` — atualização de registros;
- `DELETE` — exclusão de registros.

O script contendo a estrutura do banco e exemplos das operações está disponível em:

`database/gineagenda.sql`

## Controle de Versão

O projeto utiliza **Git** para controle de versão e **GitHub** para armazenamento do repositório remoto.

As alterações do projeto são registradas por meio de commits com mensagens descritivas, permitindo acompanhar a evolução do desenvolvimento.
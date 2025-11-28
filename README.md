# Sistema de Gerenciamento de Dietas

Uma aplicação completa de gerenciamento de dietas com API REST e interface gráfica, desenvolvida em Python seguindo arquitetura MVC.

## Características

- **API REST** com Flask e Flask-RESTful
- **Interface Gráfica** com Tkinter
- **Banco de Dados** PostgreSQL com SQLAlchemy ORM
- **Arquitetura MVC** (Model-View-Controller)
- **Programação Orientada a Objetos** com classes, herança, polimorfismo, encapsulamento

## Requisitos

- Python 3.8+
- PostgreSQL 12+

## Estrutura do Projeto

```
diet-app/
├── app/
│   ├── __init__.py          # Inicialização da aplicação Flask
│   ├── config.py            # Configurações
│   ├── models/              # Modelos do banco de dados
│   │   ├── base_model.py    # Classe base (herança)
│   │   ├── dieta.py         # Modelo de Dieta
│   │   ├── refeicao.py      # Modelo de Refeição
│   │   └── exercicio.py     # Modelo de Exercício
│   ├── controllers/         # Controladores com lógica de negócio
│   │   ├── dieta_controller.py
│   │   ├── refeicao_controller.py
│   │   └── exercicio_controller.py
│   ├── resources/           # Recursos REST (endpoints)
│   │   ├── dieta_resource.py
│   │   ├── refeicao_resource.py
│   │   └── exercicio_resource.py
│   └── validators/          # Validadores de negócio
│       └── validators.py
├── gui/
│   ├── main_window.py       # Janela principal
│   ├── views/               # Telas CRUD
│   │   ├── dieta_view.py
│   │   ├── refeicao_view.py
│   │   └── exercicio_view.py
│   └── utils/
│       └── api_client.py    # Cliente HTTP para API
├── requirements.txt
├── run_api.py               # Script para iniciar a API
├── run_gui.py               # Script para iniciar a GUI
└── README.md
```

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd diet-app
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados PostgreSQL

Crie um banco de dados PostgreSQL:

```sql
CREATE DATABASE diet_app;
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Flask
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

# Database
DATABASE_URL=postgresql://usuario:senha@localhost:5432/diet_app

# API
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Executando a Aplicação

### Iniciando a API

```bash
python run_api.py
```

A API estará disponível em `http://localhost:5000`

### Iniciando a Interface Gráfica

Em outro terminal (com a API rodando):

```bash
python run_gui.py
```

## Endpoints da API

### Dietas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/dietas` | Criar nova dieta |
| GET | `/api/dietas` | Listar todas as dietas |
| GET | `/api/dietas/<id>` | Buscar dieta por ID |
| PUT | `/api/dietas/<id>` | Atualizar dieta |
| DELETE | `/api/dietas/<id>` | Excluir dieta |

**Exemplo de criação:**
```json
POST /api/dietas
{
    "meta": "Perder 5kg em 3 meses",
    "descricao": "Dieta focada em redução calórica com exercícios"
}
```

### Refeições

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/refeicoes` | Criar nova refeição |
| GET | `/api/refeicoes` | Listar todas as refeições |
| GET | `/api/refeicoes?dieta_id=<id>` | Filtrar por dieta |
| GET | `/api/refeicoes/<id>` | Buscar refeição por ID |
| PUT | `/api/refeicoes/<id>` | Atualizar refeição |
| DELETE | `/api/refeicoes/<id>` | Excluir refeição |

**Exemplo de criação:**
```json
POST /api/refeicoes
{
    "tipo_refeicao": "almoço",
    "quantidade": 500,
    "alimentos": ["arroz integral", "frango grelhado", "salada"],
    "dieta_id": 1
}
```

**Tipos de refeição válidos:**
- café da manhã
- almoço
- jantar
- lanche
- ceia
- pré-treino
- pós-treino

### Exercícios

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/exercicios` | Criar novo exercício |
| GET | `/api/exercicios` | Listar todos os exercícios |
| GET | `/api/exercicios?dieta_id=<id>` | Filtrar por dieta |
| GET | `/api/exercicios/<id>` | Buscar exercício por ID |
| PUT | `/api/exercicios/<id>` | Atualizar exercício |
| DELETE | `/api/exercicios/<id>` | Excluir exercício |

**Exemplo de criação:**
```json
POST /api/exercicios
{
    "tipo_exercicio": "flexão",
    "quantidade_repeticoes": 15,
    "ciclos": 3,
    "pausa_entre_ciclos": 60,
    "dieta_id": 1
}
```

## Regras de Validação

1. **Dieta**: Meta é obrigatória
2. **Refeição**: 
   - Tipo de refeição deve ser um dos tipos válidos
   - Quantidade não pode ser negativa
   - Lista de alimentos não pode estar vazia
   - Se dieta_id for fornecido, a dieta deve existir
3. **Exercício**:
   - Ciclos não podem ser negativos (regra de negócio principal)
   - Quantidade de repetições não pode ser negativa
   - Pausa entre ciclos não pode ser negativa
   - Se dieta_id for fornecido, a dieta deve existir

## Modelo de Dados

### Dieta
- `id`: Identificador único (PK)
- `meta`: Meta da dieta
- `descricao`: Descrição detalhada
- `created_at`: Data de criação

### Refeição
- `id`: Identificador único (PK)
- `tipo_refeicao`: Tipo (café, almoço, etc.)
- `quantidade`: Quantidade em gramas/ml
- `alimentos`: Lista de alimentos (JSON array)
- `dieta_id`: Referência para dieta (FK)
- `created_at`: Data de criação

### Exercício
- `id`: Identificador único (PK)
- `tipo_exercicio`: Tipo (flexão, corrida, etc.)
- `quantidade_repeticoes`: Número de repetições
- `ciclos`: Número de ciclos (não negativo)
- `pausa_entre_ciclos`: Pausa em segundos
- `dieta_id`: Referência para dieta (FK)
- `created_at`: Data de criação

## Conceitos de POO Implementados

- **Classes**: Todas as entidades são classes
- **Herança**: `BaseModel` é herdado por todos os modelos
- **Polimorfismo**: Método `to_dict()` sobrescrito em cada modelo
- **Encapsulamento**: Atributos privados com getters/setters
- **Construtores**: `__init__` em todas as classes

## Tecnologias Utilizadas

- **Python 3.8+**
- **Flask 3.0**: Framework web
- **Flask-RESTful 0.3.10**: Extensão para APIs REST
- **Flask-SQLAlchemy 3.1.1**: ORM integration
- **PostgreSQL**: Banco de dados
- **psycopg2**: Driver PostgreSQL
- **Tkinter**: Interface gráfica
- **requests**: Cliente HTTP

## Licença

Este projeto é de uso educacional.

# Sidloto

Gerador de jogos da Lotofácil com backend em Flask, frontend web em HTML/CSS/JavaScript e filtros práticos para criação de combinações com base em critérios configuráveis.

O projeto permite gerar jogos de duas formas:

- Modo básico: geração com estratégia e filtros diretos
- Modo otimizado: geração com base em repetição alvo, dezenas quentes/frias, soma, pares e restrições personalizadas

## Funcionalidades

- Geração de jogos da Lotofácil
- Estratégias básicas de geração
- Geração otimizada com parâmetros ajustáveis
- Filtro por quantidade de pares
- Filtro por faixa de soma
- Filtro por repetição em relação ao último concurso
- Definição de dezenas quentes e frias
- Definição de dezenas obrigatórias e dezenas a evitar
- Histórico de lotes gerados
- Exportação em CSV
- Interface web simples e direta
- API local para integração e testes

## Tecnologias utilizadas

### Backend
- Python
- Flask
- Flask-CORS
- python-dotenv

### Frontend
- HTML5
- CSS3
- JavaScript

### Persistência
- SQLite

## Estrutura do projeto

```text
Sidloto/
├── backend/
│   └── app.py
├── config/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── strategies/
├── utils/
└── README.md
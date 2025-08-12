# Sidloto2025

Gerador de jogos **Lotofácil** com:
- Backend **Flask** (Python)
- Estratégias básicas + **geração otimizada**
- Filtros: repetição (8–9), pares/ímpares (7/8–8/7), faixa de soma (185–200)
- Persistência **SQLite** com `/api/last` e `/api/history`
- Frontend (HTML/JS/CSS) com tema **MSI**
- **Compartilhar por WhatsApp** (texto), **baixar CSV**

## Executar local
```powershell
cd "$env:USERPROFILE\Documents\Sidloto2025"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r .\config\requirements.txt
cd .\backend
python app.py

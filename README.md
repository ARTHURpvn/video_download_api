# YouTube Video Downloader API

Uma API robusta para download de vídeos do YouTube com suporte a Shorts e múltiplas estratégias anti-bloqueio.

## Estrutura do Projeto

```
app/
├── __init__.py
├── main.py              # Aplicação principal FastAPI
├── models/
│   ├── __init__.py
│   └── schemas.py       # Modelos Pydantic
├── services/
│   ├── __init__.py
│   ├── youtube.py       # Lógica de download do YouTube
│   └── file_manager.py  # Gerenciamento de arquivos
├── routes/
│   ├── __init__.py
│   ├── video.py         # Endpoints de vídeo
│   ├── downloads.py     # Endpoints de downloads
│   └── health.py        # Endpoints de health/debug
└── utils/
    ├── __init__.py
    ├── config.py         # Configurações
    └── helpers.py        # Funções auxiliares
```

## Como executar

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `POST /video/info` - Obter informações do vídeo
- `POST /video/download` - Baixar vídeo
- `POST /video/diagnose` - Diagnosticar problemas
- `GET /downloads` - Listar downloads
- `DELETE /downloads/{filename}` - Deletar arquivo
- `GET /health` - Health check
- `GET /debug/common-errors` - Lista de erros comuns

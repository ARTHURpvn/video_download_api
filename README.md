# 🎬 YouTube Video Downloader API

API robusta para download de vídeos do YouTube (incluindo Shorts) com suporte a streaming em tempo real e múltiplas estratégias de fallback.

## 🚀 Features

- ✅ Download de vídeos do YouTube e Shorts
- ✅ Suporte a áudio MP3
- ✅ Progresso em tempo real via Server-Sent Events (SSE)
- ✅ Múltiplas estratégias de fallback anti-bloqueio
- ✅ Conversão automática para MP4
- ✅ API RESTful com FastAPI
- ✅ Deploy fácil no Render

## 📋 Pré-requisitos

- Python 3.11+
- FFmpeg instalado no sistema

## 🔧 Instalação Local

```bash
# Clonar repositório
git clone <seu-repo>
cd PythonProject

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

## 🌐 Deploy no Render

### Método 1: Deploy Automático (Recomendado)

1. **Conecte seu repositório ao Render**
   - Vá para [Render Dashboard](https://dashboard.render.com/)
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub

2. **Configure o serviço**
   - **Name**: `youtube-downloader-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Adicione variável de ambiente**
   - `RENDER` = `true`

4. **Deploy!**
   - Clique em "Create Web Service"
   - Aguarde o build (3-5 minutos)

### Método 2: Deploy via render.yaml

O arquivo `render.yaml` já está configurado. Basta:

1. Push para seu repositório Git
2. No Render, selecione "New" → "Blueprint"
3. Conecte o repositório
4. Render detectará automaticamente o `render.yaml`

### ⚠️ Importante para Deploy

- ✅ FFmpeg já vem instalado no Render
- ✅ Arquivos são salvos em `/tmp` (único diretório gravável)
- ✅ `/tmp` é limpo periodicamente - não é armazenamento permanente
- ✅ Health check configurado em `/health`

## 📡 Endpoints da API

### 1. Health Check
```http
GET /health
```

### 2. Obter informações do vídeo
```http
POST /video/info
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### 3. Download com progresso (Recomendado)
```http
POST /video/download-stream
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "audio_only": false
}
```

Retorna: Server-Sent Events com progresso em tempo real

### 4. Download simples
```http
POST /video/download
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "quality": "best",
  "audio_only": false
}
```

### 5. Baixar arquivo processado
```http
GET /downloads/{filename}
```

## 🔧 Configurações de Ambiente

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `RENDER` | Detecta ambiente Render | `false` |
| `PORT` | Porta do servidor | `8000` |
| `HOST` | Host do servidor | `0.0.0.0` |

## 🐛 Troubleshooting

### Erro 403 Forbidden
- A API usa múltiplas estratégias de fallback automaticamente
- Se persistir, atualize: `pip install --upgrade yt-dlp`

### Erro de conversão de vídeo
- Verifique se FFmpeg está instalado: `ffmpeg -version`
- No Render, FFmpeg já vem pré-instalado

### Erro de espaço em disco (Render)
- Use `/tmp` para arquivos temporários (já configurado)
- Arquivos em `/tmp` são limpos automaticamente

## 📊 Monitoramento

Logs disponíveis no Render Dashboard:
- ✅ Progresso de downloads
- ✅ Estratégias tentadas
- ✅ Erros e exceções
- ✅ Health checks

## 🔒 Segurança

- CORS configurado para aceitar requisições do frontend
- Rate limiting recomendado para produção
- Validação de URLs do YouTube

## 📝 Stack Tecnológico

- **FastAPI** - Framework web moderno
- **yt-dlp** - Download de vídeos
- **FFmpeg** - Processamento de vídeo
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validação de dados

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 🆘 Suporte

Para problemas ou dúvidas:
- Abra uma issue no GitHub
- Verifique os logs no Render Dashboard
- Consulte a documentação: `/docs` (Swagger UI)

---

**Desenvolvido com ❤️ usando FastAPI**


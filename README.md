# 🎬 YouTube Downloader

Aplicativo desktop para baixar vídeos e áudios do YouTube de forma simples e rápida.

**Instalação 100% automática - não precisa ter Python instalado!**

---

## 🚀 Instalação Super Simples

### 🪟 **Windows**

**Duplo clique em:** `INSTALAR_WINDOWS.bat`

✅ Pronto! Aguarde 10-15 minutos e o executável estará na sua Área de Trabalho!

O instalador faz **TUDO automaticamente**:
- ✓ Detecta e instala Python se necessário
- ✓ Instala todas as dependências
- ✓ Compila o executável
- ✓ Coloca na Área de Trabalho

### 🍎 **macOS**

```bash
bash INSTALAR_MACOS.sh
```

✅ Pronto! Aguarde 10-15 minutos e o aplicativo estará na sua Área de Trabalho!

O instalador faz **TUDO automaticamente**:
- ✓ Detecta e instala Python se necessário
- ✓ Instala FFmpeg via Homebrew
- ✓ Instala todas as dependências
- ✓ Compila o aplicativo
- ✓ Coloca na Área de Trabalho

---

## 📋 Pré-requisitos

**NENHUM!** 🎉

Os instaladores cuidam de tudo automaticamente, incluindo:
- Instalação do Python (se não estiver instalado)
- Instalação de todas as bibliotecas necessárias
- Compilação do executável

---

## 💻 Como Usar

1. Abra o **YouTubeDownloader** na sua Área de Trabalho
2. Cole o link do vídeo do YouTube
3. Escolha o formato (MP4 ou MP3)
4. Clique em "BAIXAR AGORA"
5. Arquivos salvos em: `Downloads/Videos Baixados`

---

## 🎯 Recursos

- ✅ Download de vídeos (MP4) e áudios (MP3)
- ✅ Múltiplas qualidades (360p até 1080p)
- ✅ Interface moderna e intuitiva
- ✅ Progresso em tempo real
- ✅ **Executável standalone (não precisa Python instalado)**
- ✅ **Instalação 100% automática**
- ✅ Sem propaganda ou limitações

---

## 📂 Estrutura do Projeto

```
PythonProject/
├── INSTALAR_WINDOWS.bat       # ← Instalador Windows (duplo clique)
├── INSTALAR_MACOS.sh          # ← Instalador macOS (bash)
├── README.md                  # Este arquivo
├── LEIA-ME.txt                # Guia em português
├── gui_app.py                 # Aplicativo principal
├── build_executable.py        # Gerador de executável
├── requirements.txt           # Dependências
├── app/                       # Backend (FastAPI)
└── instaladores/              # Instaladores Python alternativos
```

---

## 🛠️ Para Desenvolvedores

### Executar em modo dev (requer Python)

```bash
pip install -r requirements.txt
python gui_app.py
```

### Criar executável manualmente

```bash
python build_executable.py
```

---

## 📝 Dependências (instaladas automaticamente)

- `yt-dlp` - Download de vídeos
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `requests` - Cliente HTTP
- `pydantic` - Validação
- `python-multipart` - Upload
- `pyinstaller` - Criação de executável

---

## ⚠️ Solução de Problemas

**Windows: "Python não reconhecido" após instalação automática?**
- Reinicie o computador e execute o instalador novamente

**macOS: "Desenvolvedor não identificado"?**
- Sistema > Segurança > Permitir mesmo assim

**macOS: Erro de permissão no .sh?**
- Execute: `chmod +x INSTALAR_MACOS.sh`
- Depois: `bash INSTALAR_MACOS.sh`

📖 Mais detalhes em **[LEIA-ME.txt](LEIA-ME.txt)**

---

## ⏱️ Tempo de Instalação

- **Primeira vez (sem Python):** 15-20 minutos
- **Com Python já instalado:** 10 minutos

---

**Desenvolvido com ❤️ | 2025**

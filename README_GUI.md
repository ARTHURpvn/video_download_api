# 🖥️ YouTube Downloader - Interface Gráfica Desktop

Aplicação desktop standalone para download de vídeos do YouTube com interface gráfica moderna e escura.

## ✨ Características

- 🎨 Interface gráfica moderna com tema escuro (estilo YouTube)
- 🔄 Servidor FastAPI integrado (não precisa rodar separadamente)
- ⚡ **Busca automática de informações** - Cole o link e veja as informações automaticamente
- 📊 Visualização rica: título, canal, duração, visualizações e descrição
- 📁 Gerenciamento inteligente de downloads
- 🎯 Suporte a vídeos e áudios (MP4/MP3)
- 🎬 Funciona com vídeos normais e YouTube Shorts
- 💾 Downloads salvos automaticamente em "Videos Baixados"

## 🚀 Executar Localmente (Modo Desenvolvimento)

### Pré-requisitos

1. **Python 3.11+** instalado
2. **FFmpeg** instalado no sistema:
   ```bash
   # macOS
   brew install ffmpeg
   
   # Windows
   # Baixar de: https://ffmpeg.org/download.html
   # Adicionar ao PATH do sistema
   
   # Linux (Ubuntu/Debian)
   sudo apt install ffmpeg
   
   # Linux (Fedora/RHEL)
   sudo yum install ffmpeg
   ```

### Instalação e Execução

```bash
# 1. Clonar o repositório (se ainda não clonou)
git clone <seu-repo>
cd PythonProject

# 2. Criar ambiente virtual
python3 -m venv .venv

# 3. Ativar ambiente virtual
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar a aplicação
python gui_app.py
```

## 📦 Criar Executável Standalone

### macOS/Linux

```bash
# Dar permissão de execução ao script
chmod +x build_executable.sh

# Executar o build
./build_executable.sh
```

### Windows

```cmd
# Executar o script de build
build_executable.bat
```

### Alternativa Manual

```bash
# Instalar PyInstaller
pip install pyinstaller

# Executar o script de build
python build_executable.py
```

## 📂 Localização dos Arquivos

- **Executável criado**: `dist/YouTubeDownloader` (ou `.exe` no Windows)
- **Downloads salvos**: `~/Downloads/Videos Baixados/`

## 🎯 Como Usar a Interface

### Interface Moderna e Intuitiva

1. **Cole a URL** do vídeo do YouTube no campo de entrada
   - ✨ As informações são carregadas **automaticamente** após 0.8s
   - Você verá título, canal, duração, visualizações e descrição

2. **Aguarde o carregamento** das informações (opcional - pode baixar direto)

3. **Selecione o formato**:
   - 🎬 **Vídeo (MP4)** - Download completo com vídeo e áudio
   - 🎵 **Áudio (MP3)** - Apenas o áudio extraído

4. **Escolha a qualidade**:
   - 360p - Qualidade básica
   - 480p - Qualidade padrão
   - 720p - HD (recomendado)
   - 1080p - Full HD
   - best - Melhor qualidade disponível

5. **Clique em "⬇️ BAIXAR AGORA"**
   - Acompanhe o progresso na barra
   - Receba notificação ao concluir

6. **Gerencie seus downloads**:
   - 🔄 **Atualizar** - Recarrega a lista
   - 📂 **Abrir Pasta** - Abre a pasta de downloads
   - ▶️ **Reproduzir** - Abre o arquivo selecionado

## 🎨 Design da Interface

### Cores e Tema
- **Tema escuro moderno** inspirado no YouTube
- **Vermelho YouTube** (#FF0000) para botões principais
- **Cards com fundo escuro** para melhor organização
- **Ícones intuitivos** para fácil compreensão

### Recursos Visuais
- ✅ Indicadores de status em tempo real
- ⏳ Feedback visual durante carregamento
- 📊 Barra de progresso animada
- 🟢 Status do servidor sempre visível

## 🔧 Estrutura do Projeto

```
PythonProject/
├── gui_app.py              # Aplicação desktop com GUI moderna
├── build_executable.py     # Script para criar executável
├── build_executable.sh     # Build script para macOS/Linux
├── build_executable.bat    # Build script para Windows
├── app/                    # Backend FastAPI
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
├── requirements.txt
└── README_GUI.md          # Esta documentação
```

## 🐛 Solução de Problemas

### "Servidor ainda não está pronto"
- Aguarde 5-10 segundos após abrir a aplicação
- O indicador ficará 🟢 quando estiver pronto
- Verifique se a porta 8765 não está em uso

### "FFmpeg não encontrado"
- Certifique-se de ter FFmpeg instalado
- Teste no terminal: `ffmpeg -version`
- Adicione FFmpeg ao PATH do sistema

### Informações não carregam automaticamente
- Certifique-se que o servidor está online (🟢)
- Verifique se a URL é válida do YouTube
- Aguarde 0.8 segundos após colar a URL

### Erro ao criar executável
- Certifique-se de ter todas as dependências instaladas
- Tente limpar o cache: `rm -rf build dist *.spec`
- Execute novamente o script de build

### macOS: "Aplicação de desenvolvedor não identificado"
```bash
# Remover quarentena
xattr -d com.apple.quarantine dist/YouTubeDownloader
```

### Windows: Antivírus bloqueia o executável
- Adicione exceção no antivírus
- É comum com executáveis PyInstaller (falso positivo)

## 🎨 Melhorias na Nova Versão

### ✨ Novidades
- **Busca automática**: Não precisa mais clicar em "Info"
- **Interface dark mode**: Design moderno e confortável
- **Cards organizados**: Layout limpo e profissional
- **Botão destacado**: "BAIXAR AGORA" em destaque vermelho
- **Feedback visual**: Indicadores de carregamento claros
- **Pasta renomeada**: Agora é "Videos Baixados" (antes era "YouTubeDownloader")

### 🎯 Experiência do Usuário
1. Cole o link → Aguarde 0.8s → Veja as informações
2. Ajuste formato e qualidade
3. Clique para baixar
4. Receba notificação quando concluir

## 📝 Notas Importantes

1. **Busca automática funciona após digitar/colar**: Aguarde 800ms
2. **Primeira execução pode ser lenta**: O servidor FastAPI precisa inicializar (5-10s)
3. **Downloads em "Videos Baixados"**: Pasta criada automaticamente em ~/Downloads
4. **FFmpeg é obrigatório**: Para conversão de vídeo/áudio
5. **Executável é portátil**: Pode ser movido, mas FFmpeg deve estar no PATH
6. **Suporta múltiplos formatos**: MP4 (vídeo) e MP3 (áudio)

## 🔄 Atualizações

Para atualizar a aplicação:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python gui_app.py  # ou reconstruir o executável
```

## 💡 Dicas de Uso

- **Atalho**: Pressione Enter no campo de URL para baixar diretamente
- **Lista de downloads**: Clique duas vezes para abrir o arquivo
- **Pasta rápida**: Use "📂 Abrir Pasta" para ver todos os downloads
- **Sem espera**: Pode baixar sem esperar carregar as informações

## 📄 Licença

Este projeto é para uso pessoal. Respeite os termos de serviço do YouTube.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## ⚠️ Aviso Legal

Esta ferramenta é apenas para uso pessoal e educacional. Respeite os direitos autorais e os termos de serviço do YouTube. Não use para distribuição não autorizada de conteúdo protegido por direitos autorais.

---

**Desenvolvido com ❤️ para facilitar downloads do YouTube**

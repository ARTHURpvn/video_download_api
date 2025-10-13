#!/usr/bin/env python3
"""
YouTube Downloader - Interface Gráfica Desktop
Aplicação standalone com servidor FastAPI integrado
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import os
import sys
import time
from pathlib import Path
import requests
import subprocess
import re
import json

# Configurações
API_HOST = "127.0.0.1"
API_PORT = 8765
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"  # Usar http, não https
DOWNLOAD_DIR = Path.home() / "Downloads" / "Videos Baixados"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)

        # Configurar fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Servidor backend
        self.server_process = None
        self.server_ready = False

        # Fila para comunicação entre threads
        self.queue = queue.Queue()

        # Variáveis
        self.downloading = False
        self.current_download_file = None
        self.last_url = ""
        self.fetch_info_timer = None

        # Configurar estilo
        self.setup_styles()

        # Criar interface
        self.create_widgets()

        # Iniciar servidor backend
        self.start_backend_server()

        # Verificar atualizações da fila
        self.process_queue()

    def setup_styles(self):
        """Configurar estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')

        # Cores modernas
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.primary_color = "#FF0000"  # Vermelho YouTube
        self.secondary_color = "#282828"
        self.accent_color = "#3ea6ff"
        self.success_color = "#00ff00"
        self.card_bg = "#2d2d2d"

        self.root.configure(bg=self.bg_color)

        # Estilo dos botões
        style.configure("Primary.TButton",
                       background=self.primary_color,
                       foreground="red",
                       padding=12,
                       font=('SF Pro Display', 11, 'bold'),
                       borderwidth=0)

        style.map("Primary.TButton",
                 background=[('active', '#CC0000'), ('disabled', '#555555')])

        style.configure("Secondary.TButton",
                       background=self.secondary_color,
                       foreground="white",
                       padding=8,
                       font=('SF Pro Display', 10),
                       borderwidth=0)

        style.map("Secondary.TButton",
                 background=[('active', '#3d3d3d')])

        # Estilo dos frames
        style.configure("Card.TFrame",
                       background=self.card_bg,
                       relief='flat')

        style.configure("TLabelframe",
                       background=self.card_bg,
                       foreground=self.fg_color,
                       borderwidth=0)

        style.configure("TLabelframe.Label",
                       background=self.card_bg,
                       foreground=self.fg_color,
                       font=('SF Pro Display', 12, 'bold'))

        # Estilo da barra de progresso - VERMELHO
        style.configure("Red.Horizontal.TProgressbar",
                       background=self.primary_color,
                       troughcolor=self.secondary_color,
                       bordercolor=self.card_bg,
                       lightcolor=self.primary_color,
                       darkcolor=self.primary_color)

    def create_widgets(self):
        """Criar todos os widgets da interface"""

        # Container principal com scrollbar
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header com gradiente visual
        header_frame = tk.Frame(main_container, bg=self.bg_color, height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Logo e título
        title_container = tk.Frame(header_frame, bg=self.bg_color)
        title_container.pack()

        title_label = tk.Label(title_container,
                              text="YouTube Downloader",
                              font=('SF Pro Display', 32, 'bold'),
                              fg=self.primary_color,
                              bg=self.bg_color)
        title_label.pack()

        subtitle_label = tk.Label(title_container,
                                 text="Baixe vídeos e áudios do YouTube de forma rápida e fácil",
                                 font=('SF Pro Display', 11),
                                 fg="#999999",
                                 bg=self.bg_color)
        subtitle_label.pack()

        # Card de entrada de URL
        url_card = tk.Frame(main_container, bg=self.card_bg, relief='flat', bd=0)
        url_card.pack(fill=tk.X, pady=(0, 15))

        url_inner = tk.Frame(url_card, bg=self.card_bg)
        url_inner.pack(fill=tk.X, padx=20, pady=15)

        url_label = tk.Label(url_inner,
                           text="🔗 Cole o link do vídeo aqui:",
                           font=('SF Pro Display', 12, 'bold'),
                           fg=self.fg_color,
                           bg=self.card_bg)
        url_label.pack(anchor=tk.W, pady=(0, 8))

        self.url_var = tk.StringVar()
        self.url_var.trace('w', self.on_url_change)

        url_entry = tk.Entry(url_inner,
                           textvariable=self.url_var,
                           font=('SF Pro Display', 13),
                           bg="#1a1a1a",
                           fg=self.fg_color,
                           insertbackground=self.fg_color,
                           relief='flat',
                           bd=0)
        url_entry.pack(fill=tk.X, ipady=12, ipadx=10)
        url_entry.bind('<Return>', lambda e: self.start_download())

        # Indicador de carregamento de info
        self.loading_label = tk.Label(url_inner,
                                     text="",
                                     font=('SF Pro Display', 10),
                                     fg=self.accent_color,
                                     bg=self.card_bg)
        self.loading_label.pack(anchor=tk.W, pady=(5, 0))

        # Card de informações do vídeo (estilo YouTube)
        info_card = tk.Frame(main_container, bg=self.card_bg, relief='flat')
        info_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        info_inner = tk.Frame(info_card, bg=self.card_bg)
        info_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        info_header = tk.Label(info_inner,
                             text="📺 Informações do Vídeo",
                             font=('SF Pro Display', 14, 'bold'),
                             fg=self.fg_color,
                             bg=self.card_bg)
        info_header.pack(anchor=tk.W, pady=(0, 10))

        # Frame para thumbnail e info lado a lado
        content_frame = tk.Frame(info_inner, bg=self.card_bg)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Área de texto para informações
        self.info_text = tk.Text(content_frame,
                                height=6,
                                wrap=tk.WORD,
                                font=('SF Pro Display', 11),
                                bg="#1a1a1a",
                                fg="#cccccc",
                                relief='flat',
                                bd=0,
                                padx=15,
                                pady=15,
                                state='disabled')
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Mensagem inicial
        self.info_text.config(state='normal')
        self.info_text.insert(1.0, "✨ Cole um link do YouTube acima e as informações aparecerão automaticamente aqui!")
        self.info_text.config(state='disabled')

        # Card de opções de download
        options_card = tk.Frame(main_container, bg=self.card_bg, relief='flat')
        options_card.pack(fill=tk.X, pady=(0, 15))

        options_inner = tk.Frame(options_card, bg=self.card_bg)
        options_inner.pack(fill=tk.X, padx=20, pady=15)

        options_label = tk.Label(options_inner,
                               text="⚙️ Configurações de Download",
                               font=('SF Pro Display', 12, 'bold'),
                               fg=self.fg_color,
                               bg=self.card_bg)
        options_label.pack(anchor=tk.W, pady=(0, 10))

        options_grid = tk.Frame(options_inner, bg=self.card_bg)
        options_grid.pack(fill=tk.X)

        # Formato
        format_frame = tk.Frame(options_grid, bg=self.card_bg)
        format_frame.pack(side=tk.LEFT, padx=(0, 30))

        format_label = tk.Label(format_frame,
                              text="Formato:",
                              font=('SF Pro Display', 11),
                              fg="#999999",
                              bg=self.card_bg)
        format_label.pack(anchor=tk.W)

        self.format_var = tk.StringVar(value="video")

        format_buttons = tk.Frame(format_frame, bg=self.card_bg)
        format_buttons.pack(fill=tk.X, pady=(5, 0))

        video_radio = tk.Radiobutton(format_buttons,
                                    text="🎬 Vídeo (MP4)",
                                    variable=self.format_var,
                                    value="video",
                                    font=('SF Pro Display', 11),
                                    fg=self.fg_color,
                                    bg=self.card_bg,
                                    selectcolor=self.secondary_color,
                                    activebackground=self.card_bg,
                                    activeforeground=self.fg_color,
                                    relief='flat')
        video_radio.pack(side=tk.LEFT, padx=(0, 15))

        audio_radio = tk.Radiobutton(format_buttons,
                                    text="🎵 Áudio (MP3)",
                                    variable=self.format_var,
                                    value="audio",
                                    font=('SF Pro Display', 11),
                                    fg=self.fg_color,
                                    bg=self.card_bg,
                                    selectcolor=self.secondary_color,
                                    activebackground=self.card_bg,
                                    activeforeground=self.fg_color,
                                    relief='flat')
        audio_radio.pack(side=tk.LEFT)

        # Qualidade
        quality_frame = tk.Frame(options_grid, bg=self.card_bg)
        quality_frame.pack(side=tk.LEFT)

        quality_label = tk.Label(quality_frame,
                               text="Qualidade:",
                               font=('SF Pro Display', 11),
                               fg="#999999",
                               bg=self.card_bg)
        quality_label.pack(anchor=tk.W)

        self.quality_var = tk.StringVar(value="1080p")  # Mudado de 720p para 1080p
        quality_combo = ttk.Combobox(quality_frame,
                                    textvariable=self.quality_var,
                                    values=["360p", "480p", "720p", "1080p", "best"],
                                    state="readonly",
                                    width=12,
                                    font=('SF Pro Display', 11))
        quality_combo.pack(pady=(5, 0))

        # Botão de download grande e destacado
        self.download_btn = tk.Button(main_container,
                                     text="⬇ BAIXAR AGORA",
                                     command=self.start_download,
                                     font=('SF Pro Display', 14, 'bold'),
                                     bg=self.secondary_color,
                                     fg="red",
                                     activebackground='red',
                                     activeforeground="red",
                                     disabledforeground='#FFF',  # Texto cinza quando desabilitado
                                     relief='flat',
                                     bd=0,
                                     cursor='hand2',
                                     pady=15,
                                     state='disabled')  # Iniciar desabilitado
        self.download_btn.pack(fill=tk.X, pady=(0, 15))

        # Forçar fundo vermelho mesmo quando desabilitado
        self.download_btn.configure(disabledforeground='#999999')

        # Barra de progresso moderna
        self.progress_card = tk.Frame(main_container, bg=self.card_bg, relief='flat')
        self.progress_card.pack(fill=tk.X, pady=(0, 15))

        progress_inner = tk.Frame(self.progress_card, bg=self.card_bg)
        progress_inner.pack(fill=tk.X, padx=20, pady=15)

        self.status_var = tk.StringVar(value="Aguardando download...")
        status_label = tk.Label(progress_inner,
                              textvariable=self.status_var,
                              font=('SF Pro Display', 11),
                              fg="#999999",
                              bg=self.card_bg)
        status_label.pack(anchor=tk.W, pady=(0, 8))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_inner,
                                           variable=self.progress_var,
                                           maximum=100,
                                           mode='determinate',
                                           length=400,
                                           style="Red.Horizontal.TProgressbar")  # Usar estilo vermelho
        self.progress_bar.pack(fill=tk.X)

        # Label para mostrar porcentagem
        self.progress_label = tk.Label(progress_inner,
                                      text="0%",
                                      font=('SF Pro Display', 10, 'bold'),
                                      fg=self.accent_color,
                                      bg=self.card_bg)
        self.progress_label.pack(anchor=tk.W, pady=(5, 0))

        # Card de arquivos baixados
        self.downloads_card = tk.Frame(main_container, bg=self.card_bg, relief='flat')
        self.downloads_card.pack(fill=tk.BOTH, expand=True)

        downloads_inner = tk.Frame(self.downloads_card, bg=self.card_bg)
        downloads_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        downloads_header_frame = tk.Frame(downloads_inner, bg=self.card_bg)
        downloads_header_frame.pack(fill=tk.X, pady=(0, 10))

        downloads_label = tk.Label(downloads_header_frame,
                                  text="📁 Arquivos Baixados",
                                  font=('SF Pro Display', 14, 'bold'),
                                  fg=self.fg_color,
                                  bg=self.card_bg)
        downloads_label.pack(side=tk.LEFT)

        # Lista de downloads com estilo
        self.downloads_listbox = tk.Listbox(downloads_inner,
                                           height=5,
                                           font=('SF Pro Display', 11),
                                           bg="#1a1a1a",
                                           fg=self.fg_color,
                                           selectbackground=self.accent_color,
                                           selectforeground="white",
                                           relief='flat',
                                           bd=0,
                                           highlightthickness=0)
        self.downloads_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Botões de ação
        btn_frame = tk.Frame(downloads_inner, bg=self.card_bg)
        btn_frame.pack(fill=tk.X)

        refresh_btn = tk.Button(btn_frame,
                              text="🔄 Atualizar",
                              command=self.refresh_downloads,
                              font=('SF Pro Display', 10),
                              bg=self.secondary_color,
                              fg=self.fg_color,
                              activebackground='#3d3d3d',
                              activeforeground=self.fg_color,
                              relief='flat',
                              bd=0,
                              cursor='hand2',
                              padx=15,
                              pady=8)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))

        folder_btn = tk.Button(btn_frame,
                             text="📂 Abrir Pasta",
                             command=self.open_downloads_folder,
                             font=('SF Pro Display', 10),
                             bg=self.secondary_color,
                             fg=self.fg_color,
                             activebackground='#3d3d3d',
                             activeforeground=self.fg_color,
                             relief='flat',
                             bd=0,
                             cursor='hand2',
                             padx=15,
                             pady=8)
        folder_btn.pack(side=tk.LEFT, padx=(0, 10))

        play_btn = tk.Button(btn_frame,
                           text="▶️ Reproduzir",
                           command=self.open_selected_file,
                           font=('SF Pro Display', 10),
                           bg=self.secondary_color,
                           fg=self.fg_color,
                           activebackground='#3d3d3d',
                           activeforeground=self.fg_color,
                           relief='flat',
                           bd=0,
                           cursor='hand2',
                           padx=15,
                           pady=8)
        play_btn.pack(side=tk.LEFT)

        # Status do servidor (footer)
        footer_frame = tk.Frame(main_container, bg=self.bg_color)
        footer_frame.pack(fill=tk.X, pady=(15, 0))

        self.server_status_var = tk.StringVar(value="⚪ Iniciando servidor...")
        server_status = tk.Label(footer_frame,
                               textvariable=self.server_status_var,
                               font=('SF Pro Display', 9),
                               fg='#666666',
                               bg=self.bg_color)
        server_status.pack()

    def on_url_change(self, *args):
        """Detectar mudança na URL e buscar informações automaticamente"""
        url = self.url_var.get().strip()

        # Cancelar timer anterior se existir
        if self.fetch_info_timer:
            self.root.after_cancel(self.fetch_info_timer)

        # Limpar estado anterior se URL foi apagada
        if not url:
            self.loading_label.config(text="")
            self.clear_video_info()
            self.download_btn.config(state='disabled')  # Desabilitar botão
            return

        # Verificar se é uma URL válida do YouTube
        if self.is_youtube_url(url):
            if url != self.last_url:
                self.loading_label.config(text="⏳ Buscando informações...")
                self.download_btn.config(state='disabled')  # Desabilitar enquanto valida
                # Aguardar 800ms após parar de digitar
                self.fetch_info_timer = self.root.after(800, lambda: self.auto_fetch_info(url))
        else:
            # URL não é do YouTube
            self.loading_label.config(text="❌ Link inválido! Use um link do YouTube", fg="#FF0000")
            self.download_btn.config(state='disabled')  # Manter desabilitado
            self.clear_video_info()

            # Mostrar mensagem de erro nas informações
            self.info_text.config(state='normal')
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0,
                "❌ Link inválido para download!\n\n"
                "Por favor, cole um link válido do YouTube:\n"
                "• https://www.youtube.com/watch?v=...\n"
                "• https://youtu.be/...\n"
                "• https://www.youtube.com/shorts/...")
            self.info_text.config(state='disabled')

    def is_youtube_url(self, url):
        """Verificar se é uma URL válida do YouTube"""
        youtube_patterns = [
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)',
            r'youtube\.com/watch\?v=',
            r'youtu\.be/',
            r'youtube\.com/shorts/'
        ]
        return any(re.search(pattern, url) for pattern in youtube_patterns)

    def auto_fetch_info(self, url):
        """Buscar informações automaticamente"""
        if not self.server_ready:
            self.loading_label.config(text="⏳ Aguardando servidor...")
            self.download_btn.config(state='disabled')
            return

        self.last_url = url

        def fetch_info():
            try:
                response = requests.post(
                    f"{API_BASE_URL}/video/info",
                    json={"url": url},
                    timeout=30
                )

                if response.status_code == 200:
                    info = response.json()
                    self.queue.put(('video_info', info))
                    self.queue.put(('loading_done', True))  # True = sucesso
                    self.queue.put(('enable_download', True))  # Habilitar botão
                else:
                    self.queue.put(('loading_done', False))  # False = erro
                    self.queue.put(('info_error', 'Erro ao buscar informações do vídeo'))
                    self.queue.put(('enable_download', False))  # Desabilitar botão
            except Exception as e:
                self.queue.put(('loading_done', False))
                self.queue.put(('info_error', f'Erro: {str(e)}'))
                self.queue.put(('enable_download', False))  # Desabilitar botão

        threading.Thread(target=fetch_info, daemon=True).start()

    def clear_video_info(self):
        """Limpar informações do vídeo"""
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, "✨ Cole um link do YouTube acima e as informações aparecerão automaticamente aqui!")
        self.info_text.config(state='disabled')
        self.last_url = ""
        self.download_btn.config(state='disabled')  # Desabilitar botão

    def start_backend_server(self):
        """Iniciar servidor FastAPI em background"""
        def run_server():
            try:
                import uvicorn
                from app.main import app

                # Configurar diretório de downloads
                os.environ['DOWNLOAD_DIR'] = str(DOWNLOAD_DIR)

                # Iniciar servidor
                self.queue.put(('server_status', 'starting'))
                uvicorn.run(app, host=API_HOST, port=API_PORT, log_level="warning")
            except Exception as e:
                self.queue.put(('server_status', f'error: {str(e)}'))

        # Iniciar em thread separada
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Verificar se servidor está pronto
        check_thread = threading.Thread(target=self.check_server_ready, daemon=True)
        check_thread.start()

    def check_server_ready(self):
        """Verificar se servidor está pronto"""
        max_attempts = 30
        for i in range(max_attempts):
            try:
                response = requests.get(f"{API_BASE_URL}/health", timeout=1)
                if response.status_code == 200:
                    self.server_ready = True
                    self.queue.put(('server_status', 'ready'))
                    self.queue.put(('refresh_downloads', None))
                    return
            except:
                pass
            time.sleep(0.5)

        self.queue.put(('server_status', 'failed'))

    def get_video_info(self):
        """Obter informações do vídeo"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL do YouTube")
            return

        self.auto_fetch_info(url)

    def start_download(self):
        """Iniciar download do vídeo"""
        if not self.server_ready:
            messagebox.showerror("Erro", "Servidor ainda não está pronto. Aguarde um momento.")
            return

        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL do YouTube")
            return

        # Validar se é URL do YouTube
        if not self.is_youtube_url(url):
            messagebox.showerror("Link Inválido",
                               "Este não é um link válido do YouTube!\n\n"
                               "Use links como:\n"
                               "• https://www.youtube.com/watch?v=...\n"
                               "• https://youtu.be/...\n"
                               "• https://www.youtube.com/shorts/...")
            return

        if self.downloading:
            messagebox.showwarning("Aviso", "Um download já está em andamento")
            return

        self.downloading = True
        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.progress_label.config(text="0%")

        # Mostrar barra de progresso
        self.progress_card.pack(fill=tk.X, pady=(0, 15), before=self.downloads_card)

        def download():
            try:
                self.queue.put(('status', 'Iniciando download...'))
                self.queue.put(('progress', 0))

                # Preparar payload
                payload = {
                    "url": url,
                    "format": self.format_var.get(),
                    "quality": self.quality_var.get()
                }

                # Usar o endpoint de streaming para progresso real
                response = requests.post(
                    f"{API_BASE_URL}/video/download-stream",
                    json=payload,
                    stream=True,
                    timeout=300
                )

                if response.status_code == 200:
                    # Processar eventos SSE em tempo real
                    for line in response.iter_lines():
                        if line:
                            line_text = line.decode('utf-8')

                            # SSE envia linhas no formato "data: {json}"
                            if line_text.startswith('data: '):
                                json_data = line_text[6:]  # Remove "data: "

                                try:
                                    event = json.loads(json_data)

                                    # Atualizar progresso real
                                    if 'progress_percent' in event:
                                        progress = event['progress_percent']
                                        self.queue.put(('progress', progress))

                                    # Atualizar status
                                    if 'status' in event:
                                        status = event['status']

                                        if status == 'starting':
                                            self.queue.put(('status', 'Iniciando download...'))
                                        elif status == 'downloading':
                                            message = event.get('message', 'Baixando...')
                                            self.queue.put(('status', message))
                                        elif status == 'processing':
                                            self.queue.put(('status', 'Processando vídeo...'))
                                        elif status == 'completed':
                                            self.queue.put(('status', 'Download concluído!'))
                                            self.queue.put(('progress', 100))
                                            self.queue.put(('download_complete', event))
                                        elif status == 'error':
                                            error_msg = event.get('message', 'Erro desconhecido')
                                            self.queue.put(('error', error_msg))

                                except json.JSONDecodeError:
                                    pass
                else:
                    self.queue.put(('error', f"Erro no servidor: {response.status_code}"))

            except Exception as e:
                self.queue.put(('error', f"Erro ao baixar: {str(e)}"))
            finally:
                self.downloading = False
                self.queue.put(('download_finished', None))

        threading.Thread(target=download, daemon=True).start()

    def refresh_downloads(self):
        """Atualizar lista de downloads"""
        def fetch_downloads():
            try:
                response = requests.get(f"{API_BASE_URL}/downloads", timeout=10)
                if response.status_code == 200:
                    downloads = response.json()
                    self.queue.put(('downloads_list', downloads))
            except Exception as e:
                print(f"Erro ao atualizar downloads: {e}")

        threading.Thread(target=fetch_downloads, daemon=True).start()

    def open_downloads_folder(self):
        """Abrir pasta de downloads"""
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', str(DOWNLOAD_DIR)])
        elif sys.platform == 'win32':  # Windows
            os.startfile(str(DOWNLOAD_DIR))
        else:  # Linux
            subprocess.run(['xdg-open', str(DOWNLOAD_DIR)])

    def open_selected_file(self):
        """Abrir arquivo selecionado"""
        selection = self.downloads_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Selecione um arquivo para abrir")
            return

        filename = self.downloads_listbox.get(selection[0])
        filepath = DOWNLOAD_DIR / filename

        if filepath.exists():
            if sys.platform == 'darwin':
                subprocess.run(['open', str(filepath)])
            elif sys.platform == 'win32':
                os.startfile(str(filepath))
            else:
                subprocess.run(['xdg-open', str(filepath)])
        else:
            messagebox.showerror("Erro", "Arquivo não encontrado")

    def process_queue(self):
        """Processar mensagens da fila"""
        try:
            while True:
                msg_type, data = self.queue.get_nowait()

                if msg_type == 'server_status':
                    if data == 'ready':
                        self.server_status_var.set("🟢 Servidor online e pronto")
                    elif data == 'starting':
                        self.server_status_var.set("🟡 Iniciando servidor...")
                    elif data == 'failed':
                        self.server_status_var.set("🔴 Erro ao iniciar servidor")
                    elif data.startswith('error'):
                        self.server_status_var.set(f"🔴 Erro: {data}")

                elif msg_type == 'status':
                    self.status_var.set(data)

                elif msg_type == 'progress':
                    self.progress_var.set(data)
                    # Atualizar label de porcentagem
                    self.progress_label.config(text=f"{int(data)}%")

                elif msg_type == 'video_info':
                    self.display_video_info(data)

                elif msg_type == 'enable_download':
                    # Habilitar ou desabilitar botão de download baseado na validação
                    if data and not self.downloading:
                        self.download_btn.config(state='normal')
                    else:
                        self.download_btn.config(state='disabled')

                elif msg_type == 'loading_done':
                    if data:  # True = sucesso
                        self.loading_label.config(text="✅ Informações carregadas!", fg=self.accent_color)
                    else:  # False = erro
                        self.loading_label.config(text="❌ Erro ao carregar", fg="#FF0000")
                    self.root.after(3000, lambda: self.loading_label.config(text=""))

                elif msg_type == 'info_error':
                    self.loading_label.config(text=f"❌ {data}", fg="#FF0000")
                    # Mostrar erro nas informações do vídeo
                    self.info_text.config(state='normal')
                    self.info_text.delete(1.0, tk.END)
                    self.info_text.insert(1.0,
                        f"❌ Erro ao buscar informações!\n\n"
                        f"{data}\n\n"
                        f"Verifique se:\n"
                        f"• O link do YouTube está correto\n"
                        f"• Você está conectado à internet\n"
                        f"• O vídeo está disponível publicamente")
                    self.info_text.config(state='disabled')
                    self.root.after(5000, lambda: self.loading_label.config(text=""))

                elif msg_type == 'download_complete':
                    self.handle_download_complete(data)

                elif msg_type == 'download_finished':
                    # Verificar se há um link válido antes de reabilitar
                    url = self.url_var.get().strip()
                    if url and self.is_youtube_url(url) and self.last_url == url:
                        self.download_btn.config(state='normal')
                    else:
                        self.download_btn.config(state='disabled')
                    self.refresh_downloads()

                elif msg_type == 'downloads_list':
                    self.update_downloads_list(data)

                elif msg_type == 'error':
                    self.status_var.set("❌ Erro no download")
                    messagebox.showerror("Erro", data)
                    # Verificar se há um link válido antes de reabilitar
                    url = self.url_var.get().strip()
                    if url and self.is_youtube_url(url) and self.last_url == url:
                        self.download_btn.config(state='normal')
                    else:
                        self.download_btn.config(state='disabled')
                    self.downloading = False

                elif msg_type == 'refresh_downloads':
                    self.refresh_downloads()

        except queue.Empty:
            pass

        # Agendar próxima verificação
        self.root.after(100, self.process_queue)

    def display_video_info(self, info):
        """Exibir informações do vídeo com estilo melhorado"""
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)

        text = f"📺 {info.get('title', 'N/A')}\n\n"
        text += f"👤 Canal: {info.get('uploader', 'N/A')}\n"

        if info.get('duration'):
            minutes = info['duration'] // 60
            seconds = info['duration'] % 60
            text += f"⏱️  Duração: {minutes}:{seconds:02d}\n"

        if info.get('view_count'):
            views = info['view_count']
            if views >= 1000000:
                text += f"👁️  {views/1000000:.1f}M visualizações\n"
            elif views >= 1000:
                text += f"👁️  {views/1000:.1f}K visualizações\n"
            else:
                text += f"👁️  {views} visualizações\n"

        if info.get('upload_date'):
            date = info['upload_date']
            text += f"📅 Publicado em: {date[6:]}/{date[4:6]}/{date[:4]}\n"

        if info.get('description'):
            desc = info['description'][:150].replace('\n', ' ')
            text += f"\n📝 {desc}..."

        self.info_text.insert(1.0, text)
        self.info_text.config(state='disabled')

    def handle_download_complete(self, result):
        """Processar conclusão do download"""
        video_info = result.get('video_info', {})
        title = video_info.get('title', 'Vídeo')

        self.status_var.set(f"✅ Download completo: {title}")
        messagebox.showinfo("✅ Sucesso!",
                          f"Download concluído!\n\n{title}\n\n📁 Arquivo salvo em: Videos Baixados",
                          icon='info')

    def update_downloads_list(self, downloads):
        """Atualizar lista de arquivos baixados"""
        self.downloads_listbox.delete(0, tk.END)

        if isinstance(downloads, list):
            for item in downloads:
                if isinstance(item, dict):
                    filename = item.get('filename', '')
                else:
                    filename = str(item)

                if filename:
                    self.downloads_listbox.insert(tk.END, filename)

    def on_closing(self):
        """Lidar com fechamento da aplicação"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.root.destroy()
            # Terminar processo Python completamente
            os._exit(0)


def main():
    """Função principal"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

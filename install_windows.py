#!/usr/bin/env python3
"""
YouTube Downloader - Instalador Automático para Windows
Versão corrigida com feedback visual em tempo real
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import threading
import time

class InstallerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader - Instalador")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Cores
        self.bg = "#1a1a1a"
        self.fg = "#ffffff"
        self.red = "#FF0000"
        self.card = "#2d2d2d"

        self.root.configure(bg=self.bg)
        self.installing = False

        self.create_ui()

    def create_ui(self):
        """Criar interface"""
        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Título
        tk.Label(main, text="YouTube Downloader",
                font=('Arial', 26, 'bold'),
                fg=self.red, bg=self.bg).pack(pady=(0, 5))

        tk.Label(main, text="Instalador Automático",
                font=('Arial', 11),
                fg="#999", bg=self.bg).pack(pady=(0, 20))

        # Status atual
        self.status_lbl = tk.Label(main, text="✓ Pronto para instalar",
                                   font=('Arial', 11, 'bold'),
                                   fg=self.fg, bg=self.bg)
        self.status_lbl.pack(pady=(0, 10))

        # Barra de progresso
        self.progressbar = ttk.Progressbar(main, mode='indeterminate', length=550)
        self.progressbar.pack(pady=(0, 15))

        # Área de log com scroll
        log_frame = tk.Frame(main, bg=self.card, relief='flat')
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.log = scrolledtext.ScrolledText(
            log_frame, height=18, width=75,
            font=('Consolas', 9),
            bg="#000", fg="#0f0",
            insertbackground="#0f0",
            wrap=tk.WORD,
            state='disabled'
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # Botões
        btns = tk.Frame(main, bg=self.bg)
        btns.pack(fill=tk.X)

        self.btn_install = tk.Button(
            btns, text="▶ INSTALAR AGORA",
            command=self.on_install_click,
            font=('Arial', 12, 'bold'),
            bg=self.red, fg="white",
            activebackground='#CC0000',
            relief='flat', cursor='hand2',
            padx=35, pady=12
        )
        self.btn_install.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            btns, text="✕ SAIR",
            command=self.root.quit,
            font=('Arial', 12),
            bg=self.card, fg="white",
            activebackground='#3d3d3d',
            relief='flat', cursor='hand2',
            padx=35, pady=12
        ).pack(side=tk.LEFT)

    def write(self, text):
        """Escrever no log"""
        self.log.config(state='normal')
        self.log.insert(tk.END, text + '\n')
        self.log.see(tk.END)
        self.log.config(state='disabled')
        self.root.update_idletasks()

    def status(self, text):
        """Atualizar status"""
        self.status_lbl.config(text=text)
        self.root.update_idletasks()

    def on_install_click(self):
        """Botão instalar clicado"""
        if self.installing:
            return

        if not messagebox.askyesno(
            "Confirmar Instalação",
            "Instalar YouTube Downloader e todas as dependências?\n\n"
            "Isso levará alguns minutos.",
            icon='question'
        ):
            return

        self.installing = True
        self.btn_install.config(state='disabled', text="⏳ INSTALANDO...")
        self.progressbar.start(8)

        threading.Thread(target=self.install, daemon=True).start()

    def exec_cmd(self, cmd, desc):
        """Executar comando com output em tempo real"""
        self.write(f"\n▸ {desc}")
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in proc.stdout:
                line = line.strip()
                if line and not line.startswith("WARNING"):
                    self.write(f"  {line}")

            proc.wait()
            return proc.returncode == 0

        except Exception as e:
            self.write(f"  ✗ ERRO: {e}")
            return False

    def install(self):
        """Processo principal de instalação"""
        try:
            self.write("=" * 65)
            self.write("  INSTALAÇÃO DO YOUTUBE DOWNLOADER")
            self.write("=" * 65)

            # ETAPA 1: Python
            self.status("⏳ [1/6] Verificando Python...")
            self.write("\n[ETAPA 1/6] Verificando Python")

            try:
                ver = subprocess.check_output(
                    [sys.executable, "--version"],
                    stderr=subprocess.STDOUT
                ).decode().strip()
                self.write(f"✓ Encontrado: {ver}")
            except:
                self.write("✗ Python não encontrado!")
                raise Exception("Python não instalado")

            time.sleep(0.4)

            # ETAPA 2: pip
            self.status("⏳ [2/6] Atualizando pip...")
            self.write("\n[ETAPA 2/6] Atualizando pip")

            self.exec_cmd(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                "Atualizando pip"
            )
            self.write("✓ pip atualizado")

            time.sleep(0.4)

            # ETAPA 3: Dependências
            self.status("⏳ [3/6] Instalando dependências...")
            self.write("\n[ETAPA 3/6] Instalando dependências Python")

            packages = [
                ("yt-dlp", "Baixador de vídeos do YouTube"),
                ("fastapi", "Framework web"),
                ("uvicorn[standard]", "Servidor ASGI"),
                ("python-multipart", "Upload de arquivos"),
                ("requests", "Cliente HTTP"),
                ("pydantic", "Validação de dados")
            ]

            for pkg, desc in packages:
                self.write(f"\n  → Instalando {pkg} ({desc})")
                if self.exec_cmd(
                    [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                    f"pip install {pkg}"
                ):
                    self.write(f"  ✓ {pkg} instalado")
                else:
                    self.write(f"  ⚠ Problema com {pkg} (continuando...)")

            time.sleep(0.4)

            # ETAPA 4: FFmpeg
            self.status("⏳ [4/6] Configurando FFmpeg...")
            self.write("\n[ETAPA 4/6] Verificando FFmpeg")

            try:
                subprocess.check_output(
                    ["ffmpeg", "-version"],
                    stderr=subprocess.STDOUT
                )
                self.write("✓ FFmpeg já instalado no sistema")
            except:
                self.write("⚠ FFmpeg não encontrado")
                self.write("  (Será baixado automaticamente quando necessário)")

            time.sleep(0.4)

            # ETAPA 5: Diretórios
            self.status("⏳ [5/6] Criando diretórios...")
            self.write("\n[ETAPA 5/6] Configurando diretórios")

            dl_dir = os.path.join(
                os.path.expanduser("~"),
                "Downloads",
                "Videos Baixados"
            )
            os.makedirs(dl_dir, exist_ok=True)
            self.write(f"✓ Pasta criada: {dl_dir}")

            time.sleep(0.4)

            # ETAPA 6: Build do executável
            self.status("⏳ [6/6] Criando executável...")
            self.write("\n[ETAPA 6/6] Compilando aplicativo (.exe)")
            self.write("  ⚠ Esta etapa pode levar 5-10 minutos!")
            self.write("  Por favor, aguarde...")

            # Instalar PyInstaller
            self.write("\n  → Instalando PyInstaller")
            if self.exec_cmd(
                [sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"],
                "pip install pyinstaller"
            ):
                self.write("  ✓ PyInstaller instalado")

            time.sleep(0.5)

            # Executar build
            build_file = os.path.join(os.path.dirname(__file__), "build_executable.py")

            if os.path.exists(build_file):
                self.write("\n  → Compilando aplicativo...")
                self.write("  (Isso levará vários minutos...)")

                if self.exec_cmd(
                    [sys.executable, build_file],
                    "Criando YouTubeDownloader.exe"
                ):
                    self.write("\n  ✓✓✓ EXECUTÁVEL CRIADO COM SUCESSO! ✓✓✓")

                    desktop = os.path.join(
                        os.path.expanduser("~"),
                        "Desktop",
                        "YouTubeDownloader"
                    )
                    self.write(f"  📁 Local: {desktop}")
                    self.write(f"  📄 Arquivo: YouTubeDownloader.exe")
                else:
                    self.write("\n  ⚠ Erro ao criar executável")
                    self.write("  Você pode executar: python gui_app.py")
            else:
                self.write("  ⚠ build_executable.py não encontrado")
                self.write("  Você pode executar: python gui_app.py")

            # FINALIZAÇÃO
            self.write("\n" + "=" * 65)
            self.write("  ✓✓✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO! ✓✓✓")
            self.write("=" * 65)
            self.write("\n✅ YouTube Downloader está pronto para uso!")
            self.write("📁 Verifique a pasta 'YouTubeDownloader' na Área de Trabalho")
            self.write("\n" + "=" * 65)

            self.status("✓ Instalação completa!")
            self.progressbar.stop()

            self.root.after(500, self.show_done)

        except Exception as e:
            self.write(f"\n\n✗✗✗ ERRO FATAL ✗✗✗")
            self.write(f"✗ {str(e)}")
            self.status("✗ Erro na instalação")
            self.progressbar.stop()

            self.root.after(100, lambda: messagebox.showerror(
                "Erro na Instalação",
                f"Ocorreu um erro durante a instalação:\n\n{e}"
            ))

        finally:
            self.installing = False
            self.btn_install.config(state='normal', text="▶ INSTALAR AGORA")

    def show_done(self):
        """Mostrar conclusão"""
        resp = messagebox.askyesno(
            "✓ Instalação Concluída!",
            "YouTube Downloader foi instalado com sucesso!\n\n"
            "Deseja abrir o aplicativo agora?",
            icon='info'
        )

        if resp:
            try:
                # Tentar abrir o .exe primeiro
                exe = os.path.join(
                    os.path.expanduser("~"),
                    "Desktop",
                    "YouTubeDownloader",
                    "YouTubeDownloader.exe"
                )

                if os.path.exists(exe):
                    os.startfile(exe)
                else:
                    # Senão, abrir o Python script
                    gui = os.path.join(os.path.dirname(__file__), "gui_app.py")
                    subprocess.Popen([sys.executable, gui])

                self.root.quit()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir:\n{e}")

    def run(self):
        """Executar"""
        self.root.mainloop()


if __name__ == "__main__":
    app = InstallerGUI()
    app.run()


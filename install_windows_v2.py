#!/usr/bin/env python3
"""
YouTube Downloader - Instalador Simplificado para Windows
Versão robusta com melhor feedback visual
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import threading
import time

class InstallerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader - Instalador")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # Cores
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.primary_color = "#FF0000"
        self.card_bg = "#2d2d2d"

        self.root.configure(bg=self.bg_color)

        self.installing = False
        self.setup_ui()

    def setup_ui(self):
        """Configurar interface"""
        # Container principal
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title = tk.Label(container, text="YouTube Downloader",
                        font=('Arial', 28, 'bold'),
                        fg=self.primary_color, bg=self.bg_color)
        title.pack(pady=(0, 5))

        subtitle = tk.Label(container, text="Instalador Automático",
                           font=('Arial', 11),
                           fg="#999999", bg=self.bg_color)
        subtitle.pack(pady=(0, 20))

        # Status
        self.status_label = tk.Label(container,
                                     text="Pronto para instalar",
                                     font=('Arial', 11, 'bold'),
                                     fg=self.fg_color,
                                     bg=self.bg_color)
        self.status_label.pack(pady=(0, 10))

        # Barra de progresso
        self.progress = ttk.Progressbar(container, mode='indeterminate', length=500)
        self.progress.pack(pady=(0, 15))

        # Área de log
        log_frame = tk.Frame(container, bg=self.card_bg)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.log_area = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            width=80,
            font=('Consolas', 9),
            bg="#0a0a0a",
            fg="#00ff00",
            insertbackground="#00ff00",
            wrap=tk.WORD,
            state='disabled'
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Botões
        btn_frame = tk.Frame(container, bg=self.bg_color)
        btn_frame.pack(fill=tk.X)

        self.install_btn = tk.Button(
            btn_frame,
            text="INSTALAR AGORA",
            command=self.start_install,
            font=('Arial', 12, 'bold'),
            bg=self.primary_color,
            fg="white",
            activebackground='#CC0000',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=12
        )
        self.install_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = tk.Button(
            btn_frame,
            text="SAIR",
            command=self.root.quit,
            font=('Arial', 12),
            bg=self.card_bg,
            fg="white",
            activebackground='#3d3d3d',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=12
        )
        cancel_btn.pack(side=tk.LEFT)

    def write_log(self, text):
        """Escrever no log"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, text + '\n')
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        self.log_area.update()

    def set_status(self, text):
        """Atualizar status"""
        self.status_label.config(text=text)
        self.status_label.update()

    def start_install(self):
        """Iniciar instalação"""
        if self.installing:
            return

        response = messagebox.askyesno(
            "Confirmar",
            "Instalar YouTube Downloader e todas as dependências?\n\n"
            "Isso pode levar vários minutos.",
            icon='question'
        )

        if not response:
            return

        self.installing = True
        self.install_btn.config(state='disabled', text="INSTALANDO...")
        self.progress.start(10)

        # Iniciar instalação em thread separada
        thread = threading.Thread(target=self.install_process, daemon=True)
        thread.start()

    def run_command(self, cmd, description):
        """Executar comando e capturar saída"""
        self.write_log(f"\n>>> {description}")
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )

            for line in process.stdout:
                line = line.strip()
                if line:
                    self.write_log(f"    {line}")

            process.wait()
            return process.returncode == 0
        except Exception as e:
            self.write_log(f"    ERRO: {e}")
            return False

    def install_process(self):
        """Processo de instalação"""
        try:
            self.write_log("=" * 60)
            self.write_log("INSTALAÇÃO DO YOUTUBE DOWNLOADER")
            self.write_log("=" * 60)

            # Passo 1: Verificar Python
            self.set_status("Verificando Python...")
            self.write_log("\n[1/6] Verificando Python")

            try:
                version = subprocess.check_output(
                    [sys.executable, "--version"],
                    stderr=subprocess.STDOUT
                ).decode().strip()
                self.write_log(f"✓ {version}")
            except:
                self.write_log("✗ Python não encontrado!")
                messagebox.showerror("Erro", "Python não instalado!")
                return

            time.sleep(0.3)

            # Passo 2: Atualizar pip
            self.set_status("Atualizando pip...")
            self.write_log("\n[2/6] Atualizando pip")

            if self.run_command(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"],
                "pip install --upgrade pip"
            ):
                self.write_log("✓ pip atualizado")
            else:
                self.write_log("⚠ Falha ao atualizar pip (continuando...)")

            time.sleep(0.3)

            # Passo 3: Instalar dependências
            self.set_status("Instalando dependências...")
            self.write_log("\n[3/6] Instalando dependências Python")

            deps = [
                "yt-dlp",
                "fastapi",
                "uvicorn[standard]",
                "python-multipart",
                "requests",
                "pydantic"
            ]

            for dep in deps:
                self.write_log(f"\n  Instalando: {dep}")
                if self.run_command(
                    [sys.executable, "-m", "pip", "install", dep, "-q"],
                    f"pip install {dep}"
                ):
                    self.write_log(f"  ✓ {dep} instalado")
                else:
                    self.write_log(f"  ⚠ Erro ao instalar {dep}")

            time.sleep(0.3)

            # Passo 4: FFmpeg
            self.set_status("Configurando FFmpeg...")
            self.write_log("\n[4/6] Verificando FFmpeg")

            try:
                subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
                self.write_log("✓ FFmpeg já instalado")
            except:
                self.write_log("⚠ FFmpeg não encontrado")
                self.write_log("  O aplicativo tentará baixar automaticamente quando necessário")

            time.sleep(0.3)

            # Passo 5: Criar diretórios
            self.set_status("Configurando diretórios...")
            self.write_log("\n[5/6] Criando diretórios")

            download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Videos Baixados")
            os.makedirs(download_dir, exist_ok=True)
            self.write_log(f"✓ Pasta criada: {download_dir}")

            time.sleep(0.3)

            # Passo 6: Criar executável
            self.set_status("Criando executável...")
            self.write_log("\n[6/6] Criando executável (.exe)")
            self.write_log("  Isso pode levar 5-10 minutos...")

            # Instalar PyInstaller
            self.write_log("\n  Instalando PyInstaller...")
            if self.run_command(
                [sys.executable, "-m", "pip", "install", "pyinstaller", "-q"],
                "pip install pyinstaller"
            ):
                self.write_log("  ✓ PyInstaller instalado")

            time.sleep(0.3)

            # Executar build
            build_script = os.path.join(os.path.dirname(__file__), "build_executable.py")

            if os.path.exists(build_script):
                self.write_log("\n  Compilando aplicativo...")
                self.write_log("  Por favor, aguarde...")

                if self.run_command(
                    [sys.executable, build_script],
                    "Criando executável"
                ):
                    self.write_log("\n✓ EXECUTÁVEL CRIADO COM SUCESSO!")
                    self.write_log("📁 Local: Área de Trabalho/YouTubeDownloader/")
                else:
                    self.write_log("\n⚠ Erro ao criar executável")
                    self.write_log("  Você pode executar: python gui_app.py")
            else:
                self.write_log("⚠ build_executable.py não encontrado")

            # Finalizar
            self.write_log("\n" + "=" * 60)
            self.write_log("INSTALAÇÃO CONCLUÍDA!")
            self.write_log("=" * 60)
            self.write_log("\n✅ YouTube Downloader instalado com sucesso!")

            self.set_status("✓ Instalação concluída!")
            self.progress.stop()

            # Mostrar mensagem de sucesso
            self.root.after(500, self.show_complete)

        except Exception as e:
            self.write_log(f"\n✗ ERRO FATAL: {e}")
            self.write_log(f"   {type(e).__name__}")
            self.set_status("✗ Erro na instalação")
            self.progress.stop()
            messagebox.showerror("Erro", f"Erro durante instalação:\n{e}")

        finally:
            self.installing = False
            self.install_btn.config(state='normal', text="INSTALAR AGORA")

    def show_complete(self):
        """Mostrar mensagem de conclusão"""
        response = messagebox.askyesno(
            "Instalação Concluída!",
            "YouTube Downloader instalado com sucesso!\n\n"
            "Deseja abrir o aplicativo agora?",
            icon='info'
        )

        if response:
            try:
                gui_path = os.path.join(os.path.dirname(__file__), "gui_app.py")
                if os.path.exists(gui_path):
                    subprocess.Popen([sys.executable, gui_path])
                else:
                    desktop = os.path.join(os.path.expanduser("~"), "Desktop", "YouTubeDownloader", "YouTubeDownloader.exe")
                    if os.path.exists(desktop):
                        os.startfile(desktop)
                self.root.quit()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir: {e}")

    def run(self):
        """Executar janela"""
        self.root.mainloop()


if __name__ == "__main__":
    app = InstallerWindow()
    app.run()


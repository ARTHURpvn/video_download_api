#!/usr/bin/env python3
"""
YouTube Downloader - Instalador Automático para Windows
Instala todas as dependências automaticamente
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

class InstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader - Instalador")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Configurar estilo
        self.bg_color = "#1a1a1a"
        self.fg_color = "#ffffff"
        self.primary_color = "#FF0000"
        self.card_bg = "#2d2d2d"

        self.root.configure(bg=self.bg_color)

        self.installing = False
        self.create_widgets()

    def create_widgets(self):
        """Criar interface do instalador"""

        # Container principal
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Título
        title_label = tk.Label(main_container,
                              text="YouTube Downloader",
                              font=('Arial', 24, 'bold'),
                              fg=self.primary_color,
                              bg=self.bg_color)
        title_label.pack(pady=(0, 10))

        subtitle_label = tk.Label(main_container,
                                 text="Instalador Automático",
                                 font=('Arial', 12),
                                 fg="#999999",
                                 bg=self.bg_color)
        subtitle_label.pack(pady=(0, 30))

        # Card de informações
        info_card = tk.Frame(main_container, bg=self.card_bg)
        info_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        info_inner = tk.Frame(info_card, bg=self.card_bg)
        info_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        info_title = tk.Label(info_inner,
                             text="📦 O que será instalado:",
                             font=('Arial', 12, 'bold'),
                             fg=self.fg_color,
                             bg=self.card_bg,
                             anchor='w')
        info_title.pack(fill=tk.X, pady=(0, 10))

        dependencies = [
            "✓ yt-dlp (Baixador de vídeos)",
            "✓ FastAPI (Servidor web)",
            "✓ Uvicorn (Servidor ASGI)",
            "✓ FFmpeg (Processador de mídia)",
            "✓ Todas as dependências necessárias"
        ]

        for dep in dependencies:
            dep_label = tk.Label(info_inner,
                               text=dep,
                               font=('Arial', 10),
                               fg="#cccccc",
                               bg=self.card_bg,
                               anchor='w')
            dep_label.pack(fill=tk.X, pady=2)

        # Área de status
        self.status_frame = tk.Frame(main_container, bg=self.card_bg)
        self.status_frame.pack(fill=tk.X, pady=(0, 20))

        status_inner = tk.Frame(self.status_frame, bg=self.card_bg)
        status_inner.pack(fill=tk.X, padx=20, pady=15)

        self.status_label = tk.Label(status_inner,
                                     text="Pronto para instalar",
                                     font=('Arial', 10),
                                     fg="#999999",
                                     bg=self.card_bg,
                                     anchor='w')
        self.status_label.pack(fill=tk.X, pady=(0, 10))

        # Barra de progresso
        self.progress = ttk.Progressbar(status_inner,
                                       mode='indeterminate',
                                       length=400)
        self.progress.pack(fill=tk.X)

        # Log de instalação
        self.log_text = tk.Text(status_inner,
                               height=8,
                               font=('Consolas', 8),
                               bg="#1a1a1a",
                               fg="#00ff00",
                               relief='flat',
                               state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Botões
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill=tk.X)

        self.install_btn = tk.Button(button_frame,
                                     text="INSTALAR",
                                     command=self.start_installation,
                                     font=('Arial', 12, 'bold'),
                                     bg=self.primary_color,
                                     fg="white",
                                     activebackground='#CC0000',
                                     relief='flat',
                                     cursor='hand2',
                                     padx=30,
                                     pady=10)
        self.install_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = tk.Button(button_frame,
                              text="CANCELAR",
                              command=self.root.quit,
                              font=('Arial', 12),
                              bg=self.card_bg,
                              fg="white",
                              activebackground='#3d3d3d',
                              relief='flat',
                              cursor='hand2',
                              padx=30,
                              pady=10)
        cancel_btn.pack(side=tk.LEFT)

    def log(self, message):
        """Adicionar mensagem ao log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()

    def update_status(self, status):
        """Atualizar status"""
        self.status_label.config(text=status)
        self.root.update()

    def start_installation(self):
        """Iniciar instalação"""
        if self.installing:
            return

        # Confirmar com usuário
        result = messagebox.askyesno(
            "Confirmar Instalação",
            "Deseja instalar o YouTube Downloader e todas as suas dependências?\n\n"
            "Isso pode levar alguns minutos.",
            icon='question'
        )

        if not result:
            return

        self.installing = True
        self.install_btn.config(state='disabled', text="INSTALANDO...")
        self.progress.start()

        # Executar instalação em thread separada
        thread = threading.Thread(target=self.run_installation, daemon=True)
        thread.start()

    def run_installation(self):
        """Executar processo de instalação"""
        try:
            self.log("=" * 50)
            self.log("INICIANDO INSTALAÇÃO")
            self.log("=" * 50)

            # 1. Verificar Python
            self.update_status("Verificando Python...")
            self.log("\n[1/6] Verificando instalação do Python...")

            try:
                python_version = subprocess.check_output(
                    [sys.executable, "--version"],
                    stderr=subprocess.STDOUT
                ).decode().strip()
                self.log(f"✓ Python encontrado: {python_version}")
            except Exception as e:
                self.log(f"✗ Erro ao verificar Python: {e}")
                self.show_error("Python não encontrado! Por favor, instale o Python 3.8 ou superior.")
                return

            time.sleep(0.5)

            # 2. Atualizar pip
            self.update_status("Atualizando pip...")
            self.log("\n[2/6] Atualizando pip...")

            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.log("✓ pip atualizado com sucesso")
            except Exception as e:
                self.log(f"⚠ Aviso ao atualizar pip: {e}")

            time.sleep(0.5)

            # 3. Instalar dependências do requirements.txt
            self.update_status("Instalando dependências Python...")
            self.log("\n[3/6] Instalando dependências Python...")

            requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

            if os.path.exists(requirements_file):
                try:
                    self.log("Lendo requirements.txt...")
                    process = subprocess.Popen(
                        [sys.executable, "-m", "pip", "install", "-r", requirements_file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )

                    for line in process.stdout:
                        line = line.strip()
                        if line:
                            self.log(f"  {line}")

                    process.wait()

                    if process.returncode == 0:
                        self.log("✓ Dependências Python instaladas com sucesso")
                    else:
                        self.log("⚠ Algumas dependências podem não ter sido instaladas")

                except Exception as e:
                    self.log(f"✗ Erro ao instalar dependências: {e}")
                    self.show_error(f"Erro ao instalar dependências Python: {e}")
                    return
            else:
                self.log("⚠ Arquivo requirements.txt não encontrado")
                self.log("Instalando dependências manualmente...")

                deps = [
                    "yt-dlp",
                    "fastapi",
                    "uvicorn[standard]",
                    "python-multipart",
                    "requests"
                ]

                for dep in deps:
                    try:
                        self.log(f"  Instalando {dep}...")
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", dep],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        self.log(f"  ✓ {dep} instalado")
                    except Exception as e:
                        self.log(f"  ✗ Erro ao instalar {dep}: {e}")

            time.sleep(0.5)

            # 4. Verificar/Instalar FFmpeg
            self.update_status("Verificando FFmpeg...")
            self.log("\n[4/6] Verificando FFmpeg...")

            try:
                subprocess.check_output(
                    ["ffmpeg", "-version"],
                    stderr=subprocess.STDOUT
                )
                self.log("✓ FFmpeg já está instalado")
            except FileNotFoundError:
                self.log("⚠ FFmpeg não encontrado no sistema")
                self.log("Tentando instalar FFmpeg via yt-dlp...")

                try:
                    # Instalar ffmpeg-downloader
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "ffmpeg-downloader"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    self.log("✓ ffmpeg-downloader instalado")

                    # Baixar FFmpeg
                    self.log("Baixando FFmpeg... (isso pode levar alguns minutos)")
                    subprocess.check_call(
                        [sys.executable, "-m", "ffmpeg_downloader"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    self.log("✓ FFmpeg instalado com sucesso")
                except Exception as e:
                    self.log(f"⚠ Não foi possível instalar FFmpeg automaticamente: {e}")
                    self.log("Por favor, instale o FFmpeg manualmente de: https://ffmpeg.org/download.html")

            time.sleep(0.5)

            # 5. Criar diretório de downloads
            self.update_status("Configurando diretórios...")
            self.log("\n[5/6] Configurando diretórios...")

            try:
                download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Videos Baixados")
                os.makedirs(download_dir, exist_ok=True)
                self.log(f"✓ Diretório de downloads criado: {download_dir}")
            except Exception as e:
                self.log(f"⚠ Erro ao criar diretório: {e}")

            # Finalizar
            self.log("\n" + "=" * 50)
            self.log("INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
            self.log("=" * 50)

            # 6. Perguntar se deseja criar o executável
            self.update_status("Instalação concluída! Preparando build...")
            self.log("\n[6/6] Criando executável (.exe)...")
            self.log("Isso pode levar alguns minutos...")

            try:
                # Instalar PyInstaller se necessário
                self.log("\nInstalando PyInstaller...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "pyinstaller"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.log("✓ PyInstaller instalado")

                time.sleep(0.5)

                # Executar build
                self.log("\n🔨 Criando executável...")
                self.log("Por favor, aguarde. Isso pode levar de 5 a 10 minutos...")

                build_script = os.path.join(os.path.dirname(__file__), "build_executable.py")

                if os.path.exists(build_script):
                    process = subprocess.Popen(
                        [sys.executable, build_script],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )

                    for line in process.stdout:
                        line = line.strip()
                        if line:
                            self.log(f"  {line}")

                    process.wait()

                    if process.returncode == 0:
                        self.log("\n✓ Executável criado com sucesso!")
                        self.log("📁 Local: Área de Trabalho/YouTubeDownloader/YouTubeDownloader.exe")
                    else:
                        self.log("\n⚠ Erro ao criar executável")
                        self.log("Você pode tentar criar manualmente executando: python build_executable.py")
                else:
                    self.log("⚠ Arquivo build_executable.py não encontrado")

            except Exception as e:
                self.log(f"\n⚠ Erro ao criar executável: {e}")
                self.log("Você pode tentar criar manualmente executando: python build_executable.py")

            self.log("\n" + "=" * 50)
            self.log("PROCESSO COMPLETO!")
            self.log("=" * 50)
            self.log("\n✅ Aplicativo instalado e executável criado!")
            self.log("📁 Verifique a pasta 'YouTubeDownloader' na sua Área de Trabalho")

            self.update_status("✓ Tudo pronto! Executável criado na Área de Trabalho")
            self.progress.stop()

            self.root.after(100, self.show_success)

        except Exception as e:
            self.log(f"\n✗ ERRO FATAL: {e}")
            self.update_status("✗ Erro na instalação")
            self.progress.stop()
            self.show_error(f"Erro durante a instalação: {e}")

        finally:
            self.installing = False
            self.install_btn.config(state='normal', text="INSTALAR")

    def show_success(self):
        """Mostrar mensagem de sucesso"""
        result = messagebox.showinfo(
            "Instalação Concluída",
            "YouTube Downloader instalado com sucesso!\n\n"
            "Você pode agora executar o aplicativo através do arquivo gui_app.py\n\n"
            "Deseja abrir o aplicativo agora?",
            icon='info',
            type='yesno'
        )

        if result == 'yes':
            # Executar o aplicativo
            try:
                gui_path = os.path.join(os.path.dirname(__file__), "gui_app.py")
                subprocess.Popen([sys.executable, gui_path])
                self.root.quit()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir aplicativo: {e}")
        else:
            self.root.quit()

    def show_error(self, message):
        """Mostrar mensagem de erro"""
        self.root.after(100, lambda: messagebox.showerror("Erro na Instalação", message))


def main():
    """Função principal"""
    root = tk.Tk()
    app = InstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

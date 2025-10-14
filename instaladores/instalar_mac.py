#!/usr/bin/env python3
"""
YouTube Downloader - Instalador para macOS
Instala dependências e cria aplicativo na Área de Trabalho
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import threading
import time

class InstaladorMac:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("YouTube Downloader - Instalador macOS")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")
        self.installing = False
        self.create_ui()

    def create_ui(self):
        main = tk.Frame(self.root, bg="#1a1a1a")
        main.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        tk.Label(main, text="YouTube Downloader", font=('Arial', 26, 'bold'),
                fg="#FF0000", bg="#1a1a1a").pack(pady=(0, 5))
        tk.Label(main, text="Instalador para macOS", font=('Arial', 11),
                fg="#999", bg="#1a1a1a").pack(pady=(0, 20))

        self.status_lbl = tk.Label(main, text="✓ Pronto para instalar",
                                   font=('Arial', 11, 'bold'),
                                   fg="#fff", bg="#1a1a1a")
        self.status_lbl.pack(pady=(0, 10))

        self.progressbar = ttk.Progressbar(main, mode='indeterminate', length=550)
        self.progressbar.pack(pady=(0, 15))

        log_frame = tk.Frame(main, bg="#2d2d2d")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.log = scrolledtext.ScrolledText(log_frame, height=15, width=75,
            font=('Monaco', 9), bg="#000", fg="#0f0", wrap=tk.WORD, state='disabled')
        self.log.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        btns = tk.Frame(main, bg="#1a1a1a")
        btns.pack(fill=tk.X)

        self.btn_install = tk.Button(btns, text="▶ INSTALAR AGORA",
            command=self.on_install_click, font=('Arial', 12, 'bold'),
            bg="#FF0000", fg="white", relief='flat', cursor='hand2', padx=35, pady=12)
        self.btn_install.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(btns, text="✕ SAIR", command=self.root.quit,
            font=('Arial', 12), bg="#2d2d2d", fg="white", relief='flat',
            cursor='hand2', padx=35, pady=12).pack(side=tk.LEFT)

    def write(self, text):
        self.log.config(state='normal')
        self.log.insert(tk.END, text + '\n')
        self.log.see(tk.END)
        self.log.config(state='disabled')
        self.root.update_idletasks()

    def status(self, text):
        self.status_lbl.config(text=text)
        self.root.update_idletasks()

    def on_install_click(self):
        if self.installing:
            return
        if not messagebox.askyesno("Confirmar",
            "Instalar YouTube Downloader?\n\nIsso levará 5-10 minutos."):
            return
        self.installing = True
        self.btn_install.config(state='disabled', text="⏳ INSTALANDO...")
        self.progressbar.start(8)
        threading.Thread(target=self.install, daemon=True).start()

    def exec_cmd(self, cmd):
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1,
                shell=isinstance(cmd, str))
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
        try:
            self.write("═" * 65)
            self.write("  INSTALAÇÃO DO YOUTUBE DOWNLOADER")
            self.write("═" * 65)

            self.status("⏳ [1/6] Verificando Python...")
            self.write("\n[1/6] Verificando Python")
            ver = subprocess.check_output([sys.executable, "--version"],
                stderr=subprocess.STDOUT).decode().strip()
            self.write(f"✓ {ver}")
            time.sleep(0.3)

            self.status("⏳ [2/6] Atualizando pip...")
            self.write("\n[2/6] Atualizando pip")
            self.exec_cmd([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
            time.sleep(0.3)

            self.status("⏳ [3/6] Instalando dependências...")
            self.write("\n[3/6] Instalando dependências")
            packages = ["yt-dlp", "fastapi", "uvicorn[standard]",
                       "python-multipart", "requests", "pydantic", "pyinstaller"]
            for pkg in packages:
                self.write(f"  → {pkg}")
                self.exec_cmd([sys.executable, "-m", "pip", "install", pkg, "-q"])
            time.sleep(0.3)

            self.status("⏳ [4/6] Verificando FFmpeg...")
            self.write("\n[4/6] Verificando FFmpeg")
            try:
                subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
                self.write("✓ FFmpeg instalado")
            except:
                self.write("⚠ FFmpeg não encontrado (instale: brew install ffmpeg)")
            time.sleep(0.3)

            self.status("⏳ [5/6] Criando diretórios...")
            self.write("\n[5/6] Configurando diretórios")
            dl_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Videos Baixados")
            os.makedirs(dl_dir, exist_ok=True)
            self.write(f"✓ {dl_dir}")
            time.sleep(0.3)

            self.status("⏳ [6/6] Compilando aplicativo...")
            self.write("\n[6/6] Compilando aplicativo (aguarde 5-10 min)")
            build_file = os.path.join(os.path.dirname(__file__), "..", "build_executable.py")
            if self.exec_cmd([sys.executable, build_file]):
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                app_path = os.path.join(desktop, "YouTubeDownloader")
                if os.path.exists(app_path):
                    self.write(f"\n✓✓✓ APLICATIVO CRIADO! ✓✓✓")
                    self.write(f"📁 Local: {app_path}")

            self.write("\n" + "═" * 65)
            self.write("  ✅ INSTALAÇÃO CONCLUÍDA!")
            self.write("═" * 65)
            self.write("\nVá até sua Área de Trabalho e abra YouTubeDownloader")

            self.status("✓ Instalação completa!")
            self.progressbar.stop()
            self.root.after(500, self.show_done)

        except Exception as e:
            self.write(f"\n✗ ERRO: {e}")
            self.status("✗ Erro na instalação")
            self.progressbar.stop()
        finally:
            self.installing = False
            self.btn_install.config(state='normal', text="▶ INSTALAR AGORA")

    def show_done(self):
        if messagebox.askyesno("Concluído!",
            "Instalação concluída!\n\nAbrir aplicativo agora?"):
            try:
                app = os.path.join(os.path.expanduser("~"), "Desktop", "YouTubeDownloader")
                if os.path.exists(app):
                    subprocess.Popen(["open", app])
                self.root.quit()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InstaladorMac()
    app.run()


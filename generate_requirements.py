#!/usr/bin/env python3
"""Script para gerar requirements.txt completo do ambiente virtual"""

import subprocess
import sys
from pathlib import Path

def generate_requirements():
    """Gera requirements.txt com todas as dependências instaladas"""

    print("📦 Capturando dependências do ambiente virtual...")

    try:
        # Executar pip freeze para pegar todas as dependências
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'freeze'],
            capture_output=True,
            text=True,
            check=True
        )

        requirements = result.stdout

        # Salvar no requirements.txt
        requirements_path = Path('requirements.txt')
        requirements_path.write_text(requirements)

        print(f"✅ requirements.txt atualizado com sucesso!")
        print(f"📝 Total de pacotes: {len(requirements.strip().split(chr(10)))}")
        print(f"\n📄 Conteúdo salvo em: {requirements_path.absolute()}")

        # Mostrar preview
        print("\n📋 Preview das primeiras linhas:")
        print("-" * 50)
        lines = requirements.strip().split('\n')
        for line in lines[:10]:
            print(f"  {line}")
        if len(lines) > 10:
            print(f"  ... e mais {len(lines) - 10} pacotes")
        print("-" * 50)

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar pip freeze: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_requirements()


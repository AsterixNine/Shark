#!/usr/bin/env python3
"""
SHARK UPDATER - Atualiza o Shark para a versao mais recente do GitHub
"""

import os
import sys
import json
import shutil
import tempfile
import platform
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACAO
# ═══════════════════════════════════════════════════════════════════════════════

# URL do repositorio (altere para o seu)
GITHUB_USER = "seuusuario"
GITHUB_REPO = "shark"
GITHUB_BRANCH = "main"

# URLs
RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}"
RELEASES_URL = f"{API_URL}/releases/latest"

# Arquivos para atualizar
FILES_TO_UPDATE = [
    "shark.py",
    "shark_update.py",
]

# Versao atual (sera lida do shark.py)
VERSION_FILE = Path(__file__).parent / "shark.py"
CURRENT_VERSION = "2.0.0"

# Cores ANSI
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    
    @staticmethod
    def hex(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{r};{g};{b}m"


# Habilita cores no Windows
def enable_colors():
    if platform.system().lower() == 'windows':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass

enable_colors()


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCOES DE ATUALIZACAO
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Exibe banner do updater"""
    banner = f"""
{Colors.CYAN}{'='*60}{Colors.RESET}
{Colors.BOLD}  SHARK UPDATER{Colors.RESET}
{Colors.DIM}  Atualizador automatico via GitHub{Colors.RESET}
{Colors.CYAN}{'='*60}{Colors.RESET}
"""
    print(banner)


def get_local_version():
    """Obtem versao local do shark.py"""
    try:
        if VERSION_FILE.exists():
            content = VERSION_FILE.read_text(encoding='utf-8')
            # Procura por VERSION = "x.x.x" ou version = "x.x.x"
            for line in content.split('\n'):
                if 'VERSION' in line.upper() and '=' in line:
                    parts = line.split('=')
                    if len(parts) >= 2:
                        version = parts[1].strip().strip('"\'')
                        return version
        return CURRENT_VERSION
    except:
        return CURRENT_VERSION


def get_remote_version():
    """Obtem versao mais recente do GitHub"""
    try:
        # Tenta obter da release mais recente
        req = Request(RELEASES_URL, headers={'User-Agent': 'Shark-Updater'})
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('tag_name', '').lstrip('v'), data.get('html_url', '')
    except:
        pass
    
    # Fallback: tenta ler do arquivo remoto
    try:
        url = f"{RAW_URL}/shark.py"
        req = Request(url, headers={'User-Agent': 'Shark-Updater'})
        with urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            for line in content.split('\n'):
                if 'VERSION' in line.upper() and '=' in line:
                    parts = line.split('=')
                    if len(parts) >= 2:
                        version = parts[1].strip().strip('"\'')
                        return version, None
    except:
        pass
    
    return None, None


def download_file(filename):
    """Baixa um arquivo do GitHub"""
    url = f"{RAW_URL}/{filename}"
    
    try:
        req = Request(url, headers={'User-Agent': 'Shark-Updater'})
        with urlopen(req, timeout=30) as response:
            return response.read()
    except HTTPError as e:
        print(f"  {Colors.RED}[X] Erro HTTP {e.code}: {filename}{Colors.RESET}")
        return None
    except URLError as e:
        print(f"  {Colors.RED}[X] Erro de conexao: {e.reason}{Colors.RESET}")
        return None
    except Exception as e:
        print(f"  {Colors.RED}[X] Erro: {e}{Colors.RESET}")
        return None


def backup_file(filepath):
    """Cria backup de um arquivo"""
    if filepath.exists():
        backup_path = filepath.with_suffix(filepath.suffix + '.backup')
        shutil.copy2(filepath, backup_path)
        return backup_path
    return None


def restore_backup(filepath):
    """Restaura arquivo do backup"""
    backup_path = filepath.with_suffix(filepath.suffix + '.backup')
    if backup_path.exists():
        shutil.copy2(backup_path, filepath)
        backup_path.unlink()
        return True
    return False


def update_file(filename, content):
    """Atualiza um arquivo com novo conteudo"""
    filepath = Path(__file__).parent / filename
    
    # Cria backup
    backup = backup_file(filepath)
    
    try:
        # Escreve novo conteudo
        filepath.write_bytes(content)
        
        # Remove backup se sucesso
        if backup and backup.exists():
            backup.unlink()
        
        return True
    except Exception as e:
        # Restaura backup em caso de erro
        if backup:
            restore_backup(filepath)
        print(f"  {Colors.RED}[X] Erro ao atualizar {filename}: {e}{Colors.RESET}")
        return False


def check_for_updates():
    """Verifica se ha atualizacoes disponiveis"""
    print(f"\n  {Colors.CYAN}Verificando atualizacoes...{Colors.RESET}\n")
    
    local_version = get_local_version()
    remote_version, release_url = get_remote_version()
    
    print(f"  Versao local:  {Colors.YELLOW}{local_version}{Colors.RESET}")
    
    if remote_version:
        print(f"  Versao remota: {Colors.GREEN}{remote_version}{Colors.RESET}")
        
        # Compara versoes (simples)
        if remote_version != local_version:
            print(f"\n  {Colors.GREEN}[!] Nova versao disponivel!{Colors.RESET}")
            if release_url:
                print(f"  {Colors.DIM}{release_url}{Colors.RESET}")
            return True, remote_version
        else:
            print(f"\n  {Colors.GREEN}[V] Shark esta atualizado!{Colors.RESET}")
            return False, local_version
    else:
        print(f"  {Colors.RED}[X] Nao foi possivel verificar versao remota{Colors.RESET}")
        return None, local_version


def perform_update():
    """Executa a atualizacao"""
    print(f"\n  {Colors.CYAN}Baixando atualizacoes...{Colors.RESET}\n")
    
    success_count = 0
    fail_count = 0
    
    for filename in FILES_TO_UPDATE:
        print(f"  [{Colors.CYAN}...{Colors.RESET}] {filename}", end="", flush=True)
        
        content = download_file(filename)
        
        if content:
            if update_file(filename, content):
                print(f"\r  [{Colors.GREEN} V {Colors.RESET}] {filename}")
                success_count += 1
            else:
                print(f"\r  [{Colors.RED} X {Colors.RESET}] {filename}")
                fail_count += 1
        else:
            print(f"\r  [{Colors.RED} X {Colors.RESET}] {filename}")
            fail_count += 1
    
    return success_count, fail_count


def update_from_git():
    """Atualiza usando git pull (se estiver em um repositorio git)"""
    shark_dir = Path(__file__).parent
    git_dir = shark_dir / ".git"
    
    if not git_dir.exists():
        return False
    
    print(f"\n  {Colors.CYAN}Atualizando via git...{Colors.RESET}\n")
    
    try:
        import subprocess
        
        # git fetch
        result = subprocess.run(
            ["git", "fetch", "origin"],
            cwd=shark_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  {Colors.RED}[X] Erro no git fetch{Colors.RESET}")
            return False
        
        # git pull
        result = subprocess.run(
            ["git", "pull", "origin", GITHUB_BRANCH],
            cwd=shark_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"  {Colors.GREEN}[V] Atualizado via git!{Colors.RESET}")
            if result.stdout.strip():
                print(f"\n{Colors.DIM}{result.stdout}{Colors.RESET}")
            return True
        else:
            print(f"  {Colors.RED}[X] Erro no git pull{Colors.RESET}")
            if result.stderr:
                print(f"  {Colors.DIM}{result.stderr}{Colors.RESET}")
            return False
            
    except FileNotFoundError:
        print(f"  {Colors.YELLOW}[!] Git nao encontrado, usando download direto{Colors.RESET}")
        return False
    except Exception as e:
        print(f"  {Colors.RED}[X] Erro: {e}{Colors.RESET}")
        return False


def interactive_update():
    """Atualizacao interativa"""
    print_banner()
    
    # Verifica atualizacoes
    has_update, version = check_for_updates()
    
    if has_update is None:
        print(f"\n  {Colors.YELLOW}Nao foi possivel verificar. Tentar atualizar mesmo assim?{Colors.RESET}")
        choice = input(f"\n  {Colors.hex('#00FF88')}Atualizar? (s/n):{Colors.RESET} ").strip().lower()
        if choice != 's':
            return
    elif has_update is False:
        choice = input(f"\n  {Colors.hex('#00FF88')}Forcar atualizacao? (s/n):{Colors.RESET} ").strip().lower()
        if choice != 's':
            print(f"\n  {Colors.DIM}Nenhuma acao necessaria.{Colors.RESET}\n")
            return
    else:
        choice = input(f"\n  {Colors.hex('#00FF88')}Atualizar agora? (s/n):{Colors.RESET} ").strip().lower()
        if choice != 's':
            print(f"\n  {Colors.YELLOW}Atualizacao cancelada.{Colors.RESET}\n")
            return
    
    # Tenta git primeiro
    shark_dir = Path(__file__).parent
    if (shark_dir / ".git").exists():
        if update_from_git():
            print(f"""
{Colors.GREEN}{'='*60}{Colors.RESET}
  Atualizacao concluida via Git!
{Colors.GREEN}{'='*60}{Colors.RESET}
""")
            return
    
    # Fallback: download direto
    success, fail = perform_update()
    
    if fail == 0:
        print(f"""
{Colors.GREEN}{'='*60}{Colors.RESET}
  Atualizacao concluida!
  
  Arquivos atualizados: {success}
  
  {Colors.BOLD}Reinicie o terminal para aplicar.{Colors.RESET}
{Colors.GREEN}{'='*60}{Colors.RESET}
""")
    else:
        print(f"""
{Colors.YELLOW}{'='*60}{Colors.RESET}
  Atualizacao parcial.
  
  Sucesso: {success}
  Falha:   {fail}
{Colors.YELLOW}{'='*60}{Colors.RESET}
""")


def silent_update():
    """Atualizacao silenciosa (para uso em scripts)"""
    has_update, _ = check_for_updates()
    
    if has_update:
        # Tenta git
        shark_dir = Path(__file__).parent
        if (shark_dir / ".git").exists():
            if update_from_git():
                return True
        
        # Download direto
        success, fail = perform_update()
        return fail == 0
    
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcao principal"""
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd in ("--check", "-c", "check"):
            print_banner()
            check_for_updates()
        
        elif cmd in ("--force", "-f", "force"):
            print_banner()
            print(f"\n  {Colors.YELLOW}Forcando atualizacao...{Colors.RESET}")
            
            shark_dir = Path(__file__).parent
            if (shark_dir / ".git").exists():
                if update_from_git():
                    print(f"\n  {Colors.GREEN}Concluido!{Colors.RESET}\n")
                    return
            
            success, fail = perform_update()
            if fail == 0:
                print(f"\n  {Colors.GREEN}Concluido! {success} arquivos atualizados.{Colors.RESET}\n")
            else:
                print(f"\n  {Colors.YELLOW}Parcial: {success} ok, {fail} falhas.{Colors.RESET}\n")
        
        elif cmd in ("--silent", "-s", "silent"):
            if silent_update():
                sys.exit(0)
            else:
                sys.exit(1)
        
        elif cmd in ("--help", "-h", "help"):
            print(f"""
{Colors.CYAN}SHARK UPDATER{Colors.RESET}

{Colors.BOLD}Uso:{Colors.RESET}
  python shark_update.py              Atualizacao interativa
  python shark_update.py check        Verifica atualizacoes
  python shark_update.py force        Forca atualizacao
  python shark_update.py silent       Atualizacao silenciosa

{Colors.BOLD}Configuracao:{Colors.RESET}
  Edite as variaveis GITHUB_USER e GITHUB_REPO no inicio
  do arquivo para apontar para seu repositorio.

{Colors.BOLD}Repositorio:{Colors.RESET}
  {GITHUB_USER}/{GITHUB_REPO} (branch: {GITHUB_BRANCH})
""")
        
        else:
            print(f"{Colors.RED}Comando desconhecido. Use --help{Colors.RESET}")
    
    else:
        interactive_update()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🦈 SHARK - Sistema de Personalização Total para Terminais
Personalize ABSOLUTAMENTE TUDO no seu terminal!
"""

import os
import sys
import json
import platform
from pathlib import Path

# Detecta o sistema operacional
SYSTEM = platform.system().lower()
IS_TERMUX = os.environ.get('TERMUX_VERSION') is not None

# Diretório de configuração
if IS_TERMUX:
    CONFIG_DIR = Path.home() / ".shark"
elif SYSTEM == "windows":
    CONFIG_DIR = Path(os.environ.get('APPDATA', '')) / "Shark"
else:
    CONFIG_DIR = Path.home() / ".config" / "shark"

CONFIG_FILE = CONFIG_DIR / "config.json"
THEMES_DIR = CONFIG_DIR / "themes"
BANNERS_DIR = CONFIG_DIR / "banners"


class Colors:
    """Sistema de cores ANSI - Personalize TUDO!"""
    
    # Reset
    RESET = "\033[0m"
    
    # Cores básicas
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Cores brilhantes
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Estilos
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    
    @staticmethod
    def rgb(r, g, b, bg=False):
        """Cor RGB customizada (256 cores)"""
        return f"\033[{'48' if bg else '38'};2;{r};{g};{b}m"
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Converte HEX para RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def hex(hex_color, bg=False):
        """Cor HEX customizada"""
        r, g, b = Colors.hex_to_rgb(hex_color)
        return Colors.rgb(r, g, b, bg)


class Banners:
    """Banners ASCII épicos!"""
    
    SHARK = r"""
   _____ _    _          _____  _  __
  / ____| |  | |   /\   |  __ \| |/ /
 | (___ | |__| |  /  \  | |__) | ' / 
  \___ \|  __  | / /\ \ |  _  /|  <  
  ____) | |  | |/ ____ \| | \ \| . \ 
 |_____/|_|  |_/_/    \_\_|  \_\_|\_\
    """
    
    SHARK_MINI = r"""
  █▀ █░█ ▄▀█ █▀█ █▄▀
  ▄█ █▀█ █▀█ █▀▄ █░█
    """
    
    SHARK_WAVE = r"""
    ~^~^~^~^~^~^~^~^~^~^~^~^~^~
    🦈  S H A R K  🦈
    ~^~^~^~^~^~^~^~^~^~^~^~^~^~
    """
    
    @staticmethod
    def gradient_text(text, start_color, end_color):
        """Aplica gradiente de cores no texto"""
        start_r, start_g, start_b = Colors.hex_to_rgb(start_color)
        end_r, end_g, end_b = Colors.hex_to_rgb(end_color)
        
        result = ""
        length = len(text.replace('\n', ''))
        char_count = 0
        
        for char in text:
            if char == '\n':
                result += char
                continue
            
            ratio = char_count / max(length - 1, 1)
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            
            result += f"{Colors.rgb(r, g, b)}{char}"
            char_count += 1
        
        return result + Colors.RESET


class ProgressBar:
    """Barras de progresso customizáveis"""
    
    STYLES = {
        "default": ("█", "░"),
        "shark": ("🦈", "~"),
        "arrows": ("▶", "▷"),
        "blocks": ("■", "□"),
        "dots": ("●", "○"),
        "lines": ("━", "─"),
    }
    
    @staticmethod
    def render(progress, total, width=40, style="default", color="#00BFFF"):
        """Renderiza barra de progresso"""
        fill_char, empty_char = ProgressBar.STYLES.get(style, ProgressBar.STYLES["default"])
        
        percentage = progress / total
        filled = int(width * percentage)
        empty = width - filled
        
        bar = fill_char * filled + empty_char * empty
        percent_text = f"{percentage * 100:.1f}%"
        
        return f"{Colors.hex(color)}[{bar}] {percent_text}{Colors.RESET}"


class Prompt:
    """Sistema de prompt customizável"""
    
    TEMPLATES = {
        "minimal": "{user}@{host} {cwd} $ ",
        "shark": "🦈 {cwd} ❯ ",
        "powerline": "{user}  {cwd}  ",
        "arrow": "╭─[{user}@{host}]─[{cwd}]\n╰─➤ ",
        "simple": "{cwd} > ",
    }
    
    @staticmethod
    def render(template_name="shark", custom_template=None, colors=None):
        """Renderiza o prompt"""
        import getpass
        import socket
        
        template = custom_template or Prompt.TEMPLATES.get(template_name, Prompt.TEMPLATES["shark"])
        
        variables = {
            "user": getpass.getuser(),
            "host": socket.gethostname(),
            "cwd": os.getcwd().replace(str(Path.home()), "~"),
            "system": SYSTEM,
        }
        
        return template.format(**variables)


class Config:
    """Gerenciador de configuração"""
    
    DEFAULT_CONFIG = {
        "theme": "shark",
        "banner": "SHARK",
        "banner_colors": ["#00BFFF", "#0080FF"],
        "prompt_style": "shark",
        "prompt_color": "#00BFFF",
        "progress_style": "default",
        "show_banner_on_start": True,
    }
    
    @staticmethod
    def ensure_dirs():
        """Cria diretórios necessários"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        THEMES_DIR.mkdir(parents=True, exist_ok=True)
        BANNERS_DIR.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def load():
        """Carrega configuração"""
        Config.ensure_dirs()
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return {**Config.DEFAULT_CONFIG, **json.load(f)}
        return Config.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save(config):
        """Salva configuração"""
        Config.ensure_dirs()
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)


class Shark:
    """🦈 Classe principal do Shark"""
    
    def __init__(self):
        self.config = Config.load()
        self.colors = Colors()
        self.banners = Banners()
    
    def show_banner(self):
        """Exibe o banner com gradiente"""
        banner_name = self.config.get("banner", "SHARK")
        banner = getattr(Banners, banner_name, Banners.SHARK)
        colors = self.config.get("banner_colors", ["#00BFFF", "#0080FF"])
        
        print(Banners.gradient_text(banner, colors[0], colors[1]))
    
    def print_colored(self, text, color="#00BFFF", style=""):
        """Imprime texto colorido"""
        style_code = getattr(Colors, style.upper(), "") if style else ""
        print(f"{style_code}{Colors.hex(color)}{text}{Colors.RESET}")
    
    def clear_screen(self):
        """Limpa a tela"""
        os.system('cls' if SYSTEM == 'windows' else 'clear')
    
    def get_prompt(self):
        """Retorna o prompt customizado"""
        style = self.config.get("prompt_style", "shark")
        color = self.config.get("prompt_color", "#00BFFF")
        prompt = Prompt.render(style)
        return f"{Colors.hex(color)}{prompt}{Colors.RESET}"
    
    def progress_demo(self):
        """Demonstração de barras de progresso"""
        import time
        
        print(f"\n{Colors.BOLD}Estilos de barra de progresso:{Colors.RESET}\n")
        
        for style in ProgressBar.STYLES.keys():
            print(f"  {style:10} ", end="")
            print(ProgressBar.render(75, 100, width=30, style=style))
        
        print(f"\n{Colors.BOLD}Animação:{Colors.RESET}\n")
        for i in range(101):
            print(f"\r  {ProgressBar.render(i, 100, width=40, style='shark', color='#00FF88')}", end="")
            time.sleep(0.02)
        print()
    
    def interactive_menu(self):
        """Menu interativo principal"""
        self.clear_screen()
        self.show_banner()
        
        menu = f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════{Colors.RESET}
{Colors.BRIGHT_WHITE}  🦈 SHARK - Personalize TUDO!{Colors.RESET}
{Colors.CYAN}═══════════════════════════════════════════════{Colors.RESET}

  {Colors.hex("#00BFFF")}[1]{Colors.RESET} Mudar tema de cores
  {Colors.hex("#00BFFF")}[2]{Colors.RESET} Personalizar banner
  {Colors.hex("#00BFFF")}[3]{Colors.RESET} Configurar prompt
  {Colors.hex("#00BFFF")}[4]{Colors.RESET} Estilos de barra de progresso
  {Colors.hex("#00BFFF")}[5]{Colors.RESET} Ver configuração atual
  {Colors.hex("#00BFFF")}[6]{Colors.RESET} Demonstração de cores
  {Colors.hex("#00BFFF")}[0]{Colors.RESET} Sair

{Colors.CYAN}═══════════════════════════════════════════════{Colors.RESET}
"""
        print(menu)
        
        try:
            choice = input(f"  {Colors.hex('#00FF88')}Escolha uma opção:{Colors.RESET} ")
            
            if choice == "1":
                self.theme_menu()
            elif choice == "2":
                self.banner_menu()
            elif choice == "3":
                self.prompt_menu()
            elif choice == "4":
                self.progress_demo()
                input("\n  Pressione Enter para continuar...")
                self.interactive_menu()
            elif choice == "5":
                self.show_config()
            elif choice == "6":
                self.color_demo()
            elif choice == "0":
                self.print_colored("\n  🦈 Até mais! Shark out! 🌊\n", "#00BFFF")
                sys.exit(0)
            else:
                self.interactive_menu()
                
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}  Operação cancelada.{Colors.RESET}")
            sys.exit(0)
    
    def theme_menu(self):
        """Menu de temas"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  Temas disponíveis:{Colors.RESET}\n")
        
        themes = {
            "1": ("Shark (Azul)", "#00BFFF", "#0080FF"),
            "2": ("Ocean (Verde-azul)", "#00CED1", "#20B2AA"),
            "3": ("Fire (Vermelho)", "#FF4500", "#FF6347"),
            "4": ("Matrix (Verde)", "#00FF00", "#32CD32"),
            "5": ("Purple Rain", "#9400D3", "#8A2BE2"),
            "6": ("Sunset", "#FF6B6B", "#FFE66D"),
        }
        
        for key, (name, c1, c2) in themes.items():
            gradient = Banners.gradient_text(f"███████ {name}", c1, c2)
            print(f"  [{key}] {gradient}")
        
        choice = input(f"\n  {Colors.hex('#00FF88')}Escolha um tema:{Colors.RESET} ")
        
        if choice in themes:
            _, c1, c2 = themes[choice]
            self.config["banner_colors"] = [c1, c2]
            self.config["prompt_color"] = c1
            Config.save(self.config)
            print(f"\n  {Colors.GREEN}✓ Tema aplicado!{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def banner_menu(self):
        """Menu de banners"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  Banners disponíveis:{Colors.RESET}\n")
        
        banners = ["SHARK", "SHARK_MINI", "SHARK_WAVE"]
        for i, name in enumerate(banners, 1):
            banner = getattr(Banners, name)
            colors = self.config.get("banner_colors", ["#00BFFF", "#0080FF"])
            print(f"  [{i}] {name}")
            print(Banners.gradient_text(banner, colors[0], colors[1]))
        
        choice = input(f"\n  {Colors.hex('#00FF88')}Escolha um banner:{Colors.RESET} ")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(banners):
                self.config["banner"] = banners[idx]
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Banner atualizado!{Colors.RESET}")
        except ValueError:
            pass
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def prompt_menu(self):
        """Menu de prompts"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  Estilos de Prompt:{Colors.RESET}\n")
        
        for i, (name, template) in enumerate(Prompt.TEMPLATES.items(), 1):
            preview = Prompt.render(name)
            color = self.config.get("prompt_color", "#00BFFF")
            print(f"  [{i}] {name:12} → {Colors.hex(color)}{preview}{Colors.RESET}")
        
        choice = input(f"\n  {Colors.hex('#00FF88')}Escolha um estilo:{Colors.RESET} ")
        
        try:
            idx = int(choice) - 1
            styles = list(Prompt.TEMPLATES.keys())
            if 0 <= idx < len(styles):
                self.config["prompt_style"] = styles[idx]
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Prompt atualizado!{Colors.RESET}")
        except ValueError:
            pass
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def show_config(self):
        """Mostra configuração atual"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  Configuração Atual:{Colors.RESET}\n")
        
        for key, value in self.config.items():
            print(f"  {Colors.CYAN}{key}:{Colors.RESET} {value}")
        
        print(f"\n  {Colors.DIM}Arquivo: {CONFIG_FILE}{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def color_demo(self):
        """Demonstração de todas as cores"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  🎨 Demonstração de Cores{Colors.RESET}\n")
        
        print(f"  {Colors.BOLD}Cores básicas:{Colors.RESET}")
        for color in ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]:
            c = getattr(Colors, color)
            print(f"  {c}███{Colors.RESET} {color}", end="  ")
        print("\n")
        
        print(f"  {Colors.BOLD}Cores brilhantes:{Colors.RESET}")
        for color in ["BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW", "BRIGHT_BLUE", "BRIGHT_MAGENTA", "BRIGHT_CYAN"]:
            c = getattr(Colors, color)
            print(f"  {c}███{Colors.RESET} {color}", end="  ")
        print("\n")
        
        print(f"  {Colors.BOLD}Estilos:{Colors.RESET}")
        print(f"  {Colors.BOLD}Negrito{Colors.RESET}  {Colors.ITALIC}Itálico{Colors.RESET}  {Colors.UNDERLINE}Sublinhado{Colors.RESET}  {Colors.DIM}Dim{Colors.RESET}")
        print()
        
        print(f"  {Colors.BOLD}Gradiente RGB:{Colors.RESET}")
        gradient = ""
        for i in range(50):
            r = int(255 * (1 - i/50))
            g = int(255 * (i/50) if i < 25 else 255 * (1 - (i-25)/25))
            b = int(255 * (i/50))
            gradient += f"{Colors.rgb(r, g, b)}█"
        print(f"  {gradient}{Colors.RESET}\n")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()


def main():
    """Função principal"""
    shark = Shark()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "banner":
            shark.show_banner()
        elif cmd == "prompt":
            print(shark.get_prompt(), end="")
        elif cmd == "colors":
            shark.color_demo()
        elif cmd == "config":
            print(json.dumps(shark.config, indent=2))
        elif cmd == "--help" or cmd == "-h":
            print(f"""
{Colors.CYAN}🦈 SHARK - Sistema de Personalização Total{Colors.RESET}

{Colors.BOLD}Uso:{Colors.RESET}
  python shark.py          Abre o menu interativo
  python shark.py banner   Exibe o banner
  python shark.py prompt   Exibe o prompt customizado
  python shark.py colors   Demonstração de cores
  python shark.py config   Mostra configuração JSON

{Colors.BOLD}Configuração:{Colors.RESET}
  Arquivo: {CONFIG_FILE}
""")
        else:
            print(f"{Colors.RED}Comando não reconhecido. Use --help{Colors.RESET}")
    else:
        shark.interactive_menu()


if __name__ == "__main__":
    main()

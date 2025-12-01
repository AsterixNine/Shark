#!/usr/bin/env python3
"""
🦈 SHARK - Sistema de Personalização TOTAL para Terminais
Personalize ABSOLUTAMENTE TUDO no seu terminal!
Compatível com: Windows (CMD, PowerShell, VS Code), Linux, Mac, Termux
"""

import os
import sys
import json
import time
import random
import hashlib
import platform
import threading
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# COMPATIBILIDADE WINDOWS - Habilita cores ANSI em todos os terminais
# ═══════════════════════════════════════════════════════════════════════════════

def enable_windows_ansi():
    """Habilita suporte a cores ANSI no Windows (CMD, PowerShell, VS Code)"""
    if platform.system().lower() != 'windows':
        return True
    
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        
        # Habilita VT100 para stdout
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        ENABLE_PROCESSED_OUTPUT = 0x0001
        
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING | ENABLE_PROCESSED_OUTPUT
        kernel32.SetConsoleMode(handle, mode)
        
        # Também para stderr
        STD_ERROR_HANDLE = -12
        handle_err = kernel32.GetStdHandle(STD_ERROR_HANDLE)
        kernel32.GetConsoleMode(handle_err, ctypes.byref(mode))
        mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING | ENABLE_PROCESSED_OUTPUT
        kernel32.SetConsoleMode(handle_err, mode)
        
        return True
    except Exception:
        # Fallback: define variável de ambiente para VS Code
        os.environ['FORCE_COLOR'] = '1'
        os.environ['TERM'] = 'xterm-256color'
        return False

# Inicializa suporte ANSI
ANSI_ENABLED = enable_windows_ansi()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES GLOBAIS
# ═══════════════════════════════════════════════════════════════════════════════

SYSTEM = platform.system().lower()
IS_TERMUX = os.environ.get('TERMUX_VERSION') is not None
IS_VSCODE = os.environ.get('TERM_PROGRAM') == 'vscode' or 'VSCODE' in os.environ.get('TERM_PROGRAM', '')

# Detecta terminal
def detect_terminal():
    """Detecta qual terminal está sendo usado"""
    if IS_VSCODE:
        return "vscode"
    if IS_TERMUX:
        return "termux"
    if SYSTEM == 'windows':
        if os.environ.get('WT_SESSION'):
            return "windows-terminal"
        if os.environ.get('ConEmuANSI'):
            return "conemu"
        parent = os.environ.get('PROMPT', '')
        if '$P$G' in parent:
            return "cmd"
        return "powershell"
    return os.environ.get('TERM', 'unknown')

TERMINAL = detect_terminal()

# Diretórios de configuração
if IS_TERMUX:
    CONFIG_DIR = Path.home() / ".shark"
elif SYSTEM == "windows":
    CONFIG_DIR = Path(os.environ.get('APPDATA', Path.home())) / "Shark"
else:
    CONFIG_DIR = Path.home() / ".config" / "shark"

CONFIG_FILE = CONFIG_DIR / "config.json"
THEMES_DIR = CONFIG_DIR / "themes"
BANNERS_DIR = CONFIG_DIR / "banners"
ANIMATIONS_DIR = CONFIG_DIR / "animations"
CREDENTIALS_FILE = CONFIG_DIR / ".credentials"


# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE CORES EXPANDIDO
# ═══════════════════════════════════════════════════════════════════════════════

class Colors:
    """Sistema de cores ANSI completo - 16M cores!"""
    
    # Reset
    RESET = "\033[0m"
    
    # Cores básicas (8 cores)
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Cores brilhantes (8 cores)
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background básico
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    # Background brilhante
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"
    
    # Estilos de texto
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    BLINK_FAST = "\033[6m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"
    DOUBLE_UNDERLINE = "\033[21m"
    OVERLINE = "\033[53m"
    
    # Paletas de cores predefinidas
    PALETTES = {
        "ocean": ["#006994", "#0099CC", "#00CED1", "#40E0D0", "#7FFFD4"],
        "fire": ["#8B0000", "#FF4500", "#FF6347", "#FFA500", "#FFD700"],
        "forest": ["#013220", "#228B22", "#32CD32", "#7CFC00", "#ADFF2F"],
        "sunset": ["#FF6B6B", "#FF8E53", "#FFBE5C", "#FFE66D", "#F7FFF7"],
        "neon": ["#FF00FF", "#00FFFF", "#FF00AA", "#00FF00", "#FFFF00"],
        "pastel": ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],
        "dark": ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#533483"],
        "cyberpunk": ["#00ff9f", "#00b8ff", "#001eff", "#bd00ff", "#d600ff"],
        "matrix": ["#003B00", "#008F11", "#00FF41", "#00FF00", "#39FF14"],
        "galaxy": ["#0B0B45", "#1B1B6F", "#2E2E99", "#5555FF", "#8888FF"],
        "blood": ["#2D0000", "#5C0000", "#8B0000", "#B22222", "#DC143C"],
        "ice": ["#E0FFFF", "#B0E0E6", "#87CEEB", "#4169E1", "#0000CD"],
        "gold": ["#B8860B", "#DAA520", "#FFD700", "#FFEC8B", "#FFFACD"],
        "purple_rain": ["#2E0854", "#4B0082", "#8A2BE2", "#9400D3", "#DA70D6"],
        "toxic": ["#00FF00", "#7FFF00", "#ADFF2F", "#DFFF00", "#FFFF00"],
    }
    
    @staticmethod
    def rgb(r, g, b, bg=False):
        """Cor RGB customizada (16 milhões de cores!)"""
        return f"\033[{'48' if bg else '38'};2;{r};{g};{b}m"
    
    @staticmethod
    def rgb_bg(r, g, b):
        """Background RGB"""
        return Colors.rgb(r, g, b, bg=True)
    
    @staticmethod
    def ansi256(code, bg=False):
        """Cor do padrão 256 cores"""
        return f"\033[{'48' if bg else '38'};5;{code}m"
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Converte HEX para RGB"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(r, g, b):
        """Converte RGB para HEX"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def hex(hex_color, bg=False):
        """Cor HEX customizada"""
        r, g, b = Colors.hex_to_rgb(hex_color)
        return Colors.rgb(r, g, b, bg)
    
    @staticmethod
    def hex_bg(hex_color):
        """Background HEX"""
        return Colors.hex(hex_color, bg=True)
    
    @staticmethod
    def gradient(text, start_color, end_color, bold=False):
        """Aplica gradiente linear de cores no texto"""
        start_r, start_g, start_b = Colors.hex_to_rgb(start_color)
        end_r, end_g, end_b = Colors.hex_to_rgb(end_color)
        
        result = ""
        if bold:
            result += Colors.BOLD
            
        visible_chars = [c for c in text if c not in '\n\r\t']
        length = len(visible_chars)
        char_count = 0
        
        for char in text:
            if char in '\n\r\t':
                result += char
                continue
            
            ratio = char_count / max(length - 1, 1)
            r = int(start_r + (end_r - start_r) * ratio)
            g = int(start_g + (end_g - start_g) * ratio)
            b = int(start_b + (end_b - start_b) * ratio)
            
            result += f"{Colors.rgb(r, g, b)}{char}"
            char_count += 1
        
        return result + Colors.RESET
    
    @staticmethod
    def multi_gradient(text, colors, bold=False):
        """Gradiente com múltiplas cores"""
        if len(colors) < 2:
            return text
        
        result = ""
        if bold:
            result += Colors.BOLD
        
        visible_chars = [c for c in text if c not in '\n\r\t']
        length = len(visible_chars)
        segments = len(colors) - 1
        chars_per_segment = length / segments
        
        char_count = 0
        for char in text:
            if char in '\n\r\t':
                result += char
                continue
            
            segment = min(int(char_count / chars_per_segment), segments - 1)
            local_ratio = (char_count - segment * chars_per_segment) / chars_per_segment
            
            start_r, start_g, start_b = Colors.hex_to_rgb(colors[segment])
            end_r, end_g, end_b = Colors.hex_to_rgb(colors[segment + 1])
            
            r = int(start_r + (end_r - start_r) * local_ratio)
            g = int(start_g + (end_g - start_g) * local_ratio)
            b = int(start_b + (end_b - start_b) * local_ratio)
            
            result += f"{Colors.rgb(r, g, b)}{char}"
            char_count += 1
        
        return result + Colors.RESET
    
    @staticmethod
    def rainbow(text, bold=False):
        """Aplica cores do arco-íris"""
        rainbow_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
        return Colors.multi_gradient(text, rainbow_colors, bold)
    
    @staticmethod
    def random_color():
        """Gera uma cor aleatória"""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return Colors.rgb_to_hex(r, g, b)


# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE ANIMAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════

class Animations:
    """Sistema de animações para terminal"""
    
    # Spinners predefinidos
    SPINNERS = {
        "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "line": ["-", "\\", "|", "/"],
        "arrow": ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
        "bounce": ["⠁", "⠂", "⠄", "⡀", "⢀", "⠠", "⠐", "⠈"],
        "shark": ["🦈", "🦈 ", "🦈  ", "🦈   ", "🦈    ", "   🦈", "  🦈", " 🦈"],
        "wave": ["~", "~~", "~~~", "~~~~", "~~~~~", "~~~~", "~~~", "~~"],
        "pulse": ["●", "○", "●", "○"],
        "clock": ["🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"],
        "moon": ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"],
        "earth": ["🌍", "🌎", "🌏"],
        "hearts": ["💛", "💙", "💜", "💚", "❤️"],
        "fire": ["🔥", "🔥🔥", "🔥🔥🔥", "🔥🔥", "🔥"],
        "blocks": ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂"],
    }
    
    # Animações de loading
    LOADING_STYLES = {
        "bar": lambda p, w: "█" * int(p * w) + "░" * (w - int(p * w)),
        "gradient": lambda p, w: Colors.gradient("█" * w, "#FF0000", "#00FF00")[:int(p * w)] + "░" * (w - int(p * w)),
        "wave": lambda p, w: "".join(["█" if (i / w + p) % 1 < 0.5 else "░" for i in range(w)]),
    }
    
    @staticmethod
    def typing_effect(text, delay=0.03, color=None):
        """Efeito de digitação"""
        for char in text:
            if color:
                sys.stdout.write(f"{Colors.hex(color)}{char}{Colors.RESET}")
            else:
                sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def fade_in(text, steps=10, delay=0.05, color="#FFFFFF"):
        """Efeito de fade in"""
        r, g, b = Colors.hex_to_rgb(color)
        
        for i in range(steps + 1):
            factor = i / steps
            current_r = int(r * factor)
            current_g = int(g * factor)
            current_b = int(b * factor)
            
            sys.stdout.write(f"\r{Colors.rgb(current_r, current_g, current_b)}{text}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def matrix_rain(duration=5, width=None):
        """Efeito Matrix Rain"""
        if width is None:
            try:
                width = os.get_terminal_size().columns
            except:
                width = 80
        
        chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789"
        columns = [0] * width
        
        print("\033[2J\033[H", end="")  # Limpa tela
        
        start_time = time.time()
        while time.time() - start_time < duration:
            line = ""
            for i in range(width):
                if random.random() < 0.1:
                    columns[i] = random.randint(5, 15)
                
                if columns[i] > 0:
                    char = random.choice(chars)
                    brightness = min(255, columns[i] * 25)
                    line += f"{Colors.rgb(0, brightness, 0)}{char}"
                    columns[i] -= 1
                else:
                    line += " "
            
            print(line + Colors.RESET)
            time.sleep(0.05)
    
    @staticmethod
    def spinner(text="Loading", style="dots", duration=3, color="#00BFFF"):
        """Exibe um spinner animado"""
        frames = Animations.SPINNERS.get(style, Animations.SPINNERS["dots"])
        
        start_time = time.time()
        i = 0
        while time.time() - start_time < duration:
            frame = frames[i % len(frames)]
            sys.stdout.write(f"\r{Colors.hex(color)}{frame}{Colors.RESET} {text}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
        sys.stdout.flush()
    
    @staticmethod
    def progress_animated(total, callback=None, style="bar", width=40, color="#00BFFF"):
        """Barra de progresso animada"""
        for i in range(total + 1):
            progress = i / total
            bar = Animations.LOADING_STYLES.get(style, Animations.LOADING_STYLES["bar"])(progress, width)
            
            sys.stdout.write(f"\r{Colors.hex(color)}[{bar}]{Colors.RESET} {progress*100:.1f}%")
            sys.stdout.flush()
            
            if callback:
                callback(i, total)
            
            time.sleep(0.02)
        print()
    
    @staticmethod
    def glitch_text(text, intensity=3, duration=1, color="#00FF00"):
        """Efeito glitch no texto"""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?`~"
        
        start_time = time.time()
        while time.time() - start_time < duration:
            glitched = ""
            for char in text:
                if random.random() < 0.1 * intensity:
                    glitched += random.choice(glitch_chars)
                else:
                    glitched += char
            
            offset = random.randint(-intensity, intensity)
            padding = " " * max(0, offset)
            
            sys.stdout.write(f"\r{padding}{Colors.hex(color)}{glitched}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.05)
        
        sys.stdout.write(f"\r{Colors.hex(color)}{text}{Colors.RESET}" + " " * 10)
        print()
    
    @staticmethod
    def wave_text(text, cycles=3, color="#00BFFF"):
        """Texto com efeito de onda"""
        for cycle in range(cycles * len(text)):
            output = ""
            for i, char in enumerate(text):
                offset = (cycle + i) % len(text)
                height = int(2 * abs((offset / len(text)) - 0.5))
                output += " " * height + char + " " * (2 - height)
            
            sys.stdout.write(f"\r{Colors.hex(color)}{output}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
        print()
    
    @staticmethod
    def color_cycle(text, duration=3, speed=0.1):
        """Ciclo de cores no texto"""
        start_time = time.time()
        hue = 0
        
        while time.time() - start_time < duration:
            # HSV para RGB (simplificado)
            h = hue % 360
            s = 1.0
            v = 1.0
            
            c = v * s
            x = c * (1 - abs((h / 60) % 2 - 1))
            m = v - c
            
            if h < 60:
                r, g, b = c, x, 0
            elif h < 120:
                r, g, b = x, c, 0
            elif h < 180:
                r, g, b = 0, c, x
            elif h < 240:
                r, g, b = 0, x, c
            elif h < 300:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
            
            sys.stdout.write(f"\r{Colors.rgb(r, g, b)}{text}{Colors.RESET}")
            sys.stdout.flush()
            
            hue += 10
            time.sleep(speed)
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE BANNERS PERSONALIZADOS
# ═══════════════════════════════════════════════════════════════════════════════

class Banners:
    """Sistema de banners ASCII com suporte a banners personalizados"""
    
    # Banners predefinidos
    BUILTIN = {
        "SHARK": r"""
   _____ _    _          _____  _  __
  / ____| |  | |   /\   |  __ \| |/ /
 | (___ | |__| |  /  \  | |__) | ' / 
  \___ \|  __  | / /\ \ |  _  /|  <  
  ____) | |  | |/ ____ \| | \ \| . \ 
 |_____/|_|  |_/_/    \_\_|  \_\_|\_\
        """,
        
        "SHARK_MINI": r"""
  █▀ █░█ ▄▀█ █▀█ █▄▀
  ▄█ █▀█ █▀█ █▀▄ █░█
        """,
        
        "SHARK_WAVE": r"""
    ~^~^~^~^~^~^~^~^~^~^~^~^~^~
    🦈  S H A R K  🦈
    ~^~^~^~^~^~^~^~^~^~^~^~^~^~
        """,
        
        "SHARK_3D": r"""
     ██████  ██   ██  █████  ██████  ██   ██ 
    ██       ██   ██ ██   ██ ██   ██ ██  ██  
    ███████  ███████ ███████ ██████  █████   
         ██ ██   ██ ██   ██ ██   ██ ██  ██  
    ██████  ██   ██ ██   ██ ██   ██ ██   ██ 
        """,
        
        "SHARK_BLOCK": r"""
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃  ███████╗██╗  ██╗ █████╗ ██████╗ ██╗ ┃
    ┃  ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ┃
    ┃  ███████╗███████║███████║██████╔╝█║  ┃
    ┃  ╚════██║██╔══██║██╔══██║██╔══██╗██║ ┃
    ┃  ███████║██║  ██║██║  ██║██║  ██║██║ ┃
    ┃  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        """,
        
        "HACKER": r"""
    ╔═══════════════════════════════════════╗
    ║  [SYSTEM INITIALIZED]                  ║
    ║  > SHARK TERMINAL v2.0                 ║
    ║  > STATUS: ACTIVE                      ║
    ║  > ACCESS: GRANTED                     ║
    ╚═══════════════════════════════════════╝
        """,
        
        "MINIMAL": r"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            S H A R K
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """,
        
        "OCEAN": r"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ≋≋≋  🌊 SHARK 🦈 ≋≋≋
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """,
    }
    
    # Alfabeto para gerar banners personalizados
    ALPHABET_BLOCK = {
        'A': ["█▀█", "█▀█", "▀ ▀"],
        'B': ["█▀▄", "█▀▄", "▀▀ "],
        'C': ["█▀▀", "█  ", "▀▀▀"],
        'D': ["█▀▄", "█ █", "▀▀ "],
        'E': ["█▀▀", "█▀▀", "▀▀▀"],
        'F': ["█▀▀", "█▀▀", "▀  "],
        'G': ["█▀▀", "█ █", "▀▀▀"],
        'H': ["█ █", "█▀█", "▀ ▀"],
        'I': ["▀█▀", " █ ", "▀▀▀"],
        'J': ["  █", "  █", "▀▀ "],
        'K': ["█ █", "█▀▄", "▀ ▀"],
        'L': ["█  ", "█  ", "▀▀▀"],
        'M': ["█▄█", "█ █", "▀ ▀"],
        'N': ["█▀█", "█ █", "▀ ▀"],
        'O': ["█▀█", "█ █", "▀▀▀"],
        'P': ["█▀█", "█▀▀", "▀  "],
        'Q': ["█▀█", "█ █", "▀▀█"],
        'R': ["█▀█", "█▀▄", "▀ ▀"],
        'S': ["█▀▀", "▀▀█", "▀▀▀"],
        'T': ["▀█▀", " █ ", " ▀ "],
        'U': ["█ █", "█ █", "▀▀▀"],
        'V': ["█ █", "█ █", " ▀ "],
        'W': ["█ █", "█ █", "█▀█"],
        'X': ["█ █", " ▀ ", "█ █"],
        'Y': ["█ █", " █ ", " ▀ "],
        'Z': ["▀▀█", " █ ", "█▀▀"],
        '0': ["█▀█", "█ █", "▀▀▀"],
        '1': ["▄█ ", " █ ", "▀▀▀"],
        '2': ["▀▀█", "█▀▀", "▀▀▀"],
        '3': ["▀▀█", " ▀█", "▀▀▀"],
        '4': ["█ █", "▀▀█", "  ▀"],
        '5': ["█▀▀", "▀▀█", "▀▀▀"],
        '6': ["█▀▀", "█▀█", "▀▀▀"],
        '7': ["▀▀█", "  █", "  ▀"],
        '8': ["█▀█", "█▀█", "▀▀▀"],
        '9': ["█▀█", "▀▀█", "▀▀▀"],
        ' ': ["   ", "   ", "   "],
        '_': ["   ", "   ", "▀▀▀"],
        '-': ["   ", "▀▀▀", "   "],
        '.': ["   ", "   ", " ▀ "],
        '!': [" █ ", " █ ", " ▀ "],
    }
    
    @staticmethod
    def generate_text_banner(text, style="block"):
        """Gera um banner a partir de texto"""
        text = text.upper()
        lines = ["", "", ""]
        
        for char in text:
            if char in Banners.ALPHABET_BLOCK:
                for i, row in enumerate(Banners.ALPHABET_BLOCK[char]):
                    lines[i] += row + " "
            else:
                for i in range(3):
                    lines[i] += "   "
        
        return "\n".join(lines)
    
    @staticmethod
    def load_custom_banners():
        """Carrega banners personalizados do usuário"""
        custom = {}
        if BANNERS_DIR.exists():
            for file in BANNERS_DIR.glob("*.txt"):
                name = file.stem.upper()
                custom[name] = file.read_text(encoding='utf-8')
        return custom
    
    @staticmethod
    def save_custom_banner(name, content):
        """Salva um banner personalizado"""
        BANNERS_DIR.mkdir(parents=True, exist_ok=True)
        file_path = BANNERS_DIR / f"{name.lower()}.txt"
        file_path.write_text(content, encoding='utf-8')
    
    @staticmethod
    def get_all_banners():
        """Retorna todos os banners (builtin + custom)"""
        all_banners = Banners.BUILTIN.copy()
        all_banners.update(Banners.load_custom_banners())
        return all_banners
    
    @staticmethod
    def render(name, colors=None, bold=False):
        """Renderiza um banner com cores"""
        all_banners = Banners.get_all_banners()
        banner = all_banners.get(name.upper(), Banners.BUILTIN["SHARK"])
        
        if colors and len(colors) >= 2:
            return Colors.multi_gradient(banner, colors, bold)
        elif colors and len(colors) == 1:
            return f"{Colors.hex(colors[0])}{banner}{Colors.RESET}"
        else:
            return banner


# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE SENHA/SEGURANÇA
# ═══════════════════════════════════════════════════════════════════════════════

class Security:
    """Sistema de proteção por senha"""
    
    @staticmethod
    def hash_password(password, salt=None):
        """Gera hash seguro da senha"""
        if salt is None:
            salt = os.urandom(32).hex()
        
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return salt, hash_obj.hex()
    
    @staticmethod
    def verify_password(password, salt, stored_hash):
        """Verifica se a senha está correta"""
        _, new_hash = Security.hash_password(password, salt)
        return new_hash == stored_hash
    
    @staticmethod
    def save_credentials(password):
        """Salva credenciais de forma segura"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        salt, password_hash = Security.hash_password(password)
        
        credentials = {
            "salt": salt,
            "hash": password_hash,
            "created": datetime.now().isoformat()
        }
        
        with open(CREDENTIALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(credentials, f)
        
        # Torna o arquivo oculto no Windows
        if SYSTEM == 'windows':
            try:
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(CREDENTIALS_FILE), 2)
            except:
                pass
    
    @staticmethod
    def load_credentials():
        """Carrega credenciais"""
        if not CREDENTIALS_FILE.exists():
            return None
        
        with open(CREDENTIALS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def is_password_set():
        """Verifica se existe senha configurada"""
        return CREDENTIALS_FILE.exists()
    
    @staticmethod
    def remove_password():
        """Remove a senha"""
        if CREDENTIALS_FILE.exists():
            CREDENTIALS_FILE.unlink()
    
    @staticmethod
    def prompt_password(message="Senha: ", hidden=True):
        """Solicita senha do usuário"""
        if hidden:
            try:
                import getpass
                return getpass.getpass(message)
            except:
                pass
        return input(message)
    
    @staticmethod
    def authenticate():
        """Processo de autenticação"""
        if not Security.is_password_set():
            return True
        
        credentials = Security.load_credentials()
        if not credentials:
            return True
        
        print(f"\n{Colors.hex('#FF6B6B')}🔒 Shark protegido por senha{Colors.RESET}\n")
        
        for attempt in range(3):
            password = Security.prompt_password(f"  Digite a senha ({3 - attempt} tentativas): ")
            
            if Security.verify_password(password, credentials["salt"], credentials["hash"]):
                print(f"\n  {Colors.GREEN}✓ Acesso autorizado!{Colors.RESET}\n")
                return True
            else:
                print(f"  {Colors.RED}✗ Senha incorreta{Colors.RESET}")
        
        print(f"\n  {Colors.RED}✗ Muitas tentativas. Acesso negado.{Colors.RESET}\n")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE PROMPT
# ═══════════════════════════════════════════════════════════════════════════════

class Prompt:
    """Sistema de prompt customizável"""
    
    TEMPLATES = {
        "minimal": "{user}@{host} {cwd} $ ",
        "shark": "🦈 {cwd} ❯ ",
        "powerline": " {user}   {cwd}  ",
        "arrow": "╭─[{user}@{host}]─[{cwd}]\n╰─➤ ",
        "simple": "{cwd} > ",
        "hacker": "[{time}] {user}@{host}:{cwd}# ",
        "lambda": "λ {cwd} → ",
        "git": "⎇ {cwd} ❯ ",
        "neon": "◈ {cwd} ⟫ ",
        "box": "┌[{user}]─[{cwd}]\n└─$ ",
    }
    
    @staticmethod
    def get_variables():
        """Retorna variáveis disponíveis para o prompt"""
        import getpass
        import socket
        
        cwd = os.getcwd()
        home = str(Path.home())
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
        
        return {
            "user": getpass.getuser(),
            "host": socket.gethostname(),
            "cwd": cwd,
            "system": SYSTEM,
            "terminal": TERMINAL,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
    
    @staticmethod
    def render(template_name="shark", custom_template=None, color=None):
        """Renderiza o prompt"""
        template = custom_template or Prompt.TEMPLATES.get(template_name, Prompt.TEMPLATES["shark"])
        variables = Prompt.get_variables()
        
        try:
            prompt = template.format(**variables)
        except KeyError:
            prompt = Prompt.TEMPLATES["shark"].format(**variables)
        
        if color:
            return f"{Colors.hex(color)}{prompt}{Colors.RESET}"
        return prompt


# ═══════════════════════════════════════════════════════════════════════════════
# BARRAS DE PROGRESSO
# ═══════════════════════════════════════════════════════════════════════════════

class ProgressBar:
    """Barras de progresso customizáveis"""
    
    STYLES = {
        "default": ("█", "░"),
        "shark": ("🦈", "~"),
        "arrows": ("▶", "▷"),
        "blocks": ("■", "□"),
        "dots": ("●", "○"),
        "lines": ("━", "─"),
        "equals": ("=", "-"),
        "hash": ("#", "."),
        "stars": ("★", "☆"),
        "circles": ("◉", "○"),
        "diamonds": ("◆", "◇"),
        "gradient": ("█", "▓", "▒", "░"),
    }
    
    @staticmethod
    def render(progress, total, width=40, style="default", color="#00BFFF", show_percent=True):
        """Renderiza barra de progresso"""
        chars = ProgressBar.STYLES.get(style, ProgressBar.STYLES["default"])
        fill_char = chars[0]
        empty_char = chars[-1]
        
        percentage = progress / total if total > 0 else 0
        filled = int(width * percentage)
        empty = width - filled
        
        bar = fill_char * filled + empty_char * empty
        
        if show_percent:
            percent_text = f" {percentage * 100:.1f}%"
        else:
            percent_text = ""
        
        return f"{Colors.hex(color)}[{bar}]{percent_text}{Colors.RESET}"


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

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
        "password_protected": False,
        "animations_enabled": True,
        "default_animation_speed": 0.05,
        "terminal_title": "🦈 Shark Terminal",
        "custom_prompt": None,
    }
    
    @staticmethod
    def ensure_dirs():
        """Cria diretórios necessários"""
        for dir_path in [CONFIG_DIR, THEMES_DIR, BANNERS_DIR, ANIMATIONS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def load():
        """Carrega configuração"""
        Config.ensure_dirs()
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return {**Config.DEFAULT_CONFIG, **json.load(f)}
            except:
                return Config.DEFAULT_CONFIG.copy()
        return Config.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def save(config):
        """Salva configuração"""
        Config.ensure_dirs()
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def reset():
        """Reseta para configuração padrão"""
        Config.save(Config.DEFAULT_CONFIG.copy())


# ═══════════════════════════════════════════════════════════════════════════════
# CLASSE PRINCIPAL SHARK
# ═══════════════════════════════════════════════════════════════════════════════

class Shark:
    """🦈 Classe principal do Shark - Personalize TUDO!"""
    
    def __init__(self):
        self.config = Config.load()
        self.colors = Colors()
        self.banners = Banners()
        self.animations = Animations()
        self.security = Security()
    
    def show_banner(self, animated=False):
        """Exibe o banner"""
        banner_name = self.config.get("banner", "SHARK")
        colors = self.config.get("banner_colors", ["#00BFFF", "#0080FF"])
        
        banner = Banners.render(banner_name, colors, bold=True)
        
        if animated and self.config.get("animations_enabled", True):
            for line in banner.split('\n'):
                print(line)
                time.sleep(0.05)
        else:
            print(banner)
    
    def print_colored(self, text, color="#00BFFF", style=""):
        """Imprime texto colorido"""
        style_code = getattr(Colors, style.upper(), "") if style else ""
        print(f"{style_code}{Colors.hex(color)}{text}{Colors.RESET}")
    
    def clear_screen(self):
        """Limpa a tela"""
        if SYSTEM == 'windows': 
            os.system('cls')
        else:
            os.system('clear')
    
    def set_terminal_title(self, title=None):
        """Define o título do terminal"""
        title = title or self.config.get("terminal_title", "🦈 Shark")
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
    
    def get_prompt(self):
        """Retorna o prompt customizado"""
        style = self.config.get("prompt_style", "shark")
        color = self.config.get("prompt_color", "#00BFFF")
        custom = self.config.get("custom_prompt")
        return Prompt.render(style, custom, color)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MENUS INTERATIVOS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def interactive_menu(self):
        """Menu interativo principal"""
        self.clear_screen()
        self.set_terminal_title()
        self.show_banner()
        
        menu = f"""
{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════{Colors.RESET}
{Colors.BRIGHT_WHITE}  🦈 SHARK - Personalize ABSOLUTAMENTE TUDO!{Colors.RESET}
{Colors.DIM}  Terminal: {TERMINAL} | Sistema: {SYSTEM}{Colors.RESET}
{Colors.CYAN}═══════════════════════════════════════════════════════════{Colors.RESET}

  {Colors.hex("#00BFFF")}[1]{Colors.RESET} Temas e Cores
  {Colors.hex("#00BFFF")}[2]{Colors.RESET} Banners (incluindo personalizados)
  {Colors.hex("#00BFFF")}[3]{Colors.RESET} Configurar Prompt
  {Colors.hex("#00BFFF")}[4]{Colors.RESET} Barras de Progresso
  {Colors.hex("#00BFFF")}[5]{Colors.RESET} Animacoes e Efeitos
  {Colors.hex("#00BFFF")}[6]{Colors.RESET} Seguranca (Senha)
  {Colors.hex("#00BFFF")}[7]{Colors.RESET} Configuracoes
  {Colors.hex("#00BFFF")}[8]{Colors.RESET} Demo Completo
  {Colors.hex("#FF6B6B")}[I]{Colors.RESET} INSTALAR no Terminal (permanente)
  {Colors.hex("#00FF88")}[U]{Colors.RESET} Atualizar Shark (GitHub)
  {Colors.hex("#00BFFF")}[0]{Colors.RESET} Sair

{Colors.CYAN}═══════════════════════════════════════════════════════════{Colors.RESET}
"""
        print(menu)
        
        try:
            choice = input(f"  {Colors.hex('#00FF88')}Escolha uma opção:{Colors.RESET} ").strip()
            
            actions = {
                "1": self.theme_menu,
                "2": self.banner_menu,
                "3": self.prompt_menu,
                "4": self.progress_menu,
                "5": self.animation_menu,
                "6": self.security_menu,
                "7": self.config_menu,
                "8": self.full_demo,
                "i": self.install_menu,
                "u": self.update_menu,
                "0": self.exit_shark,
            }
            
            if choice in actions:
                actions[choice]()
            else:
                self.interactive_menu()
                
        except KeyboardInterrupt:
            self.exit_shark()
    
    def theme_menu(self):
        """Menu de temas e cores"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  🎨 Temas e Cores{Colors.RESET}\n")
        
        print(f"  {Colors.CYAN}Paletas disponíveis:{Colors.RESET}\n")
        
        for i, (name, palette) in enumerate(Colors.PALETTES.items(), 1):
            gradient = Colors.multi_gradient("██████████", palette)
            print(f"  [{i:2}] {name:15} {gradient}")
        
        print(f"\n  [{len(Colors.PALETTES) + 1}] Cor personalizada (HEX)")
        print(f"  [{len(Colors.PALETTES) + 2}] Cor aleatória")
        print(f"  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip()
        
        if choice == "0":
            self.interactive_menu()
            return
        
        try:
            idx = int(choice) - 1
            palettes = list(Colors.PALETTES.items())
            
            if 0 <= idx < len(palettes):
                name, palette = palettes[idx]
                self.config["banner_colors"] = palette[:2]
                self.config["prompt_color"] = palette[0]
                self.config["theme"] = name
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Tema '{name}' aplicado!{Colors.RESET}")
            elif idx == len(palettes):
                hex_color = input("  Digite a cor HEX (ex: #FF5500): ").strip()
                if hex_color:
                    self.config["banner_colors"] = [hex_color, hex_color]
                    self.config["prompt_color"] = hex_color
                    Config.save(self.config)
                    print(f"\n  {Colors.GREEN}✓ Cor aplicada!{Colors.RESET}")
            elif idx == len(palettes) + 1:
                random_color = Colors.random_color()
                self.config["banner_colors"] = [random_color, Colors.random_color()]
                self.config["prompt_color"] = random_color
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Cor aleatória {random_color} aplicada!{Colors.RESET}")
        except ValueError:
            pass
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def banner_menu(self):
        """Menu de banners"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  🖼️  Banners{Colors.RESET}\n")
        
        all_banners = Banners.get_all_banners()
        colors = self.config.get("banner_colors", ["#00BFFF", "#0080FF"])
        
        print(f"  {Colors.CYAN}Banners disponíveis:{Colors.RESET}\n")
        
        for i, name in enumerate(all_banners.keys(), 1):
            print(f"  [{i:2}] {name}")
        
        print(f"\n  [C] Criar banner personalizado")
        print(f"  [T] Gerar banner a partir de texto")
        print(f"  [V] Visualizar banner atual")
        print(f"  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip().upper()
        
        if choice == "0":
            self.interactive_menu()
            return
        elif choice == "C":
            self.create_custom_banner()
            return
        elif choice == "T":
            self.generate_text_banner()
            return
        elif choice == "V":
            self.clear_screen()
            print(f"\n{Colors.BOLD}  Banner atual:{Colors.RESET}\n")
            print(Banners.render(self.config.get("banner", "SHARK"), colors, bold=True))
            input("\n  Pressione Enter para continuar...")
            self.banner_menu()
            return
        
        try:
            idx = int(choice) - 1
            banner_names = list(all_banners.keys())
            if 0 <= idx < len(banner_names):
                self.config["banner"] = banner_names[idx]
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Banner '{banner_names[idx]}' selecionado!{Colors.RESET}")
        except ValueError:
            pass
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def create_custom_banner(self):
        """Cria um banner personalizado"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  🖼️  Criar Banner Personalizado{Colors.RESET}\n")
        print(f"  {Colors.DIM}Digite seu banner ASCII (linha vazia para terminar):{Colors.RESET}\n")
        
        lines = []
        while True:
            line = input("  ")
            if line == "":
                break
            lines.append(line)
        
        if lines:
            name = input("\n  Nome do banner: ").strip()
            if name:
                content = "\n".join(lines)
                Banners.save_custom_banner(name, content)
                self.config["banner"] = name.upper()
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Banner '{name}' salvo e selecionado!{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.banner_menu()
    
    def generate_text_banner(self):
        """Gera banner a partir de texto"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  🔤 Gerar Banner a partir de Texto{Colors.RESET}\n")
        
        text = input("  Digite o texto: ").strip()
        if text:
            banner = Banners.generate_text_banner(text)
            colors = self.config.get("banner_colors", ["#00BFFF", "#0080FF"])
            
            print(f"\n  {Colors.BOLD}Preview:{Colors.RESET}\n")
            print(Colors.multi_gradient(banner, colors))
            
            save = input("\n  Salvar este banner? (s/n): ").strip().lower()
            if save == 's':
                name = input("  Nome do banner: ").strip()
                if name:
                    Banners.save_custom_banner(name, banner)
                    self.config["banner"] = name.upper()
                    Config.save(self.config)
                    print(f"\n  {Colors.GREEN}✓ Banner '{name}' salvo!{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.banner_menu()
    
    def prompt_menu(self):
        """Menu de prompts"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  💻 Configurar Prompt{Colors.RESET}\n")
        
        color = self.config.get("prompt_color", "#00BFFF")
        
        print(f"  {Colors.CYAN}Estilos disponíveis:{Colors.RESET}\n")
        
        for i, (name, template) in enumerate(Prompt.TEMPLATES.items(), 1):
            preview = Prompt.render(name, color=color)
            print(f"  [{i:2}] {name:12} → {preview}")
        
        print(f"\n  [C] Prompt customizado")
        print(f"  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip().upper()
        
        if choice == "0":
            self.interactive_menu()
            return
        elif choice == "C":
            print(f"\n  {Colors.DIM}Variáveis: {{user}}, {{host}}, {{cwd}}, {{time}}, {{date}}{Colors.RESET}")
            custom = input("  Digite o template: ").strip()
            if custom:
                self.config["custom_prompt"] = custom
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Prompt customizado salvo!{Colors.RESET}")
        else:
            try:
                idx = int(choice) - 1
                styles = list(Prompt.TEMPLATES.keys())
                if 0 <= idx < len(styles):
                    self.config["prompt_style"] = styles[idx]
                    self.config["custom_prompt"] = None
                    Config.save(self.config)
                    print(f"\n  {Colors.GREEN}✓ Prompt '{styles[idx]}' selecionado!{Colors.RESET}")
            except ValueError:
                pass
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def progress_menu(self):
        """Menu de barras de progresso"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  📊 Barras de Progresso{Colors.RESET}\n")
        
        color = self.config.get("prompt_color", "#00BFFF")
        
        print(f"  {Colors.CYAN}Estilos disponíveis:{Colors.RESET}\n")
        
        for i, style in enumerate(ProgressBar.STYLES.keys(), 1):
            bar = ProgressBar.render(75, 100, width=30, style=style, color=color)
            print(f"  [{i:2}] {style:12} {bar}")
        
        print(f"\n  [D] Demo animado")
        print(f"  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip().upper()
        
        if choice == "0":
            self.interactive_menu()
            return
        elif choice == "D":
            print(f"\n  {Colors.BOLD}Demo animado:{Colors.RESET}\n")
            Animations.progress_animated(100, width=40, color=color)
        else:
            try:
                idx = int(choice) - 1
                styles = list(ProgressBar.STYLES.keys())
                if 0 <= idx < len(styles):
                    self.config["progress_style"] = styles[idx]
                    Config.save(self.config)
                    print(f"\n  {Colors.GREEN}✓ Estilo '{styles[idx]}' selecionado!{Colors.RESET}")
            except ValueError:
                pass
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def animation_menu(self):
        """Menu de animações"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  ✨ Animações e Efeitos{Colors.RESET}\n")
        
        color = self.config.get("prompt_color", "#00BFFF")
        
        options = [
            ("Efeito Typing", lambda: Animations.typing_effect("🦈 Shark - Personalize TUDO!", color=color)),
            ("Fade In", lambda: Animations.fade_in("SHARK", color=color)),
            ("Glitch", lambda: Animations.glitch_text("SHARK", color=color)),
            ("Ciclo de Cores", lambda: Animations.color_cycle("★ SHARK ★", duration=3)),
            ("Rainbow Text", lambda: print(Colors.rainbow("🌈 SHARK RAINBOW 🌈", bold=True))),
            ("Matrix Rain", lambda: Animations.matrix_rain(duration=3)),
            ("Spinners", self.spinner_demo),
        ]
        
        for i, (name, _) in enumerate(options, 1):
            print(f"  [{i}] {name}")
        
        print(f"\n  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip()
        
        if choice == "0":
            self.interactive_menu()
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                print()
                options[idx][1]()
        except ValueError:
            pass
        
        input("\n  Pressione Enter para continuar...")
        self.animation_menu()
    
    def spinner_demo(self):
        """Demonstração de spinners"""
        color = self.config.get("prompt_color", "#00BFFF")
        
        for name in list(Animations.SPINNERS.keys())[:6]:
            print(f"  {name}: ", end="")
            Animations.spinner(f"Loading...", style=name, duration=1.5, color=color)
            print()
    
    def security_menu(self):
        """Menu de segurança"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  🔒 Segurança{Colors.RESET}\n")
        
        has_password = Security.is_password_set()
        status = f"{Colors.GREEN}Ativada{Colors.RESET}" if has_password else f"{Colors.YELLOW}Desativada{Colors.RESET}"
        print(f"  Status: Proteção por senha {status}\n")
        
        if has_password:
            print(f"  [1] Alterar senha")
            print(f"  [2] Remover senha")
        else:
            print(f"  [1] Definir senha")
        
        print(f"\n  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip()
        
        if choice == "0":
            self.interactive_menu()
            return
        elif choice == "1":
            if has_password:
                current = Security.prompt_password("  Senha atual: ")
                creds = Security.load_credentials()
                if not Security.verify_password(current, creds["salt"], creds["hash"]):
                    print(f"\n  {Colors.RED}✗ Senha incorreta{Colors.RESET}")
                    input("\n  Pressione Enter para continuar...")
                    self.security_menu()
                    return
            
            new_pass = Security.prompt_password("  Nova senha: ")
            confirm = Security.prompt_password("  Confirmar senha: ")
            
            if new_pass == confirm:
                Security.save_credentials(new_pass)
                self.config["password_protected"] = True
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Senha {'alterada' if has_password else 'definida'}!{Colors.RESET}")
            else:
                print(f"\n  {Colors.RED}✗ Senhas não coincidem{Colors.RESET}")
        elif choice == "2" and has_password:
            current = Security.prompt_password("  Senha atual: ")
            creds = Security.load_credentials()
            if Security.verify_password(current, creds["salt"], creds["hash"]):
                Security.remove_password()
                self.config["password_protected"] = False
                Config.save(self.config)
                print(f"\n  {Colors.GREEN}✓ Senha removida!{Colors.RESET}")
            else:
                print(f"\n  {Colors.RED}✗ Senha incorreta{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def config_menu(self):
        """Menu de configurações"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  ⚙️  Configurações{Colors.RESET}\n")
        
        print(f"  {Colors.CYAN}Configuração atual:{Colors.RESET}\n")
        for key, value in self.config.items():
            print(f"  {Colors.DIM}{key}:{Colors.RESET} {value}")
        
        print(f"\n  {Colors.DIM}Arquivo: {CONFIG_FILE}{Colors.RESET}")
        print(f"\n  [R] Resetar para padrão")
        print(f"  [E] Exportar configuração")
        print(f"  [0] Voltar\n")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip().upper()
        
        if choice == "0":
            self.interactive_menu()
            return
        elif choice == "R":
            confirm = input("  Tem certeza? (s/n): ").strip().lower()
            if confirm == 's':
                Config.reset()
                self.config = Config.load()
                print(f"\n  {Colors.GREEN}✓ Configuração resetada!{Colors.RESET}")
        elif choice == "E":
            print(f"\n{json.dumps(self.config, indent=2, ensure_ascii=False)}")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def full_demo(self):
        """Demo completo de todas as funcionalidades"""
        self.clear_screen()
        
        # Banner com gradiente
        print(f"\n{Colors.BOLD}  🎬 Demo Completo do Shark{Colors.RESET}\n")
        time.sleep(0.5)
        
        # Cores
        print(f"  {Colors.BOLD}1. Sistema de Cores:{Colors.RESET}")
        print(f"     {Colors.rainbow('Rainbow Text Demo')}")
        time.sleep(0.3)
        
        # Gradientes
        print(f"\n  {Colors.BOLD}2. Gradientes:{Colors.RESET}")
        for name, palette in list(Colors.PALETTES.items())[:5]:
            print(f"     {name:12} {Colors.multi_gradient('████████████████', palette)}")
        time.sleep(0.3)
        
        # Barras de progresso
        print(f"\n  {Colors.BOLD}3. Barras de Progresso:{Colors.RESET}")
        for style in list(ProgressBar.STYLES.keys())[:4]:
            bar = ProgressBar.render(75, 100, width=20, style=style)
            print(f"     {style:12} {bar}")
        time.sleep(0.3)
        
        # Animação
        print(f"\n  {Colors.BOLD}4. Animação:{Colors.RESET}")
        print("     ", end="")
        Animations.typing_effect("Typing effect demo...", delay=0.02, color="#00FF88")
        
        # Spinners
        print(f"\n  {Colors.BOLD}5. Spinners:{Colors.RESET}")
        for name in list(Animations.SPINNERS.keys())[:3]:
            print(f"     ", end="")
            Animations.spinner("Loading...", style=name, duration=1)
        
        print(f"\n  {Colors.GREEN}✓ Demo completo!{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def update_menu(self):
        """Menu de atualizacao do Shark"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  Atualizar Shark{Colors.RESET}\n")
        
        print(f"  {Colors.CYAN}Verificando atualizacoes...{Colors.RESET}\n")
        
        # Verifica se existe o updater
        updater_path = Path(__file__).parent / "shark_update.py"
        
        if not updater_path.exists():
            print(f"  {Colors.RED}[X] shark_update.py nao encontrado{Colors.RESET}")
            print(f"  {Colors.DIM}Baixe do repositorio GitHub{Colors.RESET}")
            input("\n  Pressione Enter para continuar...")
            self.interactive_menu()
            return
        
        # Verifica versao
        shark_dir = Path(__file__).parent
        has_git = (shark_dir / ".git").exists()
        
        print(f"  Diretorio: {Colors.DIM}{shark_dir}{Colors.RESET}")
        print(f"  Git:       {Colors.GREEN if has_git else Colors.YELLOW}{'Sim' if has_git else 'Nao'}{Colors.RESET}")
        
        # Tenta obter versao remota
        try:
            from urllib.request import urlopen, Request
            import json as json_module
            
            # Configuracao do repositorio (mesma do shark_update.py)
            github_user = "seuusuario"
            github_repo = "shark"
            
            api_url = f"https://api.github.com/repos/{github_user}/{github_repo}/releases/latest"
            req = Request(api_url, headers={'User-Agent': 'Shark'})
            
            with urlopen(req, timeout=5) as response:
                data = json_module.loads(response.read().decode())
                remote_version = data.get('tag_name', 'N/A').lstrip('v')
                print(f"  Versao remota: {Colors.GREEN}{remote_version}{Colors.RESET}")
        except:
            print(f"  Versao remota: {Colors.YELLOW}Nao foi possivel verificar{Colors.RESET}")
        
        print(f"""
  [1] Atualizar agora
  [2] Verificar atualizacoes
  [3] Forcar atualizacao
  [0] Voltar
""")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip()
        
        if choice == "0":
            self.interactive_menu()
            return
        
        # Executa o updater
        import subprocess
        
        if choice == "1":
            subprocess.run([sys.executable, str(updater_path)])
        elif choice == "2":
            subprocess.run([sys.executable, str(updater_path), "check"])
        elif choice == "3":
            subprocess.run([sys.executable, str(updater_path), "force"])
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def install_menu(self):
        """Menu de instalacao no terminal"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}  INSTALAR no Terminal{Colors.RESET}\n")
        
        # Verifica status atual
        installed = ShellIntegration.check_installation()
        
        print(f"  {Colors.CYAN}Status atual:{Colors.RESET}\n")
        for shell, is_installed in installed.items():
            status = f"{Colors.GREEN}Instalado{Colors.RESET}" if is_installed else f"{Colors.DIM}Nao instalado{Colors.RESET}"
            print(f"  {shell}: {status}")
        
        print(f"""
  {Colors.YELLOW}O que a instalacao faz:{Colors.RESET}
  - Exibe banner ao abrir qualquer terminal
  - Substitui prompt padrao pelo Shark
  - Adiciona comandos: shark, shark-banner, shark-matrix
  
  [1] Instalar no terminal
  [2] Remover do terminal
  [0] Voltar
""")
        
        choice = input(f"  {Colors.hex('#00FF88')}Escolha:{Colors.RESET} ").strip()
        
        if choice == "1":
            print(f"\n  {Colors.CYAN}Instalando...{Colors.RESET}\n")
            results = ShellIntegration.install_all()
            for shell, result in results.items():
                if "Erro" in str(result):
                    print(f"  {Colors.RED}[X] {shell}: {result}{Colors.RESET}")
                else:
                    print(f"  {Colors.GREEN}[V] {shell}: Instalado{Colors.RESET}")
            print(f"\n  {Colors.GREEN}Feche e abra o terminal para ver as mudancas!{Colors.RESET}")
        elif choice == "2":
            print(f"\n  {Colors.CYAN}Removendo...{Colors.RESET}\n")
            results = ShellIntegration.uninstall_all()
            for shell, success in results.items():
                if success:
                    print(f"  {Colors.GREEN}[V] {shell}: Removido{Colors.RESET}")
                else:
                    print(f"  {Colors.DIM}[-] {shell}: Nao estava instalado{Colors.RESET}")
            print(f"\n  {Colors.GREEN}Shark removido. Reinicie o terminal.{Colors.RESET}")
        
        input("\n  Pressione Enter para continuar...")
        self.interactive_menu()
    
    def exit_shark(self):
        """Sai do Shark"""
        self.print_colored("\n  Ate mais! Shark out!\n", "#00BFFF")
        sys.exit(0)


# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA DE INSTALACAO - INTEGRA COM SHELLS
# ═══════════════════════════════════════════════════════════════════════════════

class ShellIntegration:
    """Integra Shark com shells do sistema - fica PERMANENTE"""
    
    # Caminho do script shark.py
    SHARK_SCRIPT = Path(__file__).resolve()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # POWERSHELL
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def get_powershell_profile_path():
        """Retorna caminho do profile do PowerShell"""
        # PowerShell Core (pwsh)
        ps_core = Path.home() / "Documents" / "PowerShell" / "Microsoft.PowerShell_profile.ps1"
        # Windows PowerShell
        ps_win = Path.home() / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
        
        # Prefere PowerShell Core se existir o diretorio
        if ps_core.parent.exists():
            return ps_core
        return ps_win
    
    @staticmethod
    def generate_powershell_profile():
        """Gera codigo para PowerShell profile"""
        shark_path = str(ShellIntegration.SHARK_SCRIPT).replace("\\", "/")
        
        return f'''
# ═══════════════════════════════════════════════════════════════════════════════
# SHARK - Terminal Customization System
# Instalado automaticamente pelo Shark
# Para remover: python "{shark_path}" uninstall
# ═══════════════════════════════════════════════════════════════════════════════

# Habilita cores ANSI
$env:TERM = "xterm-256color"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Funcao para obter prompt do Shark
function Get-SharkPrompt {{
    $output = python "{shark_path}" prompt 2>$null
    if ($output) {{ return $output }}
    return "PS> "
}}

# Exibe banner ao iniciar
python "{shark_path}" banner

# Sobrescreve o prompt padrao
function prompt {{
    $sharkPrompt = Get-SharkPrompt
    return $sharkPrompt
}}

# Aliases uteis do Shark
function shark {{ python "{shark_path}" $args }}
function shark-banner {{ python "{shark_path}" banner }}
function shark-matrix {{ python "{shark_path}" matrix }}
function shark-rainbow {{ python "{shark_path}" rainbow $args }}

# Define titulo do terminal
$Host.UI.RawUI.WindowTitle = "Shark Terminal"

# ═══════════════════════════════════════════════════════════════════════════════
# FIM SHARK
# ═══════════════════════════════════════════════════════════════════════════════
'''
    
    @staticmethod
    def install_powershell():
        """Instala no PowerShell"""
        profile_path = ShellIntegration.get_powershell_profile_path()
        shark_code = ShellIntegration.generate_powershell_profile()
        marker_start = "# SHARK - Terminal Customization System"
        marker_end = "# FIM SHARK"
        
        # Cria diretorio se nao existir
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Le profile existente
        existing_content = ""
        if profile_path.exists():
            existing_content = profile_path.read_text(encoding='utf-8')
        
        # Remove instalacao anterior se existir
        if marker_start in existing_content:
            lines = existing_content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if marker_start in line:
                    skip = True
                elif marker_end in line:
                    skip = False
                    continue
                if not skip:
                    new_lines.append(line)
            existing_content = '\n'.join(new_lines).strip()
        
        # Adiciona codigo do Shark
        new_content = existing_content + "\n" + shark_code
        profile_path.write_text(new_content, encoding='utf-8')
        
        return profile_path
    
    @staticmethod
    def uninstall_powershell():
        """Remove do PowerShell"""
        profile_path = ShellIntegration.get_powershell_profile_path()
        marker_start = "# SHARK - Terminal Customization System"
        marker_end = "# FIM SHARK"
        
        if not profile_path.exists():
            return False
        
        content = profile_path.read_text(encoding='utf-8')
        
        if marker_start not in content:
            return False
        
        lines = content.split('\n')
        new_lines = []
        skip = False
        for line in lines:
            if marker_start in line:
                skip = True
            elif marker_end in line:
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines).strip()
        profile_path.write_text(new_content, encoding='utf-8')
        
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BASH
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def get_bash_profile_path():
        """Retorna caminho do .bashrc"""
        bashrc = Path.home() / ".bashrc"
        bash_profile = Path.home() / ".bash_profile"
        
        # Prefere .bashrc
        if bashrc.exists():
            return bashrc
        return bash_profile if bash_profile.exists() else bashrc
    
    @staticmethod
    def generate_bash_profile():
        """Gera codigo para Bash"""
        shark_path = str(ShellIntegration.SHARK_SCRIPT)
        
        return f'''
# ═══════════════════════════════════════════════════════════════════════════════
# SHARK - Terminal Customization System
# Instalado automaticamente pelo Shark
# Para remover: python3 "{shark_path}" uninstall
# ═══════════════════════════════════════════════════════════════════════════════

# Habilita cores
export TERM="xterm-256color"
export FORCE_COLOR=1

# Funcao para prompt do Shark
shark_prompt() {{
    python3 "{shark_path}" prompt 2>/dev/null
}}

# Exibe banner ao iniciar
python3 "{shark_path}" banner

# Sobrescreve PS1
export PS1='$(shark_prompt)'

# Aliases
alias shark='python3 "{shark_path}"'
alias shark-banner='python3 "{shark_path}" banner'
alias shark-matrix='python3 "{shark_path}" matrix'
shark-rainbow() {{ python3 "{shark_path}" rainbow "$@"; }}

# ═══════════════════════════════════════════════════════════════════════════════
# FIM SHARK
# ═══════════════════════════════════════════════════════════════════════════════
'''
    
    @staticmethod
    def install_bash():
        """Instala no Bash"""
        profile_path = ShellIntegration.get_bash_profile_path()
        shark_code = ShellIntegration.generate_bash_profile()
        marker_start = "# SHARK - Terminal Customization System"
        marker_end = "# FIM SHARK"
        
        existing_content = ""
        if profile_path.exists():
            existing_content = profile_path.read_text(encoding='utf-8')
        
        # Remove instalacao anterior
        if marker_start in existing_content:
            lines = existing_content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if marker_start in line:
                    skip = True
                elif marker_end in line:
                    skip = False
                    continue
                if not skip:
                    new_lines.append(line)
            existing_content = '\n'.join(new_lines).strip()
        
        new_content = existing_content + "\n" + shark_code
        profile_path.write_text(new_content, encoding='utf-8')
        
        return profile_path
    
    @staticmethod
    def uninstall_bash():
        """Remove do Bash"""
        profile_path = ShellIntegration.get_bash_profile_path()
        marker_start = "# SHARK - Terminal Customization System"
        marker_end = "# FIM SHARK"
        
        if not profile_path.exists():
            return False
        
        content = profile_path.read_text(encoding='utf-8')
        
        if marker_start not in content:
            return False
        
        lines = content.split('\n')
        new_lines = []
        skip = False
        for line in lines:
            if marker_start in line:
                skip = True
            elif marker_end in line:
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines).strip()
        profile_path.write_text(new_content, encoding='utf-8')
        
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ZSH
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def get_zsh_profile_path():
        """Retorna caminho do .zshrc"""
        return Path.home() / ".zshrc"
    
    @staticmethod
    def generate_zsh_profile():
        """Gera codigo para Zsh"""
        shark_path = str(ShellIntegration.SHARK_SCRIPT)
        
        return f'''
# ═══════════════════════════════════════════════════════════════════════════════
# SHARK - Terminal Customization System
# Instalado automaticamente pelo Shark
# Para remover: python3 "{shark_path}" uninstall
# ═══════════════════════════════════════════════════════════════════════════════

# Habilita cores
export TERM="xterm-256color"
export FORCE_COLOR=1

# Funcao para prompt do Shark
shark_prompt() {{
    python3 "{shark_path}" prompt 2>/dev/null
}}

# Exibe banner ao iniciar
python3 "{shark_path}" banner

# Sobrescreve PROMPT
setopt PROMPT_SUBST
export PROMPT='$(shark_prompt)'

# Aliases
alias shark='python3 "{shark_path}"'
alias shark-banner='python3 "{shark_path}" banner'
alias shark-matrix='python3 "{shark_path}" matrix'
shark-rainbow() {{ python3 "{shark_path}" rainbow "$@"; }}

# ═══════════════════════════════════════════════════════════════════════════════
# FIM SHARK
# ═══════════════════════════════════════════════════════════════════════════════
'''
    
    @staticmethod
    def install_zsh():
        """Instala no Zsh"""
        profile_path = ShellIntegration.get_zsh_profile_path()
        shark_code = ShellIntegration.generate_zsh_profile()
        marker_start = "# SHARK - Terminal Customization System"
        marker_end = "# FIM SHARK"
        
        existing_content = ""
        if profile_path.exists():
            existing_content = profile_path.read_text(encoding='utf-8')
        
        if marker_start in existing_content:
            lines = existing_content.split('\n')
            new_lines = []
            skip = False
            for line in lines:
                if marker_start in line:
                    skip = True
                elif marker_end in line:
                    skip = False
                    continue
                if not skip:
                    new_lines.append(line)
            existing_content = '\n'.join(new_lines).strip()
        
        new_content = existing_content + "\n" + shark_code
        profile_path.write_text(new_content, encoding='utf-8')
        
        return profile_path
    
    @staticmethod
    def uninstall_zsh():
        """Remove do Zsh"""
        profile_path = ShellIntegration.get_zsh_profile_path()
        marker_start = "# SHARK - Terminal Customization System"
        marker_end = "# FIM SHARK"
        
        if not profile_path.exists():
            return False
        
        content = profile_path.read_text(encoding='utf-8')
        
        if marker_start not in content:
            return False
        
        lines = content.split('\n')
        new_lines = []
        skip = False
        for line in lines:
            if marker_start in line:
                skip = True
            elif marker_end in line:
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines).strip()
        profile_path.write_text(new_content, encoding='utf-8')
        
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CMD (Windows) - via AutoRun no Registro
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def generate_cmd_script():
        """Gera script batch para CMD"""
        shark_path = str(ShellIntegration.SHARK_SCRIPT)
        script_path = CONFIG_DIR / "shark_autorun.bat"
        
        content = f'''@echo off
REM SHARK - Terminal Customization System
python "{shark_path}" banner
doskey shark=python "{shark_path}" $*
doskey shark-banner=python "{shark_path}" banner
doskey shark-matrix=python "{shark_path}" matrix
title Shark Terminal
'''
        
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        script_path.write_text(content, encoding='utf-8')
        return script_path
    
    @staticmethod
    def install_cmd():
        """Instala no CMD via registro"""
        if SYSTEM != 'windows':
            return None
        
        try:
            import winreg
            
            script_path = ShellIntegration.generate_cmd_script()
            
            # Abre/cria chave do registro
            key_path = r"Software\Microsoft\Command Processor"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            
            # Define AutoRun
            winreg.SetValueEx(key, "AutoRun", 0, winreg.REG_SZ, str(script_path))
            winreg.CloseKey(key)
            
            return script_path
        except Exception as e:
            return None
    
    @staticmethod
    def uninstall_cmd():
        """Remove do CMD"""
        if SYSTEM != 'windows':
            return False
        
        try:
            import winreg
            
            key_path = r"Software\Microsoft\Command Processor"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            
            try:
                winreg.DeleteValue(key, "AutoRun")
            except FileNotFoundError:
                pass
            
            winreg.CloseKey(key)
            
            # Remove script
            script_path = CONFIG_DIR / "shark_autorun.bat"
            if script_path.exists():
                script_path.unlink()
            
            return True
        except Exception:
            return False
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TERMUX
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def install_termux():
        """Instala no Termux"""
        return ShellIntegration.install_bash()
    
    @staticmethod
    def uninstall_termux():
        """Remove do Termux"""
        return ShellIntegration.uninstall_bash()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INSTALACAO AUTOMATICA
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def install_all():
        """Instala em todos os shells disponiveis"""
        results = {}
        
        if SYSTEM == 'windows':
            # PowerShell
            try:
                path = ShellIntegration.install_powershell()
                results['PowerShell'] = str(path)
            except Exception as e:
                results['PowerShell'] = f"Erro: {e}"
            
            # CMD
            try:
                path = ShellIntegration.install_cmd()
                results['CMD'] = str(path) if path else "Erro ao instalar"
            except Exception as e:
                results['CMD'] = f"Erro: {e}"
        else:
            # Bash
            try:
                path = ShellIntegration.install_bash()
                results['Bash'] = str(path)
            except Exception as e:
                results['Bash'] = f"Erro: {e}"
            
            # Zsh (se existir)
            zshrc = Path.home() / ".zshrc"
            if zshrc.exists() or (Path.home() / ".oh-my-zsh").exists():
                try:
                    path = ShellIntegration.install_zsh()
                    results['Zsh'] = str(path)
                except Exception as e:
                    results['Zsh'] = f"Erro: {e}"
        
        return results
    
    @staticmethod
    def uninstall_all():
        """Remove de todos os shells"""
        results = {}
        
        if SYSTEM == 'windows':
            results['PowerShell'] = ShellIntegration.uninstall_powershell()
            results['CMD'] = ShellIntegration.uninstall_cmd()
        else:
            results['Bash'] = ShellIntegration.uninstall_bash()
            results['Zsh'] = ShellIntegration.uninstall_zsh()
        
        return results
    
    @staticmethod
    def check_installation():
        """Verifica onde o Shark esta instalado"""
        installed = {}
        marker = "# SHARK - Terminal Customization System"
        
        if SYSTEM == 'windows':
            # PowerShell
            ps_profile = ShellIntegration.get_powershell_profile_path()
            if ps_profile.exists():
                content = ps_profile.read_text(encoding='utf-8')
                installed['PowerShell'] = marker in content
            else:
                installed['PowerShell'] = False
            
            # CMD
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Command Processor")
                try:
                    value, _ = winreg.QueryValueEx(key, "AutoRun")
                    installed['CMD'] = "shark" in value.lower()
                except FileNotFoundError:
                    installed['CMD'] = False
                winreg.CloseKey(key)
            except:
                installed['CMD'] = False
        else:
            # Bash
            bashrc = ShellIntegration.get_bash_profile_path()
            if bashrc.exists():
                content = bashrc.read_text(encoding='utf-8')
                installed['Bash'] = marker in content
            else:
                installed['Bash'] = False
            
            # Zsh
            zshrc = ShellIntegration.get_zsh_profile_path()
            if zshrc.exists():
                content = zshrc.read_text(encoding='utf-8')
                installed['Zsh'] = marker in content
            else:
                installed['Zsh'] = False
        
        return installed


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCOES DE INSTALACAO CLI
# ═══════════════════════════════════════════════════════════════════════════════

def install_shark():
    """Instala Shark no terminal - fica PERMANENTE"""
    print(f"""
{Colors.CYAN}{'='*60}{Colors.RESET}
{Colors.BOLD}  SHARK - Instalacao no Terminal{Colors.RESET}
{Colors.CYAN}{'='*60}{Colors.RESET}
""")
    
    print(f"  {Colors.YELLOW}Isso vai:{Colors.RESET}")
    print(f"  - Exibir o banner ao abrir o terminal")
    print(f"  - Substituir o prompt padrao pelo do Shark")
    print(f"  - Adicionar comandos: shark, shark-banner, shark-matrix")
    print()
    
    confirm = input(f"  {Colors.hex('#00FF88')}Continuar? (s/n):{Colors.RESET} ").strip().lower()
    
    if confirm != 's':
        print(f"\n  {Colors.YELLOW}Instalacao cancelada.{Colors.RESET}\n")
        return
    
    print(f"\n  {Colors.CYAN}Instalando...{Colors.RESET}\n")
    
    results = ShellIntegration.install_all()
    
    for shell, result in results.items():
        if "Erro" in str(result):
            print(f"  {Colors.RED}[X] {shell}: {result}{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}[V] {shell}: {result}{Colors.RESET}")
    
    print(f"""
{Colors.GREEN}{'='*60}{Colors.RESET}
  Instalacao concluida!
  
  {Colors.BOLD}Proximo passo:{Colors.RESET}
  Feche e abra o terminal novamente para ver as mudancas.
  
  {Colors.DIM}Para remover: python shark.py uninstall{Colors.RESET}
{Colors.GREEN}{'='*60}{Colors.RESET}
""")


def uninstall_shark():
    """Remove Shark do terminal"""
    print(f"""
{Colors.CYAN}{'='*60}{Colors.RESET}
{Colors.BOLD}  SHARK - Remover do Terminal{Colors.RESET}
{Colors.CYAN}{'='*60}{Colors.RESET}
""")
    
    confirm = input(f"  {Colors.hex('#FF6B6B')}Remover Shark do terminal? (s/n):{Colors.RESET} ").strip().lower()
    
    if confirm != 's':
        print(f"\n  {Colors.YELLOW}Operacao cancelada.{Colors.RESET}\n")
        return
    
    print(f"\n  {Colors.CYAN}Removendo...{Colors.RESET}\n")
    
    results = ShellIntegration.uninstall_all()
    
    for shell, success in results.items():
        if success:
            print(f"  {Colors.GREEN}[V] {shell}: Removido{Colors.RESET}")
        else:
            print(f"  {Colors.DIM}[-] {shell}: Nao estava instalado{Colors.RESET}")
    
    print(f"""
{Colors.GREEN}{'='*60}{Colors.RESET}
  Shark removido do terminal.
  Feche e abra o terminal para restaurar o padrao.
{Colors.GREEN}{'='*60}{Colors.RESET}
""")


def check_status():
    """Verifica status da instalacao"""
    print(f"""
{Colors.CYAN}{'='*60}{Colors.RESET}
{Colors.BOLD}  SHARK - Status da Instalacao{Colors.RESET}
{Colors.CYAN}{'='*60}{Colors.RESET}
""")
    
    installed = ShellIntegration.check_installation()
    
    for shell, is_installed in installed.items():
        if is_installed:
            print(f"  {Colors.GREEN}[V] {shell}: Instalado{Colors.RESET}")
        else:
            print(f"  {Colors.DIM}[-] {shell}: Nao instalado{Colors.RESET}")
    
    print(f"""
  {Colors.DIM}Script: {ShellIntegration.SHARK_SCRIPT}{Colors.RESET}
  {Colors.DIM}Config: {CONFIG_FILE}{Colors.RESET}
""")


def run_updater():
    """Executa o atualizador"""
    import subprocess
    
    updater_path = Path(__file__).parent / "shark_update.py"
    
    if not updater_path.exists():
        print(f"{Colors.RED}[X] shark_update.py nao encontrado{Colors.RESET}")
        print(f"{Colors.DIM}Baixe do repositorio GitHub{Colors.RESET}")
        return
    
    subprocess.run([sys.executable, str(updater_path)])


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCAO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcao principal"""
    shark = Shark()
    
    # Verifica autenticação
    if shark.config.get("password_protected", False):
        if not Security.authenticate():
            sys.exit(1)
    
    # Comandos CLI
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        commands = {
            "banner": lambda: shark.show_banner(),
            "prompt": lambda: print(shark.get_prompt(), end=""),
            "colors": lambda: shark.full_demo(),
            "config": lambda: print(json.dumps(shark.config, indent=2)),
            "matrix": lambda: Animations.matrix_rain(duration=10),
            "rainbow": lambda: print(Colors.rainbow(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "SHARK")),
            "typing": lambda: Animations.typing_effect(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Hello Shark!"),
            "install": lambda: install_shark(),
            "uninstall": lambda: uninstall_shark(),
            "status": lambda: check_status(),
            "update": lambda: run_updater(),
        }
        
        if cmd in commands:
            commands[cmd]()
        elif cmd in ("--help", "-h", "help"):
            print(f"""
{Colors.CYAN}SHARK - Sistema de Personalizacao TOTAL{Colors.RESET}

{Colors.BOLD}Uso:{Colors.RESET}
  python shark.py              Abre o menu interativo
  python shark.py install      INSTALA no terminal (permanente)
  python shark.py uninstall    Remove do terminal
  python shark.py status       Verifica instalacao
  python shark.py update       Atualiza via GitHub
  python shark.py banner       Exibe o banner
  python shark.py prompt       Exibe o prompt customizado
  python shark.py colors       Demo de cores
  python shark.py matrix       Efeito Matrix Rain
  python shark.py rainbow [texto]  Texto com arco-iris
  python shark.py typing [texto]   Efeito digitacao
  python shark.py config       Mostra configuracao

{Colors.BOLD}Terminal:{Colors.RESET} {TERMINAL}
{Colors.BOLD}Sistema:{Colors.RESET} {SYSTEM}
{Colors.BOLD}Config:{Colors.RESET} {CONFIG_FILE}
""")
        else:
            print(f"{Colors.RED}Comando não reconhecido. Use --help{Colors.RESET}")
    else:
        shark.interactive_menu()


if __name__ == "__main__":
    main()

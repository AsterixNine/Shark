<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:006994,100:00CED1&height=200&section=header&text=SHARK&fontSize=80&fontColor=fff&animation=fadeIn&fontAlignY=35&desc=Sistema%20de%20Personaliza%C3%A7%C3%A3o%20Total%20para%20Terminais&descAlignY=55&descSize=18" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows"/>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>
  <img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS"/>
  <img src="https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=android&logoColor=white" alt="Termux"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Version-2.0-blue?style=flat-square" alt="Version"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status"/>
</p>

<br>

<p align="center">
  <b>Personalize ABSOLUTAMENTE TUDO no seu terminal.</b><br>
  Cores, banners, prompts, animacoes, barras de progresso e muito mais.
</p>

<br>

---

<br>

## Indice

- [Sobre](#sobre)
- [Recursos](#recursos)
- [Instalacao](#instalacao)
- [Uso](#uso)
- [Personalizacao](#personalizacao)
  - [Cores e Temas](#cores-e-temas)
  - [Banners](#banners)
  - [Prompts](#prompts)
  - [Animacoes](#animacoes)
  - [Seguranca](#seguranca)
- [Comandos CLI](#comandos-cli)
- [Configuracao](#configuracao)
- [Compatibilidade](#compatibilidade)
- [Contribuicao](#contribuicao)
- [Licenca](#licenca)
- [Autor](#autor)

<br>

---

<br>

## Sobre

**Shark** e um sistema de personalizacao completo para terminais, desenvolvido em Python. Projetado para funcionar em qualquer ambiente - Windows (CMD, PowerShell, VS Code Terminal, Windows Terminal), Linux, macOS e Termux.

O objetivo e simples: permitir que voce personalize **tudo** no seu terminal sem limitacoes.

<br>

<p align="center">
  <img src="https://raw.githubusercontent.com/sindresorhus/cli-spinners/main/screenshot.gif" alt="Terminal Demo" width="600"/>
</p>

<br>

---

<br>

## Recursos

<table>
  <tr>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/000000/paint-palette.png" width="48"/>
      <br><b>16 Milhoes de Cores</b>
      <br><sub>RGB, HEX, ANSI 256, gradientes</sub>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/000000/image.png" width="48"/>
      <br><b>Banners ASCII</b>
      <br><sub>Predefinidos e personalizados</sub>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/000000/console.png" width="48"/>
      <br><b>10 Estilos de Prompt</b>
      <br><sub>Ou crie o seu proprio</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/000000/video.png" width="48"/>
      <br><b>Animacoes</b>
      <br><sub>Typing, fade, glitch, matrix</sub>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/000000/loading-bar.png" width="48"/>
      <br><b>Barras de Progresso</b>
      <br><sub>12 estilos diferentes</sub>
    </td>
    <td align="center" width="33%">
      <img src="https://img.icons8.com/fluency/96/000000/lock.png" width="48"/>
      <br><b>Protecao por Senha</b>
      <br><sub>Hash seguro PBKDF2</sub>
    </td>
  </tr>
</table>

<br>

### Lista Completa

```
[x] Sistema de cores RGB/HEX com 16 milhoes de cores
[x] 15 paletas de cores predefinidas
[x] Gradientes lineares e multi-cor
[x] Efeito rainbow (arco-iris)
[x] 8 banners ASCII predefinidos
[x] Criacao de banners personalizados
[x] Geracao de banners a partir de texto
[x] 10 templates de prompt
[x] Prompt totalmente customizavel
[x] 13 estilos de spinner
[x] 12 estilos de barra de progresso
[x] Animacao typing (digitacao)
[x] Animacao fade in/out
[x] Efeito glitch
[x] Efeito matrix rain
[x] Ciclo de cores animado
[x] Protecao por senha com hash seguro
[x] Configuracao persistente em JSON
[x] Suporte nativo a Windows (VT100)
[x] Compativel com VS Code Terminal
[x] Compativel com Termux
```

<br>

---

<br>

## Instalacao

### Requisitos

- Python 3.7 ou superior
- Nenhuma dependencia externa

### Clone o Repositorio

```bash
git clone https://github.com/seuusuario/shark.git
cd shark
```

### Ou Baixe Diretamente

```bash
curl -O https://raw.githubusercontent.com/seuusuario/shark/main/shark.py
```

### Instalacao Global (Opcional)

**Windows (PowerShell como Admin):**
```powershell
copy shark.py C:\Windows\System32\shark.py
```

**Linux/macOS:**
```bash
sudo cp shark.py /usr/local/bin/shark
sudo chmod +x /usr/local/bin/shark
```

<br>

---

<br>

## Uso

### Menu Interativo

```bash
python shark.py
```

<p align="center">
  <img src="https://user-images.githubusercontent.com/placeholder/shark-menu.gif" alt="Menu Demo" width="600"/>
</p>

### Comandos Rapidos

```bash
python shark.py banner       # Exibe o banner configurado
python shark.py prompt       # Exibe o prompt customizado
python shark.py matrix       # Efeito Matrix Rain
python shark.py colors       # Demo de cores
python shark.py config       # Mostra configuracao JSON
```

<br>

---

<br>

## Personalizacao

### Cores e Temas

Shark oferece 15 paletas de cores predefinidas:

| Paleta | Cores | Uso |
|--------|-------|-----|
| `ocean` | Azul, turquesa, verde-agua | Tema padrao |
| `fire` | Vermelho, laranja, amarelo | Alto contraste |
| `forest` | Tons de verde | Natural |
| `sunset` | Rosa, laranja, amarelo | Quente |
| `neon` | Magenta, ciano, verde | Vibrante |
| `cyberpunk` | Verde neon, azul, roxo | Futurista |
| `matrix` | Tons de verde | Estilo hacker |
| `galaxy` | Azul escuro, roxo | Espacial |
| `blood` | Tons de vermelho | Escuro |
| `ice` | Azul claro, branco | Frio |
| `gold` | Dourado, amarelo | Elegante |
| `purple_rain` | Tons de roxo | Misterioso |
| `toxic` | Verde neon, amarelo | Radioativo |
| `pastel` | Cores suaves | Minimalista |
| `dark` | Escuro com destaques | Profissional |

**Uso programatico:**

```python
from shark import Colors

# Cor RGB
print(f"{Colors.rgb(255, 100, 50)}Texto colorido{Colors.RESET}")

# Cor HEX
print(f"{Colors.hex('#FF6432')}Texto colorido{Colors.RESET}")

# Gradiente
print(Colors.gradient("Texto com gradiente", "#FF0000", "#0000FF"))

# Rainbow
print(Colors.rainbow("Texto arco-iris"))

# Multi-gradiente
print(Colors.multi_gradient("Texto", ["#FF0000", "#00FF00", "#0000FF"]))
```

<br>

### Banners

#### Banners Predefinidos

| Nome | Estilo |
|------|--------|
| `SHARK` | ASCII classico |
| `SHARK_MINI` | Compacto com blocos |
| `SHARK_WAVE` | Com ondas decorativas |
| `SHARK_3D` | Efeito 3D |
| `SHARK_BLOCK` | Com bordas |
| `HACKER` | Estilo terminal |
| `MINIMAL` | Simples |
| `OCEAN` | Com ondas |

#### Criar Banner Personalizado

No menu interativo, selecione `Banners > Criar banner personalizado` e digite seu ASCII art.

Os banners sao salvos em:
- **Windows:** `%APPDATA%\Shark\banners\`
- **Linux/Mac:** `~/.config/shark/banners/`
- **Termux:** `~/.shark/banners/`

#### Gerar Banner de Texto

```python
from shark import Banners

banner = Banners.generate_text_banner("MEU APP")
print(banner)
```

Saida:
```
█▄█ █▀▀ █ █   █▀█ █▀█ █▀█ 
█ █ █▀▀ █▄█   █▀█ █▀▀ █▀▀ 
▀ ▀ ▀▀▀ ▀ ▀   ▀ ▀ ▀   ▀   
```

<br>

### Prompts

| Estilo | Preview |
|--------|---------|
| `minimal` | `user@host ~/path $` |
| `shark` | `[shark] ~/path >` |
| `powerline` | ` user   ~/path ` |
| `arrow` | `[user@host]-[~/path] ->` |
| `simple` | `~/path >` |
| `hacker` | `[12:30:45] user@host:~/path#` |
| `lambda` | `[lambda] ~/path ->` |
| `git` | `[branch] ~/path >` |
| `neon` | `[diamond] ~/path >>` |
| `box` | `[user]-[~/path] $` |

#### Prompt Customizado

Variaveis disponiveis:
- `{user}` - Nome do usuario
- `{host}` - Nome do host
- `{cwd}` - Diretorio atual
- `{time}` - Hora atual
- `{date}` - Data atual
- `{system}` - Sistema operacional
- `{terminal}` - Terminal detectado

```python
from shark import Prompt

# Usando template
prompt = Prompt.render("hacker", color="#00FF00")

# Template customizado
prompt = Prompt.render(custom_template="[{time}] {user} > ", color="#00BFFF")
```

<br>

### Animacoes

#### Spinners Disponiveis

| Nome | Frames |
|------|--------|
| `dots` | Pontos girando |
| `line` | Linha rotativa |
| `arrow` | Setas direcionais |
| `bounce` | Efeito quicando |
| `shark` | Tubarao nadando |
| `wave` | Ondas |
| `pulse` | Pulsacao |
| `clock` | Relogio |
| `moon` | Fases da lua |
| `earth` | Globo girando |
| `hearts` | Coracoes coloridos |
| `fire` | Chamas |
| `blocks` | Barras verticais |

#### Uso

```python
from shark import Animations

# Efeito digitacao
Animations.typing_effect("Carregando sistema...", delay=0.03, color="#00FF00")

# Fade in
Animations.fade_in("SHARK", steps=10, color="#00BFFF")

# Glitch
Animations.glitch_text("ERROR", intensity=3, duration=2)

# Matrix rain
Animations.matrix_rain(duration=5)

# Spinner
Animations.spinner("Processando", style="dots", duration=3, color="#FF00FF")

# Barra de progresso animada
Animations.progress_animated(100, width=40, color="#00FF88")

# Ciclo de cores
Animations.color_cycle("SHARK", duration=3)
```

<br>

### Seguranca

Shark permite proteger o acesso com senha usando hash PBKDF2-SHA256.

```python
from shark import Security

# Definir senha
Security.save_credentials("minha_senha_segura")

# Verificar se existe senha
if Security.is_password_set():
    # Autenticar
    if Security.authenticate():
        print("Acesso permitido")

# Remover senha
Security.remove_password()
```

As credenciais sao armazenadas de forma segura:
- Hash PBKDF2 com 100.000 iteracoes
- Salt aleatorio de 32 bytes
- Arquivo oculto no sistema

<br>

---

<br>

## Comandos CLI

```
shark.py [comando] [argumentos]

Comandos:
  (nenhum)         Abre o menu interativo
  banner           Exibe o banner configurado
  prompt           Retorna o prompt customizado
  colors           Demonstracao de cores
  matrix           Efeito Matrix Rain (10 segundos)
  rainbow [texto]  Aplica efeito arco-iris no texto
  typing [texto]   Efeito de digitacao no texto
  config           Exibe configuracao em JSON
  --help, -h       Mostra ajuda
```

### Exemplos

```bash
# Banner no inicio do terminal
python shark.py banner

# Prompt customizado para PS1
export PS1=$(python shark.py prompt)

# Texto decorativo
python shark.py rainbow "Build Successful"
python shark.py typing "Iniciando servidor..."

# Efeito visual
python shark.py matrix
```

<br>

---

<br>

## Configuracao

### Arquivo de Configuracao

| Sistema | Localizacao |
|---------|-------------|
| Windows | `%APPDATA%\Shark\config.json` |
| Linux | `~/.config/shark/config.json` |
| macOS | `~/.config/shark/config.json` |
| Termux | `~/.shark/config.json` |

### Estrutura

```json
{
  "theme": "shark",
  "banner": "SHARK",
  "banner_colors": ["#00BFFF", "#0080FF"],
  "prompt_style": "shark",
  "prompt_color": "#00BFFF",
  "progress_style": "default",
  "show_banner_on_start": true,
  "password_protected": false,
  "animations_enabled": true,
  "default_animation_speed": 0.05,
  "terminal_title": "Shark Terminal",
  "custom_prompt": null
}
```

### Diretorios

```
Shark/
  |- config.json      # Configuracao principal
  |- .credentials     # Hash da senha (oculto)
  |- themes/          # Temas customizados
  |- banners/         # Banners personalizados (.txt)
  |- animations/      # Animacoes customizadas
```

<br>

---

<br>

## Compatibilidade

### Terminais Testados

| Terminal | Status | Notas |
|----------|--------|-------|
| Windows Terminal | Completo | Suporte total |
| PowerShell 7+ | Completo | Suporte total |
| PowerShell 5.1 | Completo | VT100 habilitado automaticamente |
| CMD | Completo | VT100 habilitado automaticamente |
| VS Code Terminal | Completo | Detectado automaticamente |
| ConEmu | Completo | Suporte total |
| Git Bash | Completo | Suporte total |
| WSL | Completo | Suporte total |
| GNOME Terminal | Completo | Suporte total |
| Konsole | Completo | Suporte total |
| iTerm2 | Completo | Suporte total |
| Terminal.app | Completo | Suporte total |
| Termux | Completo | Detectado automaticamente |

### Deteccao Automatica

Shark detecta automaticamente:
- Sistema operacional (Windows, Linux, macOS)
- Tipo de terminal
- Ambiente Termux
- VS Code Terminal
- Suporte a cores ANSI

<br>

---

<br>

## Contribuicao

Contribuicoes sao bem-vindas. Por favor:

1. Fork o repositorio
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudancas (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Diretrizes

- Mantenha compatibilidade com Python 3.7+
- Nao adicione dependencias externas
- Teste em Windows e Linux
- Documente novas funcionalidades

<br>

---

<br>

## Licenca

Este projeto esta licenciado sob a [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

<br>

---

<br>

## Autor

<p align="center">
  <img src="https://img.shields.io/badge/Desenvolvido%20com-Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<p align="center">
  <a href="https://github.com/seuusuario">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

<br>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:006994,100:00CED1&height=120&section=footer" width="100%"/>
</p>

"""Gera as figuras ilustrativas usadas no README do desafio.

Uso:
    python images/gerar_diagramas.py

Gera:
  - 2 diagramas didaticos (fluxo no setoolkit e arquitetura do laboratorio)
  - 3 simulacoes visuais de tela (terminal setoolkit, pagina simulada e
    arquivo de credencias ficticias)

ATENCAO: as simulacoes NAO sao capturas de tela reais. Elas contem uma
identificacao visivel ("SIMULACAO GERADA") e devem ser usadas apenas como
documentacao ilustrativa do fluxo esperado.
"""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).resolve().parent
FONTES = Path(matplotlib.get_data_path()) / "fonts" / "ttf"


def fonte(nome, tamanho):
    return ImageFont.truetype(str(FONTES / nome), tamanho)


MONO = "DejaVuSansMono.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

COR_FUNDO = "#0d1117"
COR_CAIXA = "#161b22"
COR_BORDA = "#30363d"
COR_TEXTO = "#e6edf3"
COR_DESTAQUE = "#2f81f7"
COR_SEGURANCA = "#3fb950"


# ---------------------------------------------------------------------------
# Diagramas (matplotlib)
# ---------------------------------------------------------------------------


def caixa(ax, x, y, largura, altura, texto, destaque=False):
    cor = COR_DESTAQUE if destaque else COR_BORDA
    patch = FancyBboxPatch(
        (x - largura / 2, y - altura / 2),
        largura,
        altura,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        linewidth=1.6,
        edgecolor=cor,
        facecolor=COR_CAIXA,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        texto,
        color=COR_TEXTO,
        fontsize=14,
        ha="center",
        va="center",
        family="DejaVu Sans",
    )


def seta(ax, x, y1, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x, y1),
            (x, y2),
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=1.6,
            color=COR_SEGURANCA,
        )
    )


def estilo(ax, titulo):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(COR_FUNDO)
    ax.set_title(titulo, color=COR_TEXTO, fontsize=18, pad=18, weight="bold")
    ax.text(
        0.5,
        0.02,
        "Ilustração didática — não é uma captura de tela",
        color="#8b949e",
        fontsize=10,
        ha="center",
        va="bottom",
    )


def gerar_fluxo_setoolkit():
    fig, ax = plt.subplots(figsize=(9, 11), facecolor=COR_FUNDO)
    estilo(ax, "Fluxo no setoolkit — Credential Harvester (Site Cloner)")

    etapas = [
        "setoolkit",
        "1  Social-Engineering Attacks",
        "2  Website Attack Vectors",
        "3  Credential Harvester Attack Method",
        "4  Site Cloner",
        "ifconfig → IP do Kali",
        "URL do alvo (simulação: Instagram)",
        "Site clonado em  http://<IP>:80",
    ]

    y_inicial = 0.90
    passo = 0.112
    for indice, texto in enumerate(etapas):
        y = y_inicial - indice * passo
        caixa(ax, 0.5, y, 0.80, 0.068, texto, destaque=indice == len(etapas) - 1)
        if indice < len(etapas) - 1:
            seta(ax, 0.5, y - 0.036, y - passo + 0.036)

    fig.savefig(
        PASTA / "01-fluxo-setoolkit.png",
        dpi=150,
        bbox_inches="tight",
        facecolor=COR_FUNDO,
    )
    plt.close(fig)


def gerar_arquitetura_lab():
    fig, ax = plt.subplots(figsize=(11, 6), facecolor=COR_FUNDO)
    estilo(ax, "Arquitetura do laboratório isolado")

    caixa(ax, 0.17, 0.52, 0.26, 0.24, "Kali Linux\n(setoolkit)\nIP local", destaque=True)
    caixa(ax, 0.50, 0.52, 0.26, 0.24, "Rede interna\n(host-only)\nSem internet")
    caixa(ax, 0.83, 0.52, 0.26, 0.24, "Máquina de teste\n(navegador)\nLogin fictício")

    ax.add_patch(
        FancyArrowPatch(
            (0.31, 0.52),
            (0.36, 0.52),
            arrowstyle="<|-|>",
            mutation_scale=18,
            linewidth=1.6,
            color=COR_SEGURANCA,
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            (0.64, 0.52),
            (0.69, 0.52),
            arrowstyle="<|-|>",
            mutation_scale=18,
            linewidth=1.6,
            color=COR_SEGURANCA,
        )
    )

    ax.text(
        0.5,
        0.24,
        "Todas as credenciais usadas nos testes são fictícias e o ambiente não é exposto externamente.",
        color="#8b949e",
        fontsize=11,
        ha="center",
        va="center",
    )

    fig.savefig(
        PASTA / "02-arquitetura-lab.png",
        dpi=150,
        bbox_inches="tight",
        facecolor=COR_FUNDO,
    )
    plt.close(fig)


# ---------------------------------------------------------------------------
# Simulações visuais (PIL) — NÃO são capturas de tela
# ---------------------------------------------------------------------------


def aplicar_identificacao(img, rotulo):
    """Marca a imagem como simulação, com faixa inferior e marca diagonal."""
    marca = Image.new("RGBA", (620, 80), (0, 0, 0, 0))
    md = ImageDraw.Draw(marca)
    md.text((0, 0), "SIMULAÇÃO", font=fonte(SANS_BOLD, 68), fill=(255, 255, 255, 42))
    girada = marca.rotate(28, expand=True)

    for y in range(-girada.height, img.height, girada.height + 110):
        for x in range(-girada.width, img.width, girada.width + 150):
            img.paste(girada, (x, y), girada)

    desenho = ImageDraw.Draw(img)
    altura = img.height
    desenho.rectangle([0, altura - 48, img.width, altura], fill="#7a2e0e")
    desenho.text(
        (18, altura - 33),
        f"{rotulo} — ilustração gerada, não é uma captura de tela real",
        font=fonte(SANS, 16),
        fill="#ffffff",
    )
    return img


def janela_terminal(caminho, titulo, linhas, tamanho):
    largura, altura = tamanho
    img = Image.new("RGB", (largura, altura), "#0b0b0b")
    d = ImageDraw.Draw(img)

    # Barra de titulo
    d.rectangle([0, 0, largura, 46], fill="#2b2b2b")
    for indice, cor in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        x = 22 + indice * 26
        d.ellipse([x, 15, x + 14, 29], fill=cor)
    d.text((130, 12), titulo, font=fonte(MONO, 17), fill="#cccccc")

    # Linhas do terminal
    y = 72
    for texto, cor in linhas:
        d.text((28, y), texto, font=fonte(MONO, 17), fill=cor)
        y += 24

    aplicar_identificacao(img, "TERMINAL SIMULADO")
    img.save(caminho)
    print("Gerado:", caminho.name)


def gerar_menu_setoolkit():
    verde = "#3fb950"
    cinza = "#8b949e"
    branco = "#e6edf3"
    azul = "#58a6ff"

    linhas = [
        ("root@kali:~# sudo su", verde),
        ("root@kali:~# setoolkit", verde),
        ("", branco),
        ("[---] The Social-Engineer Toolkit (SET) [---]", azul),
        ("[---] Versao 8.0.3 - laboratorio isolado   [---]", azul),
        ("", branco),
        ("Select from the menu:", branco),
        ("", branco),
        ("   1) Social-Engineering Attacks", branco),
        ("   2) Penetration Testing (Fast-Track)", cinza),
        ("   3) Third Party Modules", cinza),
        ("  99) Exit the Social-Engineer Toolkit", cinza),
        ("", branco),
        ("set> 1", verde),
        ("", branco),
        ("   1) Spear-Phishing Attack Vectors", cinza),
        ("   2) Website Attack Vectors", branco),
        ("   3) Infectious Media Generator", cinza),
        ("  99) Return back to the main menu.", cinza),
        ("", branco),
        ("set> 2", verde),
        ("", branco),
        ("   1) Java Applet Attack Method", cinza),
        ("   2) Metasploit Browser Exploit Method", cinza),
        ("   3) Credential Harvester Attack Method", branco),
        ("   4) Tabnabbing Attack Method", cinza),
        ("  99) Return to Main Menu", cinza),
        ("", branco),
        ("set> 3", verde),
        ("", branco),
        ("   1) Web Templates", cinza),
        ("   2) Site Cloner", branco),
        ("   3) Custom Import", cinza),
        ("  99) Return to Main Menu", cinza),
        ("", branco),
        ("set> 2", verde),
        ("", branco),
        (" [-] Modo Site Cloner selecionado.", azul),
        (" [-] IP de escuta: 192.168.56.101 (host-only)", azul),
        (" [-] URL para clonar: http://127.0.0.1:8000/", azul),
    ]

    janela_terminal(
        PASTA / "03-menu-setoolkit.png",
        "root@kali:~  —  setoolkit",
        linhas,
        (1500, 1140),
    )


def gerar_pagina_simulada():
    largura, altura = 1400, 900
    img = Image.new("RGB", (largura, altura), "#fafafa")
    d = ImageDraw.Draw(img)

    # Navegador
    d.rectangle([0, 0, largura, 110], fill="#e9edf2")
    d.rounded_rectangle([18, 14, 250, 50], radius=8, fill="#ffffff")
    d.text((34, 21), "Instagram — Laboratório", font=fonte(SANS, 15), fill="#333333")
    d.rounded_rectangle([18, 58, largura - 18, 98], radius=8, fill="#ffffff")
    d.text(
        (36, 67),
        "http://192.168.56.101/",
        font=fonte(MONO, 16),
        fill="#262626",
    )

    # Aviso de ambiente simulado
    d.rectangle([0, 110, largura, 168], fill="#b62324")
    d.text(
        (28, 128),
        "AMBIENTE DE TESTE — PÁGINA SIMULADA. NÃO INSIRA DADOS REAIS.",
        font=fonte(SANS_BOLD, 20),
        fill="#ffffff",
    )

    # Cartao de login
    cartao = (420, 210, 980, 780)
    d.rounded_rectangle(cartao, radius=14, fill="#ffffff", outline="#dbdbdb", width=2)

    titulo = "Instagram"
    ftitulo = fonte(SANS_BOLD, 52)
    largura_titulo = d.textlength(titulo, font=ftitulo)
    # Texto com gradiente simples
    x0 = largura // 2 - largura_titulo / 2
    for indice, caractere in enumerate(titulo):
        proporcao = indice / max(len(titulo) - 1, 1)
        cor = (
            int(249 - 160 * proporcao),
            int(113 + 60 * proporcao),
            int(53 + 100 * proporcao),
        )
        d.text((x0, 246), caractere, font=ftitulo, fill=cor)
        x0 += d.textlength(caractere, font=ftitulo)

    d.text(
        (largura // 2 - 205, 336),
        "Entre para ver o que há de novo no laboratório",
        font=fonte(SANS, 16),
        fill="#737373",
    )

    # Campos
    for indice, (rotulo, placeholder) in enumerate(
        [("Usuário", "usuario_teste"), ("Senha", "senha_ficticia_123")]
    ):
        y = 400 + indice * 110
        d.text((470, y), rotulo, font=fonte(SANS_BOLD, 16), fill="#262626")
        d.rounded_rectangle(
            [470, y + 28, 930, y + 78], radius=8, fill="#fafafa", outline="#dbdbdb", width=2
        )
        d.text((488, y + 42), placeholder, font=fonte(SANS, 17), fill="#a8a8a8")

    d.rounded_rectangle([470, 632, 930, 690], radius=8, fill="#0095f6")
    d.text(
        (largura // 2 - 28, 651),
        "Entrar",
        font=fonte(SANS_BOLD, 19),
        fill="#ffffff",
    )
    d.text(
        (largura // 2 - 76, 712),
        "Esqueceu a senha?",
        font=fonte(SANS, 15),
        fill="#0095f6",
    )

    d.text(
        (largura // 2 - 250, 808),
        "Página estática gerada para documentação do desafio.",
        font=fonte(SANS, 15),
        fill="#8e8e8e",
    )

    aplicar_identificacao(img, "PÁGINA SIMULADA")
    img.save(PASTA / "04-site-simulado.png")
    print("Gerado: 04-site-simulado.png")


def gerar_credenciais():
    verde = "#3fb950"
    cinza = "#8b949e"
    branco = "#e6edf3"
    azul = "#58a6ff"

    linhas = [
        ("root@kali:~# ls -l /var/www/html/harvest/", verde),
        ("total 8", cinza),
        ("-rw-r--r-- 1 root root 186 Nov 26 10:42 harvester.txt", branco),
        ("", branco),
        ("root@kali:~# cat /var/www/html/harvest/harvester.txt", verde),
        ("==================================================", azul),
        (" SET - CREDENTIAL HARVESTER (AMBIENTE DE LAB)     ", azul),
        ("==================================================", azul),
        ("[+] IP de origem  : 192.168.56.102", branco),
        ("[+] Usuario       : usuario_teste", branco),
        ("[+] Senha         : senha_ficticia_123", branco),
        ("[+] Horario       : 2026-11-26 10:42:17", branco),
        ("[+] Status        : captura simulada", branco),
        ("==================================================", azul),
        ("", branco),
        ("root@kali:~# echo 'Ambiente isolado - dados ficticios'", verde),
        ("Ambiente isolado - dados ficticios", cinza),
        ("", branco),
        ("[!] NENHUM DADO REAL FOI UTILIZADO NESTE TESTE", "#f85149"),
    ]

    janela_terminal(
        PASTA / "05-credenciais-capturadas.png",
        "root@kali:~  —  harvester.txt",
        linhas,
        (1400, 680),
    )


if __name__ == "__main__":
    gerar_fluxo_setoolkit()
    gerar_arquitetura_lab()
    gerar_menu_setoolkit()
    gerar_pagina_simulada()
    gerar_credenciais()
    print("Arquivos gerados em:", PASTA)

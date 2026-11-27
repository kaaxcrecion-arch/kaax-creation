#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_multilingual.py
Génère les 126 pages multilingues pour kaaxcreacion.com
7 pages service × 6 langues + 14 pages zone × 6 langues = 126 pages
Langues: fr (Français), en (English), it (Italiano), de (Deutsch), ru (Русский), pt (Português)
"""

import os
import sys

sys.path.insert(0, '/home/claude/kaax-creation')
from generate_pages import (
    COMMON_CSS, COMMON_JS, ZONE_DATA,
    FLAG_MX, FLAG_US, FLAG_FR, FLAG_IT, FLAG_DE, FLAG_RU, FLAG_PT,
    WA_URL, DOMAIN, ticker_html
)

# ═══════════════════════════════════════════════════════════════
# CONFIG LANGUES
# ═══════════════════════════════════════════════════════════════

LANG_META = {
    "fr": {"name": "Français", "flag": FLAG_FR, "html_lang": "fr", "locale": "fr_FR", "code": "FR"},
    "en": {"name": "English", "flag": FLAG_US, "html_lang": "en", "locale": "en_US", "code": "EN"},
    "it": {"name": "Italiano", "flag": FLAG_IT, "html_lang": "it", "locale": "it_IT", "code": "IT"},
    "de": {"name": "Deutsch", "flag": FLAG_DE, "html_lang": "de", "locale": "de_DE", "code": "DE"},
    "ru": {"name": "Русский", "flag": FLAG_RU, "html_lang": "ru", "locale": "ru_RU", "code": "RU"},
    "pt": {"name": "Português", "flag": FLAG_PT, "html_lang": "pt", "locale": "pt_BR", "code": "PT"},
}

LANGS = list(LANG_META.keys())

# ═══════════════════════════════════════════════════════════════
# NAV LABELS PAR LANGUE
# ═══════════════════════════════════════════════════════════════

NAV_LABELS = {
    "fr": {
        "cocinas": "Cuisines", "closets": "Dressings", "realizaciones": "Réalisations",
        "metodo": "Méthode", "nosotros": "À propos", "contacto": "Contact",
        "zona": "Zones", "cta": "Devis gratuit",
        "logo_sub": "Cuisines &amp; Dressings · Riviera Maya",
    },
    "en": {
        "cocinas": "Kitchens", "closets": "Closets", "realizaciones": "Portfolio",
        "metodo": "Method", "nosotros": "About", "contacto": "Contact",
        "zona": "Areas", "cta": "Free Quote",
        "logo_sub": "Kitchens &amp; Closets · Riviera Maya",
    },
    "it": {
        "cocinas": "Cucine", "closets": "Cabine Armadio", "realizaciones": "Realizzazioni",
        "metodo": "Metodo", "nosotros": "Chi Siamo", "contacto": "Contatto",
        "zona": "Zone", "cta": "Preventivo Gratuito",
        "logo_sub": "Cucine &amp; Armadi · Riviera Maya",
    },
    "de": {
        "cocinas": "Küchen", "closets": "Ankleideräume", "realizaciones": "Portfolio",
        "metodo": "Methode", "nosotros": "Über uns", "contacto": "Kontakt",
        "zona": "Gebiete", "cta": "Kostenloses Angebot",
        "logo_sub": "Küchen &amp; Einbauschränke · Riviera Maya",
    },
    "ru": {
        "cocinas": "Кухни", "closets": "Гардеробные", "realizaciones": "Портфолио",
        "metodo": "Метод", "nosotros": "О нас", "contacto": "Контакт",
        "zona": "Зоны", "cta": "Бесплатный расчёт",
        "logo_sub": "Кухни &amp; Гардеробные · Riviera Maya",
    },
    "pt": {
        "cocinas": "Cozinhas", "closets": "Closets", "realizaciones": "Realizações",
        "metodo": "Método", "nosotros": "Sobre nós", "contacto": "Contato",
        "zona": "Zonas", "cta": "Orçamento Grátis",
        "logo_sub": "Cozinhas &amp; Closets · Riviera Maya",
    },
}

# WA messages par langue
WA_MSGS = {
    "fr": "Bonjour%20Ka%27ax%20Cr%C3%A9ation%2C%20je%20souhaite%20un%20devis%20gratuit.",
    "en": "Hello%20Ka%27ax%20Cre%C3%A1ci%C3%B3n%2C%20I%27d%20like%20a%20free%20quote.",
    "it": "Buongiorno%20Ka%27ax%20Creaci%C3%B3n%2C%20vorrei%20un%20preventivo%20gratuito.",
    "de": "Guten%20Tag%20Ka%27ax%20Creaci%C3%B3n%2C%20ich%20m%C3%B6chte%20ein%20kostenloses%20Angebot.",
    "ru": "%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5%2C%20%D1%85%D0%BE%D1%87%D1%83%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9%20%D1%80%D0%B0%D1%81%D1%87%D1%91%D1%82.",
    "pt": "Ol%C3%A1%20Ka%27ax%20Crea%C3%A7%C3%A3o%2C%20gostaria%20de%20um%20or%C3%A7amento%20gratuito.",
}

def wa_url_lang(lang):
    return f"https://wa.me/529843121942?text={WA_MSGS[lang]}"

# ═══════════════════════════════════════════════════════════════
# LANG DROPDOWN — VERSION MULTILINGUE COMPLÈTE
# ═══════════════════════════════════════════════════════════════

def lang_dropdown_full(current_lang, es_url, page_base_path):
    """
    current_lang: 'fr', 'en', etc.
    es_url: URL absolue vers la page ES (ex: https://kaaxcreacion.com/cocinas-a-medida/)
    page_base_path: préfixe relatif pour les autres langues (ex: '../' pour /cocinas-a-medida/fr/)
    """
    meta = LANG_META[current_lang]
    items = []
    # ES (toujours non-actif)
    items.append(f'<a href="{es_url}" class="lang-dropdown-item">{FLAG_MX}<span class="name">Español</span></a>')
    items.append('<div class="lang-dropdown-divider"></div>')
    for lang, lm in LANG_META.items():
        active = ' active-lang' if lang == current_lang else ''
        if lang == current_lang:
            href = ""  # lien vide = page courante
            link = f'<a href="#" class="lang-dropdown-item{active}" onclick="return false">{lm["flag"]}<span class="name">{lm["name"]}</span></a>'
        else:
            href = f"{page_base_path}{lang}/"
            link = f'<a href="{href}" class="lang-dropdown-item{active}">{lm["flag"]}<span class="name">{lm["name"]}</span></a>'
        items.append(link)
    items_html = "\n".join(items)
    return f"""
<div class="lang-select-wrap">
  <button class="lang-select-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false">
    {meta["flag"]}
    <span class="lang-code">{meta["code"]}</span>
    <span class="chevron">▼</span>
  </button>
  <div class="lang-dropdown" id="langDropdown">
    {items_html}
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# NAV HTML PAR LANGUE
# ═══════════════════════════════════════════════════════════════

def nav_html_lang(lang, root_prefix, active_page, es_url, page_base_path):
    lbl = NAV_LABELS[lang]
    wa = wa_url_lang(lang)
    dropdown = lang_dropdown_full(lang, es_url, page_base_path)

    def nav_item(slug, label, href):
        is_active = active_page.startswith(slug)
        cls = ' class="active"' if is_active else ''
        return f'<li{cls}><a href="{root_prefix}{href}">{label}</a></li>'

    return f"""<nav id="navbar">
  <div class="nav-inner">
    <a href="{root_prefix}" class="nav-logo">KA'AX <span>CREACIÓN</span><sub>{lbl["logo_sub"]}</sub></a>
    <ul class="nav-links">
      {nav_item("cocinas-a-medida", lbl["cocinas"], f"cocinas-a-medida/{lang}/")}
      {nav_item("closets-y-vestidores", lbl["closets"], f"closets-y-vestidores/{lang}/")}
      {nav_item("realizaciones", lbl["realizaciones"], f"realizaciones/{lang}/")}
      {nav_item("zona", lbl["zona"], f"zona/{lang}/")}
      {nav_item("metodo", lbl["metodo"], f"metodo/{lang}/")}
      {nav_item("nosotros", lbl["nosotros"], f"nosotros/{lang}/")}
      {nav_item("contacto", lbl["contacto"], f"contacto/{lang}/")}
    </ul>
    <div style="display:flex;align-items:center;gap:12px">
      {dropdown}
      <a href="{wa}" target="_blank" rel="noopener" class="nav-cta">{lbl["cta"]}</a>
    </div>
    <button class="nav-hamburger" id="navHamburger" aria-label="Menu" aria-expanded="false" aria-controls="navMobileMenu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="nav-mobile-menu" id="navMobileMenu" aria-hidden="true">
    <ul>
      <li><a href="{root_prefix}cocinas-a-medida/{lang}/">{lbl["cocinas"]}</a></li>
      <li><a href="{root_prefix}closets-y-vestidores/{lang}/">{lbl["closets"]}</a></li>
      <li><a href="{root_prefix}realizaciones/{lang}/">{lbl["realizaciones"]}</a></li>
      <li><a href="{root_prefix}zona/{lang}/">{lbl["zona"]}</a></li>
      <li><a href="{root_prefix}metodo/{lang}/">{lbl["metodo"]}</a></li>
      <li><a href="{root_prefix}nosotros/{lang}/">{lbl["nosotros"]}</a></li>
      <li><a href="{root_prefix}contacto/{lang}/">{lbl["contacto"]}</a></li>
    </ul>
    <a href="{wa}" class="nav-mobile-cta" target="_blank" rel="noopener">💬 {lbl["cta"]}</a>
  </div>
</nav>"""

# ═══════════════════════════════════════════════════════════════
# FOOTER PAR LANGUE
# ═══════════════════════════════════════════════════════════════

FOOTER_LABELS = {
    "fr": {
        "maya": "Ka'ax — «forêt · bois» en maya",
        "desc": "Menuiserie européenne de luxe sur mesure, fabriquée à Playa del Carmen. Formé par les Compagnons du Tour de France — Major de promotion 2023.",
        "services": "Services", "blog": "Blog", "contact": "Contact",
        "cocinas": "Cuisines sur mesure", "closets": "Dressings &amp; Armoires",
        "realizaciones": "Réalisations", "nosotros": "Notre ADN",
        "devis": "Devis gratuit", "copy": "Menuiserie européenne artisanale sur mesure",
    },
    "en": {
        "maya": "Ka'ax — «forest · wood» in Maya",
        "desc": "Luxury European custom carpentry, crafted in Playa del Carmen. Trained by the Compagnons du Tour de France — Top of class 2023.",
        "services": "Services", "blog": "Blog", "contact": "Contact",
        "cocinas": "Custom Kitchens", "closets": "Custom Closets",
        "realizaciones": "Portfolio", "nosotros": "Our DNA",
        "devis": "Free Quote", "copy": "Artisan European custom carpentry",
    },
    "it": {
        "maya": "Ka'ax — «foresta · legno» in maya",
        "desc": "Falegnameria europea di lusso su misura, realizzata a Playa del Carmen. Formato dai Compagnons du Tour de France — Primo della promozione 2023.",
        "services": "Servizi", "blog": "Blog", "contact": "Contatto",
        "cocinas": "Cucine su misura", "closets": "Cabine Armadio",
        "realizaciones": "Realizzazioni", "nosotros": "Il nostro DNA",
        "devis": "Preventivo Gratuito", "copy": "Falegnameria europea artigianale su misura",
    },
    "de": {
        "maya": "Ka'ax — «Wald · Holz» auf Maya",
        "desc": "Luxuriöse europäische Maßschreinerei, gefertigt in Playa del Carmen. Ausgebildet von den Compagnons du Tour de France — Jahrgangsbester 2023.",
        "services": "Leistungen", "blog": "Blog", "contact": "Kontakt",
        "cocinas": "Maßküchen", "closets": "Ankleideräume &amp; Schränke",
        "realizaciones": "Portfolio", "nosotros": "Unsere DNA",
        "devis": "Kostenloses Angebot", "copy": "Handwerkliche europäische Maßschreinerei",
    },
    "ru": {
        "maya": "Ka'ax — «лес · дерево» на языке майя",
        "desc": "Роскошная европейская мебель на заказ, изготовленная в Плая-дель-Кармен. Выпускник Compagnons du Tour de France — лучший студент выпуска 2023.",
        "services": "Услуги", "blog": "Блог", "contact": "Контакт",
        "cocinas": "Кухни на заказ", "closets": "Гардеробные &amp; Шкафы",
        "realizaciones": "Портфолио", "nosotros": "Наша ДНК",
        "devis": "Бесплатный расчёт", "copy": "Авторская европейская мебель на заказ",
    },
    "pt": {
        "maya": "Ka'ax — «floresta · madeira» em maia",
        "desc": "Marcenaria europeia de luxo sob medida, fabricada em Playa del Carmen. Formado pelos Compagnons du Tour de France — Melhor aluno da turma 2023.",
        "services": "Serviços", "blog": "Blog", "contact": "Contato",
        "cocinas": "Cozinhas sob medida", "closets": "Closets &amp; Armários",
        "realizaciones": "Realizações", "nosotros": "Nosso DNA",
        "devis": "Orçamento Grátis", "copy": "Marcenaria europeia artesanal sob medida",
    },
}

def footer_html_lang(lang, root_prefix):
    fl = FOOTER_LABELS[lang]
    wa = wa_url_lang(lang)
    return f"""<footer>
  <div>
    <div class="footer-logo">KA'AX <span>CREACIÓN</span></div>
    <div class="footer-maya">{fl["maya"]}</div>
    <p class="footer-desc">{fl["desc"]}</p>
  </div>
  <div class="footer-col"><h4>{fl["services"]}</h4><ul>
    <li><a href="{root_prefix}cocinas-a-medida/{lang}/">{fl["cocinas"]}</a></li>
    <li><a href="{root_prefix}closets-y-vestidores/{lang}/">{fl["closets"]}</a></li>
    <li><a href="{root_prefix}realizaciones/{lang}/">{fl["realizaciones"]}</a></li>
    <li><a href="{root_prefix}nosotros/{lang}/">{fl["nosotros"]}</a></li>
  </ul></div>
  <div class="footer-col"><h4>{fl["blog"]}</h4><ul>
    <li><a href="/blog/cocinas-integrales-playa-del-carmen.html">Cocinas Integrales PDC</a></li>
    <li><a href="/blog/vestidores-a-medida-playa-del-carmen.html">Vestidores a Medida</a></li>
    <li><a href="/blog/maderas-clima-tropical-riviera-maya.html">Maderas Tropicales</a></li>
    <li><a href="/blog/tendencias-2026-cocinas-lujo-riviera-maya.html">Tendencias 2026</a></li>
  </ul></div>
  <div class="footer-col"><h4>{fl["contact"]}</h4><ul>
    <li><a href="{wa}" target="_blank" rel="noopener">💬 +52 984 312 19 42</a></li>
    <li><a href="{root_prefix}contacto/{lang}/">{fl["devis"]}</a></li>
    <li>Instagram @kaaxcreation</li>
    <li>YouTube Ka'ax Creación</li>
  </ul></div>
</footer>
<div class="footer-bottom">
  <span>© 2026 Ka'ax Creación · Playa del Carmen, México</span>
  <span>{fl["copy"]}</span>
</div>"""

# ═══════════════════════════════════════════════════════════════
# BUILD PAGE MULTILINGUE
# ═══════════════════════════════════════════════════════════════

def build_page_lang(lang, title, description, canonical, breadcrumbs_html, content,
                    root_prefix, active_page, es_url, page_base_path,
                    schema_ld="", image_prefix="../../", hreflang_links=""):
    lm = LANG_META[lang]
    schema_block = f'<script type="application/ld+json">{schema_ld}</script>' if schema_ld else ""
    hero_bg_style = f"background:linear-gradient(135deg,rgba(13,13,13,.92) 0%,rgba(45,74,62,.2) 50%,rgba(13,13,13,.95) 100%),url('{image_prefix}images/hero-bg.jpg') center/cover"
    nav = nav_html_lang(lang, root_prefix, active_page, es_url, page_base_path)
    footer = footer_html_lang(lang, root_prefix)
    ticker = ticker_html()

    # Inject ticker after page-hero (after h1+lead text, before the first content section)
    hero_pos = content.find('class="page-hero')
    if hero_pos >= 0:
        close_div = content.find('</div>', hero_pos)
        if close_div >= 0:
            content = content[:close_div+6] + f'\n{ticker}\n' + content[close_div+6:]
            ticker = ""  # already injected inside content

    return f"""<!DOCTYPE html>
<html lang="{lm["html_lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/images/hero-bg.jpg">
<meta property="og:locale" content="{lm["locale"]}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{hreflang_links}
{schema_block}
<style>{COMMON_CSS}</style>
</head>
<body>

{nav}

<div style="position:fixed;inset:0;{hero_bg_style};z-index:-1"></div>

{breadcrumbs_html}

{content}

{footer}

{COMMON_JS}
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════
# BREADCRUMB MULTILINGUE
# ═══════════════════════════════════════════════════════════════

BREADCRUMB_HOME = {
    "fr": "Accueil", "en": "Home", "it": "Home", "de": "Startseite", "ru": "Главная", "pt": "Início",
}

def breadcrumb_lang(lang, items, root_prefix):
    home = BREADCRUMB_HOME[lang]
    parts = f'<a href="{root_prefix}">{home}</a>'
    for label, href in items[:-1]:
        parts += f'<span>›</span><a href="{href}">{label}</a>'
    parts += f'<span>›</span><span>{items[-1][0]}</span>'
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{parts}</nav>'

# ═══════════════════════════════════════════════════════════════
# HREFLANG HELPER
# ═══════════════════════════════════════════════════════════════

def hreflang_service(service_slug):
    """Génère les balises hreflang pour une page service."""
    lines = [f'<link rel="alternate" hreflang="es" href="{DOMAIN}/{service_slug}/">',
             f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{service_slug}/">']
    for lang in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{DOMAIN}/{service_slug}/{lang}/">')
    return "\n".join(lines)

def hreflang_zone(zone_slug):
    """Génère les balises hreflang pour une page zone."""
    lines = [f'<link rel="alternate" hreflang="es" href="{DOMAIN}/zona/{zone_slug}/">',
             f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/zona/{zone_slug}/">']
    for lang in LANGS:
        lines.append(f'<link rel="alternate" hreflang="{lang}" href="{DOMAIN}/zona/{zone_slug}/{lang}/">')
    return "\n".join(lines)

# ═══════════════════════════════════════════════════════════════
# PAGE COCINAS — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_cocinas(lang, root_prefix):
    wa = wa_url_lang(lang)
    if lang == "fr":
        return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Cuisines sur mesure — Ka'ax Création</p>
  <h1>Cuisines intégrales<br><em>sur mesure</em></h1>
  <p class="lead">Chaque cuisine Ka'ax Création est unique. Conçue dans notre atelier de Playa del Carmen avec un savoir-faire européen transmis par les Compagnons du Tour de France — pour votre villa, votre condominium ou votre résidence en Riviera Maya.</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Cuisines artisanales<br><em>au niveau européen</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:40px">Ka'ax Création fabrique chaque cuisine à la main dans notre atelier de Playa del Carmen. Façades en MDF laqué mat, panneaux antihumidité, plans de travail en quartz ou granit, ferrures Blum — le même niveau d'exigence qu'en Europe, adapté au climat tropical.</p>
  <div class="content-grid-3">
    <div class="feature-card"><div class="feature-icon">🏗️</div><h3>Fabrication 100% locale</h3><p>Fabriqué dans notre atelier de Playa del Carmen. Zéro intermédiaire, délais maîtrisés, suivi personnalisé de A à Z.</p></div>
    <div class="feature-card"><div class="feature-icon">🇫🇷</div><h3>Savoir-faire des Compagnons</h3><p>Notre maître menuisier est Major de promotion 2023 des Compagnons du Tour de France — la plus haute distinction artisanale française.</p></div>
    <div class="feature-card"><div class="feature-icon">🌿</div><h3>Matériaux tropicaux</h3><p>MDF antihumidité, quartz ou granit, ferrures inox 316L — sélectionnés pour résister au climat chaud et humide des Caraïbes.</p></div>
  </div>
</div>
<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px">Nos finitions<br><em style="font-style:italic;color:#E8C97A">signatures</em></h2>
    <div class="content-grid-3" style="margin-top:40px">
      <div class="feature-card"><div class="feature-icon">🎨</div><h3>Laque mat premium</h3><p>Façades en MDF laqué mat dans toutes les teintes RAL. Finition veloutée, toucher doux, résistance aux UV et à l'humidité.</p></div>
      <div class="feature-card"><div class="feature-icon">🪵</div><h3>Bois naturels certifiés</h3><p>Chêne, noyer, cèdre — bois massifs certifiés FSC disponibles pour les projets premium et les villas de luxe.</p></div>
      <div class="feature-card"><div class="feature-icon">⚙️</div><h3>Ferrures Blum &amp; Hettich</h3><p>Charnières silencieuses, coulisses amortissantes, systèmes de fermeture intégrés — les meilleures ferrures européennes.</p></div>
      <div class="feature-card"><div class="feature-icon">🏝️</div><h3>Adaptation tropicale</h3><p>Chaque cuisine est traitée anti-sel, anti-humidité et anti-UV pour résister aux conditions climatiques de la Riviera Maya.</p></div>
      <div class="feature-card"><div class="feature-icon">🔆</div><h3>Éclairage LED intégré</h3><p>Bandeau LED sous les meubles hauts, spots dans les colonnes, éclairage indirect — pour une ambiance et une fonctionnalité optimales.</p></div>
      <div class="feature-card"><div class="feature-icon">🗄️</div><h3>Rangements intelligents</h3><p>Plateaux tournants, tiroirs de couverts, organisateurs intégrés — chaque centimètre optimisé pour votre usage quotidien.</p></div>
    </div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Votre cuisine sur mesure<br><em>en 4 étapes</em></h2>
  <div class="process-steps">
    <div class="process-step"><div class="step-num">01</div><h3>Visite technique</h3><p>Prise de mesures précises, analyse des contraintes techniques, discussion de vos envies et de votre budget.</p></div>
    <div class="process-step"><div class="step-num">02</div><h3>Conception 3D</h3><p>Plan 3D de votre cuisine avec choix des matériaux, couleurs et finitions. Devis détaillé sous 48 heures.</p></div>
    <div class="process-step"><div class="step-num">03</div><h3>Fabrication artisanale</h3><p>Fabrication dans notre atelier de Playa del Carmen. Chaque pièce est taillée, assemblée et finalisée à la main.</p></div>
    <div class="process-step"><div class="step-num">04</div><h3>Pose &amp; finitions</h3><p>Installation par notre équipe, réglages précis, contrôle qualité final. Garantie de 3 ans sur toute la menuiserie.</p></div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>Votre cuisine de rêve<br><em>en Riviera Maya</em></h2>
    <p>Devis gratuit · Visite technique offerte · Déplacement inclus</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">💬 Devis WhatsApp</a>
      <a href="{root_prefix}contacto/fr/" class="btn-secondary">Formulaire de contact</a>
    </div>
  </div>
</div>"""

    elif lang == "en":
        return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Custom Kitchens — Ka'ax Creación</p>
  <h1>Custom integrated<br><em>kitchens</em></h1>
  <p class="lead">Every Ka'ax Creación kitchen is one of a kind. Crafted in our Playa del Carmen workshop with European expertise from the Compagnons du Tour de France — for your villa, condo or residence in the Riviera Maya.</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Handcrafted kitchens<br><em>to European standards</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:40px">Ka'ax Creación builds every kitchen by hand in our Playa del Carmen workshop. Matte lacquered MDF fronts, moisture-resistant panels, quartz or granite countertops, Blum hardware — the same European quality standard, adapted to the tropical climate.</p>
  <div class="content-grid-3">
    <div class="feature-card"><div class="feature-icon">🏗️</div><h3>100% local fabrication</h3><p>Built in our Playa del Carmen workshop. No middlemen, controlled timelines, personalized follow-up from start to finish.</p></div>
    <div class="feature-card"><div class="feature-icon">🇫🇷</div><h3>Compagnons expertise</h3><p>Our master craftsman is the Top Graduate of 2023 from the Compagnons du Tour de France — France's highest artisan distinction.</p></div>
    <div class="feature-card"><div class="feature-icon">🌿</div><h3>Tropical-grade materials</h3><p>Moisture-resistant MDF, quartz or granite, 316L stainless hardware — selected to withstand the hot and humid Caribbean climate.</p></div>
  </div>
</div>
<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px">Our signature<br><em style="font-style:italic;color:#E8C97A">finishes</em></h2>
    <div class="content-grid-3" style="margin-top:40px">
      <div class="feature-card"><div class="feature-icon">🎨</div><h3>Premium matte lacquer</h3><p>MDF fronts in matte lacquer across all RAL colors. Velvety finish, smooth touch, UV and moisture resistant.</p></div>
      <div class="feature-card"><div class="feature-icon">🪵</div><h3>FSC-certified hardwoods</h3><p>Oak, walnut, cedar — FSC-certified solid woods available for premium projects and luxury villas.</p></div>
      <div class="feature-card"><div class="feature-icon">⚙️</div><h3>Blum &amp; Hettich hardware</h3><p>Silent hinges, soft-close drawer slides, integrated closing systems — the finest European hardware.</p></div>
      <div class="feature-card"><div class="feature-icon">🏝️</div><h3>Tropical adaptation</h3><p>Every kitchen is treated against salt, moisture and UV to withstand Riviera Maya climate conditions.</p></div>
      <div class="feature-card"><div class="feature-icon">🔆</div><h3>Integrated LED lighting</h3><p>Under-cabinet LED strips, column spotlights, indirect lighting — for optimal ambiance and functionality.</p></div>
      <div class="feature-card"><div class="feature-icon">🗄️</div><h3>Smart storage</h3><p>Lazy Susans, cutlery drawers, integrated organizers — every centimeter optimized for your daily use.</p></div>
    </div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Your custom kitchen<br><em>in 4 steps</em></h2>
  <div class="process-steps">
    <div class="process-step"><div class="step-num">01</div><h3>Technical visit</h3><p>Precise measurements, technical analysis, discussion of your vision and budget.</p></div>
    <div class="process-step"><div class="step-num">02</div><h3>3D design</h3><p>3D plan of your kitchen with material, color and finish selection. Detailed quote within 48 hours.</p></div>
    <div class="process-step"><div class="step-num">03</div><h3>Artisan fabrication</h3><p>Built in our Playa del Carmen workshop. Every piece is cut, assembled and finished by hand.</p></div>
    <div class="process-step"><div class="step-num">04</div><h3>Installation &amp; finishing</h3><p>Installation by our team, precise adjustments, final quality check. 3-year warranty on all cabinetry.</p></div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>Your dream kitchen<br><em>in the Riviera Maya</em></h2>
    <p>Free quote · Free technical visit · Travel included</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">💬 WhatsApp Quote</a>
      <a href="{root_prefix}contacto/en/" class="btn-secondary">Contact form</a>
    </div>
  </div>
</div>"""

    elif lang == "it":
        return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Cucine su misura — Ka'ax Creación</p>
  <h1>Cucine integrate<br><em>su misura</em></h1>
  <p class="lead">Ogni cucina Ka'ax Creación è unica. Realizzata nel nostro laboratorio di Playa del Carmen con il know-how europeo dei Compagnons du Tour de France — per la vostra villa, condominio o residenza nella Riviera Maya.</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Cucine artigianali<br><em>a livello europeo</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:40px">Ka'ax Creación realizza ogni cucina a mano nel nostro laboratorio di Playa del Carmen. Ante in MDF laccato opaco, pannelli anti-umidità, piani in quarzo o granito, ferramenta Blum — lo stesso standard europeo, adattato al clima tropicale.</p>
  <div class="content-grid-3">
    <div class="feature-card"><div class="feature-icon">🏗️</div><h3>Produzione 100% locale</h3><p>Realizzato nel nostro laboratorio di Playa del Carmen. Nessun intermediario, tempi controllati, follow-up personalizzato dalla A alla Z.</p></div>
    <div class="feature-card"><div class="feature-icon">🇫🇷</div><h3>Maestria dei Compagnons</h3><p>Il nostro maestro falegname è il Primo della promozione 2023 dei Compagnons du Tour de France — la più alta distinzione artigianale francese.</p></div>
    <div class="feature-card"><div class="feature-icon">🌿</div><h3>Materiali per clima tropicale</h3><p>MDF anti-umidità, quarzo o granito, ferramenta inox 316L — selezionati per resistere al clima caldo e umido dei Caraibi.</p></div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>La vostra cucina su misura<br><em>in 4 fasi</em></h2>
  <div class="process-steps">
    <div class="process-step"><div class="step-num">01</div><h3>Visita tecnica</h3><p>Rilievo preciso delle misure, analisi tecnica, discussione delle vostre esigenze e del budget.</p></div>
    <div class="process-step"><div class="step-num">02</div><h3>Progettazione 3D</h3><p>Progetto 3D della cucina con scelta di materiali, colori e finiture. Preventivo dettagliato entro 48 ore.</p></div>
    <div class="process-step"><div class="step-num">03</div><h3>Produzione artigianale</h3><p>Realizzazione nel nostro laboratorio di Playa del Carmen. Ogni pezzo è tagliato, assemblato e rifinito a mano.</p></div>
    <div class="process-step"><div class="step-num">04</div><h3>Posa &amp; finiture</h3><p>Installazione da parte del nostro team, regolazioni precise, controllo qualità finale. Garanzia 3 anni su tutta la falegnameria.</p></div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>La vostra cucina dei sogni<br><em>nella Riviera Maya</em></h2>
    <p>Preventivo gratuito · Visita tecnica inclusa · Trasferta inclusa</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">💬 Preventivo WhatsApp</a>
      <a href="{root_prefix}contacto/it/" class="btn-secondary">Modulo di contatto</a>
    </div>
  </div>
</div>"""

    elif lang == "de":
        return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Maßküchen — Ka'ax Creación</p>
  <h1>Maßgefertigte<br><em>Einbauküchen</em></h1>
  <p class="lead">Jede Ka'ax Creación Küche ist einzigartig. Gefertigt in unserer Werkstatt in Playa del Carmen mit europäischem Handwerk der Compagnons du Tour de France — für Ihre Villa, Ihr Apartment oder Ihre Residenz in der Riviera Maya.</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Handgefertigte Küchen<br><em>nach europäischem Standard</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:40px">Ka'ax Creación fertigt jede Küche von Hand in unserer Werkstatt in Playa del Carmen. Mattlackierte MDF-Fronten, feuchtigkeitsbeständige Platten, Quarz- oder Granitarbeitsplatten, Blum-Beschläge — europäische Qualitätsstandards, angepasst an das tropische Klima.</p>
  <div class="content-grid-3">
    <div class="feature-card"><div class="feature-icon">🏗️</div><h3>100% lokale Fertigung</h3><p>Gefertigt in unserer Werkstatt in Playa del Carmen. Keine Zwischenhändler, kontrollierte Lieferzeiten, persönliche Betreuung von A bis Z.</p></div>
    <div class="feature-card"><div class="feature-icon">🇫🇷</div><h3>Compagnons-Handwerk</h3><p>Unser Meisterschreiner ist Jahrgangsbester 2023 der Compagnons du Tour de France — Frankreichs höchste Handwerksauszeichnung.</p></div>
    <div class="feature-card"><div class="feature-icon">🌿</div><h3>Tropentaugliche Materialien</h3><p>Feuchtigkeitsbeständiges MDF, Quarz oder Granit, 316L Edelstahlbeschläge — ausgewählt für das heiß-feuchte Karibikklima.</p></div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Ihre Maßküche<br><em>in 4 Schritten</em></h2>
  <div class="process-steps">
    <div class="process-step"><div class="step-num">01</div><h3>Technischer Besuch</h3><p>Präzise Aufmaßnahme, technische Analyse, Besprechung Ihrer Wünsche und Ihres Budgets.</p></div>
    <div class="process-step"><div class="step-num">02</div><h3>3D-Planung</h3><p>3D-Plan Ihrer Küche mit Material-, Farb- und Oberflächenauswahl. Detailliertes Angebot innerhalb von 48 Stunden.</p></div>
    <div class="process-step"><div class="step-num">03</div><h3>Handwerkliche Fertigung</h3><p>Fertigung in unserer Werkstatt in Playa del Carmen. Jedes Teil wird von Hand zugeschnitten, montiert und veredelt.</p></div>
    <div class="process-step"><div class="step-num">04</div><h3>Montage &amp; Finishing</h3><p>Einbau durch unser Team, präzise Einstellungen, abschließende Qualitätskontrolle. 3 Jahre Garantie auf alle Schreinerarbeiten.</p></div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>Ihre Traumküche<br><em>in der Riviera Maya</em></h2>
    <p>Kostenloses Angebot · Technischer Besuch inklusive · Anfahrt inklusive</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">💬 WhatsApp Angebot</a>
      <a href="{root_prefix}contacto/de/" class="btn-secondary">Kontaktformular</a>
    </div>
  </div>
</div>"""

    elif lang == "ru":
        return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Кухни на заказ — Ka'ax Creación</p>
  <h1>Встроенные кухни<br><em>на заказ</em></h1>
  <p class="lead">Каждая кухня Ka'ax Creación уникальна. Изготовлена в нашей мастерской в Плая-дель-Кармен с европейским мастерством Compagnons du Tour de France — для вашей виллы, апартаментов или резиденции на Ривьере Майя.</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Ручная работа<br><em>по европейским стандартам</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:40px">Ka'ax Creación изготавливает каждую кухню вручную в нашей мастерской в Плая-дель-Кармен. Матовые лакированные фасады из МДФ, влагостойкие панели, столешницы из кварца или гранита, фурнитура Blum — европейский стандарт качества, адаптированный к тропическому климату.</p>
  <div class="content-grid-3">
    <div class="feature-card"><div class="feature-icon">🏗️</div><h3>100% местное производство</h3><p>Изготовлено в нашей мастерской в Плая-дель-Кармен. Без посредников, контролируемые сроки, личное сопровождение от начала до конца.</p></div>
    <div class="feature-card"><div class="feature-icon">🇫🇷</div><h3>Мастерство Compagnons</h3><p>Наш главный мастер — лучший выпускник 2023 года гильдии Compagnons du Tour de France, высшей награды французского ремесленного мастерства.</p></div>
    <div class="feature-card"><div class="feature-icon">🌿</div><h3>Тропические материалы</h3><p>Влагостойкий МДФ, кварц или гранит, нержавеющая фурнитура 316L — специально подобранные для жаркого и влажного карибского климата.</p></div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Ваша кухня на заказ<br><em>за 4 шага</em></h2>
  <div class="process-steps">
    <div class="process-step"><div class="step-num">01</div><h3>Технический выезд</h3><p>Точные замеры, технический анализ, обсуждение ваших пожеланий и бюджета.</p></div>
    <div class="process-step"><div class="step-num">02</div><h3>3D-проектирование</h3><p>3D-план вашей кухни с выбором материалов, цветов и отделки. Детальный расчёт в течение 48 часов.</p></div>
    <div class="process-step"><div class="step-num">03</div><h3>Ручное изготовление</h3><p>Производство в нашей мастерской в Плая-дель-Кармен. Каждая деталь вырезается, собирается и доводится до совершенства вручную.</p></div>
    <div class="process-step"><div class="step-num">04</div><h3>Монтаж и финальная отделка</h3><p>Установка нашей командой, точная регулировка, финальный контроль качества. Гарантия 3 года на все столярные работы.</p></div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>Кухня вашей мечты<br><em>на Ривьере Майя</em></h2>
    <p>Бесплатный расчёт · Технический выезд включён · Доставка включена</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">💬 Расчёт в WhatsApp</a>
      <a href="{root_prefix}contacto/ru/" class="btn-secondary">Форма связи</a>
    </div>
  </div>
</div>"""

    else:  # pt
        return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Cozinhas sob medida — Ka'ax Creación</p>
  <h1>Cozinhas integradas<br><em>sob medida</em></h1>
  <p class="lead">Cada cozinha Ka'ax Creación é única. Fabricada na nossa oficina em Playa del Carmen com o savoir-faire europeu dos Compagnons du Tour de France — para a sua villa, condomínio ou residência na Riviera Maya.</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Cozinhas artesanais<br><em>ao nível europeu</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:40px">Ka'ax Creación fabrica cada cozinha à mão na nossa oficina em Playa del Carmen. Frentes em MDF lacado mate, painéis anti-humidade, bancadas em quartzo ou granito, ferragens Blum — o mesmo padrão europeu, adaptado ao clima tropical.</p>
  <div class="content-grid-3">
    <div class="feature-card"><div class="feature-icon">🏗️</div><h3>Fabricação 100% local</h3><p>Fabricado na nossa oficina em Playa del Carmen. Sem intermediários, prazos controlados, acompanhamento personalizado de A a Z.</p></div>
    <div class="feature-card"><div class="feature-icon">🇫🇷</div><h3>Mestria dos Compagnons</h3><p>O nosso mestre marceneiro é o Melhor Aluno de 2023 dos Compagnons du Tour de France — a mais alta distinção artesanal francesa.</p></div>
    <div class="feature-card"><div class="feature-icon">🌿</div><h3>Materiais tropicais</h3><p>MDF anti-humidade, quartzo ou granito, ferragens inox 316L — selecionados para resistir ao clima quente e húmido das Caraíbas.</p></div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>A sua cozinha sob medida<br><em>em 4 etapas</em></h2>
  <div class="process-steps">
    <div class="process-step"><div class="step-num">01</div><h3>Visita técnica</h3><p>Medições precisas, análise técnica, discussão das suas necessidades e orçamento.</p></div>
    <div class="process-step"><div class="step-num">02</div><h3>Projeto 3D</h3><p>Plano 3D da sua cozinha com escolha de materiais, cores e acabamentos. Orçamento detalhado em 48 horas.</p></div>
    <div class="process-step"><div class="step-num">03</div><h3>Fabricação artesanal</h3><p>Fabricado na nossa oficina em Playa del Carmen. Cada peça é cortada, montada e acabada à mão.</p></div>
    <div class="process-step"><div class="step-num">04</div><h3>Instalação &amp; acabamentos</h3><p>Instalação pela nossa equipa, ajustes precisos, controlo de qualidade final. Garantia de 3 anos em toda a marcenaria.</p></div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>A sua cozinha de sonho<br><em>na Riviera Maya</em></h2>
    <p>Orçamento grátis · Visita técnica incluída · Deslocação incluída</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">💬 Orçamento WhatsApp</a>
      <a href="{root_prefix}contacto/pt/" class="btn-secondary">Formulário de contato</a>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE CLOSETS — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_closets(lang, root_prefix):
    wa = wa_url_lang(lang)
    titles = {
        "fr": ("Dressings &amp; Armoires sur mesure", "Espaces<br><em>dressing sur mesure</em>", "Dressings walk-in et armoires<br><em>de luxe</em>"),
        "en": ("Custom Custom Closets", "Custom<br><em>walk-in closets</em>", "Walk-in closets and<br><em>custom storage</em>"),
        "it": ("Cabine Armadio su Misura", "Cabine armadio<br><em>e armadi su misura</em>", "Walk-in closet e armadi<br><em>di lusso</em>"),
        "de": ("Ankleideräume &amp; Schränke nach Maß", "Maßgefertigte<br><em>Ankleideräume</em>", "Walk-in Ankleideräume und<br><em>Luxusschränke</em>"),
        "ru": ("Гардеробные и шкафы на заказ", "Гардеробные<br><em>на заказ</em>", "Walk-in гардеробные и<br><em>элитные шкафы</em>"),
        "pt": ("Closets &amp; Armários sob Medida", "Closets<br><em>e armários sob medida</em>", "Walk-in closets e armários<br><em>de luxo</em>"),
    }
    eyebrow, h1, h2 = titles[lang]

    paragraphs = {
        "fr": "Ka'ax Création conçoit et fabrique des dressings et armoires entièrement sur mesure. Walk-in closets spacieux, armoires encastrées optimisées, dressing avec îlot central — chaque solution est pensée pour s'intégrer parfaitement à votre espace et à vos habitudes.",
        "en": "Ka'ax Creación designs and builds fully custom closets. Spacious walk-in closets, optimized built-in closets, dressing rooms with central island — every solution is designed to fit perfectly in your space and your lifestyle.",
        "it": "Ka'ax Creación progetta e realizza cabine armadio e armadi completamente su misura. Walk-in closet spaziosi, armadi a muro ottimizzati, cabine armadio con isola centrale — ogni soluzione è pensata per integrarsi perfettamente nel vostro spazio e nelle vostre abitudini.",
        "de": "Ka'ax Creación entwirft und fertigt vollständig maßgeschneiderte Ankleideräume und Schränke. Geräumige Walk-in-Ankleideräume, optimierte Einbauschränke, Ankleidezimmer mit Mittelinsel — jede Lösung ist perfekt auf Ihren Raum und Ihre Gewohnheiten abgestimmt.",
        "ru": "Ka'ax Creación проектирует и изготавливает гардеробные и шкафы полностью на заказ. Просторные walk-in гардеробные, встроенные шкафы с оптимальным использованием пространства, гардеробные с центральным островом — каждое решение идеально вписывается в ваш интерьер.",
        "pt": "Ka'ax Creación projeta e fabrica closets e armários completamente sob medida. Walk-in closets espaçosos, armários embutidos otimizados, closets com ilha central — cada solução é pensada para se integrar perfeitamente ao seu espaço e hábitos.",
    }

    features = {
        "fr": [
            ("🚶", "Walk-in closets", "Espaces de rangement ouverts avec îlot central, miroirs intégrés et éclairage LED — l'expérience dressing d'un hôtel de luxe dans votre résidence."),
            ("🗄️", "Armoires encastrées", "Armoires sur mesure qui s'intègrent parfaitement à vos murs, avec systèmes coulissants, miroirs et finitions au choix."),
            ("🔆", "Éclairage intégré", "LED sous les cintres, spots dans les tiroirs, miroir rétroéclairé — pour préparer votre journée dans les meilleures conditions."),
            ("💎", "Accessoires premium", "Valet butler, tiroirs à bijoux en velours, compartiments à chaussures, rangement sacs — des détails qui font la différence."),
        ],
        "en": [
            ("🚶", "Walk-in closets", "Open storage spaces with central island, integrated mirrors and LED lighting — the luxury hotel dressing experience in your home."),
            ("🗄️", "Built-in Closets", "Custom closets that perfectly integrate into your walls, with sliding systems, mirrors and finishes of your choice."),
            ("🔆", "Integrated lighting", "LED under the hanging rail, spotlights in drawers, backlit mirror — to get ready in the best possible light."),
            ("💎", "Premium accessories", "Butler valet, velvet jewelry drawers, shoe compartments, bag storage — the details that make the difference."),
        ],
        "it": [
            ("🚶", "Walk-in closet", "Spazi di guardaroba aperti con isola centrale, specchi integrati e illuminazione LED — l'esperienza di un hotel di lusso nella vostra residenza."),
            ("🗄️", "Armadi su misura", "Armadi personalizzati che si integrano perfettamente nelle vostre pareti, con sistemi scorrevoli, specchi e finiture a scelta."),
            ("🔆", "Illuminazione integrata", "LED sotto le aste, faretti nei cassetti, specchio retroilluminato — per prepararsi nelle migliori condizioni."),
            ("💎", "Accessori premium", "Valet butler, cassetti per gioielli in velluto, scomparti per scarpe, porta borse — i dettagli che fanno la differenza."),
        ],
        "de": [
            ("🚶", "Walk-in Ankleideräume", "Offene Stauräume mit Mittelinsel, integrierten Spiegeln und LED-Beleuchtung — das Luxushotel-Erlebnis in Ihrer Residenz."),
            ("🗄️", "Einbauschränke", "Maßgeschneiderte Schränke, die sich perfekt in Ihre Wände einfügen, mit Schiebesystemen, Spiegeln und Oberflächen nach Wahl."),
            ("🔆", "Integrierte Beleuchtung", "LED unter der Kleiderstange, Spots in den Schubladen, beleuchteter Spiegel — für die beste Vorbereitung auf den Tag."),
            ("💎", "Premium-Zubehör", "Valet Butler, Schmuckschubladen in Samt, Schuhfächer, Handtaschen-Aufbewahrung — Details, die den Unterschied machen."),
        ],
        "ru": [
            ("🚶", "Walk-in гардеробные", "Открытые гардеробные с центральным островом, встроенными зеркалами и LED-освещением — уровень люксового отеля в вашей резиденции."),
            ("🗄️", "Встроенные шкафы", "Шкафы на заказ, идеально вписывающиеся в стены, с раздвижными системами, зеркалами и отделкой на выбор."),
            ("🔆", "Встроенное освещение", "LED под штангами, споты в ящиках, подсвеченное зеркало — лучшие условия для сборов."),
            ("💎", "Премиум аксессуары", "Вешалка-дворецкий, бархатные ящики для украшений, отсеки для обуви, хранение сумок — детали, которые меняют всё."),
        ],
        "pt": [
            ("🚶", "Walk-in closets", "Espaços de armazenamento abertos com ilha central, espelhos integrados e iluminação LED — a experiência de um hotel de luxo na sua residência."),
            ("🗄️", "Armários embutidos", "Armários sob medida que se integram perfeitamente nas suas paredes, com sistemas deslizantes, espelhos e acabamentos à sua escolha."),
            ("🔆", "Iluminação integrada", "LED sob as barras de cabides, spots nos gavetas, espelho com retroiluminação — para se preparar nas melhores condições."),
            ("💎", "Acessórios premium", "Valet butler, gavetas para joias em veludo, compartimentos para sapatos, armazenamento de bolsas — os detalhes que fazem a diferença."),
        ],
    }

    cta_text = {
        "fr": ("Votre dressing sur mesure<br><em>en Riviera Maya</em>", "Devis gratuit · Visite technique offerte", "💬 Devis WhatsApp", f"{root_prefix}contacto/fr/", "Formulaire de contact"),
        "en": ("Your custom closet<br><em>in the Riviera Maya</em>", "Free quote · Technical visit included", "💬 WhatsApp Quote", f"{root_prefix}contacto/en/", "Contact form"),
        "it": ("La vostra cabina armadio<br><em>nella Riviera Maya</em>", "Preventivo gratuito · Visita tecnica inclusa", "💬 Preventivo WhatsApp", f"{root_prefix}contacto/it/", "Modulo di contatto"),
        "de": ("Ihr Ankleideraum nach Maß<br><em>in der Riviera Maya</em>", "Kostenloses Angebot · Technischer Besuch inklusive", "💬 WhatsApp Angebot", f"{root_prefix}contacto/de/", "Kontaktformular"),
        "ru": ("Ваша гардеробная на заказ<br><em>на Ривьере Майя</em>", "Бесплатный расчёт · Технический выезд включён", "💬 Расчёт в WhatsApp", f"{root_prefix}contacto/ru/", "Форма связи"),
        "pt": ("O seu closet sob medida<br><em>na Riviera Maya</em>", "Orçamento grátis · Visita técnica incluída", "💬 Orçamento WhatsApp", f"{root_prefix}contacto/pt/", "Formulário de contato"),
    }

    feats_html = "\n".join(
        f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>'
        for icon, title, desc in features[lang]
    )
    cta_h2, cta_p, cta_btn, cta_href, cta_sec = cta_text[lang]

    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{eyebrow} — Ka'ax Creación</p>
  <h1>{h1}</h1>
  <p class="lead">{paragraphs[lang]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>{h2}</h2>
  <div class="content-grid-3" style="margin-top:40px">
    {feats_html}
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>{cta_h2}</h2>
    <p>{cta_p}</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">{cta_btn}</a>
      <a href="{cta_href}" class="btn-secondary">{cta_sec}</a>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE REALIZACIONES — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_realizaciones(lang, root_prefix):
    wa = wa_url_lang(lang)
    t = {
        "fr": {
            "eyebrow": "Portfolio — Ka'ax Création",
            "h1": "Nos<br><em>Réalisations</em>",
            "lead": "Chaque projet Ka'ax Création est unique. Cuisines intégrales haut de gamme, dressings de luxe, compartiments cachés — découvrez nos réalisations dans les villas, condominiums et résidences de la Riviera Maya.",
            "h2": "Types de projets<br><em>réalisés</em>",
            "cards": [
                ("🏖️", "Villas de luxe — Riviera Maya", "Cuisines haut de gamme avec îlot central, walk-in closets et mobilier extérieur en bois traité. Projets à Playa del Carmen, Tulum et Cancún."),
                ("🏢", "Condominiums &amp; Penthouses", "Optimisation des espaces en appartements de luxe. Cuisines intégrées compactes, armoires encastrées et solutions de rangement intelligentes."),
                ("🏨", "Projets commerciaux", "Mobilier sur mesure pour boutique hôtels, restaurants et espaces commerciaux. Qualité luxe adaptée à un usage intensif."),
            ],
            "cta_h2": "Votre projet<br><em>dans notre portfolio ?</em>",
            "cta_p": "Contactez-nous pour discuter de votre projet et obtenir un devis gratuit.",
            "cta_btn": "💬 Contactez-nous",
            "cta_sec": "Formulaire de contact",
        },
        "en": {
            "eyebrow": "Portfolio — Ka'ax Creación",
            "h1": "Our<br><em>Portfolio</em>",
            "lead": "Every Ka'ax Creación project is unique. High-end integrated kitchens, luxury walk-in closets, hidden compartments — discover our work in villas, condos and residences of the Riviera Maya.",
            "h2": "Types of<br><em>completed projects</em>",
            "cards": [
                ("🏖️", "Luxury villas — Riviera Maya", "High-end kitchens with central island, walk-in closets and outdoor furniture in treated wood. Projects in Playa del Carmen, Tulum and Cancún."),
                ("🏢", "Condos &amp; Penthouses", "Space optimization in luxury apartments. Compact integrated kitchens, built-in closets and smart storage solutions."),
                ("🏨", "Commercial projects", "Custom furniture for boutique hotels, restaurants and commercial spaces. Luxury quality adapted for heavy use."),
            ],
            "cta_h2": "Your project<br><em>in our portfolio?</em>",
            "cta_p": "Contact us to discuss your project and get a free quote.",
            "cta_btn": "💬 Contact us",
            "cta_sec": "Contact form",
        },
        "it": {
            "eyebrow": "Portfolio — Ka'ax Creación",
            "h1": "Le nostre<br><em>Realizzazioni</em>",
            "lead": "Ogni progetto Ka'ax Creación è unico. Cucine integrate di alta gamma, cabine armadio di lusso, compartimenti nascosti — scoprite le nostre realizzazioni nelle ville, condomini e residenze della Riviera Maya.",
            "h2": "Tipologie di<br><em>progetti realizzati</em>",
            "cards": [
                ("🏖️", "Ville di lusso — Riviera Maya", "Cucine di alta gamma con isola centrale, walk-in closet e arredi da esterno in legno trattato. Progetti a Playa del Carmen, Tulum e Cancún."),
                ("🏢", "Condomini &amp; Attico", "Ottimizzazione degli spazi in appartamenti di lusso. Cucine integrate compatte, armadi a muro e soluzioni di stoccaggio intelligenti."),
                ("🏨", "Progetti commerciali", "Arredi su misura per boutique hotel, ristoranti e spazi commerciali. Qualità lusso adatta all'uso intensivo."),
            ],
            "cta_h2": "Il vostro progetto<br><em>nel nostro portfolio?</em>",
            "cta_p": "Contattateci per discutere del vostro progetto e ottenere un preventivo gratuito.",
            "cta_btn": "💬 Contattateci",
            "cta_sec": "Modulo di contatto",
        },
        "de": {
            "eyebrow": "Portfolio — Ka'ax Creación",
            "h1": "Unsere<br><em>Projekte</em>",
            "lead": "Jedes Ka'ax Creación Projekt ist einzigartig. High-End Einbauküchen, luxuriöse Ankleideräume, versteckte Fächer — entdecken Sie unsere Arbeiten in Villen, Apartments und Residenzen der Riviera Maya.",
            "h2": "Arten unserer<br><em>abgeschlossenen Projekte</em>",
            "cards": [
                ("🏖️", "Luxusvillen — Riviera Maya", "High-End Küchen mit Mittelinsel, Walk-in-Ankleideräume und Outdoor-Möbel aus behandeltem Holz. Projekte in Playa del Carmen, Tulum und Cancún."),
                ("🏢", "Apartments &amp; Penthäuser", "Raumoptimierung in Luxusapartments. Kompakte Einbauküchen, eingebaute Schränke und intelligente Stauraumlösungen."),
                ("🏨", "Gewerbliche Projekte", "Maßmöbel für Boutique-Hotels, Restaurants und Gewerbeflächen. Luxusqualität für intensiven Einsatz."),
            ],
            "cta_h2": "Ihr Projekt<br><em>in unserem Portfolio?</em>",
            "cta_p": "Kontaktieren Sie uns, um Ihr Projekt zu besprechen und ein kostenloses Angebot zu erhalten.",
            "cta_btn": "💬 Kontaktieren Sie uns",
            "cta_sec": "Kontaktformular",
        },
        "ru": {
            "eyebrow": "Портфолио — Ka'ax Creación",
            "h1": "Наши<br><em>Проекты</em>",
            "lead": "Каждый проект Ka'ax Creación уникален. Встроенные кухни класса люкс, гардеробные, потайные секции — ознакомьтесь с нашими работами на виллах, в апартаментах и резиденциях Ривьеры Майя.",
            "h2": "Типы выполненных<br><em>проектов</em>",
            "cards": [
                ("🏖️", "Роскошные виллы — Ривьера Майя", "Кухни высшего класса с центральным островом, walk-in гардеробные и уличная мебель из обработанного дерева. Проекты в Плая-дель-Кармен, Тулум и Канкун."),
                ("🏢", "Апартаменты &amp; Пентхаусы", "Оптимизация пространства в элитных апартаментах. Компактные встроенные кухни, встроенные шкафы и умные системы хранения."),
                ("🏨", "Коммерческие проекты", "Мебель на заказ для бутик-отелей, ресторанов и коммерческих помещений. Качество класса люкс для интенсивного использования."),
            ],
            "cta_h2": "Ваш проект<br><em>в нашем портфолио?</em>",
            "cta_p": "Свяжитесь с нами, чтобы обсудить ваш проект и получить бесплатный расчёт.",
            "cta_btn": "💬 Написать нам",
            "cta_sec": "Форма связи",
        },
        "pt": {
            "eyebrow": "Portfolio — Ka'ax Creación",
            "h1": "Nossas<br><em>Realizações</em>",
            "lead": "Cada projeto Ka'ax Creación é único. Cozinhas integradas de alto padrão, closets de luxo, compartimentos ocultos — descubra nossas realizações em villas, condomínios e residências da Riviera Maya.",
            "h2": "Tipos de projetos<br><em>realizados</em>",
            "cards": [
                ("🏖️", "Villas de luxo — Riviera Maya", "Cozinhas de alto padrão com ilha central, walk-in closets e mobiliário exterior em madeira tratada. Projetos em Playa del Carmen, Tulum e Cancún."),
                ("🏢", "Condomínios &amp; Coberturas", "Otimização de espaços em apartamentos de luxo. Cozinhas integradas compactas, armários embutidos e soluções de armazenamento inteligentes."),
                ("🏨", "Projetos comerciais", "Móveis sob medida para boutique hotels, restaurantes e espaços comerciais. Qualidade luxo adaptada para uso intensivo."),
            ],
            "cta_h2": "Seu projeto<br><em>no nosso portfolio?</em>",
            "cta_p": "Entre em contato para discutir seu projeto e obter um orçamento gratuito.",
            "cta_btn": "💬 Entre em contato",
            "cta_sec": "Formulário de contato",
        },
    }
    d = t[lang]
    cards_html = "\n".join(
        f'<div class="feature-card"><div class="feature-icon">{ic}</div><h3>{ti}</h3><p>{de}</p></div>'
        for ic, ti, de in d["cards"]
    )
    contact_href = f"{root_prefix}contacto/{lang}/"
    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{d["eyebrow"]}</p>
  <h1>{d["h1"]}</h1>
  <p class="lead">{d["lead"]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div style="display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:300px 240px;gap:4px;max-width:1300px;margin:0 auto">
    <div style="grid-column:span 7;overflow:hidden"><img src="{root_prefix}images/portfolio-1.jpg" alt="Ka'ax Creación portfolio" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 5;overflow:hidden"><img src="{root_prefix}images/portfolio-2.jpg" alt="Ka'ax Creación portfolio" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 4;overflow:hidden"><img src="{root_prefix}images/portfolio-3.jpg" alt="Ka'ax Creación portfolio" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 4;overflow:hidden"><img src="{root_prefix}images/adn-detail.jpg" alt="Ka'ax Creación detail" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 4;overflow:hidden"><img src="{root_prefix}images/portfolio-4.jpg" alt="Ka'ax Creación portfolio" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
  </div>
</div>
<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px">{d["h2"]}</h2>
    <div class="content-grid-3" style="margin-top:40px">{cards_html}</div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>{d["cta_h2"]}</h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:620px;margin-bottom:36px">{d["cta_p"]}</p>
  <div class="cta-buttons" style="justify-content:flex-start">
    <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">{d["cta_btn"]}</a>
    <a href="{contact_href}" class="btn-secondary">{d["cta_sec"]}</a>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE METODO — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_metodo(lang, root_prefix):
    wa = wa_url_lang(lang)
    t = {
        "fr": {
            "eyebrow": "Notre savoir-faire — Ka'ax Création",
            "h1": "Notre<br><em>Méthode</em>",
            "lead": "Ka'ax Création est née de la rencontre entre l'excellence artisanale française et la passion pour le bois mexicain. Notre méthode repose sur la transmission du geste, la rigueur des finitions et le respect du client.",
            "steps": [
                ("01", "Écoute &amp; conseil", "Chaque projet commence par une écoute attentive. Nous analysons vos besoins, votre espace et votre budget pour vous proposer la solution la plus adaptée."),
                ("02", "Conception sur mesure", "Nos plans 3D vous permettent de visualiser votre future cuisine ou dressing avant la fabrication. Chaque détail est validé avec vous."),
                ("03", "Fabrication artisanale", "Dans notre atelier de Playa del Carmen, chaque pièce est taillée, assemblée et finalisée à la main. Nous utilisons des machines de précision et les gestes appris des Compagnons."),
                ("04", "Pose &amp; garantie", "Notre équipe installe votre mobilier avec le même soin qu'en atelier. Garantie de 3 ans sur toute la menuiserie Ka'ax Création."),
            ],
            "adn_title": "L'ADN<br><em>Ka'ax Création</em>",
            "adn_items": [
                ("🎓", "Compagnons du Tour de France", "Major de promotion 2023. La plus haute distinction artisanale française, transmise de maître à compagnon depuis des siècles."),
                ("🌿", "Ka'ax — «forêt» en maya", "Notre nom est un hommage aux forêts mayas et aux bois locaux qui inspirent notre travail. Enracinés ici, formés en Europe."),
                ("🌍", "Matériaux européens sélectionnés", "Panneaux Egger, quartz Silestone, ferrures Blum &amp; Hettich — les mêmes marques qu'en Europe, importées directement pour chaque projet."),
            ],
            "cta_h2": "Envie d'en savoir plus<br><em>sur notre méthode ?</em>",
            "cta_btn": "💬 Parlons de votre projet",
            "cta_sec": "Formulaire de contact",
        },
        "en": {
            "eyebrow": "Our expertise — Ka'ax Creación",
            "h1": "Our<br><em>Method</em>",
            "lead": "Ka'ax Creación was born from the meeting of French artisan excellence and a passion for Mexican wood. Our method is built on the transmission of craft, the rigor of finishing and the respect for every client.",
            "steps": [
                ("01", "Listening &amp; advice", "Every project begins with careful listening. We analyze your needs, your space and your budget to propose the most suitable solution."),
                ("02", "Custom design", "Our 3D plans let you visualize your future kitchen or closet before fabrication. Every detail is validated with you."),
                ("03", "Artisan fabrication", "In our Playa del Carmen workshop, each piece is cut, assembled and finished by hand. We use precision machinery and techniques learned from the Compagnons."),
                ("04", "Installation &amp; warranty", "Our team installs your furniture with the same care as in the workshop. 3-year warranty on all Ka'ax Creación cabinetry."),
            ],
            "adn_title": "The Ka'ax Creación<br><em>DNA</em>",
            "adn_items": [
                ("🎓", "Compagnons du Tour de France", "Top Graduate 2023. France's highest artisan distinction, passed from master to apprentice for centuries."),
                ("🌿", "Ka'ax — 'forest' in Mayan", "Our name is a tribute to the Mayan forests and local woods that inspire our work. Rooted here, trained in Europe."),
                ("🌍", "Selected European materials", "Egger panels, Silestone quartz, Blum &amp; Hettich hardware — the same European brands, imported directly for each project."),
            ],
            "cta_h2": "Want to know more<br><em>about our method?</em>",
            "cta_btn": "💬 Let's talk about your project",
            "cta_sec": "Contact form",
        },
        "it": {
            "eyebrow": "Il nostro know-how — Ka'ax Creación",
            "h1": "Il nostro<br><em>Metodo</em>",
            "lead": "Ka'ax Creación nasce dall'incontro tra l'eccellenza artigianale francese e la passione per il legno messicano. Il nostro metodo si basa sulla trasmissione del gesto, il rigore delle finiture e il rispetto del cliente.",
            "steps": [
                ("01", "Ascolto &amp; consulenza", "Ogni progetto inizia con un ascolto attento. Analizziamo le vostre esigenze, il vostro spazio e il vostro budget per proporre la soluzione più adatta."),
                ("02", "Progettazione su misura", "I nostri piani 3D vi permettono di visualizzare la futura cucina o cabina armadio prima della produzione. Ogni dettaglio viene validato con voi."),
                ("03", "Produzione artigianale", "Nel nostro laboratorio di Playa del Carmen, ogni pezzo è tagliato, assemblato e rifinito a mano con le tecniche apprese dai Compagnons."),
                ("04", "Posa &amp; garanzia", "Il nostro team installa i vostri mobili con la stessa cura del laboratorio. Garanzia 3 anni su tutta la falegnameria Ka'ax Creación."),
            ],
            "adn_title": "Il DNA<br><em>Ka'ax Creación</em>",
            "adn_items": [
                ("🎓", "Compagnons du Tour de France", "Primo della promozione 2023. La più alta distinzione artigianale francese, trasmessa di maestro in maestro da secoli."),
                ("🌿", "Ka'ax — «foresta» in maya", "Il nostro nome è un omaggio alle foreste maya e ai legni locali che ispirano il nostro lavoro. Radicati qui, formati in Europa."),
                ("🌍", "Materiali europei selezionati", "Pannelli Egger, quarzo Silestone, ferramenta Blum &amp; Hettich — gli stessi marchi europei, importati direttamente per ogni progetto."),
            ],
            "cta_h2": "Volete saperne di più<br><em>sul nostro metodo?</em>",
            "cta_btn": "💬 Parliamo del vostro progetto",
            "cta_sec": "Modulo di contatto",
        },
        "de": {
            "eyebrow": "Unser Handwerk — Ka'ax Creación",
            "h1": "Unsere<br><em>Methode</em>",
            "lead": "Ka'ax Creación entstand aus der Begegnung zwischen französischer Handwerkskunst und einer Leidenschaft für mexikanisches Holz. Unsere Methode basiert auf der Weitergabe des Handwerks, der Präzision der Oberflächen und dem Respekt für jeden Kunden.",
            "steps": [
                ("01", "Zuhören &amp; Beratung", "Jedes Projekt beginnt mit aufmerksamem Zuhören. Wir analysieren Ihre Bedürfnisse, Ihren Raum und Ihr Budget, um die passendste Lösung vorzuschlagen."),
                ("02", "Maßplanung", "Unsere 3D-Pläne ermöglichen es Ihnen, Ihre zukünftige Küche oder Ihren Ankleideraum vor der Fertigung zu visualisieren. Jedes Detail wird mit Ihnen abgestimmt."),
                ("03", "Handwerkliche Fertigung", "In unserer Werkstatt in Playa del Carmen wird jedes Teil von Hand zugeschnitten, montiert und veredelt. Wir verwenden Präzisionsmaschinen und die von den Compagnons erlernten Techniken."),
                ("04", "Einbau &amp; Garantie", "Unser Team baut Ihre Möbel mit der gleichen Sorgfalt wie in der Werkstatt ein. 3 Jahre Garantie auf alle Ka'ax Creación Schreinerarbeiten."),
            ],
            "adn_title": "Die Ka'ax Creación<br><em>DNA</em>",
            "adn_items": [
                ("🎓", "Compagnons du Tour de France", "Jahrgangsbester 2023. Frankreichs höchste Handwerksauszeichnung, seit Jahrhunderten von Meister zu Gesellen weitergegeben."),
                ("🌿", "Ka'ax — «Wald» auf Maya", "Unser Name ist eine Hommage an die Maya-Wälder und lokalen Hölzer, die unsere Arbeit inspirieren. Hier verwurzelt, in Europa ausgebildet."),
                ("🌍", "Ausgewählte europäische Materialien", "Egger-Platten, Silestone-Quarz, Blum &amp; Hettich-Beschläge — dieselben europäischen Marken, direkt für jedes Projekt importiert."),
            ],
            "cta_h2": "Möchten Sie mehr<br><em>über unsere Methode erfahren?</em>",
            "cta_btn": "💬 Sprechen Sie mit uns",
            "cta_sec": "Kontaktformular",
        },
        "ru": {
            "eyebrow": "Наше мастерство — Ka'ax Creación",
            "h1": "Наш<br><em>Метод</em>",
            "lead": "Ka'ax Creación родилась на пересечении французского ремесленного совершенства и страсти к мексиканской древесине. Наш метод основан на передаче мастерства, строгости отделки и уважении к каждому клиенту.",
            "steps": [
                ("01", "Слушаем &amp; консультируем", "Каждый проект начинается с внимательного слушания. Мы анализируем ваши потребности, пространство и бюджет, чтобы предложить наиболее подходящее решение."),
                ("02", "Проектируем на заказ", "Наши 3D-планы позволяют вам увидеть будущую кухню или гардеробную до начала производства. Каждая деталь согласовывается с вами."),
                ("03", "Ручное изготовление", "В нашей мастерской в Плая-дель-Кармен каждая деталь вырезается, собирается и доводится до совершенства вручную, с применением техник, усвоенных у Compagnons."),
                ("04", "Монтаж &amp; гарантия", "Наша команда устанавливает мебель с той же тщательностью, что и в мастерской. Гарантия 3 года на всю мебель Ka'ax Creación."),
            ],
            "adn_title": "ДНК<br><em>Ka'ax Creación</em>",
            "adn_items": [
                ("🎓", "Compagnons du Tour de France", "Лучший выпускник 2023. Высшая ремесленная награда Франции, передаваемая от мастера к ученику на протяжении столетий."),
                ("🌿", "Ka'ax — «лес» на языке майя", "Наше название — дань уважения лесам майя и местным породам дерева, которые вдохновляют нашу работу. Корни здесь, образование — в Европе."),
                ("🌍", "Отборные европейские материалы", "Панели Egger, кварц Silestone, фурнитура Blum &amp; Hettich — те же европейские бренды, импортируемые напрямую для каждого проекта."),
            ],
            "cta_h2": "Хотите узнать больше<br><em>о нашем методе?</em>",
            "cta_btn": "💬 Обсудить ваш проект",
            "cta_sec": "Форма связи",
        },
        "pt": {
            "eyebrow": "Nosso saber-fazer — Ka'ax Creación",
            "h1": "Nosso<br><em>Método</em>",
            "lead": "Ka'ax Creación nasceu do encontro entre a excelência artesanal francesa e a paixão pela madeira mexicana. Nosso método baseia-se na transmissão do gesto, no rigor dos acabamentos e no respeito pelo cliente.",
            "steps": [
                ("01", "Escuta &amp; conselho", "Cada projeto começa com uma escuta atenta. Analisamos as suas necessidades, espaço e orçamento para propor a solução mais adequada."),
                ("02", "Projeto sob medida", "Nossos planos 3D permitem que você visualize a sua futura cozinha ou closet antes da fabricação. Cada detalhe é validado com você."),
                ("03", "Fabricação artesanal", "Na nossa oficina em Playa del Carmen, cada peça é cortada, montada e acabada à mão com as técnicas aprendidas dos Compagnons."),
                ("04", "Instalação &amp; garantia", "Nossa equipa instala o seu mobiliário com o mesmo cuidado da oficina. Garantia de 3 anos em toda a marcenaria Ka'ax Creación."),
            ],
            "adn_title": "O DNA<br><em>Ka'ax Creación</em>",
            "adn_items": [
                ("🎓", "Compagnons du Tour de France", "Melhor Aluno de 2023. A mais alta distinção artesanal francesa, transmitida de mestre a aprendiz há séculos."),
                ("🌿", "Ka'ax — «floresta» em maia", "Nosso nome é uma homenagem às florestas maias e madeiras locais que inspiram o nosso trabalho. Enraizados aqui, formados na Europa."),
                ("🌍", "Materiais europeus selecionados", "Painéis Egger, quartzo Silestone, ferragens Blum &amp; Hettich — as mesmas marcas europeias, importadas diretamente para cada projeto."),
            ],
            "cta_h2": "Quer saber mais<br><em>sobre o nosso método?</em>",
            "cta_btn": "💬 Fale connosco",
            "cta_sec": "Formulário de contato",
        },
    }
    d = t[lang]
    steps_html = "\n".join(
        f'<div class="process-step"><div class="step-num">{n}</div><h3>{title}</h3><p>{desc}</p></div>'
        for n, title, desc in d["steps"]
    )
    adn_html = "\n".join(
        f'<div class="feature-card"><div class="feature-icon">{ic}</div><h3>{ti}</h3><p>{de}</p></div>'
        for ic, ti, de in d["adn_items"]
    )
    contact_href = f"{root_prefix}contacto/{lang}/"
    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{d["eyebrow"]}</p>
  <h1>{d["h1"]}</h1>
  <p class="lead">{d["lead"]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="process-steps">{steps_html}</div>
</div>
<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px">{d["adn_title"]}</h2>
    <div class="content-grid-3" style="margin-top:40px">{adn_html}</div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>{d["cta_h2"]}</h2>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">{d["cta_btn"]}</a>
      <a href="{contact_href}" class="btn-secondary">{d["cta_sec"]}</a>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE NOSOTROS — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_nosotros(lang, root_prefix):
    wa = wa_url_lang(lang)
    t = {
        "fr": {
            "eyebrow": "Notre histoire — Ka'ax Création",
            "h1": "Notre<br><em>ADN</em>",
            "lead": "Ka'ax Création est née de la passion d'un artisan français pour le bois et les matériaux nobles, installé au cœur de la Riviera Maya. Un atelier artisanal au service des plus belles résidences de la région.",
            "story_h": "Deux fondateurs,<br><em>une vision commune</em>",
            "story_p": "Stéphane, expert en marketing digital et stratégie commerciale, et Raphaël, Major de promotion 2023 des Compagnons du Tour de France, ont uni leurs compétences pour créer Ka'ax Creación. L'un maîtrise les marchés internationaux et la clientèle d'exception, l'autre perpétue une tradition artisanale vieille de plusieurs siècles. Ensemble, ils ont fondé l'atelier de menuiserie d'exception de la Riviera Maya.",
            "vals": [
                ("🎓", "Excellence artisanale", "Le savoir-faire des Compagnons du Tour de France — 1 500 heures de formation annuelle, compagnonnage maître-élève, contrôle qualité à chaque étape."),
                ("🌿", "Enracinement local", "Ka'ax signifie «forêt» en maya. Nous utilisons des matériaux adaptés au climat tropical de la péninsule du Yucatán, respectant l'environnement caribéen."),
                ("🤝", "Service personnalisé", "Chaque client est unique. De la première visite à la pose finale, vous avez un interlocuteur dédié et un suivi transparent à chaque étape."),
            ],
            "cta_h2": "Rencontrons-nous<br><em>pour votre projet</em>",
            "cta_btn": "💬 Discuter de votre projet",
            "cta_sec": "Formulaire de contact",
        },
        "en": {
            "eyebrow": "Our story — Ka'ax Creación",
            "h1": "Our<br><em>DNA</em>",
            "lead": "Ka'ax Creación was born from a French craftsman's passion for wood and noble materials, settled in the heart of the Riviera Maya. An artisan workshop serving the finest residences in the region.",
            "story_h": "Two founders,<br><em>one shared vision</em>",
            "story_p": "Stéphane, expert in digital marketing and commercial strategy, and Raphaël, Top Graduate 2023 of the Compagnons du Tour de France, combined their skills to create Ka'ax Creación. One masters international markets and exceptional clientele, the other perpetuates a centuries-old artisan tradition. Together, they founded the finest custom carpentry workshop in the Riviera Maya.",
            "vals": [
                ("🎓", "Artisan excellence", "The Compagnons du Tour de France expertise — 1,500 hours of annual training, master-apprentice companionship, quality control at every stage."),
                ("🌿", "Local roots", "Ka'ax means 'forest' in Mayan. We use materials adapted to the tropical climate of the Yucatan Peninsula, respecting the Caribbean environment."),
                ("🤝", "Personalized service", "Every client is unique. From the first visit to the final installation, you have a dedicated contact person and transparent follow-up at every step."),
            ],
            "cta_h2": "Let's meet<br><em>for your project</em>",
            "cta_btn": "💬 Discuss your project",
            "cta_sec": "Contact form",
        },
        "it": {
            "eyebrow": "La nostra storia — Ka'ax Creación",
            "h1": "Il nostro<br><em>DNA</em>",
            "lead": "Ka'ax Creación nasce dalla passione di un artigiano francese per il legno e i materiali nobili, insediato nel cuore della Riviera Maya. Un laboratorio artigianale al servizio delle più belle residenze della regione.",
            "story_h": "Due fondatori,<br><em>una visione comune</em>",
            "story_p": "Stéphane, esperto di marketing digitale e strategia commerciale, e Raphaël, Primo della promozione 2023 dei Compagnons du Tour de France, hanno unito le loro competenze per creare Ka'ax Creación. L'uno padroneggia i mercati internazionali e la clientela d'eccezione, l'altro perpetua una tradizione artigianale secolare. Insieme hanno fondato il laboratorio di falegnameria d'eccellenza della Riviera Maya.",
            "vals": [
                ("🎓", "Eccellenza artigianale", "Il know-how dei Compagnons du Tour de France — 1.500 ore di formazione annuale, compagnonnage maestro-allievo, controllo qualità ad ogni fase."),
                ("🌿", "Radicamento locale", "Ka'ax significa «foresta» in maya. Utilizziamo materiali adatti al clima tropicale della penisola dello Yucatán, rispettando l'ambiente caraibico."),
                ("🤝", "Servizio personalizzato", "Ogni cliente è unico. Dalla prima visita alla posa finale, avete un interlocutore dedicato e un follow-up trasparente ad ogni tappa."),
            ],
            "cta_h2": "Incontriamoci<br><em>per il vostro progetto</em>",
            "cta_btn": "💬 Parliamo del vostro progetto",
            "cta_sec": "Modulo di contatto",
        },
        "de": {
            "eyebrow": "Unsere Geschichte — Ka'ax Creación",
            "h1": "Unsere<br><em>DNA</em>",
            "lead": "Ka'ax Creación entstand aus der Leidenschaft eines französischen Handwerkers für Holz und edle Materialien, der sich im Herzen der Riviera Maya niedergelassen hat. Eine Handwerkswerkstatt im Dienst der schönsten Residenzen der Region.",
            "story_h": "Zwei Gründer,<br><em>eine gemeinsame Vision</em>",
            "story_p": "Stéphane, Experte für digitales Marketing und Handelsstrategie, und Raphaël, Jahrgangsbester 2023 der Compagnons du Tour de France, haben ihre Kompetenzen vereint, um Ka'ax Creación zu gründen. Einer beherrscht internationale Märkte und anspruchsvolle Kundschaft, der andere pflegt eine jahrhundertealte Handwerkstradition. Gemeinsam gründeten sie die feinste Schreinerwerkstatt der Riviera Maya.",
            "vals": [
                ("🎓", "Handwerkliche Exzellenz", "Das Know-how der Compagnons du Tour de France — 1.500 Stunden jährliche Ausbildung, Meister-Gesellen-Kompagnonnage, Qualitätskontrolle auf jeder Stufe."),
                ("🌿", "Lokale Verwurzelung", "Ka'ax bedeutet «Wald» auf Maya. Wir verwenden Materialien, die für das tropische Klima der Yucatan-Halbinsel geeignet sind und die karibische Umwelt respektieren."),
                ("🤝", "Persönlicher Service", "Jeder Kunde ist einzigartig. Vom ersten Besuch bis zur endgültigen Montage haben Sie einen dedizierten Ansprechpartner und transparente Begleitung auf jedem Schritt."),
            ],
            "cta_h2": "Treffen wir uns<br><em>für Ihr Projekt</em>",
            "cta_btn": "💬 Über Ihr Projekt sprechen",
            "cta_sec": "Kontaktformular",
        },
        "ru": {
            "eyebrow": "Наша история — Ka'ax Creación",
            "h1": "Наша<br><em>ДНК</em>",
            "lead": "Ka'ax Creación родилась из страсти французского мастера к дереву и благородным материалам, обосновавшегося в самом сердце Ривьеры Майя. Ремесленная мастерская на службе лучших резиденций региона.",
            "story_h": "Два основателя,<br><em>общее видение</em>",
            "story_p": "Стефан, эксперт по цифровому маркетингу и коммерческой стратегии, и Рафаэль, лучший выпускник 2023 года гильдии Compagnons du Tour de France, объединили свои навыки для создания Ka'ax Creación. Один осваивает международные рынки и взыскательную клиентуру, другой продолжает многовековую ремесленную традицию. Вместе они основали лучшую столярную мастерскую Ривьеры Майя.",
            "vals": [
                ("🎓", "Ремесленное совершенство", "Мастерство Compagnons du Tour de France — 1500 часов ежегодного обучения, наставничество мастер-ученик, контроль качества на каждом этапе."),
                ("🌿", "Местные корни", "Ka'ax означает «лес» на языке майя. Мы используем материалы, адаптированные к тропическому климату полуострова Юкатан, уважая карибскую среду."),
                ("🤝", "Персональный сервис", "Каждый клиент уникален. От первого визита до финальной установки у вас есть выделенный контактный человек и прозрачное сопровождение на каждом шагу."),
            ],
            "cta_h2": "Встретимся<br><em>для обсуждения вашего проекта</em>",
            "cta_btn": "💬 Обсудить проект",
            "cta_sec": "Форма связи",
        },
        "pt": {
            "eyebrow": "Nossa história — Ka'ax Creación",
            "h1": "Nosso<br><em>DNA</em>",
            "lead": "Ka'ax Creación nasceu da paixão de um artesão francês pela madeira e materiais nobres, instalado no coração da Riviera Maya. Uma oficina artesanal ao serviço das mais belas residências da região.",
            "story_h": "Dois fundadores,<br><em>uma visão comum</em>",
            "story_p": "Stéphane, especialista em marketing digital e estratégia comercial, e Raphaël, Melhor Aluno de 2023 dos Compagnons du Tour de France, uniram as suas competências para criar a Ka'ax Creación. Um domina os mercados internacionais e a clientela de exceção, o outro perpetua uma tradição artesanal de séculos. Juntos fundaram a mais fina oficina de marcenaria da Riviera Maya.",
            "vals": [
                ("🎓", "Excelência artesanal", "O saber-fazer dos Compagnons du Tour de France — 1.500 horas de formação anual, compagnonnage mestre-aluno, controlo de qualidade em cada etapa."),
                ("🌿", "Enraizamento local", "Ka'ax significa «floresta» em maia. Usamos materiais adaptados ao clima tropical da Península do Yucatán, respeitando o ambiente caribenho."),
                ("🤝", "Serviço personalizado", "Cada cliente é único. Da primeira visita à instalação final, tem um interlocutor dedicado e acompanhamento transparente em cada etapa."),
            ],
            "cta_h2": "Encontremo-nos<br><em>para o seu projeto</em>",
            "cta_btn": "💬 Discutir o seu projeto",
            "cta_sec": "Formulário de contato",
        },
    }
    d = t[lang]
    vals_html = "\n".join(
        f'<div class="feature-card"><div class="feature-icon">{ic}</div><h3>{ti}</h3><p>{de}</p></div>'
        for ic, ti, de in d["vals"]
    )
    contact_href = f"{root_prefix}contacto/{lang}/"
    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{d["eyebrow"]}</p>
  <h1>{d["h1"]}</h1>
  <p class="lead">{d["lead"]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>{d["story_h"]}</h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:48px">{d["story_p"]}</p>
  <div class="content-grid-3">{vals_html}</div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>{d["cta_h2"]}</h2>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">{d["cta_btn"]}</a>
      <a href="{contact_href}" class="btn-secondary">{d["cta_sec"]}</a>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE CONTACTO — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_contacto(lang, root_prefix):
    wa = wa_url_lang(lang)
    t = {
        "fr": {
            "eyebrow": "Contact — Ka'ax Création",
            "h1": "Demande de<br><em>devis gratuit</em>",
            "lead": "Chaque projet commence par une conversation. Décrivez votre projet, et nous vous répondrons dans les 24 heures avec un premier avis et les prochaines étapes.",
            "wa_h": "Contact direct<br><em>WhatsApp</em>",
            "wa_p": "La façon la plus rapide de nous contacter. Envoyez-nous une photo de votre espace et nous vous répondrons immédiatement.",
            "wa_btn": "💬 Écrire sur WhatsApp",
            "form_h": "Formulaire de demande",
            "fname": "Prénom", "lname": "Nom", "email_lbl": "Email", "phone_lbl": "Téléphone (WhatsApp)",
            "zone_lbl": "Zone d'intervention", "zone_default": "Choisissez votre zone",
            "project_lbl": "Type de projet", "project_default": "Type de projet",
            "project_opts": ["Cuisine à medida", "Dressing / Closet", "Armoire sur mesure", "Projet complet (cuisine + dressing)", "Autre"],
            "msg_lbl": "Décrivez votre projet", "submit": "Envoyer la demande",
            "note": "Réponse garantie sous 24h · Devis gratuit · Visite technique offerte",
        },
        "en": {
            "eyebrow": "Contact — Ka'ax Creación",
            "h1": "Request a<br><em>free quote</em>",
            "lead": "Every project begins with a conversation. Describe your project, and we'll respond within 24 hours with an initial assessment and next steps.",
            "wa_h": "Direct contact<br><em>on WhatsApp</em>",
            "wa_p": "The quickest way to reach us. Send us a photo of your space and we'll respond immediately.",
            "wa_btn": "💬 Message on WhatsApp",
            "form_h": "Request form",
            "fname": "First name", "lname": "Last name", "email_lbl": "Email", "phone_lbl": "Phone (WhatsApp)",
            "zone_lbl": "Service area", "zone_default": "Choose your area",
            "project_lbl": "Project type", "project_default": "Project type",
            "project_opts": ["Custom kitchen", "Walk-in closet", "Custom closet", "Full project (kitchen + closet)", "Other"],
            "msg_lbl": "Describe your project", "submit": "Send request",
            "note": "Response within 24h · Free quote · Technical visit included",
        },
        "it": {
            "eyebrow": "Contatto — Ka'ax Creación",
            "h1": "Richiesta di<br><em>preventivo gratuito</em>",
            "lead": "Ogni progetto inizia con una conversazione. Descrivete il vostro progetto e vi risponderemo entro 24 ore con una prima valutazione e i passi successivi.",
            "wa_h": "Contatto diretto<br><em>su WhatsApp</em>",
            "wa_p": "Il modo più rapido per contattarci. Inviateci una foto del vostro spazio e risponderemo immediatamente.",
            "wa_btn": "💬 Scrivici su WhatsApp",
            "form_h": "Modulo di richiesta",
            "fname": "Nome", "lname": "Cognome", "email_lbl": "Email", "phone_lbl": "Telefono (WhatsApp)",
            "zone_lbl": "Zona di intervento", "zone_default": "Scegliete la vostra zona",
            "project_lbl": "Tipo di progetto", "project_default": "Tipo di progetto",
            "project_opts": ["Cucina su misura", "Walk-in closet", "Armadio su misura", "Progetto completo (cucina + cabina)", "Altro"],
            "msg_lbl": "Descrivete il vostro progetto", "submit": "Invia la richiesta",
            "note": "Risposta entro 24h · Preventivo gratuito · Visita tecnica inclusa",
        },
        "de": {
            "eyebrow": "Kontakt — Ka'ax Creación",
            "h1": "Kostenloses<br><em>Angebot anfordern</em>",
            "lead": "Jedes Projekt beginnt mit einem Gespräch. Beschreiben Sie Ihr Projekt, und wir antworten Ihnen innerhalb von 24 Stunden mit einer ersten Einschätzung und den nächsten Schritten.",
            "wa_h": "Direktkontakt<br><em>über WhatsApp</em>",
            "wa_p": "Der schnellste Weg uns zu erreichen. Schicken Sie uns ein Foto Ihres Raumes und wir antworten sofort.",
            "wa_btn": "💬 WhatsApp schreiben",
            "form_h": "Anfageformular",
            "fname": "Vorname", "lname": "Nachname", "email_lbl": "E-Mail", "phone_lbl": "Telefon (WhatsApp)",
            "zone_lbl": "Servicegebiet", "zone_default": "Gebiet auswählen",
            "project_lbl": "Projekttyp", "project_default": "Projekttyp",
            "project_opts": ["Maßküche", "Walk-in Ankleideraum", "Maßschrank", "Vollständiges Projekt (Küche + Ankleideraum)", "Sonstiges"],
            "msg_lbl": "Beschreiben Sie Ihr Projekt", "submit": "Anfrage senden",
            "note": "Antwort innerhalb von 24h · Kostenloses Angebot · Technischer Besuch inklusive",
        },
        "ru": {
            "eyebrow": "Контакт — Ka'ax Creación",
            "h1": "Запрос<br><em>бесплатного расчёта</em>",
            "lead": "Каждый проект начинается с разговора. Опишите ваш проект, и мы ответим в течение 24 часов с первоначальной оценкой и следующими шагами.",
            "wa_h": "Прямой контакт<br><em>в WhatsApp</em>",
            "wa_p": "Самый быстрый способ связаться с нами. Пришлите фото вашего пространства и мы ответим немедленно.",
            "wa_btn": "💬 Написать в WhatsApp",
            "form_h": "Форма запроса",
            "fname": "Имя", "lname": "Фамилия", "email_lbl": "Email", "phone_lbl": "Телефон (WhatsApp)",
            "zone_lbl": "Зона обслуживания", "zone_default": "Выберите зону",
            "project_lbl": "Тип проекта", "project_default": "Тип проекта",
            "project_opts": ["Кухня на заказ", "Walk-in гардеробная", "Шкаф на заказ", "Полный проект (кухня + гардеробная)", "Другое"],
            "msg_lbl": "Опишите ваш проект", "submit": "Отправить запрос",
            "note": "Ответ в течение 24ч · Бесплатный расчёт · Технический выезд включён",
        },
        "pt": {
            "eyebrow": "Contato — Ka'ax Creación",
            "h1": "Solicite um<br><em>orçamento grátis</em>",
            "lead": "Cada projeto começa com uma conversa. Descreva o seu projeto e responderemos em 24 horas com uma avaliação inicial e os próximos passos.",
            "wa_h": "Contato direto<br><em>no WhatsApp</em>",
            "wa_p": "A forma mais rápida de nos contactar. Envie-nos uma foto do seu espaço e respondemos imediatamente.",
            "wa_btn": "💬 Escrever no WhatsApp",
            "form_h": "Formulário de pedido",
            "fname": "Nome", "lname": "Apelido", "email_lbl": "Email", "phone_lbl": "Telefone (WhatsApp)",
            "zone_lbl": "Zona de serviço", "zone_default": "Escolha a sua zona",
            "project_lbl": "Tipo de projeto", "project_default": "Tipo de projeto",
            "project_opts": ["Cozinha sob medida", "Walk-in closet", "Armário sob medida", "Projeto completo (cozinha + closet)", "Outro"],
            "msg_lbl": "Descreva o seu projeto", "submit": "Enviar pedido",
            "note": "Resposta em 24h · Orçamento grátis · Visita técnica incluída",
        },
    }
    d = t[lang]
    opts_html = "\n".join(f'<option value="{o}">{o}</option>' for o in d["project_opts"])
    # Zone options (same names across languages)
    zone_opts = [
        ("playa-del-carmen", "Playa del Carmen"),
        ("cancun", "Cancún"),
        ("tulum", "Tulum"),
        ("puerto-morelos", "Puerto Morelos"),
        ("puerto-aventuras", "Puerto Aventuras"),
        ("coba-bacalar", "Cobá / Bacalar"),
        ("felipe-carrillo-puerto", "Felipe Carrillo Puerto"),
        ("isla-mujeres", "Isla Mujeres"),
        ("cozumel", "Cozumel"),
        ("merida", "Mérida"),
        ("holbox", "Holbox"),
        ("valladolid", "Valladolid"),
        ("tizimin", "Tizimín"),
        ("campeche", "Campeche"),
    ]
    zone_opts_html = "\n".join(f'<option value="{slug}">{name}</option>' for slug, name in zone_opts)
    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{d["eyebrow"]}</p>
  <h1>{d["h1"]}</h1>
  <p class="lead">{d["lead"]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="contact-grid">
    <div>
      <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3vw,38px);font-weight:300;margin-bottom:16px">{d["wa_h"]}</h2>
      <p style="font-size:15px;line-height:1.9;opacity:.75;margin-bottom:32px">{d["wa_p"]}</p>
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener" style="display:inline-flex">{d["wa_btn"]}</a>
    </div>
    <div>
      <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(24px,2.5vw,32px);font-weight:300;margin-bottom:24px">{d["form_h"]}</h2>
      <form action="https://formspree.io/f/mzerqzzb" method="POST" style="display:flex;flex-direction:column;gap:16px">
        <div class="name-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
          <input type="text" name="prenom" placeholder="{d["fname"]}" required style="padding:14px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none">
          <input type="text" name="nom" placeholder="{d["lname"]}" required style="padding:14px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none">
        </div>
        <input type="email" name="email" placeholder="{d["email_lbl"]}" required style="padding:14px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none">
        <input type="tel" name="tel" placeholder="{d["phone_lbl"]}" style="padding:14px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none">
        <select name="zone" style="padding:14px 16px;background:rgba(13,13,13,.95);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none">
          <option value="">{d["zone_default"]}</option>
          {zone_opts_html}
        </select>
        <select name="projet" style="padding:14px 16px;background:rgba(13,13,13,.95);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none">
          <option value="">{d["project_default"]}</option>
          {opts_html}
        </select>
        <textarea name="message" placeholder="{d["msg_lbl"]}" rows="4" required style="padding:14px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.3);color:#fff;font-family:Inter,sans-serif;font-size:14px;border-radius:0;outline:none;resize:vertical"></textarea>
        <input type="hidden" name="_language" value="{lang}">
        <button type="submit" style="padding:16px 32px;background:var(--or);color:#0D0D0D;font-family:'Cormorant Garamond',serif;font-size:16px;font-weight:600;letter-spacing:1px;border:none;cursor:pointer;text-transform:uppercase;width:100%">{d["submit"]}</button>
        <p style="font-size:12px;opacity:.5;text-align:center">{d["note"]}</p>
      </form>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE ZONA INDEX — TRADUCTIONS
# ═══════════════════════════════════════════════════════════════

def content_zona_index(lang, root_prefix):
    wa = wa_url_lang(lang)
    t = {
        "fr": {
            "eyebrow": "Couverture — Ka'ax Création",
            "h1": "Zones<br><em>d'intervention</em>",
            "lead": "Ka'ax Création est basé à Playa del Carmen et couvre toute la Riviera Maya, les îles, et accepte des projets sélectifs dans la Péninsule du Yucatán. Déplacement et installation inclus.",
            "rm_h": "Riviera Maya &amp;<br><em>Îles</em>",
            "rm_p": "Notre zone principale d'intervention. Nous fabriquons et installons cuisines, dressings et meubles sur mesure sur toute la côte caribéenne de Quintana Roo.",
            "yuc_h": "Yucatán &amp; Campeche —<br><em>Projets sélectifs</em>",
            "yuc_p": "Pour des projets de grande envergure ou de luxe exclusif, Ka'ax Création accepte des commandes dans la Péninsule du Yucatán et Campeche.",
            "cta_h2": "Dans quelle zone<br><em>êtes-vous ?</em>",
            "cta_p": "Contactez-nous pour vérifier la disponibilité dans votre zone",
            "cta_btn": "💬 Vérifier la disponibilité",
            "cta_sec": "Formulaire de contact",
        },
        "en": {
            "eyebrow": "Coverage — Ka'ax Creación",
            "h1": "Service<br><em>Areas</em>",
            "lead": "Ka'ax Creación is based in Playa del Carmen and covers the entire Riviera Maya, the islands, and accepts selective projects in the Yucatan Peninsula. Travel and installation included.",
            "rm_h": "Riviera Maya &amp;<br><em>Islands</em>",
            "rm_p": "Our main service area. We build and install kitchens, closets and custom furniture throughout the Caribbean coast of Quintana Roo.",
            "yuc_h": "Yucatán &amp; Campeche —<br><em>Selective projects</em>",
            "yuc_p": "For large-scale or exclusive luxury projects, Ka'ax Creación accepts commissions in the Yucatan Peninsula and Campeche.",
            "cta_h2": "Which area<br><em>are you in?</em>",
            "cta_p": "Contact us to check availability in your area",
            "cta_btn": "💬 Check availability",
            "cta_sec": "Contact form",
        },
        "it": {
            "eyebrow": "Copertura — Ka'ax Creación",
            "h1": "Zone di<br><em>Intervento</em>",
            "lead": "Ka'ax Creación è basata a Playa del Carmen e copre tutta la Riviera Maya, le isole, e accetta progetti selettivi nella Penisola dello Yucatán. Trasferta e installazione incluse.",
            "rm_h": "Riviera Maya &amp;<br><em>Isole</em>",
            "rm_p": "La nostra zona di intervento principale. Realizziamo e installiamo cucine, cabine armadio e mobili su misura su tutta la costa caraibica di Quintana Roo.",
            "yuc_h": "Yucatán &amp; Campeche —<br><em>Progetti selettivi</em>",
            "yuc_p": "Per progetti di grande envergadura o di lusso esclusivo, Ka'ax Creación accetta commesse nella Penisola dello Yucatán e a Campeche.",
            "cta_h2": "In quale zona<br><em>vi trovate?</em>",
            "cta_p": "Contattateci per verificare la disponibilità nella vostra zona",
            "cta_btn": "💬 Verificare disponibilità",
            "cta_sec": "Modulo di contatto",
        },
        "de": {
            "eyebrow": "Servicegebiete — Ka'ax Creación",
            "h1": "Service-<br><em>gebiete</em>",
            "lead": "Ka'ax Creación ist in Playa del Carmen ansässig und deckt die gesamte Riviera Maya, die Inseln ab und akzeptiert selektive Projekte auf der Yucatan-Halbinsel. Anfahrt und Einbau inklusive.",
            "rm_h": "Riviera Maya &amp;<br><em>Inseln</em>",
            "rm_p": "Unser Hauptservicegebiet. Wir fertigen und installieren Küchen, Ankleideräume und Maßmöbel überall an der karibischen Küste von Quintana Roo.",
            "yuc_h": "Yucatán &amp; Campeche —<br><em>Selektive Projekte</em>",
            "yuc_p": "Für großformatige oder exklusive Luxusprojekte akzeptiert Ka'ax Creación Aufträge auf der Yucatan-Halbinsel und in Campeche.",
            "cta_h2": "In welchem Gebiet<br><em>befinden Sie sich?</em>",
            "cta_p": "Kontaktieren Sie uns zur Prüfung der Verfügbarkeit in Ihrem Gebiet",
            "cta_btn": "💬 Verfügbarkeit prüfen",
            "cta_sec": "Kontaktformular",
        },
        "ru": {
            "eyebrow": "Зоны обслуживания — Ka'ax Creación",
            "h1": "Зоны<br><em>обслуживания</em>",
            "lead": "Ka'ax Creación базируется в Плая-дель-Кармен и охватывает всю Ривьеру Майя, острова, а также принимает избранные проекты на полуострове Юкатан. Доставка и монтаж включены.",
            "rm_h": "Ривьера Майя &amp;<br><em>Острова</em>",
            "rm_p": "Наша основная зона обслуживания. Мы изготавливаем и устанавливаем кухни, гардеробные и мебель на заказ по всему карибскому побережью Кинтана-Роо.",
            "yuc_h": "Юкатан &amp; Кампече —<br><em>Избранные проекты</em>",
            "yuc_p": "Для крупных или эксклюзивных люкс-проектов Ka'ax Creación принимает заказы на полуострове Юкатан и в Кампече.",
            "cta_h2": "В какой зоне<br><em>вы находитесь?</em>",
            "cta_p": "Свяжитесь с нами для проверки доступности в вашей зоне",
            "cta_btn": "💬 Проверить доступность",
            "cta_sec": "Форма связи",
        },
        "pt": {
            "eyebrow": "Cobertura — Ka'ax Creación",
            "h1": "Zonas de<br><em>Intervenção</em>",
            "lead": "Ka'ax Creación está sediada em Playa del Carmen e cobre toda a Riviera Maya, as ilhas, e aceita projetos seletivos na Península do Yucatán. Deslocação e instalação incluídas.",
            "rm_h": "Riviera Maya &amp;<br><em>Ilhas</em>",
            "rm_p": "A nossa zona principal de intervenção. Fabricamos e instalamos cozinhas, closets e móveis sob medida em toda a costa caribenha de Quintana Roo.",
            "yuc_h": "Yucatán &amp; Campeche —<br><em>Projetos seletivos</em>",
            "yuc_p": "Para projetos de grande envergadura ou de luxo exclusivo, Ka'ax Creación aceita encomendas na Península do Yucatán e Campeche.",
            "cta_h2": "Em que zona<br><em>se encontra?</em>",
            "cta_p": "Contacte-nos para verificar disponibilidade na sua zona",
            "cta_btn": "💬 Verificar disponibilidade",
            "cta_sec": "Formulário de contato",
        },
    }
    d = t[lang]
    # Zone links — labels stay in ES (place names)
    zones_rm = [
        ("playa-del-carmen", "🏖️", "Playa del Carmen", {"fr": "Notre base — réponse en 24h", "en": "Our base — 24h response time", "it": "La nostra base — risposta in 24h", "de": "Unser Standort — 24h Reaktionszeit", "ru": "Наша база — ответ в течение 24ч", "pt": "Nossa base — resposta em 24h"}),
        ("cancun", "🏙️", "Cancún", {"fr": "Riviera Maya Nord — Hotel Zone", "en": "North Riviera Maya — Hotel Zone", "it": "Riviera Maya Nord — Hotel Zone", "de": "Nördliche Riviera Maya — Hotel Zone", "ru": "Северная Ривьера Майя", "pt": "Riviera Maya Norte — Hotel Zone"}),
        ("tulum", "🌿", "Tulum", {"fr": "Riviera Maya Sud — villas de luxe", "en": "South Riviera Maya — luxury villas", "it": "Riviera Maya Sud — ville di lusso", "de": "Südliche Riviera Maya — Luxusvillen", "ru": "Южная Ривьера Майя — роскошные виллы", "pt": "Riviera Maya Sul — villas de luxo"}),
        ("puerto-morelos", "⚓", "Puerto Morelos", {"fr": "Entre Cancún et Playa del Carmen", "en": "Between Cancún and Playa del Carmen", "it": "Tra Cancún e Playa del Carmen", "de": "Zwischen Cancún und Playa del Carmen", "ru": "Между Канкуном и Плая-дель-Кармен", "pt": "Entre Cancún e Playa del Carmen"}),
        ("puerto-aventuras", "⛵", "Puerto Aventuras", {"fr": "Marina privée — résidences premium", "en": "Private marina — premium residences", "it": "Marina privata — residenze premium", "de": "Privatmarina — Premium-Residenzen", "ru": "Частная марина — премиум резиденции", "pt": "Marina privada — residências premium"}),
        ("coba-bacalar", "🏞️", "Cobá · Bacalar", {"fr": "Intérieur — projets sélectifs", "en": "Interior — selective projects", "it": "Interno — progetti selettivi", "de": "Inland — selektive Projekte", "ru": "Внутренние районы — избранные проекты", "pt": "Interior — projetos seletivos"}),
        ("felipe-carrillo-puerto", "🌳", "Felipe Carrillo Puerto", {"fr": "Sud de Quintana Roo", "en": "South of Quintana Roo", "it": "Sud di Quintana Roo", "de": "Süden von Quintana Roo", "ru": "Юг Кинтана-Роо", "pt": "Sul de Quintana Roo"}),
        ("isla-mujeres", "🏝️", "Isla Mujeres", {"fr": "Île face à Cancún — projets sélectifs", "en": "Island off Cancún — selective projects", "it": "Isola di fronte a Cancún", "de": "Insel vor Cancún — selektive Projekte", "ru": "Остров у Канкуна — избранные проекты", "pt": "Ilha em frente a Cancún"}),
        ("cozumel", "🤿", "Cozumel", {"fr": "Île face à Playa — projets sélectifs", "en": "Island off Playa — selective projects", "it": "Isola di fronte a Playa", "de": "Insel vor Playa — selektive Projekte", "ru": "Остров у Плая — избранные проекты", "pt": "Ilha em frente a Playa"}),
    ]
    zones_yuc = [
        ("merida", "🏛️", "Mérida", {"fr": "Capitale du Yucatán", "en": "Yucatán capital", "it": "Capitale dello Yucatán", "de": "Hauptstadt Yucatáns", "ru": "Столица Юкатана", "pt": "Capital do Yucatán"}),
        ("holbox", "🦩", "Holbox", {"fr": "Île sans voitures — luxe exclusif", "en": "Car-free island — exclusive luxury", "it": "Isola senza auto — lusso esclusivo", "de": "Autofreie Insel — exklusiver Luxus", "ru": "Безавтомобильный остров — эксклюзивный люкс", "pt": "Ilha sem carros — luxo exclusivo"}),
        ("valladolid", "🌺", "Valladolid", {"fr": "Cœur du Yucatán", "en": "Heart of Yucatán", "it": "Cuore dello Yucatán", "de": "Herz von Yucatán", "ru": "Сердце Юкатана", "pt": "Coração do Yucatán"}),
        ("tizimin", "🌾", "Tizimín", {"fr": "Nord du Yucatán", "en": "North Yucatán", "it": "Nord dello Yucatán", "de": "Nördliches Yucatán", "ru": "Север Юкатана", "pt": "Norte do Yucatán"}),
        ("campeche", "🏰", "Campeche", {"fr": "Capitale historique — projets sélectifs", "en": "Historic capital — selective projects", "it": "Capitale storica — progetti selettivi", "de": "Historische Hauptstadt", "ru": "Историческая столица", "pt": "Capital histórica"}),
    ]

    def zone_link(slug, icon, name, subs):
        sub = subs[lang]
        return f"""<a href="{root_prefix}zona/{slug}/{lang}/" class="zone-card">
        <span class="zone-card-icon">{icon}</span>
        <div>
          <div class="zone-card-name">{name}</div>
          <div class="zone-card-sub">{sub}</div>
        </div>
        <span class="zone-card-arrow">→</span>
      </a>"""

    rm_html = "\n".join(zone_link(*z) for z in zones_rm)
    yuc_html = "\n".join(zone_link(*z) for z in zones_yuc)
    contact_href = f"{root_prefix}contacto/{lang}/"

    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{d["eyebrow"]}</p>
  <h1>{d["h1"]}</h1>
  <p class="lead">{d["lead"]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>{d["rm_h"]}</h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;margin-bottom:32px">{d["rm_p"]}</p>
  <div class="zones-grid">{rm_html}</div>
</div>
<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:16px">{d["yuc_h"]}</h2>
    <p style="font-size:15px;line-height:1.9;opacity:.75;margin-bottom:32px;max-width:620px">{d["yuc_p"]}</p>
    <div class="zones-grid">{yuc_html}</div>
  </div>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>{d["cta_h2"]}</h2>
    <p>{d["cta_p"]}</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">{d["cta_btn"]}</a>
      <a href="{contact_href}" class="btn-secondary">{d["cta_sec"]}</a>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# PAGE ZONE — TEMPLATE MULTILINGUE
# ═══════════════════════════════════════════════════════════════

ZONE_INTRO_LANG = {
    "fr": {
        "eyebrow_tpl": "Ka'ax Création — {region}",
        "lead_tpl": "Ka'ax Création fabrique et installe des cuisines intégrales, dressings et meubles sur mesure à {name}. Notre atelier est à Playa del Carmen — même niveau d'exigence, même savoir-faire des Compagnons du Tour de France.",
        "h2_why": "Pourquoi Ka'ax Création<br><em>à {name_short} ?</em>",
        "features_tpl": [
            ("🏗️", "Fabrication locale", "Fabriqué dans notre atelier de Playa del Carmen. Zéro intermédiaire, délais maîtrisés, suivi personnalisé."),
            ("🇫🇷", "Savoir-faire des Compagnons", "Major de promotion 2023 des Compagnons du Tour de France — la plus haute distinction artisanale française."),
            ("🚐", "Déplacement inclus", "Le déplacement et l'installation à {name_short} sont inclus dans le devis. Pas de surprise."),
        ],
        "price_title": "Coût indicatif<br><em>à {name_short}</em>",
        "cta_h2": "Votre projet<br><em>à {name_short}</em>",
        "cta_p": "Devis gratuit · Réponse sous 24h · Déplacement inclus",
        "cta_btn": "💬 Devis WhatsApp",
        "contact_btn": "Formulaire de contact",
        "crumb_zones": "Zones",
    },
    "en": {
        "eyebrow_tpl": "Ka'ax Creación — {region}",
        "lead_tpl": "Ka'ax Creación builds and installs custom kitchens, walk-in closets and furniture in {name}. Our workshop is in Playa del Carmen — same quality standards, same Compagnons du Tour de France expertise.",
        "h2_why": "Why Ka'ax Creación<br><em>in {name_short}?</em>",
        "features_tpl": [
            ("🏗️", "Local fabrication", "Built in our Playa del Carmen workshop. No middlemen, controlled timelines, personalized follow-up."),
            ("🇫🇷", "Compagnons expertise", "Top Graduate 2023 of the Compagnons du Tour de France — France's highest artisan distinction."),
            ("🚐", "Travel included", "Travel and installation in {name_short} are included in the quote. No hidden costs."),
        ],
        "price_title": "Indicative cost<br><em>in {name_short}</em>",
        "cta_h2": "Your project<br><em>in {name_short}</em>",
        "cta_p": "Free quote · Response within 24h · Travel included",
        "cta_btn": "💬 WhatsApp Quote",
        "contact_btn": "Contact form",
        "crumb_zones": "Areas",
    },
    "it": {
        "eyebrow_tpl": "Ka'ax Creación — {region}",
        "lead_tpl": "Ka'ax Creación realizza e installa cucine integrate, cabine armadio e mobili su misura a {name}. Il nostro laboratorio è a Playa del Carmen — stesso livello di qualità, stesso know-how dei Compagnons du Tour de France.",
        "h2_why": "Perché Ka'ax Creación<br><em>a {name_short}?</em>",
        "features_tpl": [
            ("🏗️", "Produzione locale", "Realizzato nel nostro laboratorio di Playa del Carmen. Nessun intermediario, tempi controllati, follow-up personalizzato."),
            ("🇫🇷", "Maestria dei Compagnons", "Primo della promozione 2023 dei Compagnons du Tour de France — la più alta distinzione artigianale francese."),
            ("🚐", "Trasferta inclusa", "La trasferta e l'installazione a {name_short} sono incluse nel preventivo. Nessuna sorpresa."),
        ],
        "price_title": "Costo indicativo<br><em>a {name_short}</em>",
        "cta_h2": "Il vostro progetto<br><em>a {name_short}</em>",
        "cta_p": "Preventivo gratuito · Risposta entro 24h · Trasferta inclusa",
        "cta_btn": "💬 Preventivo WhatsApp",
        "contact_btn": "Modulo di contatto",
        "crumb_zones": "Zone",
    },
    "de": {
        "eyebrow_tpl": "Ka'ax Creación — {region}",
        "lead_tpl": "Ka'ax Creación fertigt und installiert Maßküchen, Ankleideräume und Möbel in {name}. Unsere Werkstatt befindet sich in Playa del Carmen — gleicher Qualitätsstandard, gleiches Handwerk der Compagnons du Tour de France.",
        "h2_why": "Warum Ka'ax Creación<br><em>in {name_short}?</em>",
        "features_tpl": [
            ("🏗️", "Lokale Fertigung", "Gefertigt in unserer Werkstatt in Playa del Carmen. Keine Zwischenhändler, kontrollierte Lieferzeiten, persönliche Betreuung."),
            ("🇫🇷", "Compagnons-Handwerk", "Jahrgangsbester 2023 der Compagnons du Tour de France — Frankreichs höchste Handwerksauszeichnung."),
            ("🚐", "Anfahrt inklusive", "Anfahrt und Einbau in {name_short} sind im Angebot enthalten. Keine versteckten Kosten."),
        ],
        "price_title": "Richtwert<br><em>in {name_short}</em>",
        "cta_h2": "Ihr Projekt<br><em>in {name_short}</em>",
        "cta_p": "Kostenloses Angebot · Antwort innerhalb von 24h · Anfahrt inklusive",
        "cta_btn": "💬 WhatsApp Angebot",
        "contact_btn": "Kontaktformular",
        "crumb_zones": "Gebiete",
    },
    "ru": {
        "eyebrow_tpl": "Ka'ax Creación — {region}",
        "lead_tpl": "Ka'ax Creación изготавливает и устанавливает кухни на заказ, гардеробные и мебель в {name}. Наша мастерская находится в Плая-дель-Кармен — те же стандарты качества, то же мастерство Compagnons du Tour de France.",
        "h2_why": "Почему Ka'ax Creación<br><em>в {name_short}?</em>",
        "features_tpl": [
            ("🏗️", "Местное производство", "Изготовлено в нашей мастерской в Плая-дель-Кармен. Без посредников, контролируемые сроки, личное сопровождение."),
            ("🇫🇷", "Мастерство Compagnons", "Лучший выпускник 2023 года Compagnons du Tour de France — высшая ремесленная награда Франции."),
            ("🚐", "Доставка включена", "Выезд и монтаж в {name_short} включены в смету. Никаких сюрпризов."),
        ],
        "price_title": "Ориентировочная стоимость<br><em>в {name_short}</em>",
        "cta_h2": "Ваш проект<br><em>в {name_short}</em>",
        "cta_p": "Бесплатный расчёт · Ответ в течение 24ч · Доставка включена",
        "cta_btn": "💬 Расчёт в WhatsApp",
        "contact_btn": "Форма связи",
        "crumb_zones": "Зоны",
    },
    "pt": {
        "eyebrow_tpl": "Ka'ax Creación — {region}",
        "lead_tpl": "Ka'ax Creación fabrica e instala cozinhas integradas, closets e móveis sob medida em {name}. A nossa oficina é em Playa del Carmen — mesmo padrão de qualidade, mesmo saber-fazer dos Compagnons du Tour de France.",
        "h2_why": "Porquê Ka'ax Creación<br><em>em {name_short}?</em>",
        "features_tpl": [
            ("🏗️", "Fabricação local", "Fabricado na nossa oficina em Playa del Carmen. Sem intermediários, prazos controlados, acompanhamento personalizado."),
            ("🇫🇷", "Mestria dos Compagnons", "Melhor Aluno de 2023 dos Compagnons du Tour de France — a mais alta distinção artesanal francesa."),
            ("🚐", "Deslocação incluída", "A deslocação e instalação em {name_short} estão incluídas no orçamento. Sem surpresas."),
        ],
        "price_title": "Custo indicativo<br><em>em {name_short}</em>",
        "cta_h2": "O seu projeto<br><em>em {name_short}</em>",
        "cta_p": "Orçamento grátis · Resposta em 24h · Deslocação incluída",
        "cta_btn": "💬 Orçamento WhatsApp",
        "contact_btn": "Formulário de contato",
        "crumb_zones": "Zonas",
    },
}

def content_zone(lang, slug, data, root_prefix):
    wa = wa_url_lang(lang)
    name = data["name"]
    name_short = data.get("name_short", name)
    region = data["region"]
    t = ZONE_INTRO_LANG[lang]

    eyebrow = t["eyebrow_tpl"].format(region=region)
    lead = t["lead_tpl"].format(name=name)
    h2_why = t["h2_why"].format(name_short=name_short)
    price_title = t["price_title"].format(name_short=name_short)
    cta_h2 = t["cta_h2"].format(name_short=name_short)
    crumb_zones = t["crumb_zones"]
    contact_href = f"{root_prefix}contacto/{lang}/"

    feats_html = "\n".join(
        f'<div class="feature-card"><div class="feature-icon">{ic}</div><h3>{ti}</h3><p>{de.format(name_short=name_short)}</p></div>'
        for ic, ti, de in t["features_tpl"]
    )

    specificites_html = "\n".join(
        f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>'
        for icon, title, desc in data["specificites"]
    )

    return f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{eyebrow}</p>
  <h1>{data["h1"]}</h1>
  <p class="lead">{data["lead"]}</p>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:48px">{data["intro"]}</p>
  <h2>{h2_why}</h2>
  <div class="content-grid-3" style="margin-top:40px">{feats_html}</div>
</div>
<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <div class="content-grid-3" style="margin-top:40px">{specificites_html}</div>
  </div>
</div>
<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>{price_title}</h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:720px;margin-bottom:48px">{data["price_text"]}</p>
  <p style="font-size:14px;line-height:1.9;opacity:.6;max-width:720px">{data.get("extra_text","")}</p>
</div>
<div class="cta-section">
  <div class="cta-section-content">
    <h2>{cta_h2}</h2>
    <p>{t["cta_p"]}</p>
    <div class="cta-buttons">
      <a href="{wa}" class="btn-wa" target="_blank" rel="noopener">{t["cta_btn"]}</a>
      <a href="{contact_href}" class="btn-secondary">{t["contact_btn"]}</a>
    </div>
  </div>
</div>"""

# ═══════════════════════════════════════════════════════════════
# TITRES PAR LANGUE PAR SERVICE (meta title + description)
# ═══════════════════════════════════════════════════════════════

SERVICE_META = {
    "cocinas-a-medida": {
        "fr": {
            "title": "Cuisines sur Mesure en Riviera Maya | Ka'ax Création",
            "desc": "Cuisines intégrales sur mesure fabriquées à Playa del Carmen. Savoir-faire des Compagnons du Tour de France. Devis gratuit · Déplacement inclus.",
            "h1_crumb": "Cuisines",
        },
        "en": {
            "title": "Custom Kitchens in the Riviera Maya | Ka'ax Creación",
            "desc": "Custom integrated kitchens built in Playa del Carmen. Compagnons du Tour de France craftsmanship. Free quote · Travel included.",
            "h1_crumb": "Kitchens",
        },
        "it": {
            "title": "Cucine su Misura nella Riviera Maya | Ka'ax Creación",
            "desc": "Cucine integrate su misura realizzate a Playa del Carmen. Know-how dei Compagnons du Tour de France. Preventivo gratuito · Trasferta inclusa.",
            "h1_crumb": "Cucine",
        },
        "de": {
            "title": "Maßküchen in der Riviera Maya | Ka'ax Creación",
            "desc": "Maßgefertigte Einbauküchen aus Playa del Carmen. Handwerk der Compagnons du Tour de France. Kostenloses Angebot · Anfahrt inklusive.",
            "h1_crumb": "Küchen",
        },
        "ru": {
            "title": "Кухни на заказ на Ривьере Майя | Ka'ax Creación",
            "desc": "Встроенные кухни на заказ, изготовленные в Плая-дель-Кармен. Мастерство Compagnons du Tour de France. Бесплатный расчёт · Доставка включена.",
            "h1_crumb": "Кухни",
        },
        "pt": {
            "title": "Cozinhas sob Medida na Riviera Maya | Ka'ax Creación",
            "desc": "Cozinhas integradas sob medida fabricadas em Playa del Carmen. Saber-fazer dos Compagnons du Tour de France. Orçamento grátis · Deslocação incluída.",
            "h1_crumb": "Cozinhas",
        },
    },
    "closets-y-vestidores": {
        "fr": {
            "title": "Dressings &amp; Armoires sur Mesure — Riviera Maya | Ka'ax Création",
            "desc": "Walk-in closets et dressings sur mesure en Riviera Maya. Fabriqués à Playa del Carmen par des artisans formés en France. Devis gratuit.",
            "h1_crumb": "Dressings",
        },
        "en": {
            "title": "Custom Custom Closets — Riviera Maya | Ka'ax Creación",
            "desc": "Walk-in closets and custom built-ins in the Riviera Maya. Built in Playa del Carmen by craftsmen trained in France. Free quote.",
            "h1_crumb": "Closets",
        },
        "it": {
            "title": "Cabine Armadio su Misura — Riviera Maya | Ka'ax Creación",
            "desc": "Walk-in closet e armadi su misura nella Riviera Maya. Realizzati a Playa del Carmen da artigiani formati in Francia. Preventivo gratuito.",
            "h1_crumb": "Cabine Armadio",
        },
        "de": {
            "title": "Ankleideräume &amp; Schränke nach Maß — Riviera Maya | Ka'ax Creación",
            "desc": "Maßgefertigte Walk-in Ankleideräume in der Riviera Maya. Gefertigt in Playa del Carmen von in Frankreich ausgebildeten Handwerkern. Kostenloses Angebot.",
            "h1_crumb": "Ankleideräume",
        },
        "ru": {
            "title": "Гардеробные и шкафы на заказ — Ривьера Майя | Ka'ax Creación",
            "desc": "Walk-in гардеробные на заказ на Ривьере Майя. Изготовлены в Плая-дель-Кармен мастерами, прошедшими обучение во Франции. Бесплатный расчёт.",
            "h1_crumb": "Гардеробные",
        },
        "pt": {
            "title": "Closets &amp; Armários sob Medida — Riviera Maya | Ka'ax Creación",
            "desc": "Walk-in closets e armários sob medida na Riviera Maya. Fabricados em Playa del Carmen por artesãos formados em França. Orçamento grátis.",
            "h1_crumb": "Closets",
        },
    },
    "realizaciones": {
        "fr": {
            "title": "Réalisations — Portfolio Cuisines et Dressings | Ka'ax Création",
            "desc": "Portfolio de cuisines intégrales, dressings et meubles sur mesure réalisés par Ka'ax Création en Riviera Maya. Villas de luxe, condominiums et résidences premium.",
            "h1_crumb": "Réalisations",
        },
        "en": {
            "title": "Portfolio — Custom Kitchens and Closets | Ka'ax Creación",
            "desc": "Portfolio of custom kitchens, closets and furniture made by Ka'ax Creación in the Riviera Maya. Luxury villas, condos and premium residences.",
            "h1_crumb": "Portfolio",
        },
        "it": {
            "title": "Realizzazioni — Portfolio Cucine e Cabine Armadio | Ka'ax Creación",
            "desc": "Portfolio di cucine integrate, cabine armadio e mobili su misura realizzati da Ka'ax Creación nella Riviera Maya. Ville di lusso e residenze premium.",
            "h1_crumb": "Realizzazioni",
        },
        "de": {
            "title": "Portfolio — Maßküchen und Ankleideräume | Ka'ax Creación",
            "desc": "Portfolio von Maßküchen, Ankleideräumen und Möbeln von Ka'ax Creación in der Riviera Maya. Luxusvillen, Apartments und Premium-Residenzen.",
            "h1_crumb": "Portfolio",
        },
        "ru": {
            "title": "Портфолио — Кухни и гардеробные на заказ | Ka'ax Creación",
            "desc": "Портфолио кухонь, гардеробных и мебели на заказ от Ka'ax Creación на Ривьере Майя. Роскошные виллы, апартаменты и премиум резиденции.",
            "h1_crumb": "Портфолио",
        },
        "pt": {
            "title": "Realizações — Portfolio Cozinhas e Closets | Ka'ax Creación",
            "desc": "Portfolio de cozinhas integradas, closets e móveis sob medida realizados pela Ka'ax Creación na Riviera Maya. Villas de luxo e residências premium.",
            "h1_crumb": "Realizações",
        },
    },
    "metodo": {
        "fr": {
            "title": "Notre Méthode Artisanale | Ka'ax Création — Riviera Maya",
            "desc": "La méthode Ka'ax Création : savoir-faire des Compagnons du Tour de France, matériaux européens sélectionnés, 4 étapes de la conception à la pose en Riviera Maya.",
            "h1_crumb": "Méthode",
        },
        "en": {
            "title": "Our Artisan Method | Ka'ax Creación — Riviera Maya",
            "desc": "The Ka'ax Creación method: Compagnons du Tour de France expertise, selected European materials, 4 steps from design to installation in the Riviera Maya.",
            "h1_crumb": "Method",
        },
        "it": {
            "title": "Il Nostro Metodo Artigianale | Ka'ax Creación — Riviera Maya",
            "desc": "Il metodo Ka'ax Creación: know-how dei Compagnons du Tour de France, materiali europei selezionati, 4 fasi dalla progettazione alla posa nella Riviera Maya.",
            "h1_crumb": "Metodo",
        },
        "de": {
            "title": "Unsere Handwerksmethode | Ka'ax Creación — Riviera Maya",
            "desc": "Die Ka'ax Creación Methode: Handwerk der Compagnons du Tour de France, ausgewählte europäische Materialien, 4 Schritte von der Planung bis zur Montage.",
            "h1_crumb": "Methode",
        },
        "ru": {
            "title": "Наш метод | Ka'ax Creación — Ривьера Майя",
            "desc": "Метод Ka'ax Creación: мастерство Compagnons du Tour de France, отборные европейские материалы, 4 этапа от проектирования до монтажа на Ривьере Майя.",
            "h1_crumb": "Метод",
        },
        "pt": {
            "title": "O Nosso Método Artesanal | Ka'ax Creación — Riviera Maya",
            "desc": "O método Ka'ax Creación: saber-fazer dos Compagnons du Tour de France, materiais europeus selecionados, 4 etapas da conceção à instalação na Riviera Maya.",
            "h1_crumb": "Método",
        },
    },
    "nosotros": {
        "fr": {
            "title": "Notre Histoire — Ka'ax Création | Menuiserie Riviera Maya",
            "desc": "Ka'ax Création : artisan menuisier formé par les Compagnons du Tour de France, installé à Playa del Carmen. L'excellence artisanale européenne au cœur de la Riviera Maya.",
            "h1_crumb": "À propos",
        },
        "en": {
            "title": "Our Story — Ka'ax Creación | Riviera Maya Carpentry",
            "desc": "Ka'ax Creación: master craftsman trained by the Compagnons du Tour de France, based in Playa del Carmen. European artisan excellence in the heart of the Riviera Maya.",
            "h1_crumb": "About",
        },
        "it": {
            "title": "La Nostra Storia — Ka'ax Creación | Falegnameria Riviera Maya",
            "desc": "Ka'ax Creación: falegname maestro formato dai Compagnons du Tour de France, con sede a Playa del Carmen. L'eccellenza artigianale europea nel cuore della Riviera Maya.",
            "h1_crumb": "Chi Siamo",
        },
        "de": {
            "title": "Unsere Geschichte — Ka'ax Creación | Schreinerei Riviera Maya",
            "desc": "Ka'ax Creación: Meisterschreiner ausgebildet von den Compagnons du Tour de France, in Playa del Carmen ansässig. Europäische Handwerksexzellenz im Herzen der Riviera Maya.",
            "h1_crumb": "Über uns",
        },
        "ru": {
            "title": "Наша история — Ka'ax Creación | Столярная мастерская Ривьера Майя",
            "desc": "Ka'ax Creación: мастер-столяр, обученный Compagnons du Tour de France, обосновавшийся в Плая-дель-Кармен. Европейское ремесленное совершенство в сердце Ривьеры Майя.",
            "h1_crumb": "О нас",
        },
        "pt": {
            "title": "A Nossa História — Ka'ax Creación | Marcenaria Riviera Maya",
            "desc": "Ka'ax Creación: mestre marceneiro formado pelos Compagnons du Tour de France, sediado em Playa del Carmen. Excelência artesanal europeia no coração da Riviera Maya.",
            "h1_crumb": "Sobre nós",
        },
    },
    "contacto": {
        "fr": {
            "title": "Devis Gratuit — Contact | Ka'ax Création Riviera Maya",
            "desc": "Demandez votre devis gratuit pour cuisines ou dressings sur mesure en Riviera Maya. Réponse sous 24h · Visite technique offerte · Déplacement inclus.",
            "h1_crumb": "Contact",
        },
        "en": {
            "title": "Free Quote — Contact | Ka'ax Creación Riviera Maya",
            "desc": "Request your free quote for custom kitchens or closets in the Riviera Maya. Response within 24h · Technical visit included · Travel included.",
            "h1_crumb": "Contact",
        },
        "it": {
            "title": "Preventivo Gratuito — Contatto | Ka'ax Creación Riviera Maya",
            "desc": "Richiedete il vostro preventivo gratuito per cucine o cabine armadio su misura nella Riviera Maya. Risposta entro 24h · Visita tecnica inclusa · Trasferta inclusa.",
            "h1_crumb": "Contatto",
        },
        "de": {
            "title": "Kostenloses Angebot — Kontakt | Ka'ax Creación Riviera Maya",
            "desc": "Fordern Sie Ihr kostenloses Angebot für Maßküchen oder Ankleideräume in der Riviera Maya an. Antwort innerhalb von 24h · Technischer Besuch inklusive · Anfahrt inklusive.",
            "h1_crumb": "Kontakt",
        },
        "ru": {
            "title": "Бесплатный расчёт — Контакт | Ka'ax Creación Ривьера Майя",
            "desc": "Запросите бесплатный расчёт для кухни или гардеробной на Ривьере Майя. Ответ в течение 24ч · Технический выезд включён · Доставка включена.",
            "h1_crumb": "Контакт",
        },
        "pt": {
            "title": "Orçamento Grátis — Contato | Ka'ax Creación Riviera Maya",
            "desc": "Solicite o seu orçamento grátis para cozinhas ou closets sob medida na Riviera Maya. Resposta em 24h · Visita técnica incluída · Deslocação incluída.",
            "h1_crumb": "Contato",
        },
    },
    "zona": {
        "fr": {
            "title": "Zones d'Intervention — Riviera Maya et Yucatán | Ka'ax Création",
            "desc": "Ka'ax Création couvre la Riviera Maya : Cancún, Playa del Carmen, Tulum, Puerto Morelos, Isla Mujeres, Cozumel, et projets sélectifs à Mérida, Holbox et Campeche.",
            "h1_crumb": "Zones",
        },
        "en": {
            "title": "Service Areas — Riviera Maya and Yucatán | Ka'ax Creación",
            "desc": "Ka'ax Creación covers the Riviera Maya: Cancún, Playa del Carmen, Tulum, Puerto Morelos, Isla Mujeres, Cozumel, and selective projects in Mérida, Holbox and Campeche.",
            "h1_crumb": "Areas",
        },
        "it": {
            "title": "Zone di Intervento — Riviera Maya e Yucatán | Ka'ax Creación",
            "desc": "Ka'ax Creación copre la Riviera Maya: Cancún, Playa del Carmen, Tulum, Puerto Morelos, Isla Mujeres, Cozumel, e progetti selettivi a Mérida, Holbox e Campeche.",
            "h1_crumb": "Zone",
        },
        "de": {
            "title": "Servicegebiete — Riviera Maya und Yucatán | Ka'ax Creación",
            "desc": "Ka'ax Creación deckt die Riviera Maya ab: Cancún, Playa del Carmen, Tulum, Puerto Morelos, Isla Mujeres, Cozumel, und selektive Projekte in Mérida, Holbox und Campeche.",
            "h1_crumb": "Gebiete",
        },
        "ru": {
            "title": "Зоны обслуживания — Ривьера Майя и Юкатан | Ka'ax Creación",
            "desc": "Ka'ax Creación охватывает Ривьеру Майя: Канкун, Плая-дель-Кармен, Тулум, Пуэрто-Морелос, Исла-Мухерес, Косумель, и избранные проекты в Мериде, Хольбоке и Кампече.",
            "h1_crumb": "Зоны",
        },
        "pt": {
            "title": "Zonas de Intervenção — Riviera Maya e Yucatán | Ka'ax Creación",
            "desc": "Ka'ax Creación cobre a Riviera Maya: Cancún, Playa del Carmen, Tulum, Puerto Morelos, Isla Mujeres, Cozumel, e projetos seletivos em Mérida, Holbox e Campeche.",
            "h1_crumb": "Zonas",
        },
    },
}

# ═══════════════════════════════════════════════════════════════
# CONTENT FUNCTIONS MAP
# ═══════════════════════════════════════════════════════════════

CONTENT_FUNCS = {
    "cocinas-a-medida": content_cocinas,
    "closets-y-vestidores": content_closets,
    "realizaciones": content_realizaciones,
    "metodo": content_metodo,
    "nosotros": content_nosotros,
    "contacto": content_contacto,
    "zona": content_zona_index,
}

# ═══════════════════════════════════════════════════════════════
# GENERATION PRINCIPALE
# ═══════════════════════════════════════════════════════════════

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_service_page(base, service_slug, lang):
    """Génère /service_slug/lang/index.html"""
    root_prefix = "../../"
    image_prefix = "../../"
    es_url = f"{DOMAIN}/{service_slug}/"
    page_base_path = "../"  # pour construire ../fr/, ../en/ etc.
    canonical = f"{DOMAIN}/{service_slug}/{lang}/"
    active_page = f"{service_slug}/"

    meta = SERVICE_META[service_slug][lang]
    title = meta["title"]
    description = meta["desc"]
    h1_crumb = meta["h1_crumb"]

    # Breadcrumb
    crumb_lbl = NAV_LABELS[lang].get(service_slug.split("-")[0], h1_crumb)
    crumb = breadcrumb_lang(lang, [(h1_crumb, "")], root_prefix)

    # Content
    content_fn = CONTENT_FUNCS[service_slug]
    content = content_fn(lang, root_prefix)

    # Hreflang
    hreflang = hreflang_service(service_slug)

    html = build_page_lang(
        lang=lang,
        title=title,
        description=description,
        canonical=canonical,
        breadcrumbs_html=crumb,
        content=content,
        root_prefix=root_prefix,
        active_page=active_page,
        es_url=es_url,
        page_base_path=page_base_path,
        image_prefix=image_prefix,
        hreflang_links=hreflang,
    )
    path = f"{base}/{service_slug}/{lang}"
    ensure_dir(path)
    with open(f"{path}/index.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_zone_page(base, zone_slug, data, lang):
    """Génère /zona/zone_slug/lang/index.html"""
    root_prefix = "../../../"
    image_prefix = "../../../"
    es_url = f"{DOMAIN}/zona/{zone_slug}/"
    page_base_path = "../"
    canonical = f"{DOMAIN}/zona/{zone_slug}/{lang}/"
    active_page = "zona/"

    name = data["name"]
    region = data["region"]
    t_zone = ZONE_INTRO_LANG[lang]

    # Title & desc
    zone_title_map = {
        "fr": f"Cuisines &amp; Dressings sur Mesure à {name} | Ka'ax Création",
        "en": f"Custom Kitchens &amp; Closets in {name} | Ka'ax Creación",
        "it": f"Cucine &amp; Cabine Armadio su Misura a {name} | Ka'ax Creación",
        "de": f"Maßküchen &amp; Ankleideräume in {name} | Ka'ax Creación",
        "ru": f"Кухни и гардеробные на заказ в {name} | Ka'ax Creación",
        "pt": f"Cozinhas &amp; Closets sob Medida em {name} | Ka'ax Creación",
    }
    zone_desc_map = {
        "fr": f"Menuiserie de luxe sur mesure à {name}. Cuisines intégrales et dressings fabriqués à Playa del Carmen par des artisans formés en France. Devis gratuit.",
        "en": f"Luxury custom carpentry in {name}. Integrated kitchens and closets built in Playa del Carmen by craftsmen trained in France. Free quote.",
        "it": f"Falegnameria di lusso su misura a {name}. Cucine integrate e cabine armadio realizzate a Playa del Carmen da artigiani formati in Francia. Preventivo gratuito.",
        "de": f"Luxuriöse Maßschreinerei in {name}. Einbauküchen und Ankleideräume aus Playa del Carmen von in Frankreich ausgebildeten Handwerkern. Kostenloses Angebot.",
        "ru": f"Роскошная мебель на заказ в {name}. Встроенные кухни и гардеробные, изготовленные в Плая-дель-Кармен мастерами, прошедшими обучение во Франции. Бесплатный расчёт.",
        "pt": f"Marcenaria de luxo sob medida em {name}. Cozinhas integradas e closets fabricados em Playa del Carmen por artesãos formados em França. Orçamento grátis.",
    }

    title = zone_title_map[lang]
    description = zone_desc_map[lang]

    crumb_zones = t_zone["crumb_zones"]
    crumb = breadcrumb_lang(
        lang,
        [(crumb_zones, f"{root_prefix}zona/{lang}/"), (name, "")],
        root_prefix
    )

    content = content_zone(lang, zone_slug, data, root_prefix)
    hreflang = hreflang_zone(zone_slug)

    html = build_page_lang(
        lang=lang,
        title=title,
        description=description,
        canonical=canonical,
        breadcrumbs_html=crumb,
        content=content,
        root_prefix=root_prefix,
        active_page=active_page,
        es_url=es_url,
        page_base_path=page_base_path,
        image_prefix=image_prefix,
        hreflang_links=hreflang,
    )
    path = f"{base}/zona/{zone_slug}/{lang}"
    ensure_dir(path)
    with open(f"{path}/index.html", "w", encoding="utf-8") as f:
        f.write(html)

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    base = "/home/claude/kaax-creation"
    total = 0
    errors = 0

    print("⚡ Génération des pages multilingues Ka'ax Creación")
    print(f"   Langues: {', '.join(LANGS)}")
    print(f"   Service pages: {len(CONTENT_FUNCS)} × {len(LANGS)} = {len(CONTENT_FUNCS) * len(LANGS)}")
    print(f"   Zone pages: {len(ZONE_DATA)} × {len(LANGS)} = {len(ZONE_DATA) * len(LANGS)}")
    print(f"   Total attendu: {(len(CONTENT_FUNCS) + len(ZONE_DATA)) * len(LANGS)} pages\n")

    # Service pages
    for service_slug in CONTENT_FUNCS.keys():
        for lang in LANGS:
            try:
                generate_service_page(base, service_slug, lang)
                print(f"  ✅ /{service_slug}/{lang}/index.html")
                total += 1
            except Exception as e:
                print(f"  ❌ /{service_slug}/{lang}/ — {e}")
                errors += 1

    # Zone pages
    for zone_slug, data in ZONE_DATA.items():
        for lang in LANGS:
            try:
                generate_zone_page(base, zone_slug, data, lang)
                print(f"  ✅ /zona/{zone_slug}/{lang}/index.html")
                total += 1
            except Exception as e:
                print(f"  ❌ /zona/{zone_slug}/{lang}/ — {e}")
                errors += 1

    print(f"\n{'='*60}")
    print(f"✅ {total} pages générées, {errors} erreurs")
    if errors == 0:
        print("   Toutes les pages ont été générées avec succès !")

if __name__ == "__main__":
    main()

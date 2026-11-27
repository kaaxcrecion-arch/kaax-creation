#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ka'ax Creación — Générateur de pages SEO multi-pages (Espagnol)
Génère : 7 pages service + 15 pages zone + sitemap.xml
"""

import os

# ═══ CONFIG ═══
DOMAIN = "https://kaaxcreacion.com"
WA = "529843121942"
WA_MSG = "Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20gratuito."
WA_URL = f"https://wa.me/{WA}?text={WA_MSG}"

# ═══ CSS COMMUN (extrait de index.html) ═══
COMMON_CSS = """
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Inter:wght@300;400;500&display=swap');
  :root{--noir:#0D0D0D;--or:#C9A84C;--or-clair:#E8C97A;--creme:#FAF7F0;--vert:#2D4A3E;--gris:#8C8070;--gris-clair:#1A1A1A}
  *{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
  body{background:var(--noir);color:var(--creme);font-family:'Inter',sans-serif;overflow-x:hidden}
  :focus-visible{outline:2px solid var(--or);outline-offset:3px}

  /* ═══ TICKER ═══ */
  .ticker-wrap{background:var(--or);padding:12px 0;overflow:hidden;width:100%;position:relative;z-index:10}
  .ticker-track{display:flex;white-space:nowrap;animation:ticker-scroll 28s linear infinite}
  .ticker-track:hover{animation-play-state:paused}
  .ticker-item{display:inline-flex;align-items:center;gap:10px;padding:0 40px;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--noir);font-weight:500;flex-shrink:0}
  .ticker-dot{width:4px;height:4px;background:var(--noir);border-radius:50%;opacity:.35}
  @keyframes ticker-scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

  /* ═══ NAV ═══ */
  #navbar{position:fixed;top:0;width:100%;z-index:100;padding:20px 60px;display:flex;justify-content:space-between;align-items:center;background:linear-gradient(to bottom,rgba(13,13,13,.95),transparent);transition:all .3s}
  #navbar.scrolled{background:rgba(13,13,13,.97);backdrop-filter:blur(10px)}
  .nav-inner{display:flex;justify-content:space-between;align-items:center;width:100%}
  .nav-logo{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:300;letter-spacing:4px;color:var(--creme);text-decoration:none}
  .nav-logo span{color:var(--or)}
  .nav-logo sub{display:block;font-size:9px;letter-spacing:2.5px;opacity:.45;font-family:'Inter',sans-serif;text-transform:uppercase;margin-top:2px}
  .nav-links{display:flex;gap:36px;list-style:none}
  .nav-links a{color:var(--creme);text-decoration:none;font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.75;transition:opacity .3s}
  .nav-links a:hover,.nav-links a.active{opacity:1;color:var(--or)}
  .nav-cta{background:transparent;border:1px solid var(--or);color:var(--or);padding:10px 24px;font-size:11px;letter-spacing:2px;text-transform:uppercase;cursor:pointer;transition:all .3s;font-family:'Inter',sans-serif;text-decoration:none;display:inline-block}
  .nav-cta:hover{background:var(--or);color:var(--noir)}

  /* ═══ HAMBURGER MOBILE ═══ */
  .nav-hamburger{display:none;flex-direction:column;justify-content:center;gap:5px;width:38px;height:38px;background:none;border:1px solid rgba(201,168,76,.3);cursor:pointer;padding:8px;flex-shrink:0}
  .nav-hamburger span{display:block;width:100%;height:1px;background:var(--creme);transition:all .3s}
  .nav-hamburger.open span:nth-child(1){transform:translateY(6px) rotate(45deg)}
  .nav-hamburger.open span:nth-child(2){opacity:0}
  .nav-hamburger.open span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
  .nav-mobile-menu{display:none;position:fixed;top:60px;left:0;right:0;background:rgba(13,13,13,.98);backdrop-filter:blur(12px);border-bottom:1px solid rgba(201,168,76,.2);padding:20px 24px;z-index:99;flex-direction:column;gap:4px}
  .nav-mobile-menu.open{display:flex}
  .nav-mobile-menu a{color:var(--creme);text-decoration:none;font-size:13px;letter-spacing:2px;text-transform:uppercase;opacity:.75;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.05);display:block}
  .nav-mobile-menu a:last-child{border-bottom:none}
  .nav-mobile-menu a:hover{opacity:1;color:var(--or)}
  .nav-mobile-cta{margin-top:12px;padding:12px 24px;border:1px solid var(--or);color:var(--or);text-align:center;font-size:11px;letter-spacing:2px;text-transform:uppercase;text-decoration:none;display:block}

  /* ═══ LANG SELECT ═══ */
  .lang-select-wrap{position:relative}
  .lang-select-btn{display:flex;align-items:center;gap:8px;background:rgba(250,247,240,.06);border:1px solid rgba(201,168,76,.3);padding:8px 14px;cursor:pointer;font-family:'Inter',sans-serif;font-size:12px;letter-spacing:1px;color:var(--creme);transition:all .3s;min-width:90px;justify-content:space-between}
  .lang-select-btn:hover{border-color:var(--or);background:rgba(201,168,76,.08)}
  .lang-select-btn .flag{font-size:16px}
  .lang-select-btn .lang-code{text-transform:uppercase;letter-spacing:2px;font-size:11px;opacity:.85}
  .lang-select-btn .chevron{font-size:9px;opacity:.5;transition:transform .2s;margin-left:4px}
  .lang-select-btn.open .chevron{transform:rotate(180deg)}
  .lang-dropdown{position:absolute;top:calc(100% + 6px);right:0;background:#111;border:1px solid rgba(201,168,76,.25);min-width:180px;display:none;z-index:200;box-shadow:0 8px 32px rgba(0,0,0,.5)}
  .lang-dropdown.open{display:block}
  .lang-dropdown-item{display:flex;align-items:center;gap:10px;padding:11px 16px;font-size:12px;letter-spacing:1px;color:var(--creme);cursor:pointer;transition:background .2s;text-decoration:none}
  .lang-dropdown-item.active-lang{color:var(--or)!important;font-weight:600}
  .lang-dropdown-item:hover{background:rgba(201,168,76,.1);color:var(--or)!important}
  .lang-dropdown-item .flag{font-size:16px}
  .lang-dropdown-item .name{opacity:.8}
  .lang-dropdown-divider{height:1px;background:rgba(201,168,76,.1);margin:4px 0}

  /* ═══ BREADCRUMB ═══ */
  .breadcrumb{position:static!important;z-index:auto!important;width:auto!important;background:none!important;padding:100px 60px 0;font-size:12px;letter-spacing:1px;opacity:.5}
  .breadcrumb a{color:var(--creme);text-decoration:none}
  .breadcrumb a:hover{color:var(--or)}
  .breadcrumb span{margin:0 8px;opacity:.4}

  /* ═══ PAGE HERO ═══ */
  .page-hero{padding:140px 60px 80px;max-width:1300px;margin:0 auto}
  .page-eyebrow{font-size:11px;letter-spacing:5px;text-transform:uppercase;color:var(--or);margin-bottom:20px}
  .page-hero h1{font-family:'Cormorant Garamond',serif;font-size:clamp(42px,6vw,80px);font-weight:300;line-height:1.1;margin-bottom:28px;letter-spacing:1px}
  .page-hero h1 em{font-style:italic;color:var(--or-clair)}
  .page-hero .lead{font-size:17px;font-weight:300;opacity:.7;max-width:620px;line-height:1.9;margin-bottom:36px}
  .page-hero-bg{position:fixed;inset:0;background:linear-gradient(135deg,rgba(13,13,13,.92) 0%,rgba(45,74,62,.2) 50%,rgba(13,13,13,.95) 100%),url('../../images/hero-bg.jpg') center/cover;z-index:-1}

  /* ═══ CONTENT SECTIONS ═══ */
  .content-section{padding:80px 60px;max-width:1300px;margin:0 auto}
  .content-section h2{font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px;line-height:1.3}
  .content-section h2 em{font-style:italic;color:var(--or-clair)}
  .content-section h3{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:300;margin:28px 0 14px;color:var(--or-clair)}
  .content-section p{font-size:15px;line-height:1.9;opacity:.75;margin-bottom:18px}
  .content-section ul,.content-section ol{padding-left:24px;margin-bottom:18px}
  .content-section li{font-size:15px;line-height:1.9;opacity:.75;margin-bottom:8px}
  .content-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start}
  .content-grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
  .gold-divider{width:60px;height:1px;background:var(--or);margin:0 0 40px}

  /* ═══ FEATURE CARDS ═══ */
  .feature-card{padding:32px;border:1px solid rgba(201,168,76,.2);background:rgba(201,168,76,.03);transition:border-color .3s}
  .feature-card:hover{border-color:rgba(201,168,76,.5)}
  .feature-card h3{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:300;color:var(--or-clair);margin-bottom:12px}
  .feature-card p{font-size:13px;opacity:.65;line-height:1.7;margin:0}
  .feature-icon{font-size:28px;margin-bottom:16px}

  /* ═══ ZONE CARDS ═══ */
  .zone-card{display:flex;align-items:center;gap:16px;padding:20px 24px;border:1px solid rgba(201,168,76,.2);text-decoration:none;color:var(--creme);transition:all .3s;background:rgba(201,168,76,.03)}
  .zone-card:hover{border-color:var(--or);background:rgba(201,168,76,.08);transform:translateX(4px)}
  .zone-card-icon{font-size:24px;flex-shrink:0}
  .zone-card-name{font-family:'Cormorant Garamond',serif;font-size:18px;font-weight:300}
  .zone-card-sub{font-size:11px;opacity:.5;letter-spacing:1px;text-transform:uppercase;margin-top:2px}
  .zone-card-arrow{margin-left:auto;color:var(--or);opacity:.6}
  .zones-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:40px}

  /* ═══ CTA SECTION ═══ */
  .cta-section{padding:80px 60px;background:var(--vert);text-align:center;position:relative;overflow:hidden}
  .cta-section::before{content:'';position:absolute;inset:0;background:url('../../images/hero-bg.jpg') center/cover;opacity:.06}
  .cta-section-content{position:relative}
  .cta-section h2{font-family:'Cormorant Garamond',serif;font-size:clamp(32px,4vw,52px);font-weight:300;line-height:1.2;margin-bottom:20px}
  .cta-section h2 em{font-style:italic;color:var(--or-clair)}
  .cta-section p{font-size:15px;opacity:.75;max-width:500px;margin:0 auto 36px;line-height:1.8}
  .btn-wa{display:inline-flex;align-items:center;gap:10px;background:#25D366;color:white;padding:16px 36px;font-size:12px;letter-spacing:2px;text-transform:uppercase;font-family:'Inter',sans-serif;font-weight:500;transition:all .3s;text-decoration:none}
  .btn-wa:hover{background:#1db954;transform:translateY(-2px)}
  .btn-primary{display:inline-block;background:var(--or);color:var(--noir);padding:16px 36px;font-size:12px;letter-spacing:2px;text-transform:uppercase;font-family:'Inter',sans-serif;font-weight:500;transition:all .3s;text-decoration:none}
  .btn-primary:hover{background:var(--or-clair);transform:translateY(-2px)}
  .btn-secondary{display:inline-block;background:transparent;color:var(--creme);padding:16px 36px;font-size:12px;letter-spacing:2px;text-transform:uppercase;border:1px solid rgba(250,247,240,.4);font-family:'Inter',sans-serif;transition:all .3s;text-decoration:none}
  .btn-secondary:hover{border-color:var(--or);color:var(--or);transform:translateY(-2px)}
  .cta-buttons{display:flex;gap:16px;justify-content:center;flex-wrap:wrap}

  /* ═══ STATS BAR ═══ */
  .stats-bar{background:var(--gris-clair);padding:50px 60px;display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid rgba(201,168,76,.2)}
  .stat{text-align:center;padding:20px;border-right:1px solid rgba(201,168,76,.15)}
  .stat:last-child{border-right:none}
  .stat-num{font-family:'Cormorant Garamond',serif;font-size:44px;font-weight:300;color:var(--or);line-height:1;margin-bottom:8px}
  .stat-label{font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6}

  /* ═══ PROCESS STEPS ═══ */
  .process-step{display:flex;gap:32px;align-items:flex-start;padding:32px 0;border-bottom:1px solid rgba(201,168,76,.1)}
  .process-step:last-child{border-bottom:none}
  .step-num{font-family:'Cormorant Garamond',serif;font-size:60px;font-weight:300;color:rgba(201,168,76,.55);line-height:1;flex-shrink:0;width:80px}
  .step-content h3{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:300;color:var(--or-clair);margin-bottom:10px}
  .step-content p{font-size:14px;opacity:.65;line-height:1.8}

  /* ═══ FOOTER ═══ */
  footer{padding:60px;background:#080808;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:60px;border-top:1px solid rgba(201,168,76,.15)}
  .footer-logo{font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:300;letter-spacing:4px;color:var(--creme);margin-bottom:8px}
  .footer-logo span{color:var(--or)}
  .footer-maya{font-size:11px;opacity:.35;letter-spacing:2px;margin-bottom:16px}
  .footer-desc{font-size:13px;opacity:.5;line-height:1.8;max-width:280px}
  .footer-col h4{font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--or);margin-bottom:20px}
  .footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
  .footer-col li a,.footer-col li{font-size:13px;opacity:.5;cursor:pointer;transition:opacity .3s;color:var(--creme);text-decoration:none}
  .footer-col li:hover,.footer-col li a:hover{opacity:1}
  .footer-bottom{padding:24px 60px;background:#080808;border-top:1px solid rgba(255,255,255,.05);display:flex;justify-content:space-between;align-items:center;font-size:12px;opacity:.35}

  /* ═══ ANIMATIONS ═══ */
  @keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
  .reveal{opacity:0;transform:translateY(40px);transition:all .8s ease}
  .reveal.visible{opacity:1;transform:translateY(0)}

  /* ═══ MOBILE ═══ */
  .contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start;max-width:1100px;margin:0 auto}
  .contact-grid input::placeholder,.contact-grid textarea::placeholder,.contact-grid select{color:rgba(250,247,240,.6)}
  .contact-grid input,.contact-grid textarea{background:rgba(255,255,255,.08)!important;color:rgba(250,247,240,.9)}
  @media(max-width:1024px){#navbar{padding:16px 30px}.nav-links{gap:20px}footer{grid-template-columns:1fr 1fr;gap:40px;padding:40px 30px}.footer-bottom{padding:20px 30px}.content-grid{grid-template-columns:1fr}.stats-bar{padding:40px 30px}}
  @media(max-width:768px){
    html,body{overflow-x:hidden;max-width:100vw}*{box-sizing:border-box}
    #navbar{padding:10px 14px;gap:6px;width:100%;max-width:100vw}
    .nav-logo{font-size:16px;letter-spacing:2px;white-space:nowrap}
    .nav-logo sub{display:none}.nav-links{display:none}.nav-cta{display:none}.nav-hamburger{display:flex}
    .lang-select-btn{padding:6px 8px;min-width:auto}.lang-select-btn .lang-code{display:none}
    .breadcrumb{padding:80px 20px 0}
    .page-hero{padding:120px 20px 60px}.content-section{padding:50px 20px}
    .content-grid-3{grid-template-columns:1fr}.zones-grid{grid-template-columns:1fr}
    .stats-bar{grid-template-columns:repeat(2,1fr);padding:30px 20px}
    .stat:nth-child(2){border-right:none}.stat:nth-child(3){border-right:1px solid rgba(201,168,76,.15)}.stat:nth-child(4){border-right:none}
    footer{grid-template-columns:1fr;gap:32px;padding:40px 20px}
    .footer-bottom{padding:16px 20px;flex-direction:column;gap:6px;text-align:center}
    .cta-section{padding:60px 20px}.cta-buttons{flex-direction:column;align-items:center}
    .contact-grid{grid-template-columns:1fr;gap:48px}
    .name-grid{grid-template-columns:1fr!important}
    .process-step{flex-direction:column;gap:8px;padding:24px 0}
    .step-num{font-size:36px;width:auto;line-height:1;margin-bottom:4px}
    .step-content h3{font-size:18px}
  }
  @media(max-width:768px){.ticker-track{animation-duration:14s}}
"""

# ═══ FLAGS CSS (repris de index.html) ═══
FLAG_MX = '<span style="display:inline-flex;align-items:center;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:inline-block;width:7px;height:14px;background:#006847"></span><span style="display:inline-block;width:7px;height:14px;background:#fff"></span><span style="display:inline-block;width:7px;height:14px;background:#CE1126"></span></span>'
FLAG_US = '<span style="display:inline-flex;align-items:center;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:inline-block;width:6px;height:14px;background:#3C3B6E;flex-shrink:0"></span><span style="display:inline-flex;flex-direction:column;width:15px;height:14px;flex-shrink:0"><span style="display:block;height:3.5px;background:#B22234"></span><span style="display:block;height:3.5px;background:#fff"></span><span style="display:block;height:3.5px;background:#B22234"></span><span style="display:block;height:3.5px;background:#fff"></span></span></span>'
FLAG_FR = '<span style="display:inline-flex;align-items:center;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:inline-block;width:7px;height:14px;background:#002395"></span><span style="display:inline-block;width:7px;height:14px;background:#fff"></span><span style="display:inline-block;width:7px;height:14px;background:#ED2939"></span></span>'
FLAG_IT = '<span style="display:inline-flex;align-items:center;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:inline-block;width:7px;height:14px;background:#009246"></span><span style="display:inline-block;width:7px;height:14px;background:#fff"></span><span style="display:inline-block;width:7px;height:14px;background:#CE2B37"></span></span>'
FLAG_DE = '<span style="display:inline-flex;flex-direction:column;width:21px;height:14px;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:block;width:21px;height:4px;background:#000"></span><span style="display:block;width:21px;height:4px;background:#D00"></span><span style="display:block;width:21px;height:4px;background:#FFCE00"></span></span>'
FLAG_RU = '<span style="display:inline-flex;flex-direction:column;width:21px;height:14px;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:block;width:21px;height:4px;background:#fff"></span><span style="display:block;width:21px;height:4px;background:#1C3578"></span><span style="display:block;width:21px;height:4px;background:#E4181C"></span></span>'
FLAG_PT = '<span style="display:inline-flex;align-items:center;border:1px solid rgba(255,255,255,.15);border-radius:1px;overflow:hidden;flex-shrink:0"><span style="display:inline-block;width:7px;height:14px;background:#006600"></span><span style="display:inline-block;width:7px;height:14px;background:#FF0000"></span><span style="display:inline-block;width:7px;height:14px;background:#FFD700"></span></span>'


def lang_dropdown(base_path, es_href):
    """Génère le sélecteur de langue avec les liens corrects."""
    return f"""
    <div class="lang-select-wrap">
      <button class="lang-select-btn" id="langBtn" aria-label="Seleccionar idioma" aria-expanded="false">
        {FLAG_MX}
        <span class="lang-code">ES</span>
        <span class="chevron">▼</span>
      </button>
      <div class="lang-dropdown" id="langDropdown">
        <a href="{es_href}" class="lang-dropdown-item active-lang">{FLAG_MX}<span class="name">Español</span></a>
        <div class="lang-dropdown-divider"></div>
        <a href="{base_path}en/" class="lang-dropdown-item">{FLAG_US}<span class="name">English</span></a>
        <a href="{base_path}fr/" class="lang-dropdown-item">{FLAG_FR}<span class="name">Français</span></a>
        <a href="{base_path}it/" class="lang-dropdown-item">{FLAG_IT}<span class="name">Italiano</span></a>
        <a href="{base_path}de/" class="lang-dropdown-item">{FLAG_DE}<span class="name">Deutsch</span></a>
        <a href="{base_path}ru/" class="lang-dropdown-item">{FLAG_RU}<span class="name">Русский</span></a>
        <a href="{base_path}pt/" class="lang-dropdown-item">{FLAG_PT}<span class="name">Português</span></a>
      </div>
    </div>"""


def nav_html(root_prefix, active_page=""):
    """Génère la navigation avec des URLs absolues (toujours navigables quelle que soit la profondeur)."""
    links = [
        ("/cocinas-a-medida/", "Cocinas"),
        ("/closets-y-vestidores/", "Vestidores"),
        ("/realizaciones/", "Realizaciones"),
        ("/zona/", "Zonas"),
        ("/nosotros/", "Nuestro ADN"),
        ("/blog/", "Blog"),
    ]
    nav_items = ""
    mobile_items = ""
    for href, label in links:
        slug = href.strip("/")
        is_active = slug == active_page.rstrip("/")
        cls = ' class="active"' if is_active else ""
        nav_items += f'<li><a href="{href}"{cls}>{label}</a></li>\n    '
        mobile_items += f'<a href="{href}"{cls}>{label}</a>\n  '

    base_for_lang = root_prefix
    es_href = f"{root_prefix}."

    return f"""<nav id="navbar">
  <a href="{root_prefix}" class="nav-logo" aria-label="Ka'ax Creación — página de inicio">KA'AX <span>CREACIÓN</span><sub>Cocinas &amp; Closets · Riviera Maya</sub></a>
  <ul class="nav-links" role="list">
    {nav_items}
  </ul>
  <div style="display:flex;align-items:center;gap:10px">
    <button class="nav-hamburger" id="navHamburger" aria-label="Menú" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
    {lang_dropdown(root_prefix, es_href)}
    <a href="{WA_URL}" target="_blank" rel="noopener" class="nav-cta">Presupuesto gratuito</a>
  </div>
</nav>
<div class="nav-mobile-menu" id="navMobileMenu" role="navigation" aria-label="Menú móvil">
  {mobile_items}
  <a href="{WA_URL}" class="nav-mobile-cta" target="_blank" rel="noopener">💬 Presupuesto gratuito</a>
</div>"""


def ticker_html():
    items = [
        ("🪵", "Cocinas a medida"),
        ("🪞", "Vestidores de lujo"),
        ("🔐", "Compartimentos ocultos"),
        ("🪵", "Muebles a medida"),
        ("✨", "Acabados europeos"),
        ("🪞", "Armarios empotrados"),
        ("🪵", "Madera maciza europea"),
        ("🔐", "Espacios de discreción"),
        ("🪵", "Cocinas de alta gama"),
        ("🪞", "Dressing room personalizado"),
        ("🪵", "Isla de cocina a medida"),
        ("🔐", "Cajones secretos integrados"),
    ]
    all_items = items * 2  # duplicate for seamless loop
    ticker_items = "".join(
        f'<span class="ticker-item">{icon} {text}<span class="ticker-dot"></span></span>'
        for icon, text in all_items
    )
    return f"""<div class="ticker-wrap" aria-hidden="true">
  <div class="ticker-track">{ticker_items}</div>
</div>"""


def footer_html(root_prefix):
    return f"""<footer>
  <div>
    <div class="footer-logo">KA'AX <span>CREACIÓN</span></div>
    <div class="footer-maya">Ka'ax — «bosque · madera» en maya</div>
    <p class="footer-desc">Carpintería europea de lujo a medida, fabricada en Playa del Carmen. Formado por los Compagnons du Tour de France — Major de promoción 2023.</p>
  </div>
  <div class="footer-col"><h4>Servicios</h4><ul>
    <li><a href="/cocinas-a-medida/">Cocinas a medida</a></li>
    <li><a href="/closets-y-vestidores/">Vestidores &amp; Armarios</a></li>
    <li><a href="/realizaciones/">Realizaciones</a></li>
    <li><a href="/nosotros/">Nuestro ADN</a></li>
  </ul></div>
  <div class="footer-col"><h4>Blog</h4><ul>
    <li><a href="/blog/cocinas-integrales-playa-del-carmen.html">Cocinas Integrales PDC</a></li>
    <li><a href="/blog/vestidores-a-medida-playa-del-carmen.html">Vestidores a Medida</a></li>
    <li><a href="/blog/maderas-clima-tropical-riviera-maya.html">Maderas Tropicales</a></li>
    <li><a href="/blog/tendencias-2026-cocinas-lujo-riviera-maya.html">Tendencias 2026</a></li>
  </ul></div>
  <div class="footer-col"><h4>Contacto</h4><ul>
    <li><a href="{WA_URL}" target="_blank" rel="noopener">💬 +52 984 312 19 42</a></li>
    <li><a href="/contacto/">Presupuesto gratuito</a></li>
    <li>Instagram @kaaxcreation</li>
    <li>YouTube Ka'ax Creación</li>
  </ul></div>
</footer>
<div class="footer-bottom">
  <span>© 2026 Ka'ax Creación · Playa del Carmen, México</span>
  <span>Carpintería europea artesanal a medida</span>
</div>"""


COMMON_JS = """<script>
  window.addEventListener('scroll',()=>{
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
  });
  const obs = new IntersectionObserver(entries=>{
    entries.forEach(e=>{ if(e.isIntersecting) e.target.classList.add('visible') });
  },{threshold:.1});
  document.querySelectorAll('.reveal').forEach(r=>obs.observe(r));
  // Lang dropdown
  const langBtn = document.getElementById('langBtn');
  const langDD = document.getElementById('langDropdown');
  if(langBtn && langDD){
    langBtn.addEventListener('click', e=>{
      e.stopPropagation();
      const isOpen = langDD.classList.toggle('open');
      langBtn.classList.toggle('open', isOpen);
      langBtn.setAttribute('aria-expanded', isOpen);
    });
    document.addEventListener('click', ()=>{
      langDD.classList.remove('open');
      langBtn.classList.remove('open');
      langBtn.setAttribute('aria-expanded','false');
    });
    document.addEventListener('keydown', e=>{
      if(e.key==='Escape'){langDD.classList.remove('open');langBtn.classList.remove('open');langBtn.focus();}
    });
  }
  // Hamburger
  (function(){
    var btn=document.getElementById('navHamburger'),menu=document.getElementById('navMobileMenu');
    if(!btn||!menu)return;
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      var open=menu.classList.toggle('open');
      btn.classList.toggle('open',open);btn.setAttribute('aria-expanded',open);
    });
    menu.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click',function(){menu.classList.remove('open');btn.classList.remove('open');btn.setAttribute('aria-expanded','false');});
    });
    document.addEventListener('click',function(e){
      if(!menu.contains(e.target)&&e.target!==btn){menu.classList.remove('open');btn.classList.remove('open');btn.setAttribute('aria-expanded','false');}
    });
  })();
</script>"""


def build_page(title, description, canonical, breadcrumbs, content, root_prefix, active_page="", schema_ld="", image_prefix="../../"):
    """Génère une page HTML complète."""
    schema_block = f'<script type="application/ld+json">{schema_ld}</script>' if schema_ld else ""

    # Adjust hero bg path based on depth
    hero_bg_style = f"background:linear-gradient(135deg,rgba(13,13,13,.92) 0%,rgba(45,74,62,.2) 50%,rgba(13,13,13,.95) 100%),url('{image_prefix}images/hero-bg.jpg') center/cover"

    return f"""<!DOCTYPE html>
<html lang="es">
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
<meta property="og:locale" content="es_MX">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{schema_block}
<style>{COMMON_CSS}</style>
</head>
<body>

{nav_html(root_prefix, active_page)}

{ticker_html()}

<div style="position:fixed;inset:0;{hero_bg_style};z-index:-1"></div>

{breadcrumbs}

{content}

{footer_html(root_prefix)}

{COMMON_JS}
</body>
</html>"""


def breadcrumb(items, root_prefix):
    """items = list of (label, href) — dernier item = page courante (pas de lien)"""
    parts = f'<a href="{root_prefix}">Inicio</a>'
    for label, href in items[:-1]:
        parts += f'<span>›</span><a href="{href}">{label}</a>'
    parts += f'<span>›</span><span>{items[-1][0]}</span>'
    return f'<nav class="breadcrumb" aria-label="Migas de pan">{parts}</nav>'


# ═══════════════════════════════════════════════════════════════
# PAGES SERVICE
# ═══════════════════════════════════════════════════════════════

def page_cocinas():
    schema = """{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://kaaxcreacion.com/cocinas-a-medida/#service",
  "name": "Cocinas a medida en la Riviera Maya",
  "description": "Diseño y fabricación de cocinas integrales a medida. Melamina europea, aluminio y acabados premium para casas y proyectos residenciales en Playa del Carmen, Cancún y Tulum.",
  "provider": {
    "@type": "HomeAndConstructionBusiness",
    "@id": "https://kaaxcreacion.com/#business",
    "name": "Ka'ax Creación",
    "url": "https://kaaxcreacion.com",
    "telephone": "+529843121942",
    "address": {"@type": "PostalAddress","addressLocality": "Playa del Carmen","addressRegion": "Quintana Roo","addressCountry": "MX"}
  },
  "areaServed": {"@type": "GeoCircle","geoMidpoint": {"@type": "GeoCoordinates","latitude": 20.6296,"longitude": -87.0739},"geoRadius": "250000"},
  "serviceType": "Carpintería a medida",
  "url": "https://kaaxcreacion.com/cocinas-a-medida/"
}"""

    crumb = breadcrumb([("Cocinas a medida", "")], "../")

    content = """
<div class="page-hero reveal">
  <p class="page-eyebrow">Servicio — Ka'ax Creación</p>
  <h1>Cocinas Integrales<br><em>a Medida</em></h1>
  <p class="lead">Diseñamos y fabricamos cocinas integrales únicas, adaptadas a su espacio y estilo de vida. Melamina europea de alta resistencia, aluminio anodizado y acabados premium — todo fabricado en nuestro taller de Playa del Carmen.</p>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20para%20cocina." class="btn-wa" target="_blank" rel="noopener">💬 Presupuesto gratuito</a>
    <a href="../realizaciones/" class="btn-secondary">Ver nuestras realizaciones</a>
  </div>
</div>

<div style="background:rgba(201,168,76,.08);border-top:1px solid rgba(201,168,76,.2);border-bottom:1px solid rgba(201,168,76,.2);padding:50px 60px;max-width:100%">
  <div class="stats-bar" style="background:transparent;padding:0;border:none;max-width:1300px;margin:0 auto">
    <div class="stat"><div class="stat-num">100%</div><div class="stat-label">Fabricación propia</div></div>
    <div class="stat"><div class="stat-num">6–10</div><div class="stat-label">Semanas de entrega</div></div>
    <div class="stat"><div class="stat-num">15+</div><div class="stat-label">Acabados disponibles</div></div>
    <div class="stat"><div class="stat-num">5</div><div class="stat-label">Años de garantía</div></div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="content-grid">
    <div>
      <h2>¿Por qué elegir una cocina<br><em>a medida</em>?</h2>
      <p>Una cocina de serie nunca aprovecha al máximo su espacio. Los ángulos irregulares, las columnas, los techos inclinados — en la Riviera Maya, cada vivienda tiene sus particularidades. Una cocina a medida se adapta al milímetro a su arquitectura.</p>
      <p>En Ka'ax Creación, comenzamos por una visita técnica gratuita. Medimos, fotografiamos y escuchamos sus necesidades. El diseño se realiza en 3D antes de cualquier fabricación, para que pueda visualizar el resultado final con exactitud.</p>
      <p>Utilizamos exclusivamente materiales europeos: melamina de alta densidad certificada, aluminio anodizado de calidad aeronáutica, herrajes Blum y Hettich reconocidos mundialmente. Nada de materiales de segunda categoría.</p>
      <h3>Materiales que duran en el clima tropical</h3>
      <p>El clima de la Riviera Maya — humedad alta, cambios térmicos, sal marina — es uno de los más exigentes del mundo para la carpintería. Nuestra melamina europea resiste la humedad, no se hincha, no se deforma. Los herrajes inoxidables no se oxidan. Hemos elegido cada componente en función de este entorno específico.</p>
    </div>
    <div>
      <h2>Nuestras<br><em>especialidades</em></h2>
      <ul>
        <li><strong>Cocinas lineales y en L</strong> — optimización máxima del espacio disponible con diseño ergonómico</li>
        <li><strong>Cocinas con isla central</strong> — diseñadas para los espacios abiertos de las villas y penthouse de la Riviera Maya</li>
        <li><strong>Cocinas en U</strong> — para las residencias con cocinas de gran superficie</li>
        <li><strong>Cocinas semi-abertas</strong> — integración perfecta entre sala y cocina con divisiones decorativas</li>
        <li><strong>Cocinas de lujo con compartimentos ocultos</strong> — cajones secretos integrados, perfectamente invisibles</li>
        <li><strong>Cocinas con iluminación integrada</strong> — LED empotrado en cornisas, plintos y vitrinas</li>
      </ul>
      <h3>Opciones de acabado</h3>
      <ul>
        <li>Mate liso en más de 200 colores RAL</li>
        <li>Efecto madera (roble, nogal, teca)</li>
        <li>Lacado brillante en colores personalizados</li>
        <li>Melamina satinada antihuella</li>
        <li>Puertas de aluminio y cristal</li>
        <li>Encimeras: cuarzo, mármol, madera maciza, Dekton</li>
      </ul>
    </div>
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:48px">Nuestro proceso de<br><em style="font-style:italic;color:#E8C97A">fabricación</em></h2>
    <div class="process-step">
      <div class="step-num">01</div>
      <div class="step-content">
        <h3>Visita técnica &amp; medición</h3>
        <p>Un artesano de Ka'ax Creación se desplaza a su domicilio para tomar medidas precisas, fotografiar el espacio y escuchar sus necesidades. Esta consulta es completamente gratuita y sin compromiso. Cubrimos Cancún, Playa del Carmen, Tulum y toda la Riviera Maya.</p>
      </div>
    </div>
    <div class="process-step">
      <div class="step-num">02</div>
      <div class="step-content">
        <h3>Diseño 3D &amp; selección de materiales</h3>
        <p>Presentamos una propuesta de diseño en 3D detallada, con renders realistas de su futura cocina. Seleccionamos juntos los materiales, acabados, herrajes y elementos de iluminación. El presupuesto definitivo se entrega en esta etapa.</p>
      </div>
    </div>
    <div class="process-step">
      <div class="step-num">03</div>
      <div class="step-content">
        <h3>Fabricación en taller</h3>
        <p>Toda la carpintería se fabrica en nuestro taller de Playa del Carmen. Nuestros artesanos, formados en Francia por los Compagnons du Tour de France, trabajan cada pieza con precisión milimétrica. Plazo habitual: 4 a 6 semanas.</p>
      </div>
    </div>
    <div class="process-step">
      <div class="step-num">04</div>
      <div class="step-content">
        <h3>Instalación &amp; puesta en marcha</h3>
        <p>El equipo de instalación de Ka'ax Creación se encarga de la colocación completa. Gestión de la instalación eléctrica, fontanería y pintura si es necesario. Verificación completa antes de entrega. Garantía de 5 años en materiales y mano de obra.</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Preguntas frecuentes sobre<br><em>cocinas a medida</em></h2>
  <div class="content-grid">
    <div>
      <h3>¿Cuánto cuesta una cocina a medida en Playa del Carmen?</h3>
      <p>El precio de una cocina a medida en la Riviera Maya varía según el tamaño, los materiales y la complejidad del diseño. Una cocina pequeña (8–10 m²) comienza a partir de $45,000 MXN. Una cocina con isla para un penthouse puede llegar a $150,000–200,000 MXN. Ofrecemos un presupuesto gratuito y sin compromiso tras la visita técnica.</p>
      <h3>¿Trabajan fuera de Playa del Carmen?</h3>
      <p>Sí. Ka'ax Creación interviene en toda la Riviera Maya y la Península de Yucatán: Cancún, Tulum, Puerto Morelos, Puerto Aventuras, Isla Mujeres, Cozumel, Mérida, Holbox y más. El desplazamiento está incluido en el presupuesto.</p>
    </div>
    <div>
      <h3>¿Cuánto tiempo tarda la fabricación?</h3>
      <p>El proceso completo — desde la visita técnica hasta la instalación — toma entre 6 y 10 semanas. La fabricación en taller representa 4 a 6 semanas. Los plazos se confirman en el contrato y se respetan con garantía de terminación.</p>
      <h3>¿Pueden integrar electrodomésticos de marcas específicas?</h3>
      <p>Absolutamente. Diseñamos la carpintería alrededor de los electrodomésticos de su elección: Miele, Bosch, Siemens, Sub-Zero, Gaggenau y cualquier otra marca. También podemos asesorarle en la selección según su presupuesto y necesidades.</p>
    </div>
  </div>
</div>

<div class="cta-section">
  <div class="cta-section-content">
    <h2>¿Listo para su cocina<br><em>de ensueño</em>?</h2>
    <p>Presupuesto gratuito · Desplazamiento incluido · Sin compromiso</p>
    <div class="cta-buttons">
      <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20para%20cocina." class="btn-wa" target="_blank" rel="noopener">💬 Contactar por WhatsApp</a>
      <a href="../contacto/" class="btn-secondary">Formulario de contacto</a>
    </div>
  </div>
</div>
"""
    return build_page(
        title="Cocinas a Medida en la Riviera Maya | Ka'ax Creación",
        description="Diseño y fabricación de cocinas integrales a medida en Playa del Carmen, Cancún y Tulum. Melamina europea, herrajes Blum, acabados premium. Presupuesto gratuito.",
        canonical=f"{DOMAIN}/cocinas-a-medida/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="cocinas-a-medida",
        schema_ld=schema,
        image_prefix="../"
    )


def page_closets():
    schema = """{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://kaaxcreacion.com/closets-y-vestidores/#service",
  "name": "Closets y vestidores a medida en la Riviera Maya",
  "description": "Diseño y fabricación de vestidores, closets y armarios a medida. Acabados europeos de lujo para residencias en Playa del Carmen, Cancún y Tulum.",
  "provider": {"@type": "HomeAndConstructionBusiness","@id": "https://kaaxcreacion.com/#business","name": "Ka'ax Creación","url": "https://kaaxcreacion.com","telephone": "+529843121942"},
  "areaServed": "Riviera Maya, Yucatán",
  "url": "https://kaaxcreacion.com/closets-y-vestidores/"
}"""

    crumb = breadcrumb([("Closets y Vestidores", "")], "../")

    content = """
<div class="page-hero reveal">
  <p class="page-eyebrow">Servicio — Ka'ax Creación</p>
  <h1>Closets &amp; Vestidores<br><em>a Medida</em></h1>
  <p class="lead">Un vestidor no es solo un espacio de almacenamiento: es un ritual cotidiano. Diseñamos y fabricamos closets y dressing rooms de lujo que combinan funcionalidad europea con la elegancia que merece su hogar en la Riviera Maya.</p>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20para%20vestidor." class="btn-wa" target="_blank" rel="noopener">💬 Presupuesto gratuito</a>
    <a href="../realizaciones/" class="btn-secondary">Ver nuestras realizaciones</a>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="content-grid">
    <div>
      <h2>El vestidor que<br><em>siempre imaginó</em></h2>
      <p>En la Riviera Maya, donde los interiores de lujo son la norma, un vestidor de serie nunca está a la altura. Las grandes villas, los condominios de Cancún, los apartamentos de Tulum — cada espacio merece una solución única y personalizada.</p>
      <p>Ka'ax Creación fabrica vestidores, closets empotrados, armarios y dressing rooms a medida, con los mismos estándares de calidad que nuestras cocinas. Melamina europea certificada, herrajes de alta gama (Hettich, Blum), cajones con cierre suave, iluminación LED integrada.</p>
      <h3>Tipos de vestidores que fabricamos</h3>
      <ul>
        <li><strong>Closets empotrados</strong> — integración perfecta en el espacio arquitectónico, de pared a pared y de suelo a techo</li>
        <li><strong>Dressing rooms independientes</strong> — espacios de vestir con isla central, espejos de cuerpo entero y asiento tapizado</li>
        <li><strong>Walk-in closet</strong> — conversión de habitaciones pequeñas o espacios irregulares en vestidores de lujo</li>
        <li><strong>Armarios con puertas correderas</strong> — solución elegante para espacios donde las puertas abatibles no son prácticas</li>
        <li><strong>Vestidores con compartimentos ocultos</strong> — espacios de discreción integrados para joyas, documentos y objetos de valor</li>
      </ul>
    </div>
    <div>
      <h2>Organización<br><em>inteligente</em></h2>
      <p>El interior de un vestidor Ka'ax Creación se diseña en función de su guardarropa real: conteo de prendas colgadas, dobladas, zapatos, bolsos, accesorios. Cada centímetro tiene una función.</p>
      <ul>
        <li>Barras de colgar regulables en altura</li>
        <li>Cajones con divisores a medida para accesorios</li>
        <li>Zapateros extraíbles con capacidad para 20 a 60 pares</li>
        <li>Estantes ajustables para bolsos y complementos</li>
        <li>Cajón joyero con forro de terciopelo</li>
        <li>Espejo de cuerpo entero iluminado</li>
        <li>Iluminación LED con sensor de apertura</li>
        <li>Silla o banco tapizado integrado</li>
      </ul>
      <h3>Materiales disponibles</h3>
      <ul>
        <li>Melamina mate en más de 200 colores RAL</li>
        <li>Efecto madera: roble natural, nogal oscuro, fresno</li>
        <li>Lacado brillante o satinado</li>
        <li>Puertas de cristal con perfilería aluminio</li>
        <li>Puertas espejos para ampliar visualmente el espacio</li>
      </ul>
    </div>
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:48px">También fabricamos<br><em style="font-style:italic;color:#E8C97A">a medida</em></h2>
    <div class="content-grid-3">
      <div class="feature-card">
        <div class="feature-icon">🛏️</div>
        <h3>Cabeceras de cama</h3>
        <p>Cabeceras tapizadas o en madera con iluminación integrada y almacenamiento oculto. Perfectas para las suites de las villas de lujo.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📚</div>
        <h3>Librerías &amp; estanterías</h3>
        <p>Bibliotecas de pared completa, estanterías modulares y unidades de exhibición en madera maciza o melamina europea.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🛁</div>
        <h3>Muebles de baño</h3>
        <p>Vanities y muebles de baño a medida con materiales resistentes a la humedad: MDF hidrófugo, aluminio, superficies de Corian.</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Preguntas frecuentes sobre<br><em>vestidores a medida</em></h2>
  <div class="content-grid">
    <div>
      <h3>¿Cuánto cuesta un closet a medida en Cancún o Playa del Carmen?</h3>
      <p>El precio depende del tamaño y la complejidad. Un armario empotrado estándar (3–4 metros de ancho) comienza desde $20,000 MXN. Un dressing room completo con isla y acabados premium puede llegar a $80,000–120,000 MXN. Presupuesto gratuito tras la visita técnica.</p>
      <h3>¿Pueden adaptar el vestidor a una habitación irregular?</h3>
      <p>Absolutamente. Es precisamente para esto que existe la carpintería a medida. Techos inclinados, columnas, espacios bajo escalera — diseñamos alrededor de cada particularidad arquitectónica.</p>
    </div>
    <div>
      <h3>¿Qué tipo de herrajes utilizan?</h3>
      <p>Utilizamos exclusivamente herrajes de marcas europeas reconocidas: Hettich y Blum para cajones (cierre suave garantizado 50,000 ciclos), Grass para correderas, perfilería aluminio anodizado. Todos los herrajes están garantizados 5 años.</p>
      <h3>¿Pueden añadir iluminación integrada?</h3>
      <p>Sí, es una de nuestras especialidades. Iluminación LED integrada con sensor de apertura de puerta, regletas LED en barras de colgar, iluminación de cajones — todo se diseña al mismo tiempo que la carpintería para una integración perfecta.</p>
    </div>
  </div>
</div>

<div class="cta-section">
  <div class="cta-section-content">
    <h2>Su vestidor de ensueño,<br><em>fabricado a medida</em></h2>
    <p>Visita técnica gratuita · Diseño 3D · Presupuesto sin compromiso</p>
    <div class="cta-buttons">
      <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20para%20vestidor." class="btn-wa" target="_blank" rel="noopener">💬 Contactar por WhatsApp</a>
      <a href="../contacto/" class="btn-secondary">Formulario de contacto</a>
    </div>
  </div>
</div>
"""
    return build_page(
        title="Closets y Vestidores a Medida | Ka'ax Creación Riviera Maya",
        description="Diseño y fabricación de closets, vestidores y armarios a medida en Playa del Carmen, Cancún y Tulum. Melamina europea, herrajes Blum/Hettich, acabados premium.",
        canonical=f"{DOMAIN}/closets-y-vestidores/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="closets-y-vestidores",
        schema_ld=schema,
        image_prefix="../"
    )


def page_realizaciones():
    schema = """{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "@id": "https://kaaxcreacion.com/realizaciones/#page",
  "name": "Realizaciones — Ka'ax Creación",
  "description": "Portfolio de cocinas, vestidores y muebles a medida fabricados por Ka'ax Creación en la Riviera Maya.",
  "url": "https://kaaxcreacion.com/realizaciones/",
  "provider": {"@type": "HomeAndConstructionBusiness","@id": "https://kaaxcreacion.com/#business","name": "Ka'ax Creación"}
}"""
    crumb = breadcrumb([("Realizaciones", "")], "../")
    content = """
<div class="page-hero reveal">
  <p class="page-eyebrow">Portfolio — Ka'ax Creación</p>
  <h1>Nuestras<br><em>Realizaciones</em></h1>
  <p class="lead">Cada proyecto Ka'ax Creación es único. Cocinas integrales de alta gama, vestidores de lujo, compartimentos ocultos — descubra nuestras realizaciones en villas, condominios y residencias de la Riviera Maya.</p>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div style="display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:300px 240px 300px;gap:4px;max-width:1300px;margin:0 auto">
    <div style="grid-column:span 7;overflow:hidden"><img src="../images/portfolio-1.jpg" alt="Cocina de lujo a medida, Ka'ax Creación, Playa del Carmen" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 5;overflow:hidden"><img src="../images/portfolio-2.jpg" alt="Vestidor de alta gama, Ka'ax Creación, Cancún" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 4;overflow:hidden"><img src="../images/portfolio-3.jpg" alt="Closet a medida, Ka'ax Creación, Riviera Maya" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 4;overflow:hidden"><img src="../images/adn-detail.jpg" alt="Detalle de compartimento oculto, Ka'ax Creación" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 4;overflow:hidden"><img src="../images/portfolio-4.jpg" alt="Mueble a medida, Ka'ax Creación, Tulum" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 5;overflow:hidden"><img src="../images/portfolio-5.jpg" alt="Escalera artesanal, Ka'ax Creación" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
    <div style="grid-column:span 7;overflow:hidden"><img src="../images/adn-workshop.jpg" alt="Taller Ka'ax Creación, Playa del Carmen" style="width:100%;height:100%;object-fit:cover;filter:brightness(.85);transition:transform .6s" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy"></div>
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px">Tipos de proyectos<br><em style="font-style:italic;color:#E8C97A">realizados</em></h2>
    <div class="content-grid-3" style="margin-top:40px">
      <div class="feature-card">
        <div class="feature-icon">🏖️</div>
        <h3>Villas de lujo — Riviera Maya</h3>
        <p>Cocinas de alta gama con isla central, vestidores walk-in y muebles de exterior en madera tratada. Proyectos en Playa del Carmen, Tulum y Punta Cana.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🏢</div>
        <h3>Condominios &amp; Penthouse</h3>
        <p>Optimización de espacios en apartamentos de lujo. Cocinas integrales compactas, armarios empotrados y soluciones de almacenamiento inteligentes.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🏨</div>
        <h3>Proyectos comerciales</h3>
        <p>Muebles a medida para boutique hotels, restaurantes y espacios comerciales. Calidad de lujo adaptada a un uso intensivo.</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>¿Le gustaría su proyecto<br><em>en nuestro portfolio</em>?</h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;max-width:620px;margin-bottom:36px">Cada cliente Ka'ax Creación recibe un trabajo artesanal único. Contacte con nosotros para discutir su proyecto y obtener un presupuesto gratuito.</p>
  <div class="cta-buttons" style="justify-content:flex-start">
    <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20gratuito." class="btn-wa" target="_blank" rel="noopener">💬 Contactar por WhatsApp</a>
    <a href="../contacto/" class="btn-secondary">Formulario de contacto</a>
  </div>
</div>
"""
    return build_page(
        title="Realizaciones — Portfolio Cocinas y Vestidores | Ka'ax Creación",
        description="Portfolio de cocinas integrales, vestidores y muebles a medida fabricados por Ka'ax Creación en la Riviera Maya. Villas de lujo, condominios y residencias premium.",
        canonical=f"{DOMAIN}/realizaciones/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="realizaciones/",
        schema_ld=schema,
        image_prefix="../"
    )


def page_metodo():
    schema = """{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://kaaxcreacion.com/metodo/#page",
  "name": "Nuestro método — Ka'ax Creación",
  "description": "Descubra el proceso artesanal de Ka'ax Creación: visita técnica, diseño 3D, fabricación europea y instalación con garantía.",
  "url": "https://kaaxcreacion.com/metodo/"
}"""
    crumb = breadcrumb([("Nuestro Método", "")], "../")
    content = """
<div class="page-hero reveal">
  <p class="page-eyebrow">Proceso — Ka'ax Creación</p>
  <h1>Nuestro<br><em>Método Artesanal</em></h1>
  <p class="lead">De la visita técnica a la instalación, Ka'ax Creación aplica un proceso riguroso y transparente inspirado en los mejores estándares europeos de carpintería de lujo. Cada etapa está diseñada para garantizar un resultado perfecto.</p>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="process-step">
    <div class="step-num">01</div>
    <div class="step-content">
      <h3>Visita técnica gratuita</h3>
      <p>Todo comienza con una visita a su domicilio. Un artesano de Ka'ax Creación se desplaza para tomar medidas precisas con instrumentos de alta precisión (tolerancia: ±1 mm). Fotografiamos el espacio desde todos los ángulos y analizamos las particularidades arquitectónicas: columnas, canalizaciones, desniveles, orientación de la luz natural.</p>
      <p>Esta primera reunión es también una conversación. Hablamos de sus necesidades, su guardarropa, sus hábitos culinarios, su estilo de vida. Un closet diseñado para alguien que colecciona zapatos es muy diferente al de alguien que prioriza los trajes. Una cocina para una familia de 5 no es la misma que para una pareja gourmet.</p>
    </div>
  </div>
  <div class="process-step">
    <div class="step-num">02</div>
    <div class="step-content">
      <h3>Diseño 3D &amp; selección de materiales</h3>
      <p>Con los datos recogidos, nuestro equipo de diseño realiza el proyecto en 3D. Presentamos renders fotorrealistas que permiten visualizar el resultado final antes de cualquier fabricación. ¿El color no es exactamente el que imaginaba? ¿Prefiere dos cajones en lugar de tres estantes? Todo se modifica digitalmente, sin coste adicional.</p>
      <p>En esta fase seleccionamos juntos los materiales: tipo de melamina, acabado de las puertas, herrajes visibles, encimeras (si aplica), iluminación integrada. Cada elección se acompaña de muestras físicas que puede llevarse a casa para verlas en su propio entorno.</p>
    </div>
  </div>
  <div class="process-step">
    <div class="step-num">03</div>
    <div class="step-content">
      <h3>Presupuesto detallado</h3>
      <p>Tras el diseño validado, entregamos un presupuesto línea por línea: materiales, herrajes, iluminación, mano de obra, transporte e instalación. Sin sorpresas. El precio es el que se acordó; no existe el "extra" no previsto en Ka'ax Creación.</p>
      <p>Al firmar el contrato, confirmamos el plazo de entrega — entre 6 y 10 semanas según la complejidad — y la fecha de instalación. Exigimos el cumplimiento de los plazos con la misma disciplina que aprendimos con los Compagnons du Tour de France.</p>
    </div>
  </div>
  <div class="process-step">
    <div class="step-num">04</div>
    <div class="step-content">
      <h3>Fabricación en taller — Playa del Carmen</h3>
      <p>Toda la carpintería se fabrica en nuestro taller de Playa del Carmen. Utilizamos exclusivamente materiales de origen europeo: melamina de alta densidad (melamina 18 mm, cara de alta resistencia a la abrasión), aluminio anodizado de precisión, herrajes Blum y Hettich reconocidos internacionalmente.</p>
      <p>El proceso de corte se realiza con maquinaria CNC de última generación para garantizar la precisión milimétrica. El montaje previo se hace en taller antes del transporte, lo que reduce al mínimo el tiempo de instalación en su domicilio.</p>
    </div>
  </div>
  <div class="process-step">
    <div class="step-num">05</div>
    <div class="step-content">
      <h3>Instalación &amp; verificación</h3>
      <p>El equipo de instalación de Ka'ax Creación se desplaza con todo el material ya preparado. La instalación de una cocina estándar tarda entre 1 y 3 días; un vestidor complejo puede requerir 2 a 4 días. Durante la instalación, gestionamos la coordinación con otros artesanos si es necesario (electricista, fontanero, pintor).</p>
      <p>Antes de la entrega definitiva, realizamos un control de calidad sistemático: verificación de la nivelación, ajuste de bisagras y cajones, comprobación de los sistemas de apertura, prueba de la iluminación integrada. Solo entregamos cuando todo está perfecto.</p>
    </div>
  </div>
  <div class="process-step">
    <div class="step-num">06</div>
    <div class="step-content">
      <h3>Garantía &amp; servicio post-venta</h3>
      <p>Ka'ax Creación garantiza todos sus trabajos durante 5 años: materiales y mano de obra. En caso de problema — ajuste necesario, herraje a reemplazar, acabado a retocar — intervenimos en un plazo máximo de 72 horas. Nuestros clientes son nuestra mejor publicidad, y lo sabemos.</p>
    </div>
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:24px">La formación<br><em style="font-style:italic;color:#E8C97A">que lo hace posible</em></h2>
    <div class="content-grid">
      <div>
        <p style="font-size:15px;line-height:1.9;opacity:.75">Ka'ax Creación fue fundada por Raphaël, artesano formado por los <strong style="color:#C9A84C">Compagnons du Tour de France</strong> — la orden artesanal más antigua y exigente de Francia, fundada en la Edad Media. Raphaël fue <strong style="color:#C9A84C">Major de promoción 2023</strong>: el mejor artesano de su generación.</p>
        <p style="font-size:15px;line-height:1.9;opacity:.75;margin-top:16px">Los Compagnons du Tour de France forman a sus miembros durante 5 a 7 años, recorriendo Francia para aprender con los mejores maestros de cada región. La exigencia, la precisión y el respeto del detalle son valores que Ka'ax Creación transmite a cada proyecto en la Riviera Maya.</p>
      </div>
      <div style="border:1px solid rgba(201,168,76,.3);padding:32px;background:rgba(201,168,76,.04)">
        <div style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#C9A84C;margin-bottom:16px">Nuestra filosofía</div>
        <blockquote style="font-family:'Cormorant Garamond',serif;font-size:22px;font-style:italic;opacity:.8;line-height:1.6;border-left:2px solid #C9A84C;padding-left:24px">"Lo que vale la pena hacer, vale la pena hacerlo bien."</blockquote>
        <p style="font-size:13px;opacity:.5;margin-top:16px;letter-spacing:1px">— Lema de los Compagnons du Tour de France</p>
      </div>
    </div>
  </div>
</div>

<div class="cta-section">
  <div class="cta-section-content">
    <h2>Comencemos su<br><em>proyecto</em></h2>
    <p>Visita técnica gratuita · Diseño 3D · Sin compromiso</p>
    <div class="cta-buttons">
      <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20empezar%20un%20proyecto." class="btn-wa" target="_blank" rel="noopener">💬 Contactar por WhatsApp</a>
      <a href="../contacto/" class="btn-secondary">Formulario de contacto</a>
    </div>
  </div>
</div>
"""
    return build_page(
        title="Nuestro Método Artesanal — Proceso Ka'ax Creación | Riviera Maya",
        description="Descubra el proceso Ka'ax Creación: visita técnica gratuita, diseño 3D, fabricación europea en Playa del Carmen e instalación con garantía 5 años.",
        canonical=f"{DOMAIN}/metodo/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="metodo/",
        schema_ld=schema,
        image_prefix="../"
    )


def page_nosotros():
    schema = """{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "@id": "https://kaaxcreacion.com/nosotros/#page",
  "name": "Nosotros — Ka'ax Creación",
  "description": "Ka'ax Creación: especialistas en cocinas y closets de estilo europeo en Playa del Carmen. Fabricados a medida por artesanos Compagnons du Tour de France.",
  "url": "https://kaaxcreacion.com/nosotros/",
  "mainEntity": {
    "@type": "HomeAndConstructionBusiness",
    "@id": "https://kaaxcreacion.com/#business",
    "name": "Ka'ax Creación",
    "foundingLocation": "Playa del Carmen, Quintana Roo, México",
    "url": "https://kaaxcreacion.com"
  }
}"""
    crumb = breadcrumb([("Nuestro ADN", "")], "../")
    content = """
<div class="page-hero reveal">
  <p class="page-eyebrow">Nuestro ADN — Ka'ax Creación</p>
  <h1>El Arte Europeo<br><em>en la Riviera Maya</em></h1>
  <p class="lead">Ka'ax Creación nació de la convicción de que la Riviera Maya merecía una carpintería de lujo artesanal, fabricada localmente con los estándares europeos más exigentes. Hoy, nuestro taller de Playa del Carmen es una referencia en la región.</p>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="content-grid">
    <div>
      <h2>Ka'ax —<br><em>Bosque y madera en maya</em></h2>
      <p>El nombre Ka'ax no es aleatorio. En lengua maya yucateca, Ka'ax significa «bosque», «madera», «naturaleza viva». Elegimos este nombre para enraizar nuestro taller en la tierra que nos acoge: la Península de Yucatán, donde la civilización maya construyó durante siglos con madera y piedra.</p>
      <p>Creación, en español, expresa lo que hacemos: no reproducimos, no copiamos, no fabricamos en serie. Cada pieza que sale de nuestro taller de Playa del Carmen es una creación original, diseñada para un espacio único y un cliente único.</p>
      <p>Ka'ax Creación es el encuentro entre el savoir-faire artesanal francés y la calidez de México: la precisión europea al servicio de la vida tropical.</p>
    </div>
    <div>
      <img src="../images/adn-detail.jpg" alt="Detalle de artesanía Ka'ax Creación, Playa del Carmen" style="width:100%;height:400px;object-fit:cover;filter:brightness(.9)" loading="lazy">
    </div>
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:48px">Los <em style="font-style:italic;color:#E8C97A">Compagnons du Tour de France</em></h2>
    <div class="content-grid">
      <div>
        <p style="font-size:15px;line-height:1.9;opacity:.75">Fundada en la Edad Media, la orden de los <strong style="color:#C9A84C">Compagnons du Tour de France</strong> es una de las instituciones artesanales más antiguas del mundo. Durante siglos, formó a los maestros artesanos que construyeron las catedrales, los palacios y los grandes muebles de Francia.</p>
        <p style="font-size:15px;line-height:1.9;opacity:.75;margin-top:16px">La formación dura entre 5 y 7 años. El aprendiz — el «aspirante» — recorre las ciudades de Francia, trabajando con los mejores maestros de cada región durante meses. La exigencia es total: se trabaja hasta que el resultado es perfecto, y solo cuando el resultado es perfecto.</p>
        <p style="font-size:15px;line-height:1.9;opacity:.75;margin-top:16px">Raphaël, fundador de Ka'ax Creación, fue <strong style="color:#C9A84C">Major de promoción 2023</strong>: el mejor de su generación. Este título no es honorífico — es el resultado de años de trabajo exigente y de una evaluación rigurosa por los maestros de la orden.</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:24px">
        <div class="feature-card">
          <div class="feature-icon">🎖️</div>
          <h3>Major de Promoción 2023</h3>
          <p>El reconocimiento más alto de los Compagnons du Tour de France, otorgado al mejor artesano de la generación tras 5 años de formación intensiva.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌍</div>
          <h3>Formación europea</h3>
          <p>5 años de aprendizaje recorriendo los mejores talleres de Francia, trabajando con los maestros de la carpintería, ebanistería y menuiserie de lujo.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌿</div>
          <h3>Raíces mayas</h3>
          <p>El taller se fundó en Playa del Carmen para servir a la Riviera Maya, donde la madera y la artesanía tienen una historia milenaria.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Nuestros valores<br><em>artesanales</em></h2>
  <div class="content-grid-3">
    <div class="feature-card">
      <div class="feature-icon">🎯</div>
      <h3>Precisión</h3>
      <p>Tolerancia de ±1 mm en todos nuestros trabajos. No es publicidad: es la consecuencia de años de formación con los Compagnons du Tour de France.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🤝</div>
      <h3>Transparencia</h3>
      <p>Presupuesto detallado línea por línea. Plazos respetados. Sin extras no previstos. La confianza del cliente es nuestra materia prima más valiosa.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🌱</div>
      <h3>Durabilidad</h3>
      <p>Materiales seleccionados para durar 20, 30, 40 años en el clima tropical de la Riviera Maya. No fabricamos para reemplazar, fabricamos para perdurar.</p>
    </div>
  </div>
</div>

<div class="cta-section">
  <div class="cta-section-content">
    <h2>Confienos su<br><em>proyecto</em></h2>
    <p>Un artesano formado en Francia, en su hogar de la Riviera Maya</p>
    <div class="cta-buttons">
      <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20hablar%20de%20un%20proyecto." class="btn-wa" target="_blank" rel="noopener">💬 Contactar por WhatsApp</a>
      <a href="../contacto/" class="btn-secondary">Formulario de contacto</a>
    </div>
  </div>
</div>
"""
    return build_page(
        title="Nuestro ADN — Ka'ax Creación | Compagnons du Tour de France",
        description="Ka'ax Creación: cocinas y closets a medida de estilo europeo en Playa del Carmen. Fundada por Raphaël, Major 2023 de los Compagnons du Tour de France.",
        canonical=f"{DOMAIN}/nosotros/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="nosotros/",
        schema_ld=schema,
        image_prefix="../"
    )


def page_contacto():
    schema = """{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "@id": "https://kaaxcreacion.com/contacto/#page",
  "name": "Contacto — Ka'ax Creación",
  "description": "Contacte con Ka'ax Creación para un presupuesto gratuito de cocina o vestidor a medida en la Riviera Maya.",
  "url": "https://kaaxcreacion.com/contacto/"
}"""
    crumb = breadcrumb([("Contacto", "")], "../")
    content = """
<div class="page-hero reveal">
  <p class="page-eyebrow">Contacto — Ka'ax Creación</p>
  <h1>Presupuesto<br><em>Gratuito</em></h1>
  <p class="lead">Cuéntenos su proyecto. Realizamos una visita técnica gratuita en toda la Riviera Maya y la Península de Yucatán, y entregamos un presupuesto detallado sin compromiso en 48 horas.</p>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="content-grid">
    <div>
      <h2>Contáctenos<br><em>directamente</em></h2>
      <p style="font-size:15px;line-height:1.9;opacity:.75;margin-bottom:32px">La forma más rápida de obtener un presupuesto es contactarnos por WhatsApp. Respondemos en menos de 2 horas en horario laboral (lun–sáb, 8h–20h).</p>

      <div style="display:flex;flex-direction:column;gap:16px;margin-bottom:40px">
        <a href="https://wa.me/529843121942?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20gratuito." class="btn-wa" target="_blank" rel="noopener" style="justify-content:center">💬 +52 984 312 19 42 — WhatsApp</a>
      </div>

      <div style="border-top:1px solid rgba(201,168,76,.2);padding-top:32px">
        <h3>Zonas de intervención</h3>
        <p style="font-size:14px;opacity:.7;line-height:1.9">Nuestro taller está en Playa del Carmen. Intervenimos en toda la Riviera Maya e islas: Cancún, Tulum, Puerto Morelos, Puerto Aventuras, Isla Mujeres y Cozumel. También realizamos proyectos selectivos en Mérida, Holbox, Valladolid, Tizimín y Campeche. <strong style="color:#C9A84C">El desplazamiento está incluido en el presupuesto.</strong></p>
        <h3 style="margin-top:24px">Horarios</h3>
        <p style="font-size:14px;opacity:.7;line-height:1.9">Lunes a sábado: 8h00 — 20h00<br>Domingos: solo emergencias</p>
      </div>
    </div>

    <div style="border:1px solid rgba(201,168,76,.25);padding:40px;background:rgba(201,168,76,.03)">
      <h3 style="font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:300;margin-bottom:24px;color:#E8C97A">Cuéntenos su proyecto</h3>
      <form action="https://formspree.io/f/kaaxcreacion" method="POST" style="display:flex;flex-direction:column;gap:16px">
        <div>
          <label style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6;display:block;margin-bottom:6px">Nombre *</label>
          <input type="text" name="nombre" required style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.2);color:var(--creme);padding:12px 16px;font-family:'Inter',sans-serif;font-size:14px;outline:none;transition:border-color .3s" onfocus="this.style.borderColor='rgba(201,168,76,.8)'" onblur="this.style.borderColor='rgba(201,168,76,.2)'" placeholder="Su nombre completo">
        </div>
        <div>
          <label style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6;display:block;margin-bottom:6px">WhatsApp / Teléfono *</label>
          <input type="tel" name="telefono" required style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.2);color:var(--creme);padding:12px 16px;font-family:'Inter',sans-serif;font-size:14px;outline:none;transition:border-color .3s" onfocus="this.style.borderColor='rgba(201,168,76,.8)'" onblur="this.style.borderColor='rgba(201,168,76,.2)'" placeholder="+52 984 XXX XXXX">
        </div>
        <div>
          <label style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6;display:block;margin-bottom:6px">Ciudad / Zona *</label>
          <select name="ciudad" required style="width:100%;background:#111;border:1px solid rgba(201,168,76,.2);color:var(--creme);padding:12px 16px;font-family:'Inter',sans-serif;font-size:14px;outline:none">
            <option value="">Seleccionar ciudad...</option>
            <option>Playa del Carmen</option>
            <option>Cancún</option>
            <option>Tulum</option>
            <option>Puerto Morelos</option>
            <option>Puerto Aventuras</option>
            <option>Isla Mujeres</option>
            <option>Cozumel</option>
            <option>Cobá / Bacalar</option>
            <option>Felipe Carrillo Puerto</option>
            <option>Mérida</option>
            <option>Holbox</option>
            <option>Valladolid</option>
            <option>Tizimín</option>
            <option>Campeche</option>
            <option>Otra zona</option>
          </select>
        </div>
        <div>
          <label style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6;display:block;margin-bottom:6px">Tipo de proyecto</label>
          <select name="proyecto" style="width:100%;background:#111;border:1px solid rgba(201,168,76,.2);color:var(--creme);padding:12px 16px;font-family:'Inter',sans-serif;font-size:14px;outline:none">
            <option value="">Seleccionar...</option>
            <option>Cocina integral a medida</option>
            <option>Vestidor / Closet a medida</option>
            <option>Mueble a medida</option>
            <option>Proyecto mixto (cocina + vestidor)</option>
            <option>Proyecto comercial</option>
            <option>Otro</option>
          </select>
        </div>
        <div>
          <label style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6;display:block;margin-bottom:6px">Descripción del proyecto</label>
          <textarea name="descripcion" rows="4" style="width:100%;background:rgba(255,255,255,.05);border:1px solid rgba(201,168,76,.2);color:var(--creme);padding:12px 16px;font-family:'Inter',sans-serif;font-size:14px;outline:none;resize:vertical;transition:border-color .3s" onfocus="this.style.borderColor='rgba(201,168,76,.8)'" onblur="this.style.borderColor='rgba(201,168,76,.2)'" placeholder="Cuéntenos: dimensiones aproximadas, estilo deseado, plazo previsto..."></textarea>
        </div>
        <button type="submit" style="background:var(--or);color:var(--noir);padding:16px 36px;font-size:12px;letter-spacing:2px;text-transform:uppercase;border:none;cursor:pointer;font-family:'Inter',sans-serif;font-weight:500;transition:all .3s" onmouseover="this.style.background='#E8C97A'" onmouseout="this.style.background='#C9A84C'">Enviar solicitud de presupuesto</button>
        <p style="font-size:11px;opacity:.4;text-align:center;letter-spacing:.5px">Respuesta garantizada en menos de 48 horas · Presupuesto gratuito &amp; sin compromiso</p>
      </form>
    </div>
  </div>
</div>
"""
    return build_page(
        title="Contacto — Presupuesto Gratuito | Ka'ax Creación Riviera Maya",
        description="Solicite su presupuesto gratuito para cocina o vestidor a medida en Playa del Carmen, Cancún o Tulum. Respuesta en 48h. Visita técnica gratuita en toda la Riviera Maya.",
        canonical=f"{DOMAIN}/contacto/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="contacto/",
        schema_ld=schema,
        image_prefix="../"
    )


def page_zona_index():
    """Page d'index des zones de couverture."""
    schema = """{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://kaaxcreacion.com/zona/#page",
  "name": "Zonas de Intervención — Ka'ax Creación",
  "description": "Ka'ax Creación interviene en toda la Riviera Maya y la Península de Yucatán: Cancún, Playa del Carmen, Tulum, Mérida y más.",
  "url": "https://kaaxcreacion.com/zona/"
}"""
    crumb = breadcrumb([("Zonas de Intervención", "")], "../")

    zones_rm = [
        ("playa-del-carmen", "🏖️", "Playa del Carmen", "Nuestra base — tiempo de respuesta máximo 24h"),
        ("cancun", "🏙️", "Cancún", "Riviera Maya Norte — proyectos en Hotel Zone y centro"),
        ("tulum", "🌿", "Tulum", "Riviera Maya Sur — villas de lujo y proyectos eco"),
        ("puerto-morelos", "⚓", "Puerto Morelos", "Entre Cancún y Playa del Carmen"),
        ("puerto-aventuras", "⛵", "Puerto Aventuras", "Marina privada — residencias premium"),
        ("coba-bacalar", "🏞️", "Cobá · Bacalar", "Interior — proyectos selectivos"),
        ("felipe-carrillo-puerto", "🌳", "Felipe Carrillo Puerto", "Sur de Quintana Roo"),
        ("isla-mujeres", "🏝️", "Isla Mujeres", "Isla frente a Cancún — proyectos selectivos"),
        ("cozumel", "🤿", "Cozumel", "Isla frente a Playa del Carmen — proyectos selectivos"),
    ]
    zones_yuc = [
        ("merida", "🏛️", "Mérida", "Capital de Yucatán — proyectos selectivos"),
        ("holbox", "🦩", "Holbox", "Isla sin coches — proyectos de lujo exclusivos"),
        ("valladolid", "🌺", "Valladolid", "Corazón de Yucatán"),
        ("tizimin", "🌾", "Tizimín", "Norte de Yucatán"),
        ("campeche", "🏰", "Campeche", "Capital histórica — proyectos selectivos"),
    ]

    def zone_link(slug, icon, name, sub):
        return f"""<a href="../zona/{slug}/" class="zone-card">
        <span class="zone-card-icon">{icon}</span>
        <div>
          <div class="zone-card-name">{name}</div>
          <div class="zone-card-sub">{sub}</div>
        </div>
        <span class="zone-card-arrow">→</span>
      </a>"""

    zones_rm_html = "\n".join(zone_link(*z) for z in zones_rm)
    zones_yuc_html = "\n".join(zone_link(*z) for z in zones_yuc)

    content = f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">Cobertura — Ka'ax Creación</p>
  <h1>Zonas de<br><em>Intervención</em></h1>
  <p class="lead">Ka'ax Creación tiene su taller en Playa del Carmen y cubre toda la Riviera Maya e islas, además de proyectos selectivos en la Península de Yucatán. El desplazamiento y la instalación están incluidos en el presupuesto.</p>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>Riviera Maya &amp;<br><em>Islas</em></h2>
  <p style="font-size:15px;line-height:1.9;opacity:.75;margin-bottom:32px">Nuestra zona principal de intervención. Fabricamos e instalamos cocinas, vestidores y muebles a medida en toda la costa caribeña de Quintana Roo.</p>
  <div class="zones-grid">
    {zones_rm_html}
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:16px">Yucatán &amp; Campeche —<br><em style="font-style:italic;color:#E8C97A">Proyectos selectivos</em></h2>
    <p style="font-size:15px;line-height:1.9;opacity:.75;margin-bottom:32px;max-width:620px">Para proyectos de mayor escala o de lujo exclusivo, Ka'ax Creación acepta encargos en la Península de Yucatán y Campeche. Consulte disponibilidad.</p>
    <div class="zones-grid">
      {zones_yuc_html}
    </div>
  </div>
</div>

<div class="cta-section">
  <div class="cta-section-content">
    <h2>¿En qué zona<br><em>se encuentra?</em></h2>
    <p>Contáctenos para verificar disponibilidad en su zona</p>
    <div class="cta-buttons">
      <a href="{WA_URL}" class="btn-wa" target="_blank" rel="noopener">💬 Consultar disponibilidad</a>
      <a href="../contacto/" class="btn-secondary">Formulario de contacto</a>
    </div>
  </div>
</div>
"""
    return build_page(
        title="Zonas de Intervención — Riviera Maya y Yucatán | Ka'ax Creación",
        description="Ka'ax Creación cubre la Riviera Maya: Cancún, Playa del Carmen, Tulum, Puerto Morelos, Isla Mujeres, Cozumel, y proyectos selectivos en Mérida, Holbox y Campeche.",
        canonical=f"{DOMAIN}/zona/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../",
        active_page="zona/",
        schema_ld=schema,
        image_prefix="../"
    )


# ═══════════════════════════════════════════════════════════════
# PAGES ZONE — TEMPLATE GÉNÉRIQUE
# ═══════════════════════════════════════════════════════════════

ZONE_DATA = {
    "playa-del-carmen": {
        "name": "Playa del Carmen",
        "name_short": "Playa del Carmen",
        "region": "Riviera Maya",
        "type": "primary",  # primary | isla | selectivo
        "lat": 20.6296,
        "lng": -87.0739,
        "h1": "Cocinas &amp; Vestidores<br><em>a Medida en Playa del Carmen</em>",
        "meta_title": "Cocinas a Medida Playa del Carmen | Ka'ax Creación — Riviera Maya",
        "meta_desc": "Cocinas integrales y vestidores a medida en Playa del Carmen. Fabricado en taller local por artesanos formados en Francia. Presupuesto gratuito · Desplazamiento incluido.",
        "lead": "Nuestro taller está en Playa del Carmen. Fabricamos e instalamos cocinas integrales, vestidores y muebles a medida a domicilio — con el savoir-faire europeo de los Compagnons du Tour de France y el tiempo de respuesta más rápido de la zona.",
        "intro": "Playa del Carmen es el corazón de la Riviera Maya y el hogar de Ka'ax Creación. Nuestra carpintería de lujo está disponible para todas las zonas de la ciudad: desde los condominios de Colosio y Villas del Sol hasta las exclusivas villas de Playacar y los apartamentos de la 5ª Avenida.",
        "specificites": [
            ("🏖️", "Villas de Playacar", "Proyectos de alta gama para las residencias de lujo del fraccionamiento privado de Playacar — cocinas con isla, vestidores walk-in, muebles de terraza."),
            ("🏢", "Condominios en altura", "Cocinas integrales optimizadas para los modernos condominios de Playa del Carmen, con soluciones inteligentes para espacios reducidos."),
            ("🏡", "Casas individuales", "Cocinas familiares, armarios empotrados y sistemas de almacenamiento personalizados para las casas del fraccionamiento Villas del Sol, Ejidal y otros."),
            ("🏨", "Proyectos comerciales", "Muebles a medida para boutique hotels, restaurantes y locales comerciales en la 5ª Avenida y Constituyentes."),
        ],
        "extra_text": "Al tener nuestro taller en Playa del Carmen, ofrecemos el tiempo de respuesta más rápido y el seguimiento más personalizado. Visita técnica disponible en 24 horas, instalación sin esperas innecesarias.",
        "price_text": "Para un proyecto en Playa del Carmen, una cocina a medida de tamaño medio comienza desde $45,000 MXN. El presupuesto es gratuito y se entrega en 48 horas tras la visita técnica.",
    },
    "cancun": {
        "name": "Cancún",
        "name_short": "Cancún",
        "region": "Riviera Maya Norte",
        "type": "primary",
        "lat": 21.1619,
        "lng": -86.8515,
        "h1": "Cocinas &amp; Vestidores<br><em>a Medida en Cancún</em>",
        "meta_title": "Cocinas a Medida Cancún | Ka'ax Creación — Riviera Maya",
        "meta_desc": "Carpintería de lujo a medida en Cancún. Cocinas integrales, vestidores y muebles fabricados en Playa del Carmen por artesanos formados en Francia. Presupuesto gratuito.",
        "lead": "Ka'ax Creación interviene en toda la zona de Cancún: desde las residencias de Cancún Centro hasta las villas exclusivas de la Zona Hotelera, pasando por los nuevos desarrollos residenciales de Puerto Cancún.",
        "intro": "Cancún concentra algunas de las residencias más exclusivas del Caribe mexicano. Las villas de la Zona Hotelera, los condominios premium de Puerto Cancún y las casas de Cancún Centro requieren una carpintería a la altura de su arquitectura. Ka'ax Creación responde a esta demanda con materiales europeos y un savoir-faire artesanal incomparable.",
        "specificites": [
            ("🏨", "Zona Hotelera", "Cocinas y vestidores de alta gama para las villas privadas y condominios de lujo de la Zona Hotelera de Cancún."),
            ("⛵", "Puerto Cancún", "Proyectos en los nuevos desarrollos residenciales premium de Puerto Cancún, con cocinas integradas y vestidores walk-in."),
            ("🏙️", "Cancún Centro", "Soluciones a medida para las residencias y negocios del centro de Cancún, con un equipo disponible en tiempos competitivos."),
            ("🏗️", "Proyectos en construcción", "Intervención en etapa de construcción para integrar la carpintería desde el diseño arquitectónico — la solución ideal para nuevas residencias."),
        ],
        "extra_text": "Desde nuestro taller de Playa del Carmen, llegamos a Cancún en menos de una hora. Ofrecemos el mismo nivel de exigencia artesanal y los mismos plazos de fabricación que para nuestros proyectos locales.",
        "price_text": "El costo de una cocina a medida en Cancún incluye el desplazamiento sin cargo adicional. Los proyectos en la Zona Hotelera comienzan desde $55,000 MXN según complejidad y dimensiones.",
    },
    "tulum": {
        "name": "Tulum",
        "name_short": "Tulum",
        "region": "Riviera Maya Sur",
        "type": "primary",
        "lat": 20.2114,
        "lng": -87.4654,
        "h1": "Cocinas &amp; Vestidores<br><em>a Medida en Tulum</em>",
        "meta_title": "Cocinas a Medida Tulum | Ka'ax Creación — Riviera Maya",
        "meta_desc": "Carpintería de lujo a medida en Tulum. Cocinas integrales, vestidores y muebles para villas de lujo. Artesanos formados en Francia. Materiales europeos premium.",
        "lead": "Tulum es el destino de lujo por excelencia de la Riviera Maya. Sus villas eco-chic, sus boutique hotels y sus residencias de alto standing exigen una carpintería excepcional. Ka'ax Creación fabrica e instala en Tulum con el mismo nivel de exigencia que en Playa del Carmen.",
        "intro": "Tulum representa un mercado único: clientes internacionales con altos estándares estéticos, proyectos arquitectónicos innovadores y una demanda constante de materiales nobles y acabados sofisticados. Ka'ax Creación trabaja con arquitectos e interioristas de Tulum para ofrecer soluciones de carpintería integradas en los proyectos más ambiciosos.",
        "specificites": [
            ("🌿", "Villas eco-luxury", "Cocinas en maderas naturales, vestidores con acabados orgánicos — adaptados a la estética eco-luxury que caracteriza las mejores villas de Tulum."),
            ("🏨", "Boutique hotels", "Muebles a medida para las habitaciones, restaurantes y zonas comunes de los boutique hotels de la Tulum Hotel Zone."),
            ("🌅", "Residencias de lujo", "Proyectos premium para las residencias privadas de los fraccionamientos Aldea Zama, La Veleta y otras zonas exclusivas de Tulum."),
            ("🤝", "Colaboración con arquitectos", "Trabajamos directamente con arquitectos e interioristas para integrar la carpintería desde la fase de diseño."),
        ],
        "extra_text": "Los materiales que utilizamos en Tulum están especialmente seleccionados para resistir la humedad característica de la selva maya: melamina antihumedad, herrajes inoxidables, selladores adaptados al entorno tropical.",
        "price_text": "Los proyectos en Tulum incluyen el desplazamiento sin cargo adicional. Para las villas de lujo y boutique hotels, ofrecemos un servicio premium con gestión de proyecto completa.",
    },
    "puerto-morelos": {
        "name": "Puerto Morelos",
        "name_short": "Puerto Morelos",
        "region": "Riviera Maya",
        "type": "primary",
        "lat": 20.8477,
        "lng": -86.8784,
        "h1": "Cocinas &amp; Vestidores<br><em>a Medida en Puerto Morelos</em>",
        "meta_title": "Cocinas a Medida Puerto Morelos | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Puerto Morelos. Cocinas integrales y vestidores para residencias y villas en la Riviera Maya. Artesanos formados en Francia.",
        "lead": "Puerto Morelos, joya discreta entre Cancún y Playa del Carmen, alberga algunas de las residencias más exclusivas de la Riviera Maya. Ka'ax Creación interviene en Puerto Morelos con el mismo estándar de exigencia artesanal que en su taller base de Playa del Carmen.",
        "intro": "El encanto de Puerto Morelos reside en su tranquilidad y su autenticidad. Las residencias de expats, las villas frente al mar y los nuevos condominios de lujo de esta pequeña localidad merecen una carpintería a la altura de su ambiente privilegiado.",
        "specificites": [
            ("🌊", "Villas frente al mar", "Cocinas y vestidores para las exclusivas villas con vista al mar de Puerto Morelos, con materiales resistentes a la sal marina."),
            ("🏡", "Residencias de expats", "Ka'ax Creación trabaja con la creciente comunidad internacional de Puerto Morelos — inglés, francés y español disponibles."),
            ("🏗️", "Nuevos desarrollos", "Intervención en los nuevos desarrollos residenciales entre Puerto Morelos y la carretera federal."),
            ("🌺", "Proyectos de reforma", "Renovación completa de cocinas y vestidores en residencias existentes — adaptación al espacio disponible con soluciones a medida."),
        ],
        "extra_text": "Puerto Morelos se encuentra a solo 20 minutos de nuestro taller de Playa del Carmen. Ofrecemos el tiempo de respuesta más rápido y una disponibilidad de visita técnica en 24 horas.",
        "price_text": "Para un proyecto en Puerto Morelos, el desplazamiento está incluido en el presupuesto. Una cocina a medida de tamaño medio comienza desde $45,000 MXN.",
    },
    "puerto-aventuras": {
        "name": "Puerto Aventuras",
        "name_short": "Puerto Aventuras",
        "region": "Riviera Maya",
        "type": "primary",
        "lat": 20.4799,
        "lng": -87.2374,
        "h1": "Cocinas &amp; Vestidores<br><em>a Medida en Puerto Aventuras</em>",
        "meta_title": "Cocinas a Medida Puerto Aventuras | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Puerto Aventuras. Cocinas integrales y vestidores para las exclusivas residencias de la marina privada. Artesanos formados en Francia.",
        "lead": "Puerto Aventuras es una comunidad privada con marina, golf y algunas de las residencias más exclusivas de la Riviera Maya. Ka'ax Creación fabrica e instala carpintería de lujo a la altura de este entorno privilegiado.",
        "intro": "El fraccionamiento privado de Puerto Aventuras alberga una selecta comunidad de residentes nacionales e internacionales. Las villas con vista a la marina, los condominios de alta gama y las residencias con acceso al campo de golf exigen una carpintería excepcional. Ka'ax Creación responde a este nivel de exigencia.",
        "specificites": [
            ("⛵", "Villas con vista a marina", "Cocinas y vestidores de lujo para las residencias con vista privilegiada a la marina privada de Puerto Aventuras."),
            ("🏌️", "Residencias con vista al golf", "Proyectos premium para las exclusivas casas con jardín y vista al campo de golf."),
            ("🏊", "Condominios de lujo", "Cocinas integrales y armarios para los condominios de alta gama dentro del fraccionamiento privado."),
            ("🌊", "Materiales resistentes al mar", "Selección especial de herrajes y acabados resistentes a la humedad y la sal marina del Caribe."),
        ],
        "extra_text": "Ka'ax Creación tiene experiencia trabajando en fraccionamientos privados cerrados. Coordinamos los permisos de acceso y adaptamos los horarios de trabajo a las reglas de la comunidad.",
        "price_text": "Los proyectos en Puerto Aventuras incluyen el desplazamiento sin recargo. Para las villas de alta gama de la marina, ofrecemos un servicio premium con gestión de proyecto completa.",
    },
    "coba-bacalar": {
        "name": "Cobá · Bacalar",
        "name_short": "Cobá y Bacalar",
        "region": "Interior de Quintana Roo",
        "type": "selectivo",
        "lat": 19.5929,
        "lng": -87.7167,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Cobá y Bacalar</em>",
        "meta_title": "Cocinas a Medida Cobá y Bacalar | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Cobá y Bacalar. Ka'ax Creación interviene en proyectos selectivos en el interior de Quintana Roo. Artesanos formados en Francia.",
        "lead": "Ka'ax Creación acepta proyectos selectivos en Cobá y Bacalar — dos destinos únicos del interior de Quintana Roo donde los proyectos de lujo y las ecolodges de alta gama demandan una carpintería excepcional.",
        "intro": "Bacalar, la «Laguna de los Siete Colores», y Cobá, con sus pirámides mayas rodeadas de selva, son destinos de un lujo tranquilo y auténtico. Los lodges de lujo, las casas de campo y las residencias privadas de estas zonas merecen una carpintería que respete la naturaleza del entorno y la exigencia de sus propietarios.",
        "specificites": [
            ("🏞️", "Ecolodges de lujo", "Cocinas y muebles para los exclusivos ecolodges de Bacalar y los alojamientos de lujo cerca de las ruinas de Cobá."),
            ("🌊", "Residencias junto a la laguna", "Proyectos en las exclusivas residencias con acceso directo a la Laguna de Bacalar."),
            ("🌿", "Materiales naturales", "Especial atención a los materiales naturales (madera maciza, bambu certificado) para armonizar con el entorno selvático."),
            ("🚐", "Proyectos de gran envergadura", "Para estas zonas alejadas, Ka'ax Creación acepta únicamente proyectos de tamaño significativo que justifiquen el desplazamiento."),
        ],
        "extra_text": "Para proyectos en Cobá y Bacalar, Ka'ax Creación evalúa caso por caso según la envergadura del proyecto. Contacte con nosotros para verificar disponibilidad.",
        "price_text": "El desplazamiento a Cobá y Bacalar puede conllevar un suplemento según la distancia y el proyecto. Contáctenos para obtener un presupuesto personalizado.",
    },
    "felipe-carrillo-puerto": {
        "name": "Felipe Carrillo Puerto",
        "name_short": "Felipe Carrillo Puerto",
        "region": "Sur de Quintana Roo",
        "type": "selectivo",
        "lat": 19.5812,
        "lng": -88.0453,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Felipe Carrillo Puerto</em>",
        "meta_title": "Cocinas a Medida Felipe Carrillo Puerto | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Felipe Carrillo Puerto. Ka'ax Creación interviene en proyectos selectivos en el sur de Quintana Roo.",
        "lead": "Ka'ax Creación acepta proyectos selectivos en Felipe Carrillo Puerto y el sur de Quintana Roo. Esta región, corazón histórico de la resistencia maya, es también hogar de residencias y proyectos que merecen una carpintería de calidad.",
        "intro": "Felipe Carrillo Puerto es el centro cultural y político del pueblo maya en Quintana Roo. La región está experimentando un desarrollo creciente, con nuevas residencias y proyectos comerciales que requieren carpintería de alta calidad. Ka'ax Creación lleva su savoir-faire europeo a esta zona para proyectos seleccionados.",
        "specificites": [
            ("🌳", "Proyectos residenciales", "Cocinas y vestidores a medida para las residencias familiares y propiedades de la región de Felipe Carrillo Puerto."),
            ("🏗️", "Proyectos en construcción", "Ka'ax Creación puede intervenir en etapa de construcción para integrar la carpintería desde el diseño."),
            ("🤝", "Proyectos comunitarios y comerciales", "Muebles a medida para locales comerciales, oficinas y espacios comunitarios de la región."),
        ],
        "extra_text": "Para proyectos en Felipe Carrillo Puerto, Ka'ax Creación evalúa cada solicitud individualmente. El desplazamiento puede conllevar un suplemento según la distancia.",
        "price_text": "Contáctenos para obtener un presupuesto personalizado que incluya el desplazamiento desde nuestro taller de Playa del Carmen.",
    },
    "isla-mujeres": {
        "name": "Isla Mujeres",
        "name_short": "Isla Mujeres",
        "region": "Islas del Caribe",
        "type": "isla",
        "lat": 21.2325,
        "lng": -86.7340,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Isla Mujeres</em>",
        "meta_title": "Cocinas a Medida Isla Mujeres | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Isla Mujeres. Cocinas integrales y vestidores para las exclusivas villas de la isla. Artesanos formados en Francia. Proyectos selectivos.",
        "lead": "Ka'ax Creación realiza proyectos selectivos en Isla Mujeres — la encantadora isla frente a Cancún, destino de un turismo de lujo exclusivo con villas privadas y boutique hotels de primer nivel.",
        "intro": "Isla Mujeres combina una autenticidad caribeña única con una creciente oferta de alojamientos y residencias de lujo. Las villas privadas en el norte de la isla, los boutique hotels de la costa y las residencias de expats demandan una carpintería de alta calidad que Ka'ax Creación puede proveer.",
        "specificites": [
            ("🏝️", "Villas privadas", "Cocinas y vestidores para las exclusivas villas privadas de la punta norte de Isla Mujeres."),
            ("🏨", "Boutique hotels", "Muebles a medida para los íntimos boutique hotels de la isla, con especial atención a los materiales resistentes al ambiente marino."),
            ("⛴️", "Logística isla", "Ka'ax Creación gestiona el transporte de materiales en ferry y coordina la logística de instalación específica de la isla."),
            ("🌊", "Materiales anti-sal", "Selección especial de herrajes inoxidables y acabados adaptados a la corrosión salina del entorno insular."),
        ],
        "extra_text": "Los proyectos en Isla Mujeres requieren una planificación logística específica. Ka'ax Creación gestiona el transporte de materiales y del equipo de instalación, con un suplemento reflejado en el presupuesto.",
        "price_text": "Para proyectos en Isla Mujeres, el presupuesto incluye el transporte en ferry y la logística insular. Contáctenos para una evaluación personalizada.",
    },
    "cozumel": {
        "name": "Cozumel",
        "name_short": "Cozumel",
        "region": "Islas del Caribe",
        "type": "isla",
        "lat": 20.4229,
        "lng": -86.9223,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Cozumel</em>",
        "meta_title": "Cocinas a Medida Cozumel | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Cozumel. Cocinas integrales y vestidores para las exclusivas residencias y hoteles de la isla. Materiales europeos, instalación incluida.",
        "lead": "Ka'ax Creación realiza proyectos selectivos en Cozumel — la mayor isla del Caribe mexicano, famosa por sus arrecifes de coral y sus residencias de lujo frente al mar.",
        "intro": "Cozumel es el paraíso del buceo y un destino de lujo para residentes internacionales. Las villas con vista al arrecife, las residencias de expatriados y los hoteles de lujo de la isla requieren una carpintería de alta calidad que soporte el ambiente marino extremo.",
        "specificites": [
            ("🤿", "Residencias de lujo", "Cocinas y vestidores para las exclusivas residencias privadas de Cozumel, con especial atención a los acabados resistentes al ambiente marino."),
            ("🏨", "Hoteles y resorts", "Muebles a medida para las habitaciones y zonas comunes de los hoteles de Cozumel."),
            ("⛴️", "Logística ferry", "Ka'ax Creación gestiona el transporte de materiales en ferry Playa del Carmen–Cozumel y la logística de instalación."),
            ("🛡️", "Materiales para clima marino", "Herrajes 316L marine-grade, MDF hidrófugo, lacas marinas — una selección rigurosa para el ambiente salino de Cozumel."),
        ],
        "extra_text": "El ambiente marino de Cozumel requiere materiales especialmente adaptados. Ka'ax Creación utiliza herrajes de acero inoxidable 316L marine-grade y acabados certificados para entornos costeros.",
        "price_text": "El presupuesto para Cozumel incluye el transporte en ferry y la logística de instalación. Contáctenos para una evaluación personalizada de su proyecto.",
    },
    "merida": {
        "name": "Mérida",
        "name_short": "Mérida",
        "region": "Yucatán",
        "type": "selectivo",
        "lat": 20.9674,
        "lng": -89.5926,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Mérida</em>",
        "meta_title": "Cocinas a Medida Mérida Yucatán | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Mérida, Yucatán. Cocinas integrales, vestidores y muebles para las residencias de las mejores colonias de la Ciudad Blanca.",
        "lead": "Ka'ax Creación realiza proyectos selectivos en Mérida, la «Ciudad Blanca» de Yucatán. Capital cultural y gastronómica del sureste mexicano, Mérida alberga algunas de las residencias más hermosas del país.",
        "intro": "Mérida es una ciudad de contrastes fascinantes: el patrimonio colonial de sus casonas del Centro Histórico convive con las modernas villas del norte. Ka'ax Creación interviene en las colonias Norte de Mérida — Altabrisa, Montebello, Temozón Norte — para proyectos de alta gama que requieren un nivel de acabado europeo.",
        "specificites": [
            ("🏛️", "Casonas coloniales", "Restauración y modernización de cocinas en las históricas casonas del Centro de Mérida — respeto del patrimonio con funcionalidad contemporánea."),
            ("🏡", "Villas Norte", "Cocinas y vestidores de lujo para las modernas residencias del norte de Mérida: Altabrisa, Montebello, Temozón Norte."),
            ("🌺", "Proyectos de lujo", "Ka'ax Creación acepta únicamente proyectos de alto standing en Mérida, donde la calidad de los materiales y el savoir-faire artesanal justifican el desplazamiento."),
            ("🤝", "Colaboración con arquitectos de Mérida", "Trabajamos con los principales arquitectos e interioristas de Mérida para proyectos integrados desde el diseño."),
        ],
        "extra_text": "Mérida se encuentra a aproximadamente 3 horas de nuestro taller de Playa del Carmen. Ka'ax Creación acepta proyectos en Mérida de tamaño significativo (cocinas y vestidores de alta gama), con un equipo que se instala durante los días de instalación.",
        "price_text": "Para proyectos en Mérida, el desplazamiento y la logística están incluidos en el presupuesto. Contacte con nosotros para verificar disponibilidad.",
    },
    "holbox": {
        "name": "Holbox",
        "name_short": "Holbox",
        "region": "Norte de Yucatán",
        "type": "selectivo",
        "lat": 21.5248,
        "lng": -87.3756,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Holbox</em>",
        "meta_title": "Cocinas a Medida Holbox | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Holbox. Cocinas y muebles para los exclusivos hoteles y villas de la isla sin coches del norte de Yucatán.",
        "lead": "Ka'ax Creación acepta proyectos exclusivos en Holbox — la isla sin coches del norte de Yucatán, paraíso de un turismo de lujo íntimo y consciente. Sus boutique hotels de lujo y villas privadas merecen una carpintería excepcional.",
        "intro": "Holbox es una de las islas más exclusivas del Caribe mexicano: sin coches, sin masificación, con un ecosistema único de manglares y una laguna de aguas turquesas. Los hoteles boutique de Holbox — Villas HM Paraíso del Mar, Casa Blanca, Las Nubes y otros — representan la cima del lujo tranquilo en México.",
        "specificites": [
            ("🦩", "Boutique hotels de lujo", "Muebles y cocinas para los exclusivos boutique hotels de Holbox, con materiales naturales adaptados al ecosistema de la isla."),
            ("🏡", "Villas privadas", "Proyectos residenciales para las villas privadas de propietarios nacionales e internacionales en Holbox."),
            ("🌿", "Materiales naturales", "Especial atención a la madera maciza certificada, el bambú y otros materiales naturales que respetan la filosofía eco de la isla."),
            ("⛴️", "Logística insular", "Ka'ax Creación gestiona el transporte en ferry y la logística de instalación sin vehículos motorizados en la isla."),
        ],
        "extra_text": "Holbox requiere una logística especial: sin carreteras en la isla, todos los materiales se transportan en ferry y se mueven en carritos de golf. Ka'ax Creación tiene experiencia con este tipo de proyecto insular.",
        "price_text": "Los proyectos en Holbox son necesariamente de alto standing para justificar la complejidad logística. Contacte con nosotros para una evaluación personalizada.",
    },
    "valladolid": {
        "name": "Valladolid",
        "name_short": "Valladolid",
        "region": "Corazón de Yucatán",
        "type": "selectivo",
        "lat": 20.6895,
        "lng": -88.2024,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Valladolid</em>",
        "meta_title": "Cocinas a Medida Valladolid Yucatán | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Valladolid, Yucatán. Cocinas integrales y muebles para las residencias y hoteles de la ciudad colonial. Proyectos selectivos.",
        "lead": "Ka'ax Creación acepta proyectos selectivos en Valladolid — la hermosa ciudad colonial de Yucatán, famosa por sus cenotes y su creciente turismo de lujo. Una ciudad que merece una carpintería a la altura de su patrimonio.",
        "intro": "Valladolid está experimentando un renacimiento turístico notable. Sus antiguas casonas coloniales se convierten en boutique hotels de lujo, y las nuevas residencias de expats y propietarios yucatecos que buscan una calidad de vida excepcional requieren una carpintería de alta gama.",
        "specificites": [
            ("🌺", "Boutique hotels coloniales", "Restauración y modernización de cocinas en los históricos palacios coloniales convertidos en boutique hotels de lujo."),
            ("🏡", "Residencias de expats", "Cocinas y vestidores para los propietarios internacionales que eligen Valladolid por su calidad de vida y autenticidad."),
            ("💧", "Proyectos eco cerca de cenotes", "Ka'ax Creación trabaja con materiales certificados para proyectos near-cenote, respetando el ecosistema acuático único de la región."),
        ],
        "extra_text": "Valladolid se encuentra aproximadamente a 2.5 horas de nuestro taller de Playa del Carmen, en la carretera Mérida–Cancún. Ka'ax Creación acepta proyectos selectivos de alto standing en esta ciudad.",
        "price_text": "El desplazamiento a Valladolid está incluido en el presupuesto para proyectos de envergadura. Contáctenos para verificar disponibilidad.",
    },
    "tizimin": {
        "name": "Tizimín",
        "name_short": "Tizimín",
        "region": "Norte de Yucatán",
        "type": "selectivo",
        "lat": 21.1428,
        "lng": -88.1623,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Tizimín</em>",
        "meta_title": "Cocinas a Medida Tizimín Yucatán | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Tizimín, norte de Yucatán. Ka'ax Creación acepta proyectos selectivos en la región ganadera de Yucatán.",
        "lead": "Ka'ax Creación acepta proyectos selectivos en Tizimín y la región norte de Yucatán — una zona de haciendas históricas y residencias rurales de alto standing que merecen una carpintería de calidad europea.",
        "intro": "Tizimín es el corazón de la región ganadera de Yucatán, conocida por sus haciendas henequeneras y sus tradiciones artesanales. Las haciendas reconvertidas en residencias de lujo, los proyectos rurales de alto standing y las residencias familiares de la élite regional son el mercado de Ka'ax Creación en esta zona.",
        "specificites": [
            ("🏚️", "Haciendas de lujo", "Restauración y modernización de cocinas en las haciendas históricas de la región de Tizimín."),
            ("🌾", "Residencias rurales premium", "Proyectos en las exclusivas residencias rurales de los alrededores de Tizimín."),
            ("🤝", "Proyectos evaluados caso por caso", "Ka'ax Creación evalúa individualmente cada solicitud para Tizimín según la envergadura y la viabilidad logística."),
        ],
        "extra_text": "La región de Tizimín se encuentra a aproximadamente 3 horas de nuestro taller. Ka'ax Creación acepta proyectos de alto standing con una planificación logística adecuada.",
        "price_text": "Para proyectos en Tizimín, contáctenos para una evaluación de viabilidad y un presupuesto personalizado.",
    },
    "campeche": {
        "name": "Campeche",
        "name_short": "Campeche",
        "region": "Estado de Campeche",
        "type": "selectivo",
        "lat": 19.8301,
        "lng": -90.5349,
        "h1": "Cocinas &amp; Vestidores a Medida<br><em>en Campeche</em>",
        "meta_title": "Cocinas a Medida Campeche | Ka'ax Creación",
        "meta_desc": "Carpintería de lujo a medida en Campeche. Cocinas integrales y muebles para las residencias de la ciudad amurallada Patrimonio UNESCO. Proyectos selectivos.",
        "lead": "Ka'ax Creación acepta proyectos selectivos en Campeche — la joya colonial del Golfo de México, Patrimonio de la Humanidad UNESCO, donde las casonas históricas y los nuevos proyectos de lujo requieren una carpintería excepcional.",
        "intro": "Campeche es una de las ciudades coloniales mejor conservadas de México. Sus coloridas casas del Centro Histórico Amurallado, declarado Patrimonio de la Humanidad UNESCO, se convierten cada vez más en boutique hotels de lujo y residencias de alto standing. Ka'ax Creación puede proveer la carpintería a la altura de este patrimonio excepcional.",
        "specificites": [
            ("🏰", "Centro Histórico UNESCO", "Restauración y modernización de cocinas en las casonas coloniales del Centro Histórico Amurallado de Campeche."),
            ("🏨", "Boutique hotels de lujo", "Muebles a medida para los boutique hotels que convierten las mansiones coloniales en experiencias de lujo únicas."),
            ("🌊", "Residencias frente al Malecón", "Proyectos en las exclusivas residencias con vista al Golfo de México y el Malecón de Campeche."),
            ("🤝", "Proyectos de gran envergadura", "Ka'ax Creación acepta únicamente proyectos de tamaño significativo para la distancia con Playa del Carmen."),
        ],
        "extra_text": "Campeche se encuentra a aproximadamente 4 horas de nuestro taller. Ka'ax Creación acepta proyectos de alto standing con una planificación de desplazamiento de varios días.",
        "price_text": "Para proyectos en Campeche, el presupuesto incluye el desplazamiento del equipo y la logística. Contáctenos para una evaluación personalizada.",
    },
}


def page_zone(slug, data):
    """Génère une page zone avec le LocalBusiness JSON-LD."""

    name = data["name"]
    region = data["region"]
    zone_type = data["type"]
    name_short = data.get("name_short", name)

    # Schema LocalBusiness
    schema = f"""{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "HomeAndConstructionBusiness",
      "@id": "https://kaaxcreacion.com/#business",
      "name": "Ka'ax Creación",
      "url": "https://kaaxcreacion.com",
      "telephone": "+529843121942",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Playa del Carmen",
        "addressLocality": "Playa del Carmen",
        "addressRegion": "Quintana Roo",
        "addressCountry": "MX"
      }},
      "geo": {{
        "@type": "GeoCoordinates",
        "latitude": 20.6296,
        "longitude": -87.0739
      }},
      "areaServed": {{
        "@type": "City",
        "name": "{name}",
        "containedInPlace": {{
          "@type": "State",
          "name": "{region}"
        }}
      }}
    }},
    {{
      "@type": "WebPage",
      "@id": "https://kaaxcreacion.com/zona/{slug}/#page",
      "url": "https://kaaxcreacion.com/zona/{slug}/",
      "name": "Cocinas y vestidores a medida en {name} — Ka'ax Creación",
      "description": "{data['meta_desc']}",
      "breadcrumb": {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://kaaxcreacion.com/"}},
          {{"@type": "ListItem", "position": 2, "name": "Zonas", "item": "https://kaaxcreacion.com/zona/"}},
          {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "https://kaaxcreacion.com/zona/{slug}/"}}
        ]
      }}
    }}
  ]
}}"""

    # Breadcrumb
    crumb = breadcrumb(
        [("Zonas", "../../zona/"), (name, "")],
        "../../"
    )

    # Badge zone
    if zone_type == "primary":
        badge = f'<span style="background:var(--or);color:var(--noir);font-size:10px;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;font-weight:500">Zone principale</span>'
    elif zone_type == "isla":
        badge = f'<span style="background:rgba(201,168,76,.2);color:var(--or);font-size:10px;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border:1px solid rgba(201,168,76,.4)">Isla — Proyectos selectivos</span>'
    else:
        badge = f'<span style="background:rgba(201,168,76,.2);color:var(--or);font-size:10px;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border:1px solid rgba(201,168,76,.4)">Proyectos selectivos</span>'

    # Features
    features_html = ""
    for icon, title, desc in data["specificites"]:
        features_html += f"""<div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <h3>{title}</h3>
        <p>{desc}</p>
      </div>
      """

    content = f"""
<div class="page-hero reveal">
  <p class="page-eyebrow">{region} — Ka'ax Creación</p>
  {badge}
  <h1 style="margin-top:16px">{data['h1']}</h1>
  <p class="lead">{data['lead']}</p>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <a href="https://wa.me/{WA}?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20para%20un%20proyecto%20en%20{name.replace(' ', '%20')}." class="btn-wa" target="_blank" rel="noopener">💬 Presupuesto gratuito</a>
    <a href="../../realizaciones/" class="btn-secondary">Ver realizaciones</a>
  </div>
</div>

<div style="background:rgba(201,168,76,.08);border-top:1px solid rgba(201,168,76,.2);border-bottom:1px solid rgba(201,168,76,.2);padding:40px 60px">
  <div style="max-width:1300px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:40px;text-align:center">
    <div><div style="font-family:'Cormorant Garamond',serif;font-size:40px;font-weight:300;color:var(--or);margin-bottom:8px">100%</div><div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6">Fabricación local</div></div>
    <div><div style="font-family:'Cormorant Garamond',serif;font-size:40px;font-weight:300;color:var(--or);margin-bottom:8px">✓</div><div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6">Desplazamiento incluido</div></div>
    <div><div style="font-family:'Cormorant Garamond',serif;font-size:40px;font-weight:300;color:var(--or);margin-bottom:8px">5</div><div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.6">Años de garantía</div></div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <div class="content-grid">
    <div>
      <h2>Ka'ax Creación<br><em>en {name}</em></h2>
      <p style="font-size:15px;line-height:1.9;opacity:.75">{data['intro']}</p>
      <p style="font-size:15px;line-height:1.9;opacity:.75;margin-top:16px">{data['extra_text']}</p>
      <div style="margin-top:32px;padding:24px;border:1px solid rgba(201,168,76,.3);background:rgba(201,168,76,.04)">
        <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--or);margin-bottom:12px">Presupuesto</div>
        <p style="font-size:14px;opacity:.75;line-height:1.8;margin:0">{data['price_text']}</p>
      </div>
    </div>
    <div>
      <h2>Nuestros servicios<br><em>en {name_short}</em></h2>
      <div style="display:flex;flex-direction:column;gap:12px;margin-top:8px">
        <a href="../../cocinas-a-medida/" class="zone-card">
          <span class="zone-card-icon">🍳</span>
          <div><div class="zone-card-name">Cocinas a medida</div><div class="zone-card-sub">Diseño integral · Melamina europea</div></div>
          <span class="zone-card-arrow">→</span>
        </a>
        <a href="../../closets-y-vestidores/" class="zone-card">
          <span class="zone-card-icon">👗</span>
          <div><div class="zone-card-name">Closets y vestidores</div><div class="zone-card-sub">Walk-in closet · Dressing room</div></div>
          <span class="zone-card-arrow">→</span>
        </a>
        <a href="../../realizaciones/" class="zone-card">
          <span class="zone-card-icon">🖼️</span>
          <div><div class="zone-card-name">Ver realizaciones</div><div class="zone-card-sub">Portfolio de proyectos en la Riviera Maya</div></div>
          <span class="zone-card-arrow">→</span>
        </a>
        <a href="../../metodo/" class="zone-card">
          <span class="zone-card-icon">⚙️</span>
          <div><div class="zone-card-name">Nuestro método</div><div class="zone-card-sub">Del diseño a la instalación</div></div>
          <span class="zone-card-arrow">→</span>
        </a>
      </div>
    </div>
  </div>
</div>

<div style="background:var(--gris-clair);padding:80px 60px">
  <div style="max-width:1300px;margin:0 auto">
    <div class="gold-divider"></div>
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,42px);font-weight:300;margin-bottom:48px">En {name}<br><em style="font-style:italic;color:#E8C97A">trabajamos en...</em></h2>
    <div class="content-grid-3">
      {features_html}
    </div>
  </div>
</div>

<div class="content-section reveal">
  <div class="gold-divider"></div>
  <h2>¿Por qué elegir<br><em>Ka'ax Creación en {name}?</em></h2>
  <div class="content-grid">
    <div>
      <h3>Artesanos formados en Francia</h3>
      <p style="font-size:15px;line-height:1.9;opacity:.75">Ka'ax Creación fue fundada por Raphaël, Major de Promoción 2023 de los <strong style="color:#C9A84C">Compagnons du Tour de France</strong> — la orden artesanal más exigente del mundo. Este nivel de formación se traduce en un resultado que ninguna empresa de serie puede igualar.</p>
      <h3>Materiales europeos de alta gama</h3>
      <p style="font-size:15px;line-height:1.9;opacity:.75">Melamina europea certificada, herrajes Blum y Hettich, aluminio anodizado de precisión. Materiales seleccionados para durar 20 años en el clima tropical de {region}.</p>
    </div>
    <div>
      <h3>Proceso transparente</h3>
      <p style="font-size:15px;line-height:1.9;opacity:.75">Presupuesto detallado línea por línea. Plazos respetados. Sin extras no previstos. La confianza del cliente es nuestra prioridad absoluta.</p>
      <h3>Garantía 5 años</h3>
      <p style="font-size:15px;line-height:1.9;opacity:.75">Todos nuestros trabajos están garantizados 5 años: materiales y mano de obra. En caso de problema, intervenimos en un plazo máximo de 72 horas.</p>
      <div style="margin-top:24px">
        <a href="https://wa.me/{WA}?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20en%20{name.replace(' ', '%20')}." class="btn-wa" target="_blank" rel="noopener">💬 Contactar ahora</a>
      </div>
    </div>
  </div>
</div>

<div class="cta-section">
  <div class="cta-section-content">
    <h2>Su proyecto en<br><em>{name}</em></h2>
    <p>Presupuesto gratuito · Desplazamiento incluido · Sin compromiso</p>
    <div class="cta-buttons">
      <a href="https://wa.me/{WA}?text=Hola%20Ka%27ax%20Creaci%C3%B3n%2C%20me%20gustar%C3%ADa%20un%20presupuesto%20para%20un%20proyecto%20en%20{name.replace(' ', '%20')}." class="btn-wa" target="_blank" rel="noopener">💬 Contactar por WhatsApp</a>
      <a href="../../contacto/" class="btn-secondary">Formulario de contacto</a>
    </div>
  </div>
</div>
"""

    return build_page(
        title=data["meta_title"],
        description=data["meta_desc"],
        canonical=f"{DOMAIN}/zona/{slug}/",
        breadcrumbs=crumb,
        content=content,
        root_prefix="../../",
        active_page="zona/",
        schema_ld=schema,
        image_prefix="../../"
    )


# ═══════════════════════════════════════════════════════════════
# SITEMAP
# ═══════════════════════════════════════════════════════════════

def generate_sitemap():
    urls = [
        (f"{DOMAIN}/", "1.0", "weekly"),
        (f"{DOMAIN}/cocinas-a-medida/", "0.9", "monthly"),
        (f"{DOMAIN}/closets-y-vestidores/", "0.9", "monthly"),
        (f"{DOMAIN}/realizaciones/", "0.8", "monthly"),
        (f"{DOMAIN}/metodo/", "0.8", "monthly"),
        (f"{DOMAIN}/zona/", "0.8", "weekly"),
        (f"{DOMAIN}/nosotros/", "0.7", "monthly"),
        (f"{DOMAIN}/contacto/", "0.7", "monthly"),
    ]
    for slug in ZONE_DATA.keys():
        urls.append((f"{DOMAIN}/zona/{slug}/", "0.8", "monthly"))

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, priority, freq in urls:
        xml += f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-11-27</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""
    xml += '</urlset>'
    return xml


# ═══════════════════════════════════════════════════════════════
# GENERATION
# ═══════════════════════════════════════════════════════════════

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def main():
    base = "/home/claude/kaax-creation"

    print("⚡ Génération du site Ka'ax Creación — toutes pages ES")

    # Pages service
    service_pages = [
        ("cocinas-a-medida", page_cocinas),
        ("closets-y-vestidores", page_closets),
        ("realizaciones", page_realizaciones),
        ("metodo", page_metodo),
        ("nosotros", page_nosotros),
        ("contacto", page_contacto),
        ("zona", page_zona_index),
    ]

    for slug, func in service_pages:
        path = f"{base}/{slug}"
        ensure_dir(path)
        html = func()
        with open(f"{path}/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ /{slug}/index.html")

    # Pages zone
    ensure_dir(f"{base}/zona")
    for slug, data in ZONE_DATA.items():
        path = f"{base}/zona/{slug}"
        ensure_dir(path)
        html = page_zone(slug, data)
        with open(f"{path}/index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✅ /zona/{slug}/index.html")

    # Sitemap
    sitemap = generate_sitemap()
    with open(f"{base}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("  ✅ sitemap.xml")

    print(f"\n✅ {len(service_pages) + len(ZONE_DATA)} pages générées + sitemap")
    print(f"   Service pages: {len(service_pages)}")
    print(f"   Zone pages: {len(ZONE_DATA)}")

if __name__ == "__main__":
    main()

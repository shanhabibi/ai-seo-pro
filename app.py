"""
AI Business Toolkit Pro
A professional Streamlit app with 5 AI-powered business tools.
Uses DeepSeek API (OpenAI-compatible) for all AI features.
"""

import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Toolkit Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  –  Glassmorphism + 3D inputs
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root tokens ─────────────────────────── */
:root {
  --bg-start:   #0a0a1a;
  --bg-mid:     #0d1130;
  --bg-end:     #050510;
  --glass-bg:   rgba(255,255,255,0.05);
  --glass-bdr:  rgba(255,255,255,0.12);
  --accent-1:   #7c3aed;
  --accent-2:   #06b6d4;
  --accent-3:   #f59e0b;
  --text-main:  #f0f0ff;
  --text-dim:   rgba(240,240,255,0.55);
  --radius-lg:  18px;
  --radius-md:  12px;
  --shadow-glow: 0 0 40px rgba(124,58,237,0.25);
}

/* ── Full-page gradient background ──────── */
html, body, [data-testid="stAppViewContainer"] {
  background: linear-gradient(135deg, var(--bg-start) 0%, var(--bg-mid) 50%, var(--bg-end) 100%) !important;
  background-attachment: fixed !important;
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text-main) !important;
}

/* subtle animated mesh overlay */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 10%, rgba(124,58,237,0.18) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%, rgba(6,182,212,0.12) 0%, transparent 55%);
  pointer-events: none;
  z-index: 0;
}

/* ── Remove default Streamlit chrome ────── */
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

/* ── Main content z-index ────────────────  */
[data-testid="stMain"] { position: relative; z-index: 1; }

/* ── Sidebar glass panel ─────────────────  */
[data-testid="stSidebar"] {
  background: rgba(10,10,30,0.75) !important;
  backdrop-filter: blur(24px) !important;
  border-right: 1px solid var(--glass-bdr) !important;
}
[data-testid="stSidebar"] * { color: var(--text-main) !important; }

/* ── Hero header ─────────────────────────  */
.hero-header {
  text-align: center;
  padding: 2.5rem 1rem 1rem;
  position: relative;
}
.hero-header h1 {
  font-family: 'Syne', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 5vw, 3.4rem);
  background: linear-gradient(90deg, #a78bfa, #06b6d4, #f59e0b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  letter-spacing: -1px;
}
.hero-header p {
  color: var(--text-dim);
  font-size: 1.05rem;
  margin-top: 0.5rem;
}

/* ── Glass card ──────────────────────────  */
.glass-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-bdr);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-lg);
  padding: 2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35), var(--shadow-glow);
  transition: box-shadow 0.3s ease;
}
.glass-card:hover {
  box-shadow: 0 12px 48px rgba(0,0,0,0.45), 0 0 60px rgba(124,58,237,0.35);
}

/* ── Section label ───────────────────────  */
.section-label {
  font-family: 'Syne', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--accent-2);
  margin-bottom: 0.35rem;
}
.section-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0 0 1.2rem;
}

/* ── 3-D input fields ────────────────────  */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea,
div[data-baseweb="base-input"] input {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  border-radius: var(--radius-md) !important;
  color: #ffffff !important;
  box-shadow: inset 0 2px 8px rgba(0,0,0,0.4) !important;
  font-family: 'DM Sans', sans-serif !important;
  transition: border-color 0.25s, box-shadow 0.25s !important;
  padding: 0.75rem 1rem !important;
}
div[data-baseweb="input"] input:focus,
div[data-baseweb="textarea"] textarea:focus {
  border-color: var(--accent-1) !important;
  box-shadow: inset 0 2px 8px rgba(0,0,0,0.4), 0 0 0 3px rgba(124,58,237,0.3) !important;
  outline: none !important;
}
/* label text */
label[data-testid="stWidgetLabel"] p { color: var(--text-dim) !important; font-size: 0.88rem !important; }

/* ── Gradient CTA button ─────────────────  */
div.stButton > button {
  background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 50px !important;
  padding: 0.65rem 2rem !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  letter-spacing: 0.5px !important;
  box-shadow: 0 4px 20px rgba(124,58,237,0.45) !important;
  transition: transform 0.18s ease, box-shadow 0.18s ease !important;
  cursor: pointer !important;
}
div.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(124,58,237,0.65) !important;
}
div.stButton > button:active { transform: translateY(0) !important; }

/* ── Tab pills ───────────────────────────  */
div[data-testid="stTabs"] > div:first-child {
  gap: 0.4rem !important;
  border-bottom: none !important;
  flex-wrap: wrap;
  padding-bottom: 0.5rem;
}
div[data-testid="stTabs"] button[role="tab"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 50px !important;
  color: var(--text-dim) !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
  padding: 0.45rem 1.2rem !important;
  transition: all 0.2s ease !important;
}
div[data-testid="stTabs"] button[role="tab"]:hover {
  background: rgba(124,58,237,0.2) !important;
  color: var(--text-main) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  background: linear-gradient(135deg, var(--accent-1), var(--accent-2)) !important;
  color: #ffffff !important;
  border-color: transparent !important;
  box-shadow: 0 4px 16px rgba(124,58,237,0.4) !important;
}
/* hide default blue underline */
div[data-testid="stTabs"] button[role="tab"] div[data-testid="stMarkdownContainer"] { display:none; }

/* ── Result containers ───────────────────  */
.result-box {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  margin-top: 1rem;
}
.result-box h3 {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  color: var(--accent-2);
  margin-top: 0;
}

/* ── Score badge ─────────────────────────  */
.score-badge {
  display: inline-block;
  font-family: 'Syne', sans-serif;
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── Spinner color override ──────────────  */
div[data-testid="stSpinner"] > div { border-top-color: var(--accent-1) !important; }

/* ── Markdown output colour ──────────────  */
[data-testid="stMarkdownContainer"] { color: var(--text-main) !important; }
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
  font-family: 'Syne', sans-serif !important;
  color: var(--accent-2) !important;
}
[data-testid="stMarkdownContainer"] code {
  background: rgba(124,58,237,0.2) !important;
  border-radius: 4px !important;
  color: #c4b5fd !important;
}
[data-testid="stMarkdownContainer"] pre code {
  background: transparent !important;
}
[data-testid="stMarkdownContainer"] pre {
  background: rgba(0,0,0,0.35) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
}

/* ── Divider ─────────────────────────────  */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ── Sidebar tool chips ──────────────────  */
.tool-chip {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.4rem;
  font-size: 0.82rem;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ── Mobile responsive ───────────────────  */
@media (max-width: 768px) {
  .hero-header h1 { font-size: 1.7rem; }
  .glass-card { padding: 1.2rem; }
  div[data-testid="stTabs"] button[role="tab"] { font-size: 0.72rem; padding: 0.35rem 0.8rem !important; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_client(api_key: str) -> OpenAI:
    """Return a DeepSeek-compatible OpenAI client."""
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
    )


def call_ai(api_key: str, system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> str:
    """Call DeepSeek API and return the assistant message as a string."""
    try:
        client = get_client(api_key)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ **API Error:** {str(e)}\n\nPlease check your API key and try again."


def scrape_url(url: str) -> str:
    """Scrape visible text and meta tags from a URL. Returns a compact string."""
    try:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        headers = {"User-Agent": "Mozilla/5.0 (compatible; AIToolkitBot/1.0)"}
        resp = requests.get(url, headers=headers, timeout=12)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Meta info
        title       = soup.title.string.strip() if soup.title else "N/A"
        description = ""
        keywords    = ""
        for tag in soup.find_all("meta"):
            if tag.get("name", "").lower() == "description":
                description = tag.get("content", "")
            if tag.get("name", "").lower() == "keywords":
                keywords = tag.get("content", "")

        # Body text (first 1500 chars)
        for s in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            s.decompose()
        body_text = " ".join(soup.get_text(separator=" ").split())[:1500]

        return (
            f"URL: {url}\n"
            f"Title: {title}\n"
            f"Meta Description: {description}\n"
            f"Meta Keywords: {keywords}\n"
            f"Body Excerpt: {body_text}"
        )
    except Exception as e:
        return f"Could not scrape URL ({e}). Please analyse based on the URL alone."


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
      <span style='font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800;
        background:linear-gradient(90deg,#a78bfa,#06b6d4);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text;'>⚡ AI Toolkit Pro</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='font-size:0.75rem; color:rgba(240,240,255,0.5); text-transform:uppercase; letter-spacing:2px;'>API Configuration</p>", unsafe_allow_html=True)

    api_key_input = st.text_input(
        "DeepSeek API Key",
        type="password",
        placeholder="sk-...",
        help="Your DeepSeek API key. Falls back to DEEPSEEK_API_KEY env var.",
    )
    # Resolve key: sidebar input → env var
    ACTIVE_KEY = api_key_input.strip() or os.getenv("DEEPSEEK_API_KEY", "")

    if ACTIVE_KEY:
        st.success("✅ API key loaded")
    else:
        st.warning("⚠️ Enter your DeepSeek API key")

    st.markdown("---")
    st.markdown("<p style='font-size:0.75rem; color:rgba(240,240,255,0.5); text-transform:uppercase; letter-spacing:2px; margin-bottom:0.75rem;'>Available Tools</p>", unsafe_allow_html=True)

    tools_info = [
        ("🔍", "SEO Strategist"),
        ("📧", "Cold Email Pro"),
        ("🛒", "Shopify Product Expert"),
        ("🏢", "B2B Lead Researcher"),
        ("🛠️", "AI Code Auditor"),
    ]
    for icon, name in tools_info:
        st.markdown(f"""
        <div class='tool-chip'>{icon} <span>{name}</span></div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <p style='font-size:0.72rem; color:rgba(240,240,255,0.35); text-align:center;'>
      Powered by DeepSeek AI<br>© 2025 AI Toolkit Pro
    </p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div class='hero-header'>
  <h1>⚡ AI Business Toolkit Pro</h1>
  <p>Five production-grade AI tools to supercharge your business — powered by DeepSeek</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GUARD: no key → show notice
# ─────────────────────────────────────────────

def api_key_guard() -> bool:
    if not ACTIVE_KEY:
        st.markdown("""
        <div class='glass-card' style='border-color:rgba(245,158,11,0.4); text-align:center; padding:2.5rem;'>
          <span style='font-size:2.5rem;'>🔑</span>
          <h3 style='font-family:Syne,sans-serif; margin:0.5rem 0;'>API Key Required</h3>
          <p style='color:rgba(240,240,255,0.55);'>Please enter your <b>DeepSeek API Key</b> in the sidebar to use this tool.</p>
        </div>
        """, unsafe_allow_html=True)
        return False
    return True


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 SEO Strategist",
    "📧 Cold Email Pro",
    "🛒 Shopify Expert",
    "🏢 B2B Lead Researcher",
    "🛠️ Code Auditor",
])


# ══════════════════════════════════════════════
# TAB 1 – SEO STRATEGIST
# ══════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class='glass-card'>
      <p class='section-label'>Tool 01</p>
      <h2 class='section-title'>🔍 SEO Strategist</h2>
      <p style='color:rgba(240,240,255,0.55); margin-bottom:0;'>
        Enter any website URL. The AI will analyse meta tags, suggest keywords,
        assign an SEO score (0–100) and deliver 3 content improvement tips.
      </p>
    </div>
    """, unsafe_allow_html=True)

    url_input = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        key="seo_url",
    )

    if st.button("⚡ Analyse SEO", key="seo_btn"):
        if not api_key_guard():
            pass
        elif not url_input.strip():
            st.error("Please enter a valid website URL.")
        else:
            with st.spinner("Scraping page and running SEO analysis…"):
                scraped = scrape_url(url_input.strip())

                system = (
                    "You are an expert SEO consultant. Analyse the provided website data "
                    "and respond ONLY in markdown. Structure your response with these exact sections:\n"
                    "## SEO Score\n"
                    "Provide a score from 0 to 100 as a large number with a brief justification.\n"
                    "## Keyword Recommendations\n"
                    "List 8–10 high-value keywords with search intent labels (informational/transactional/navigational).\n"
                    "## Meta Tag Analysis\n"
                    "Analyse existing title tag and meta description; flag issues.\n"
                    "## 3 Content Improvement Tips\n"
                    "Numbered list of 3 actionable, specific content tips."
                )
                user = f"Analyse this website for SEO:\n\n{scraped}"
                result = call_ai(ACTIVE_KEY, system, user, max_tokens=1400)

            st.markdown("""<div class='result-box'>""", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("""</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 – COLD EMAIL PRO
# ══════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class='glass-card'>
      <p class='section-label'>Tool 02</p>
      <h2 class='section-title'>📧 Cold Email Pro</h2>
      <p style='color:rgba(240,240,255,0.55); margin-bottom:0;'>
        Describe your business or offer. The AI generates 5 high-converting
        cold email templates — each with subject line, opening, value prop and CTA.
      </p>
    </div>
    """, unsafe_allow_html=True)

    biz_desc = st.text_area(
        "Business Description",
        placeholder="e.g. We are a SaaS company offering AI-powered customer support automation for e-commerce brands…",
        height=130,
        key="email_desc",
    )
    target_audience = st.text_input(
        "Target Audience (optional)",
        placeholder="e.g. E-commerce store owners, Shopify merchants",
        key="email_audience",
    )

    if st.button("⚡ Generate Cold Emails", key="email_btn"):
        if not api_key_guard():
            pass
        elif not biz_desc.strip():
            st.error("Please describe your business.")
        else:
            with st.spinner("Crafting 5 cold email templates…"):
                system = (
                    "You are a world-class B2B copywriter specialising in cold email outreach. "
                    "Generate 5 distinct cold email templates. Each must include:\n"
                    "- **Subject Line** (curiosity-driven or benefit-led)\n"
                    "- **Opening** (personalised first line)\n"
                    "- **Value Proposition** (2–3 sentences, pain-point focused)\n"
                    "- **CTA** (one clear, low-friction call to action)\n\n"
                    "Vary the tone across templates: Professional, Casual, Data-driven, Story-led, Pattern-interrupt.\n"
                    "Respond ONLY in markdown."
                )
                user = (
                    f"Business: {biz_desc.strip()}\n"
                    f"Target audience: {target_audience.strip() or 'General B2B decision-makers'}\n\n"
                    "Generate 5 cold email templates."
                )
                result = call_ai(ACTIVE_KEY, system, user, max_tokens=1800)

            st.markdown("""<div class='result-box'>""", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("""</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 3 – SHOPIFY PRODUCT EXPERT
# ══════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class='glass-card'>
      <p class='section-label'>Tool 03</p>
      <h2 class='section-title'>🛒 Shopify Product Expert</h2>
      <p style='color:rgba(240,240,255,0.55); margin-bottom:0;'>
        Enter your product name and key features. Get 3 SEO-optimised titles,
        a compelling 150-word description with emojis, 5 image alt texts, and a meta description.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1], gap="medium")
    with col_a:
        product_name = st.text_input("Product Name", placeholder="e.g. Ergonomic Bamboo Standing Desk", key="shopify_name")
    with col_b:
        product_category = st.text_input("Category (optional)", placeholder="e.g. Home Office Furniture", key="shopify_cat")

    product_features = st.text_area(
        "Key Features (one per line or comma-separated)",
        placeholder="Adjustable height 70–120 cm\nSustainable bamboo surface\nCable management tray\nEasy assembly < 15 min",
        height=110,
        key="shopify_features",
    )

    if st.button("⚡ Generate Product Copy", key="shopify_btn"):
        if not api_key_guard():
            pass
        elif not product_name.strip():
            st.error("Please enter a product name.")
        else:
            with st.spinner("Writing Shopify-optimised product content…"):
                system = (
                    "You are a Shopify conversion-rate optimisation expert and e-commerce copywriter. "
                    "Respond ONLY in markdown with these exact sections:\n\n"
                    "## 3 SEO-Optimised Product Titles\n"
                    "Each title: 60–80 chars, keyword-rich, benefit-led.\n\n"
                    "## Product Description\n"
                    "Exactly 150 words. Use relevant emojis. Highlight benefits, not just features. "
                    "End with a compelling reason to buy now.\n\n"
                    "## 5 Image Alt Texts\n"
                    "Descriptive, keyword-rich, screen-reader friendly.\n\n"
                    "## Meta Description\n"
                    "150–160 characters. Include primary keyword and CTA."
                )
                user = (
                    f"Product: {product_name.strip()}\n"
                    f"Category: {product_category.strip() or 'General'}\n"
                    f"Features:\n{product_features.strip()}"
                )
                result = call_ai(ACTIVE_KEY, system, user, max_tokens=1400)

            st.markdown("""<div class='result-box'>""", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("""</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 – B2B LEAD RESEARCHER
# ══════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class='glass-card'>
      <p class='section-label'>Tool 04</p>
      <h2 class='section-title'>🏢 B2B Lead Researcher</h2>
      <p style='color:rgba(240,240,255,0.55); margin-bottom:0;'>
        Enter a company website URL. The AI scrapes basic information and provides a
        business summary, key decision-maker roles, likely pain points and a tailored outreach angle.
      </p>
    </div>
    """, unsafe_allow_html=True)

    company_url = st.text_input(
        "Company Website URL",
        placeholder="https://company.com",
        key="b2b_url",
    )
    your_offer = st.text_input(
        "Your Product/Service (optional — for targeted outreach angle)",
        placeholder="e.g. AI-powered CRM software",
        key="b2b_offer",
    )

    if st.button("⚡ Research Lead", key="b2b_btn"):
        if not api_key_guard():
            pass
        elif not company_url.strip():
            st.error("Please enter a company URL.")
        else:
            with st.spinner("Scraping company website and generating lead intelligence…"):
                scraped = scrape_url(company_url.strip())

                system = (
                    "You are a senior B2B sales intelligence analyst. Based on the website data provided, "
                    "deliver a structured lead research report in markdown with these sections:\n\n"
                    "## Company Summary\n"
                    "3–4 sentences: industry, size estimate, core product/service, apparent market position.\n\n"
                    "## Key Decision-Maker Roles\n"
                    "List 4–6 typical titles/roles that would be relevant buyers or influencers.\n\n"
                    "## Likely Business Needs & Pain Points\n"
                    "5 bullet points based on their industry and web presence.\n\n"
                    "## Tailored Outreach Angle\n"
                    "A specific, personalised outreach strategy (2–3 sentences) connecting their needs to the seller's offer.\n\n"
                    "## Suggested Opening Line\n"
                    "One compelling first-touch email opening sentence."
                )
                user = (
                    f"Website data:\n{scraped}\n\n"
                    f"Seller's offer: {your_offer.strip() or 'Not specified — provide general outreach angle.'}"
                )
                result = call_ai(ACTIVE_KEY, system, user, max_tokens=1400)

            st.markdown("""<div class='result-box'>""", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("""</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 5 – AI CODE AUDITOR
# ══════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div class='glass-card'>
      <p class='section-label'>Tool 05</p>
      <h2 class='section-title'>🛠️ AI Code Auditor</h2>
      <p style='color:rgba(240,240,255,0.55); margin-bottom:0;'>
        Paste your Python, HTML or JavaScript code. The AI identifies bugs,
        performance issues, security concerns, best-practice violations,
        and returns a refactored snippet.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_x, col_y = st.columns([2, 1], gap="medium")
    with col_x:
        code_input = st.text_area(
            "Paste Your Code",
            placeholder="# Paste Python, HTML, or JavaScript here…",
            height=260,
            key="code_input",
        )
    with col_y:
        lang = st.selectbox("Language", ["Auto-detect", "Python", "JavaScript", "HTML/CSS"], key="code_lang")
        focus = st.multiselect(
            "Audit Focus",
            ["Bugs & Errors", "Performance", "Security", "Best Practices", "Readability"],
            default=["Bugs & Errors", "Performance", "Best Practices"],
            key="code_focus",
        )

    if st.button("⚡ Audit My Code", key="code_btn"):
        if not api_key_guard():
            pass
        elif not code_input.strip():
            st.error("Please paste some code to audit.")
        else:
            focus_str = ", ".join(focus) if focus else "all areas"
            with st.spinner("Auditing your code for issues and improvements…"):
                system = (
                    "You are a senior software engineer and code reviewer with 15 years of experience. "
                    "Perform a thorough code audit and respond ONLY in markdown with these sections:\n\n"
                    "## Overview\n"
                    "Brief assessment of code purpose and quality (2–3 sentences).\n\n"
                    "## 🐛 Bugs & Errors\n"
                    "List each bug with: line reference (if applicable), description, severity (Critical/High/Medium/Low).\n\n"
                    "## ⚡ Performance Issues\n"
                    "Specific bottlenecks or inefficiencies found.\n\n"
                    "## 🔒 Security Concerns\n"
                    "Any vulnerabilities or insecure patterns.\n\n"
                    "## ✅ Best Practice Violations\n"
                    "Coding standards, conventions, or patterns that should be improved.\n\n"
                    "## 🔧 Refactored Snippet\n"
                    "Provide an improved version of the most critical section as a fenced code block with comments explaining each fix."
                )
                user = (
                    f"Language: {lang}\n"
                    f"Audit focus: {focus_str}\n\n"
                    f"Code to audit:\n```\n{code_input.strip()}\n```"
                )
                result = call_ai(ACTIVE_KEY, system, user, max_tokens=2000)

            st.markdown("""<div class='result-box'>""", unsafe_allow_html=True)
            st.markdown(result)
            st.markdown("""</div>""", unsafe_allow_html=True)

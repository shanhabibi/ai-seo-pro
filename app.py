import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

# ---------- Page Config ----------
st.set_page_config(page_title="AI Business Toolkit", page_icon="⚡", layout="wide")

# ---------- Responsive Glassmorphism CSS ----------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    }
    /* Sidebar glass */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    /* Glass card */
    .glass-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(12px);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255,255,255,0.35);
    }
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border-radius: 40px !important;
        padding: 0.6rem 1.8rem !important;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(59,130,246,0.4);
    }
    /* Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 0.7rem 1rem;
    }
    /* Headers */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #f8fafc !important;
        font-weight: 600;
    }
    /* Tabs (responsive) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        color: #cbd5e1;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
    }
    /* Alerts */
    .stAlert {
        background: rgba(0,0,0,0.6);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        border-left: 4px solid;
    }
    /* Responsive text */
    @media (max-width: 768px) {
        .glass-card { padding: 1rem; }
        .stTabs [data-baseweb="tab"] { padding: 0.25rem 0.75rem; font-size: 0.8rem; }
        h1 { font-size: 1.8rem; }
    }
</style>
""", unsafe_allow_html=True)

# ---------- Helper Functions ----------
def call_ai(api_key: str, system: str, user: str) -> str:
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.7,
        max_tokens=2000
    )
    return resp.choices[0].message.content

def scrape_website(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, timeout=12, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        meta_desc = ""
        for m in soup.find_all("meta"):
            if m.get("name", "").lower() == "description":
                meta_desc = m.get("content", "")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ", strip=True)[:2000]
        return {"title": title, "description": meta_desc, "text": text, "url": url}
    except Exception as e:
        return {"error": str(e)}

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=70)
    st.markdown("## 🔐 API Key")
    api_key = st.text_input("DeepSeek API Key", type="password", value=os.environ.get("DEEPSEEK_API_KEY", ""))
    st.markdown("---")
    st.markdown("### 🛠️ Your Tools")
    st.info("1. SEO Strategist\n2. Cold Email Pro\n3. Shopify Expert\n4. B2B Lead Research\n5. Code Auditor")
    st.caption("© AI Business Toolkit | Glass UI")

# ---------- Header ----------
st.markdown('<div class="glass-card" style="text-align:center"><h1>⚡ AI Business Toolkit Pro</h1><p style="color:#94a3b8">5 professional AI tools – 100% working, mobile friendly</p></div>', unsafe_allow_html=True)

# ---------- Tabs ----------
t1, t2, t3, t4, t5 = st.tabs(["🔍 SEO Strategist", "✉️ Cold Email Pro", "🛍️ Shopify Expert", "🏢 Lead Researcher", "💻 Code Auditor"])

# ========== TOOL 1: SEO Strategist ==========
with t1:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        url_seo = st.text_input("Website URL", placeholder="https://example.com")
        if st.button("Run SEO Audit", key="seo"):
            if not api_key:
                st.error("❌ Enter DeepSeek API Key in sidebar")
            elif not url_seo:
                st.error("❌ Enter a URL")
            else:
                with st.spinner("Fetching website..."):
                    data = scrape_website(url_seo)
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        prompt = f"""Analyze this website for SEO:
URL: {data['url']}
Title: {data['title']}
Meta Description: {data['description']}
Content: {data['text'][:1500]}

Provide:
1. Meta Tags Analysis (title length, description quality)
2. Keyword Suggestions (5-7 keywords)
3. SEO Score (0-100)
4. 3 Content Improvement Tips
Format in markdown."""
                        with st.spinner("AI analyzing..."):
                            report = call_ai(api_key, "You are an SEO expert.", prompt)
                        st.markdown("### 📈 SEO Report")
                        st.markdown(report)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== TOOL 2: Cold Email Pro ==========
with t2:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        biz_desc = st.text_area("Business Description", height=120, placeholder="We sell eco-friendly yoga mats made from recycled rubber...")
        if st.button("Generate Email Templates", key="cold"):
            if not api_key:
                st.error("❌ API key missing")
            elif not biz_desc.strip():
                st.error("❌ Describe your business")
            else:
                prompt = f"""Business: {biz_desc}
Generate 5 cold email templates for B2B outreach. Each email must have:
- Subject line
- Personalized opening
- Value proposition
- Call to action
Number them 1-5. Use markdown."""
                with st.spinner("Writing emails..."):
                    emails = call_ai(api_key, "You are a B2B sales copywriter.", prompt)
                st.markdown("### ✉️ Email Templates")
                st.markdown(emails)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== TOOL 3: Shopify Product Expert ==========
with t3:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        prod_name = st.text_input("Product name")
        features = st.text_area("Key features", height=80, placeholder="Stainless steel, 500ml, leak-proof")
        if st.button("Generate Shopify Content", key="shopify"):
            if not api_key:
                st.error("❌ API key missing")
            elif not prod_name.strip():
                st.error("❌ Enter product name")
            else:
                prompt = f"""Product: {prod_name}
Features: {features}
Generate:
1. SEO Title (3 options)
2. Product Description (150 words, benefit-driven, with emojis)
3. Image Alt-text (5 variations)
4. Meta Description (max 160 chars)
Use markdown headings."""
                with st.spinner("Creating content..."):
                    content = call_ai(api_key, "You are an e‑commerce copywriter.", prompt)
                st.markdown("### 🛍️ Shopify Content")
                st.markdown(content)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== TOOL 4: B2B Lead Researcher ==========
with t4:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        company_url = st.text_input("Company Website URL", placeholder="https://company.com")
        if st.button("Research Company", key="lead"):
            if not api_key:
                st.error("❌ API key missing")
            elif not company_url:
                st.error("❌ Enter URL")
            else:
                with st.spinner("Scraping company data..."):
                    data = scrape_website(company_url)
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        prompt = f"""Company data:
URL: {data['url']}
Title: {data['title']}
Meta: {data['description']}
Text snippet: {data['text'][:1200]}

Provide a lead research report:
- Company summary (industry, size estimate)
- Potential decision-maker roles
- Services they might need
- Suggested outreach angle (1 paragraph)
Markdown format."""
                        with st.spinner("AI analyzing..."):
                            report = call_ai(api_key, "You are a B2B lead researcher.", prompt)
                        st.markdown("### 🏢 Lead Intelligence")
                        st.markdown(report)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== TOOL 5: AI Code Auditor ==========
with t5:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        code = st.text_area("Paste your code (HTML/CSS, Python, JS)", height=200)
        lang = st.selectbox("Language", ["Python", "HTML/CSS", "JavaScript"])
        if st.button("Audit Code", key="code"):
            if not api_key:
                st.error("❌ API key missing")
            elif not code.strip():
                st.error("❌ Paste some code")
            else:
                prompt = f"""Language: {lang}
Code:
{code[:3000]}

Provide a code audit:
- Bugs or errors found
- Performance improvements
- 3 best practice recommendations
- Refactored snippet (if any)
Markdown output."""
                with st.spinner("Reviewing code..."):
                    audit = call_ai(api_key, "You are a senior software engineer.", prompt)
                st.markdown("### 🧪 Code Audit Report")
                st.markdown(audit)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("Built with Streamlit + DeepSeek API | 100% Functional | Mobile Responsive")

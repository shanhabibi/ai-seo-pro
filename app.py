import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

# ---------- Page Config ----------
st.set_page_config(page_title="AI Business Toolkit Pro", page_icon="✨", layout="wide")

# ---------- Professional Glassmorphism CSS ----------
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background gradient */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0a0f1e, #030712);
    }
    
    /* Sidebar - semi-transparent glass */
    [data-testid="stSidebar"] {
        background: rgba(18, 25, 45, 0.75) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Glass card - elegant */
    .glass-card {
        background: rgba(22, 32, 52, 0.5);
        backdrop-filter: blur(12px);
        border-radius: 32px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 35px -12px rgba(0,0,0,0.3);
        padding: 1.8rem;
        margin-bottom: 1.8rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 40px -12px rgba(0,0,0,0.4);
    }
    
    /* Headers */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        font-weight: 600;
        background: linear-gradient(135deg, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Buttons - gradient with glow */
    .stButton > button {
        background: linear-gradient(105deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 48px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59,130,246,0.5);
    }
    
    /* Input fields */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 20px !important;
        color: #f1f5f9 !important;
        padding: 0.8rem 1.2rem !important;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.2);
    }
    
    /* Tabs - modern pill style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(0,0,0,0.2);
        border-radius: 60px;
        padding: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 40px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        color: #94a3b8;
        transition: all 0.2s;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        color: #cbd5e1;
    }
    
    /* Alerts */
    .stAlert {
        background: rgba(0,0,0,0.6);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        border-left: 4px solid;
    }
    
    /* Markdown text inside glass card */
    .report-text {
        color: #e2e8f0;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .report-text h4 {
        color: #facc15;
        margin-top: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.75rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .glass-card { padding: 1rem; }
        .stTabs [data-baseweb="tab"] { padding: 0.3rem 0.8rem; font-size: 0.7rem; }
        h1 { font-size: 1.8rem; }
        .stButton > button { font-size: 0.8rem; padding: 0.5rem 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ---------- Helper Functions ----------
def call_ai(api_key: str, system_prompt: str, user_prompt: str) -> str:
    if not api_key or not api_key.startswith("sk-"):
        return "⚠️ Invalid API key"
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

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
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=65)
    st.markdown("### 🔐 DeepSeek API")
    api_key = st.text_input("API Key", type="password", value=os.environ.get("DEEPSEEK_API_KEY", ""), placeholder="sk-...")
    st.markdown("---")
    st.markdown("### 🛠️ Toolkit")
    st.markdown("""✅ SEO Strategist  
✅ Cold Email Pro  
✅ Shopify Expert  
✅ Lead Researcher  
✅ Code Auditor""")
    st.markdown("---")
    st.caption("© 2025 AI Business Suite")

# ---------- Main Header ----------
st.markdown("""
<div style='text-align: center; margin-bottom: 1rem;'>
    <h1>✨ AI Business Toolkit Pro</h1>
    <p style='color: #94a3b8; font-size: 1.1rem;'>5 premium AI tools — one beautiful interface</p>
</div>
""", unsafe_allow_html=True)

# ---------- Tabs ----------
tabs = st.tabs(["🔍 SEO Strategist", "✉️ Cold Email", "🛍️ Shopify Expert", "🏢 Lead Research", "💻 Code Auditor"])

# ---------- TOOL 1 ----------
with tabs[0]:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        url_seo = st.text_input("Website URL", placeholder="https://example.com", key="seo_url")
        if st.button("Generate SEO Audit", key="btn1"):
            if not api_key:
                st.error("❌ Please add your DeepSeek API key in sidebar")
            elif not url_seo:
                st.error("❌ Enter a valid URL")
            else:
                with st.spinner("Fetching website data..."):
                    data = scrape_website(url_seo)
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        prompt = f"""URL: {data['url']}
Title: {data['title']}
Meta Description: {data['description']}
Content preview: {data['text'][:1500]}

Provide SEO audit: Meta tags analysis, 5 keyword suggestions, SEO score (0-100), 3 content improvements. Markdown format."""
                        with st.spinner("AI strategizing..."):
                            result = call_ai(api_key, "You are a senior SEO consultant", prompt)
                        st.markdown('<div class="report-text">', unsafe_allow_html=True)
                        st.markdown("### 📊 SEO Audit Report")
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOOL 2 ----------
with tabs[1]:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        biz_desc = st.text_area("Describe your business", height=120, placeholder="We provide AI-powered CRM solutions for real estate agents...", key="cold_desc")
        if st.button("Generate Cold Email Templates", key="btn2"):
            if not api_key:
                st.error("❌ API key required")
            elif not biz_desc.strip():
                st.error("❌ Enter business description")
            else:
                prompt = f"Business: {biz_desc}\nGenerate 5 cold email templates for B2B outreach. Each with subject line, opening, value prop, CTA. Number them. Use markdown."
                with st.spinner("Crafting emails..."):
                    emails = call_ai(api_key, "You are a B2B sales copywriter", prompt)
                st.markdown('<div class="report-text">', unsafe_allow_html=True)
                st.markdown("### ✉️ Cold Email Templates")
                st.markdown(emails)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOOL 3 ----------
with tabs[2]:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        prod_name = st.text_input("Product name", key="prod_name")
        features = st.text_area("Key features (comma separated)", height=80, placeholder="Stainless steel, 1L capacity, leak-proof", key="features")
        if st.button("Generate Shopify Content", key="btn3"):
            if not api_key:
                st.error("❌ API key missing")
            elif not prod_name.strip():
                st.error("❌ Enter product name")
            else:
                prompt = f"Product: {prod_name}\nFeatures: {features}\nGenerate: 3 SEO titles, 150-word description (with emojis), 5 image alt texts, meta description (max 160 chars). Use markdown."
                with st.spinner("Creating high-converting copy..."):
                    content = call_ai(api_key, "You are an e-commerce copywriter", prompt)
                st.markdown('<div class="report-text">', unsafe_allow_html=True)
                st.markdown("### 🛍️ Product Content")
                st.markdown(content)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOOL 4 ----------
with tabs[3]:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        company_url = st.text_input("Company website URL", placeholder="https://company.com", key="lead_url")
        if st.button("Research Company", key="btn4"):
            if not api_key:
                st.error("❌ API key missing")
            elif not company_url:
                st.error("❌ Enter company URL")
            else:
                with st.spinner("Scraping company data..."):
                    data = scrape_website(company_url)
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        prompt = f"""Company: {data['url']}
Title: {data['title']}
Meta: {data['description']}
Text: {data['text'][:1200]}
Provide lead research: company summary, potential decision-makers, services needed, outreach angle. Markdown."""
                        with st.spinner("Analyzing..."):
                            report = call_ai(api_key, "You are a B2B lead researcher", prompt)
                        st.markdown('<div class="report-text">', unsafe_allow_html=True)
                        st.markdown("### 🏢 Lead Intelligence Report")
                        st.markdown(report)
                        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- TOOL 5 ----------
with tabs[4]:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        code = st.text_area("Paste code (Python/HTML/JS)", height=200, key="code_input")
        lang = st.selectbox("Language", ["Python", "HTML/CSS", "JavaScript"], key="lang")
        if st.button("Audit Code", key="btn5"):
            if not api_key:
                st.error("❌ API key missing")
            elif not code.strip():
                st.error("❌ Paste some code")
            else:
                prompt = f"Language: {lang}\nCode:\n{code[:3000]}\nProvide: bugs, performance tips, 3 best practices, refactored snippet. Markdown."
                with st.spinner("Reviewing code..."):
                    audit = call_ai(api_key, "You are a senior software engineer", prompt)
                st.markdown('<div class="report-text">', unsafe_allow_html=True)
                st.markdown("### 🔍 Code Audit Report")
                st.markdown(audit)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown('<div class="footer">Powered by DeepSeek API · Enterprise Grade · Fully Responsive</div>', unsafe_allow_html=True)

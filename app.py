import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

st.set_page_config(page_title="AI Business Toolkit Pro", page_icon="✨", layout="wide")

# ---------- Professional 3D Glassmorphism CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background: radial-gradient(circle at 20% 30%, #0a0f1e, #030712); }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(18, 25, 45, 0.75) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    
    /* Glass card */
    .glass-card {
        background: rgba(22, 32, 52, 0.5);
        backdrop-filter: blur(12px);
        border-radius: 32px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 20px 35px -12px rgba(0,0,0,0.3);
        padding: 1.8rem;
        margin-bottom: 1.8rem;
        transition: all 0.3s;
    }
    .glass-card:hover {
        border-color: rgba(255,255,255,0.2);
        box-shadow: 0 25px 40px -12px rgba(0,0,0,0.4);
    }
    
    /* Headers gradient */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        font-weight: 600;
        background: linear-gradient(135deg, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent !important;
        letter-spacing: -0.02em;
    }
    
    /* 3D Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(10, 15, 30, 0.85) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 20px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 0.9rem 1.2rem !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.2), 0 0 0 3px rgba(59,130,246,0.2);
        outline: none;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #94a3b8 !important;
        font-weight: 400;
    }
    /* Ensure typed text is white */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        color: white !important;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(105deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        border-radius: 48px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(59,130,246,0.5);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(0,0,0,0.2);
        border-radius: 60px;
        padding: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
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
    
    /* Report text */
    .report-text {
        color: #e2e8f0;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .report-text h1, .report-text h2, .report-text h3 {
        background: none;
        color: #facc15 !important;
        -webkit-background-clip: unset;
        background-clip: unset;
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
    
    /* Mobile responsive */
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
    """Call DeepSeek API with error handling."""
    if not api_key or not api_key.startswith("sk-"):
        return "⚠️ Invalid or missing API key. Please add your DeepSeek API key in the sidebar."
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

def scrape_website(url: str) -> dict:
    """Scrape basic SEO data from a URL."""
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
        # Clean text
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        text = soup.get_text(separator=" ", strip=True)[:2000]
        return {"title": title, "description": meta_desc, "text": text, "url": url}
    except Exception as e:
        return {"error": str(e)}

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=65)
    st.markdown("### 🔐 DeepSeek API")
    api_key = st.text_input(
        "API Key", 
        type="password", 
        value=os.environ.get("DEEPSEEK_API_KEY", ""), 
        placeholder="sk-..."
    )
    st.markdown("---")
    st.markdown("### 🛠️ Toolkit")
    st.markdown("""
    ✅ **SEO Strategist** – Website audit  
    ✅ **Cold Email Pro** – Outreach templates  
    ✅ **Shopify Expert** – Product content  
    ✅ **Lead Researcher** – Company insights  
    ✅ **Code Auditor** – Code review
    """)
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 SEO Strategist", 
    "✉️ Cold Email", 
    "🛍️ Shopify Expert", 
    "🏢 Lead Research", 
    "💻 Code Auditor"
])

# ==================== TOOL 1: SEO Strategist ====================
with tab1:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            url_seo = st.text_input("Website URL", placeholder="https://example.com", key="seo_url")
        with col2:
            st.write("")  # spacer
        if st.button("🚀 Generate SEO Audit", key="seo_btn"):
            if not api_key:
                st.error("❌ Please add your DeepSeek API key in the sidebar")
            elif not url_seo:
                st.error("❌ Please enter a valid URL")
            else:
                # Normalize URL
                if not url_seo.startswith(("http://", "https://")):
                    url_seo = "https://" + url_seo
                with st.spinner("🌐 Fetching website data..."):
                    data = scrape_website(url_seo)
                    if "error" in data:
                        st.error(f"❌ {data['error']}")
                    else:
                        prompt = f"""Perform an SEO audit for:
URL: {data['url']}
Title: {data['title']}
Meta Description: {data['description']}
Content preview: {data['text'][:1500]}

Provide:
1. Meta Tags Analysis (title length, description quality)
2. Keyword Suggestions (5-7 primary + secondary)
3. SEO Score (0-100) with justification
4. 3 Actionable Content Improvement Tips
Output in markdown."""
                        with st.spinner("🤖 AI is analyzing..."):
                            result = call_ai(api_key, "You are a senior SEO consultant with 10+ years experience", prompt)
                        st.markdown('<div class="report-text">', unsafe_allow_html=True)
                        st.markdown("### 📊 SEO Audit Report")
                        st.markdown(result)
                        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOOL 2: Cold Email Pro ====================
with tab2:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        biz_desc = st.text_area(
            "Describe your business / product / service", 
            height=120,
            placeholder="Example: We provide AI-powered CRM for real estate agents. Our platform automates lead follow-up and increases conversion by 30%.",
            key="cold_desc"
        )
        if st.button("✉️ Generate Cold Email Templates", key="cold_btn"):
            if not api_key:
                st.error("❌ Missing API key")
            elif not biz_desc.strip():
                st.error("❌ Please describe your business")
            else:
                prompt = f"""Based on this business description:
"{biz_desc}"

Generate 5 different cold email templates for B2B outreach or client acquisition.
Each email must include:
- Compelling subject line
- Personalized opening line
- Clear value proposition (what problem you solve)
- Strong call to action

Number the emails 1-5. Use markdown formatting (headings, bullet points). Keep each email under 150 words."""
                with st.spinner("✍️ Crafting high-converting emails..."):
                    emails = call_ai(api_key, "You are an expert B2B sales copywriter who writes cold emails that get replies", prompt)
                st.markdown('<div class="report-text">', unsafe_allow_html=True)
                st.markdown("### ✉️ Cold Email Templates")
                st.markdown(emails)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOOL 3: Shopify Product Expert ====================
with tab3:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            prod_name = st.text_input("Product name", placeholder="e.g., Eco-Friendly Water Bottle", key="prod_name")
        with col2:
            pass
        features = st.text_area(
            "Key features (comma separated)", 
            height=80,
            placeholder="Stainless steel, 1L capacity, leak-proof, keeps cold 24h",
            key="features"
        )
        if st.button("🛍️ Generate Shopify Content", key="shopify_btn"):
            if not api_key:
                st.error("❌ Missing API key")
            elif not prod_name.strip():
                st.error("❌ Please enter product name")
            else:
                prompt = f"""Product: {prod_name}
Features: {features if features else 'Not specified'}

Generate high-converting Shopify content:
1. SEO Product Title (3 variations, include primary keyword)
2. Product Description (150-200 words, benefit-driven, use emojis, speak to customer pain points)
3. Image Alt Text (5 different SEO-friendly alt texts)
4. Meta Description (max 160 characters, include keyword and call to action)

Output in clear markdown sections."""
                with st.spinner("🎨 Creating professional product content..."):
                    content = call_ai(api_key, "You are an e-commerce conversion copywriter who specializes in Shopify stores", prompt)
                st.markdown('<div class="report-text">', unsafe_allow_html=True)
                st.markdown("### 🚀 Shopify Product Content")
                st.markdown(content)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOOL 4: B2B Lead Researcher ====================
with tab4:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        company_url = st.text_input("Company website URL", placeholder="https://company.com", key="lead_url")
        if st.button("🏢 Research Company", key="lead_btn"):
            if not api_key:
                st.error("❌ Missing API key")
            elif not company_url:
                st.error("❌ Please enter company URL")
            else:
                if not company_url.startswith(("http://", "https://")):
                    company_url = "https://" + company_url
                with st.spinner("🔍 Scraping company website..."):
                    data = scrape_website(company_url)
                    if "error" in data:
                        st.error(f"❌ {data['error']}")
                    else:
                        prompt = f"""Company URL: {data['url']}
Website Title: {data['title']}
Meta Description: {data['description']}
Content snippet: {data['text'][:1200]}

Based on this information, provide a B2B lead research report:
- **Company Summary** (industry, size estimate, main offerings)
- **Potential Decision‑Makers** (job titles likely responsible for purchasing)
- **Needs & Pain Points** (what services/products they might require)
- **Outreach Angle** (one paragraph, personalized pitch idea)

Make it concise, actionable, and professional. Format in markdown."""
                        with st.spinner("🧠 AI analyzing business intelligence..."):
                            report = call_ai(api_key, "You are an expert B2B lead researcher and sales strategist", prompt)
                        st.markdown('<div class="report-text">', unsafe_allow_html=True)
                        st.markdown("### 📊 Lead Intelligence Report")
                        st.markdown(report)
                        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOOL 5: AI Code Auditor ====================
with tab5:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        code_input = st.text_area(
            "Paste your code (HTML/CSS, Python, JavaScript)", 
            height=200,
            placeholder="def example_function():\n    return 'Hello World'",
            key="code_input"
        )
        lang = st.selectbox("Select language", ["Python", "HTML/CSS", "JavaScript"], key="lang")
        if st.button("💻 Audit Code", key="code_btn"):
            if not api_key:
                st.error("❌ Missing API key")
            elif not code_input.strip():
                st.error("❌ Please paste some code to audit")
            else:
                prompt = f"""Language: {lang}
Code:

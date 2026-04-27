import os
import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

# ---------------------------- Page Config ----------------------------
st.set_page_config(page_title="AI Business Toolkit Pro", page_icon="⚡", layout="wide")

# ---------------------------- Custom CSS (Glassmorphism) ----------------------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); }
[data-testid="stSidebar"] { background: rgba(15, 23, 42, 0.6) !important; backdrop-filter: blur(16px) !important; border-right: 1px solid rgba(255,255,255,0.15) !important; }
.glass-card { background: rgba(255,255,255,0.05); backdrop-filter: blur(12px); border-radius: 28px; border: 1px solid rgba(255,255,255,0.2); padding: 1.8rem; margin-bottom: 1.5rem; transition: transform 0.2s; }
.glass-card:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.3); }
.stButton > button { background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important; border-radius: 40px !important; font-weight: 600 !important; transition: all 0.2s; }
.stButton > button:hover { transform: scale(1.02); box-shadow: 0 6px 16px rgba(59,130,246,0.4); }
h1, h2, h3 { color: #f8fafc !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 16px !important; color: white !important; }
.stAlert { background: rgba(0,0,0,0.7) !important; backdrop-filter: blur(8px); border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------- Helper Functions ----------------------------
def call_deepseek(api_key: str, system_prompt: str, user_prompt: str) -> str:
    """Generic function to call DeepSeek API."""
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content

def fetch_company_info(url: str) -> dict:
    """Basic scraping for company name and meta description."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, timeout=10, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        meta_desc = ""
        for meta in soup.find_all("meta"):
            if meta.get("name", "").lower() == "description":
                meta_desc = meta.get("content", "")
        # Get first 500 chars of text
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ", strip=True)[:1500]
        return {"title": title, "description": meta_desc, "text": text, "url": url}
    except:
        return {"error": "Could not fetch website"}

# ---------------------------- Sidebar API Key ----------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=70)
    st.markdown("## 🔐 API Configuration")
    api_key = st.text_input("DeepSeek API Key", type="password", placeholder="sk-...", value=os.environ.get("DEEPSEEK_API_KEY", ""))
    st.markdown("---")
    st.markdown("### 🛠️ 5 AI Tools")
    st.info("1. SEO Strategist\n2. Cold Email Pro\n3. Shopify Expert\n4. B2B Lead Researcher\n5. Code Auditor")
    st.markdown("---")
    st.caption("Powered by DeepSeek API | Glassmorphism UI")

# ---------------------------- Main App Title ----------------------------
st.markdown('<div class="glass-card" style="text-align:center;"><h1>⚡ AI Business Toolkit Pro</h1><p style="color:#94a3b8;">5 powerful AI tools to grow your business</p></div>', unsafe_allow_html=True)

# ---------------------------- Create 5 Tabs ----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 AI SEO Strategist", "✉️ Cold Email Pro", "🛍️ Shopify Product Expert", "🏢 B2B Lead Researcher", "💻 AI Code Auditor"])

# ---------- Tool 1: AI SEO Strategist ----------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔍 Website SEO Analyzer")
    url_seo = st.text_input("Enter website URL", key="seo_url", placeholder="https://example.com")
    if st.button("Generate SEO Audit", key="seo_btn"):
        if not api_key:
            st.error("❌ Please add DeepSeek API Key in sidebar.")
        elif not url_seo:
            st.error("❌ Please enter a valid URL.")
        else:
            with st.spinner("Fetching website content..."):
                data = fetch_company_info(url_seo)
                if "error" in data:
                    st.error(data["error"])
                else:
                    prompt = f"""Analyze the following website for SEO:
URL: {data['url']}
Title: {data['title']}
Meta Description: {data['description']}
Content preview: {data['text'][:2000]}

Provide:
1. **Meta Tags Analysis** (title length, description quality)
2. **Keyword Suggestions** (5-7 primary + secondary)
3. **SEO Score** (out of 100) with explanation
4. **Content Improvement Tips** (3 bullet points)
Format in markdown."""
                    with st.spinner("AI is thinking..."):
                        result = call_deepseek(api_key, "You are a senior SEO strategist. Give actionable advice.", prompt)
                    st.markdown("### 📈 SEO Audit Report")
                    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Tool 2: Cold Email Pro ----------
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("✉️ Personalized Cold Email Templates")
    business_desc = st.text_area("Describe your business / product / service", height=120, key="cold_desc", placeholder="Example: We are a SaaS company selling AI-powered CRM for real estate agents.")
    if st.button("Generate Cold Emails", key="cold_btn"):
        if not api_key:
            st.error("❌ Add DeepSeek API Key.")
        elif not business_desc.strip():
            st.error("❌ Please describe your business.")
        else:
            prompt = f"""Based on this business description: "{business_desc}"
Generate 5 different cold email templates for outreach to potential clients or partners.
Each email should have:
- Subject line
- Personalized opening
- Value proposition
- Call to action

Make them professional, concise, and actionable. Number them 1-5. Use markdown formatting."""
            with st.spinner("Writing emails..."):
                emails = call_deepseek(api_key, "You are an expert B2B sales copywriter.", prompt)
            st.markdown("### 📧 Your Cold Email Templates")
            st.markdown(emails)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Tool 3: Shopify Product Expert ----------
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🛍️ High-Converting Shopify Content")
    product_name = st.text_input("Product name", key="prod_name", placeholder="e.g., Eco-friendly Water Bottle")
    product_features = st.text_area("Key features / benefits", height=100, key="prod_features", placeholder="Insulated, stainless steel, 1L capacity, leak-proof")
    if st.button("Generate Shopify Content", key="shopify_btn"):
        if not api_key:
            st.error("❌ Add DeepSeek API Key.")
        elif not product_name.strip():
            st.error("❌ Please enter product name.")
        else:
            prompt = f"""Product name: {product_name}
Features: {product_features}

Generate:
1. **SEO-optimized Product Title** (3 options)
2. **Product Description** (150-200 words, benefit-driven, includes emojis)
3. **Image Alt-text** (5 variations for SEO)
4. **Meta Description** (max 160 characters)

Output in clear markdown sections."""
            with st.spinner("Creating high-converting copy..."):
                content = call_deepseek(api_key, "You are an expert e-commerce copywriter who specializes in conversions.", prompt)
            st.markdown("### ✨ Shopify Product Content")
            st.markdown(content)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Tool 4: B2B Lead Researcher ----------
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏢 B2B Company Research")
    company_url = st.text_input("Enter company website URL", key="lead_url", placeholder="https://company.com")
    if st.button("Research Company", key="lead_btn"):
        if not api_key:
            st.error("❌ Add DeepSeek API Key.")
        elif not company_url.strip():
            st.error("❌ Enter a valid URL.")
        else:
            with st.spinner("Scraping and analyzing..."):
                data = fetch_company_info(company_url)
                if "error" in data:
                    st.error(data["error"])
                else:
                    prompt = f"""Based on this company data:
URL: {data['url']}
Title: {data['title']}
Meta Description: {data['description']}
Text summary: {data['text'][:1500]}

Provide a professional lead research report:
- **Company Summary** (what they do, industry, size estimate)
- **Potential Contact Roles** (e.g., CTO, Marketing Head)
- **Services/Products** they likely need (based on content)
- **Suggested Outreach Angle** (one paragraph)
Make it concise and actionable."""
                    with st.spinner("AI analyzing business..."):
                        report = call_deepseek(api_key, "You are a B2B lead researcher and sales strategist.", prompt)
                    st.markdown("### 📊 Lead Research Report")
                    st.markdown(report)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Tool 5: AI Code Auditor ----------
with tab5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("💻 Code Auditor (HTML/CSS/Python)")
    code_input = st.text_area("Paste your code here", height=250, key="code_area", placeholder="<div>Hello</div>  or  def foo(): pass")
    lang = st.selectbox("Select language", ["HTML/CSS", "Python", "JavaScript"], key="code_lang")
    if st.button("Audit Code", key="code_btn"):
        if not api_key:
            st.error("❌ Add DeepSeek API Key.")
        elif not code_input.strip():
            st.error("❌ Please paste some code.")
        else:
            prompt = f"""Language: {lang}
Code:
{code_input[:3000]}

Perform a code audit:
- Identify **bugs or errors** (if any)
- Suggest **performance improvements**
- Recommend **best practices** (3 items)
- Provide a **refactored version** of a small snippet if possible.

Output in markdown with clear sections."""
            with st.spinner("Reviewing code..."):
                audit = call_deepseek(api_key, "You are a senior software engineer and code reviewer.", prompt)
            st.markdown("### 🔍 Code Audit Report")
            st.markdown(audit)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------- Footer ----------------------------
st.markdown("---")
st.caption("Built with Streamlit + DeepSeek API | 5 AI Tools for Business | Glassmorphism UI")

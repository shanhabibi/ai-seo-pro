import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

st.set_page_config(page_title="AI SEO Suite Pro", page_icon="🚀", layout="wide")

# Glassmorphism CSS (same premium style)
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e293b); }
.glass-card { background: rgba(255,255,255,0.07); backdrop-filter: blur(10px); border-radius: 24px; padding: 2rem; margin: 1rem 0; }
.tab-card { background: rgba(255,255,255,0.05); border-radius: 20px; padding: 1rem; }
h1, h2, h3 { color: #f8fafc; }
.stButton>button { background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 40px; }
</style>
""", unsafe_allow_html=True)

# Helper: fetch website data
def fetch_website(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, timeout=12, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        meta_desc = ""
        for meta in soup.find_all("meta"):
            if meta.get("name", "").lower() == "description":
                meta_desc = meta.get("content", "")
        headings = {
            "h1": [h.get_text(strip=True) for h in soup.find_all("h1")][:3],
            "h2": [h.get_text(strip=True) for h in soup.find_all("h2")][:5],
        }
        text = soup.get_text(separator=" ", strip=True)[:4000]
        return {"title": title, "description": meta_desc, "headings": headings, "text": text, "url": url}
    except Exception as e:
        return {"error": str(e)}

# AI call (reusable)
def call_ai(api_key, prompt):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# Sidebar API Key
with st.sidebar:
    api_key = st.text_input("DeepSeek API Key", type="password", value=os.environ.get("DEEPSEEK_API_KEY", ""))
    st.markdown("---")
    st.caption("5 Powerful SEO Tools in One")

st.title("🚀 AI SEO Suite Pro")
st.markdown("### Your All‑in‑One AI‑Powered SEO Dashboard")

# Create 5 tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 SEO Auditor", "🔑 Keyword Genie", "✍️ Content Optimizer", 
    "🔗 Backlink Insight", "⚔️ Competitor Analyzer"
])

# --------------------- TAB 1: SEO Auditor ---------------------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏆 Website SEO Audit")
    url1 = st.text_input("Enter URL", key="audit_url", placeholder="https://example.com")
    if st.button("Run Audit", key="audit_btn"):
        if not api_key: st.error("Add DeepSeek API Key")
        elif not url1: st.error("Enter URL")
        else:
            with st.spinner("Fetching website..."):
                data = fetch_website(url1)
                if "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    prompt = f"""Perform a professional SEO audit for:
URL: {data['url']}
Title: {data['title']}
Meta Description: {data['description']}
Headings H1: {data['headings']['h1']}
Headings H2: {data['headings']['h2'][:5]}
Text sample: {data['text'][:2000]}

Provide: Meta tags review, heading hierarchy, keyword suggestions, content improvements.
Make it short, actionable, in markdown."""
                    with st.spinner("AI analyzing..."):
                        report = call_ai(api_key, prompt)
                    st.markdown("### 📈 Audit Report")
                    st.markdown(report)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------- TAB 2: Keyword Genie ---------------------
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔑 AI Keyword Generator")
    topic = st.text_input("Enter a topic or niche", key="keyword_topic", placeholder="e.g., vegan protein powder")
    if st.button("Generate Keywords", key="keyword_btn"):
        if not api_key: st.error("Add DeepSeek API Key")
        elif not topic: st.error("Enter topic")
        else:
            prompt = f"""Generate 15 SEO keywords (primary + long-tail) for topic: "{topic}".
Group them into: Head terms (3), Long-tail (8), LSI (4).
Add search intent (informational/transactional) for top 5.
Return in markdown bullet list."""
            with st.spinner("Generating keywords..."):
                keywords = call_ai(api_key, prompt)
            st.markdown("### ✨ Keyword Ideas")
            st.markdown(keywords)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------- TAB 3: Content Optimizer ---------------------
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("✍️ Content Rewriter & Optimizer")
    content_input = st.text_area("Paste your content here", height=200, key="content_raw")
    target_kw = st.text_input("Target keyword (optional)", key="target_kw")
    if st.button("Optimize Content", key="optimize_btn"):
        if not api_key: st.error("Add DeepSeek API Key")
        elif not content_input: st.error("Paste some content")
        else:
            prompt = f"""Improve the following content for SEO.
Target keyword: {target_kw if target_kw else 'None given'}.
Original content:
{content_input[:3000]}

Return:
1. Readability score (1-10)
2. Word count & suggested length
3. Rewritten version (200-300 words) with better keyword placement
4. 3 tips to improve structure
Output in markdown."""
            with st.spinner("Optimizing..."):
                optimized = call_ai(api_key, prompt)
            st.markdown("### ✅ Optimized Version")
            st.markdown(optimized)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------- TAB 4: Backlink Insight (Demo + AI) ---------------------
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🔗 Backlink Opportunity Analyzer")
    url4 = st.text_input("Enter your website URL", key="backlink_url", placeholder="https://yoursite.com")
    if st.button("Analyze Backlink Potential", key="backlink_btn"):
        if not api_key: st.error("Add DeepSeek API Key")
        elif not url4: st.error("Enter URL")
        else:
            # Mock data + AI
            mock_data = "Based on domain authority, potential backlink sources: industry blogs, forums, guest posts."
            prompt = f"""For website {url4}, provide a backlink strategy report:
- Current backlink profile estimate (if any)
- 5 types of websites that would link to it
- 3 actionable outreach templates
Make it concise and in markdown."""
            with st.spinner("Generating backlink insights..."):
                backlink_report = call_ai(api_key, prompt)
            st.markdown("### 🔗 Backlink Strategy")
            st.markdown(backlink_report)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------- TAB 5: Competitor Analyzer ---------------------
with tab5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("⚔️ Competitor SEO Comparison")
    col1, col2 = st.columns(2)
    with col1:
        url_a = st.text_input("Your URL", key="comp_you", placeholder="https://yourdomain.com")
    with col2:
        url_b = st.text_input("Competitor URL", key="comp_them", placeholder="https://competitor.com")
    if st.button("Compare", key="comp_btn"):
        if not api_key: st.error("Add DeepSeek API Key")
        elif not url_a or not url_b: st.error("Enter both URLs")
        else:
            with st.spinner("Fetching both sites..."):
                data_a = fetch_website(url_a)
                data_b = fetch_website(url_b)
                if "error" in data_a or "error" in data_b:
                    st.error("Could not fetch one or both URLs")
                else:
                    prompt = f"""Compare SEO metrics of these two websites:

Website A: {data_a['url']}
Title A: {data_a['title']}
Meta A: {data_a['description']}
H1s A: {data_a['headings']['h1']}

Website B: {data_b['url']}
Title B: {data_b['title']}
Meta B: {data_b['description']}
H1s B: {data_b['headings']['h1']}

Provide:
- Strengths of each
- Weaknesses
- 3 actionable recommendations for Website A to outperform B
Output in markdown."""
                    with st.spinner("AI analyzing competitors..."):
                        comparison = call_ai(api_key, prompt)
                    st.markdown("### 🏁 SEO Gap Analysis")
                    st.markdown(comparison)
    st.markdown('</div>', unsafe_allow_html=True)

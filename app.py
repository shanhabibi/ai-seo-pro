cat > app.py << 'EOF'
import os
import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

st.set_page_config(page_title="AI SEO Pro", page_icon="🔍", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e293b); }
.glass-card { background: rgba(255,255,255,0.07); backdrop-filter: blur(10px); border-radius: 24px; padding: 2rem; margin: 1rem; }
</style>
""", unsafe_allow_html=True)

def fetch_website(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, timeout=10, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string.strip() if soup.title else "No title"
    meta_desc = ""
    for meta in soup.find_all("meta"):
        if meta.get("name", "").lower() == "description":
            meta_desc = meta.get("content", "")
    text = soup.get_text(separator=" ", strip=True)[:3000]
    return {"title": title, "description": meta_desc, "text": text, "url": url}

def generate_audit(api_key, data):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
    prompt = f"""SEO audit for {data['url']}
Title: {data['title']}
Meta description: {data['description']}
Content sample: {data['text'][:1500]}
Provide recommendations: meta tags, keywords, content tips."""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

def main():
    with st.sidebar:
        api_key = st.text_input("DeepSeek API Key", type="password", value=os.environ.get("DEEPSEEK_API_KEY", ""))
    st.markdown('<div class="glass-card"><h1>🔍 AI SEO Strategist Pro</h1>', unsafe_allow_html=True)
    url = st.text_input("Enter website URL", placeholder="https://example.com")
    if st.button("Generate SEO Audit"):
        if not api_key:
            st.error("Please add DeepSeek API key")
        elif not url:
            st.error("Please enter a URL")
        else:
            try:
                with st.spinner("Fetching website..."):
                    data = fetch_website(url)
                with st.spinner("AI is analyzing..."):
                    report = generate_audit(api_key, data)
                st.markdown("## 📊 SEO Audit Report")
                st.markdown(report)
            except Exception as e:
                st.error(f"Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
EOF
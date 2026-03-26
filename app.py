import streamlit as st
import requests
import json
import re
import time
from PyPDF2 import PdfReader
import google.generativeai as genai

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

* { font-family: 'Syne', sans-serif; }
code, pre { font-family: 'Space Mono', monospace !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
}

[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #2a2a3d;
}

h1 { font-size: 2.4rem !important; font-weight: 800 !important;
     background: linear-gradient(135deg, #7c3aed, #06b6d4);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

h2, h3 { color: #c4b5fd !important; font-weight: 600 !important; }

.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%);
    color: white; border: none; border-radius: 12px;
    padding: 0.7rem 1.8rem; font-weight: 700; font-size: 1rem;
    letter-spacing: 0.04em; transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(124,58,237,0.6);
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #151520 !important; color: #e8e6f0 !important;
    border: 1px solid #2a2a3d !important; border-radius: 10px !important;
}

.card {
    background: #12121e; border: 1px solid #2a2a3d;
    border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.4);
    transition: border-color 0.2s;
}
.card:hover { border-color: #7c3aed; }

.tag {
    display: inline-block; background: #1e1e30;
    border: 1px solid #7c3aed; color: #c4b5fd;
    border-radius: 999px; padding: 2px 12px;
    font-size: 0.78rem; margin: 2px; font-family: 'Space Mono', monospace;
}

.chip-green  { border-color: #10b981; color: #6ee7b7; background: #0d2018; }
.chip-cyan   { border-color: #06b6d4; color: #67e8f9; background: #061820; }
.chip-purple { border-color: #7c3aed; color: #c4b5fd; background: #1a0f30; }

.section-header {
    font-size: 1.1rem; font-weight: 700; color: #06b6d4;
    letter-spacing: 0.08em; text-transform: uppercase;
    border-bottom: 1px solid #2a2a3d; padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

.step-badge {
    display: inline-block; width: 28px; height: 28px;
    background: linear-gradient(135deg,#7c3aed,#06b6d4);
    border-radius: 50%; text-align: center; line-height: 28px;
    font-weight: 800; font-size: 0.85rem; margin-right: 8px; color: white;
}

.highlight-box {
    background: linear-gradient(135deg, #1a0f30, #061820);
    border: 1px solid #7c3aed; border-radius: 12px;
    padding: 1rem 1.2rem; margin: 0.6rem 0;
}

.email-badge {
    background: #0d1f2d; border: 1px solid #06b6d4;
    color: #67e8f9; border-radius: 8px; padding: 4px 10px;
    font-family: 'Space Mono', monospace; font-size: 0.82rem;
}

[data-testid="stExpander"] {
    background: #12121e !important; border: 1px solid #2a2a3d !important;
    border-radius: 12px !important;
}

.stAlert { border-radius: 10px !important; }
.stSpinner > div { border-top-color: #7c3aed !important; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────────────────

def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def call_llm(prompt: str, system: str = "", groq_key: str = "",
             gemini_key: str = "") -> str:
    """Try llama-3.1-8b-instant → gemini-1.5-flash → groq fallback."""

    # 1️⃣  Groq  llama-3.1-8b-instant
    if groq_key:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}",
                         "Content-Type": "application/json"},
                json={"model": "llama-3.1-8b-instant",
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user",   "content": prompt}],
                      "temperature": 0.4, "max_tokens": 4096},
                timeout=60
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            st.warning(f"llama-3.1-8b-instant failed: {e} — trying Gemini…")

    # 2️⃣  Gemini free (gemini-1.5-flash)
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            full = f"{system}\n\n{prompt}" if system else prompt
            resp = model.generate_content(full)
            return resp.text
        except Exception as e:
            st.warning(f"Gemini failed: {e} — trying Groq mixtral fallback…")

    # 3️⃣  Groq mixtral fallback
    if groq_key:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}",
                         "Content-Type": "application/json"},
                json={"model": "mixtral-8x7b-32768",
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user",   "content": prompt}],
                      "temperature": 0.4, "max_tokens": 4096},
                timeout=60
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            st.error(f"All models failed. Last error: {e}")

    return "⚠️ Could not get a response. Check your API keys."


def tavily_search(query: str, tavily_key: str, max_results: int = 8) -> list:
    try:
        r = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": tavily_key, "query": query,
                  "max_results": max_results, "search_depth": "advanced",
                  "include_answer": True},
            timeout=30
        )
        if r.status_code == 200:
            return r.json().get("results", [])
    except Exception as e:
        st.error(f"Tavily error: {e}")
    return []


def google_search(query: str, api_key: str, cx: str,
                  num: int = 8) -> list:
    try:
        r = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": api_key, "cx": cx, "q": query, "num": num},
            timeout=20
        )
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        st.warning(f"Google Search error: {e}")
    return []


def scrape_github_profile(username: str) -> dict:
    info = {}
    try:
        u = requests.get(f"https://api.github.com/users/{username}",
                         timeout=15).json()
        info["name"]        = u.get("name", username)
        info["bio"]         = u.get("bio", "")
        info["location"]    = u.get("location", "")
        info["followers"]   = u.get("followers", 0)
        info["public_repos"]= u.get("public_repos", 0)
        info["blog"]        = u.get("blog", "")
        repos = requests.get(
            f"https://api.github.com/users/{username}/repos"
            "?sort=stars&per_page=10", timeout=15).json()
        if isinstance(repos, list):
            info["top_repos"] = [
                {"name": r["name"],
                 "description": r.get("description",""),
                 "stars": r.get("stargazers_count", 0),
                 "language": r.get("language",""),
                 "url": r.get("html_url","")}
                for r in repos
            ]
            info["languages"] = list({r.get("language","")
                                       for r in repos if r.get("language")})
    except Exception as e:
        info["error"] = str(e)
    return info


def extract_github_username(url: str) -> str:
    m = re.search(r"github\.com/([^/\s?#]+)", url)
    return m.group(1) if m else ""


def extract_kaggle_username(url: str) -> str:
    m = re.search(r"kaggle\.com/([^/\s?#]+)", url)
    return m.group(1) if m else ""


def scrape_kaggle_public(username: str, tavily_key: str) -> dict:
    info = {"username": username, "notebooks": [], "competitions": [],
            "datasets": []}
    if not tavily_key:
        return info
    results = tavily_search(
        f"site:kaggle.com/{username} notebooks competitions datasets", tavily_key, 6)
    for r in results:
        url  = r.get("url", "")
        title= r.get("title", "")
        snippet = r.get("content", "")
        if "/code/" in url or "notebook" in url.lower():
            info["notebooks"].append({"title": title, "url": url, "snippet": snippet})
        elif "competition" in url.lower():
            info["competitions"].append({"title": title, "url": url})
        elif "/datasets/" in url:
            info["datasets"].append({"title": title, "url": url})
    return info


def analyse_cv_and_profiles(cv_text, github_data, kaggle_data,
                             groq_key, gemini_key) -> dict:
    prompt = f"""
You are a career analysis AI. Analyse the following profile data and return a 
JSON object with these exact keys:
- "skills": list of top technical skills
- "domains": list of expertise domains (e.g. NLP, Computer Vision, MLOps)
- "experience_level": one of Junior / Mid / Senior / Principal
- "keywords": list of 10 best job-search keywords
- "summary": 2-sentence professional summary
- "research_interests": list of research topics this person fits

CV TEXT:
{cv_text[:3000]}

GITHUB INFO:
{json.dumps(github_data, indent=2)[:2000]}

KAGGLE INFO:
{json.dumps(kaggle_data, indent=2)[:1500]}

Return ONLY valid JSON. No markdown fences.
"""
    raw = call_llm(prompt,
                   system="You are a career analysis expert. Always respond with valid JSON only.",
                   groq_key=groq_key, gemini_key=gemini_key)
    try:
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception:
        return {"summary": raw, "skills": [], "domains": [],
                "keywords": [], "experience_level": "Mid",
                "research_interests": []}


# ─── FIND RESEARCHERS ───────────────────────────────────────────────────────

def find_researchers(profile: dict, country: str,
                     tavily_key: str, google_key: str, google_cx: str,
                     groq_key: str, gemini_key: str) -> list:
    domains    = " ".join(profile.get("domains", [])[:3])
    interests  = " ".join(profile.get("research_interests", [])[:3])
    query = (f'researcher professor "{country}" {domains} {interests} '
             f'site:scholar.google.com OR site:researchgate.net OR '
             f'site:linkedin.com/in OR site:academia.edu email contact')

    raw_results = []
    if tavily_key:
        raw_results += tavily_search(query, tavily_key, 10)
    if google_key and google_cx:
        items = google_search(query, google_key, google_cx, 8)
        raw_results += [{"title": i.get("title",""),
                         "url":   i.get("link",""),
                         "content": i.get("snippet","")} for i in items]

    if not raw_results:
        return []

    results_text = "\n".join(
        f"- {r.get('title','')}: {r.get('url','')} | {r.get('content','')[:200]}"
        for r in raw_results[:12]
    )
    prompt = f"""
From the search results below, extract real researcher profiles that match this profile:
Skills: {profile.get('skills',[])}
Domains: {profile.get('domains',[])}
Research interests: {profile.get('research_interests',[])}
Country filter: {country}

Search results:
{results_text}

Return a JSON array. Each element must have:
- "name": researcher full name
- "affiliation": university / institution
- "email": email address (or "Not found" if unavailable — but try hard to infer from URL patterns like first.last@university.edu)
- "research_areas": list of topics
- "profile_url": best URL found
- "match_reason": why this person matches the profile

Return ONLY a JSON array. No markdown.
"""
    raw = call_llm(prompt,
                   system="Extract researcher info. Return only a JSON array.",
                   groq_key=groq_key, gemini_key=gemini_key)
    try:
        raw = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        return []


# ─── FIND JOBS ───────────────────────────────────────────────────────────────

def find_jobs(profile: dict, country_filter: str,
              tavily_key: str, google_key: str, google_cx: str,
              groq_key: str, gemini_key: str) -> list:
    keywords = " ".join(profile.get("keywords", [])[:4])
    level    = profile.get("experience_level", "")
    domains  = " ".join(profile.get("domains", [])[:2])
    location_part = country_filter if country_filter.strip() else "worldwide remote"

    query = (f'{level} {domains} {keywords} job opening {location_part} '
             f'apply now 2024 2025 site:linkedin.com/jobs OR '
             f'site:careers.google.com OR site:jobs.lever.co OR '
             f'site:greenhouse.io OR site:indeed.com OR site:wellfound.com')

    raw_results = []
    if tavily_key:
        raw_results += tavily_search(query, tavily_key, 12)
    if google_key and google_cx:
        items = google_search(query, google_key, google_cx, 8)
        raw_results += [{"title": i.get("title",""),
                         "url":   i.get("link",""),
                         "content": i.get("snippet","")} for i in items]

    if not raw_results:
        return []

    results_text = "\n".join(
        f"- {r.get('title','')}: {r.get('url','')} | {r.get('content','')[:200]}"
        for r in raw_results[:14]
    )
    prompt = f"""
From search results, extract real job listings matching this profile:
Skills: {profile.get('skills',[])}
Domains: {profile.get('domains',[])}
Experience: {level}
Location filter: {location_part}

Search results:
{results_text}

Return a JSON array. Each element:
- "title": job title
- "company": company name
- "location": city / remote / country
- "apply_url": direct application link (the URL from results)
- "salary": salary if mentioned, else "Not specified"
- "match_score": 1–10 how well it matches
- "skills_needed": list of key skills from the description
- "founder_or_hr_linkedin": any founder / recruiter LinkedIn URL found near the listing (or "Not found")

Return ONLY a JSON array. No markdown.
"""
    raw = call_llm(prompt,
                   system="Extract job listings. Return only a JSON array.",
                   groq_key=groq_key, gemini_key=gemini_key)
    try:
        raw = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        return []


# ════════════════════════════════════════════════════════════════════════════
#  STREAMLIT UI
# ════════════════════════════════════════════════════════════════════════════

st.markdown('<h1>🚀 AI Career Intelligence Agent</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#8b8ba8;margin-top:-10px;">Upload your CV · Link your profiles · Discover researchers & jobs worldwide</p>',
    unsafe_allow_html=True)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Configuration</div>',
                unsafe_allow_html=True)

    groq_key   = st.text_input("🔑 Groq API Key",   type="password",
                               placeholder="gsk_…")
    gemini_key = st.text_input("🔑 Gemini API Key", type="password",
                               placeholder="AIza…")

    st.markdown("---")
    st.markdown('<div class="section-header">🔍 Search Tools</div>',
                unsafe_allow_html=True)
    tavily_key = st.text_input("🌐 Tavily API Key", type="password",
                               placeholder="tvly-…")
    google_key = st.text_input("🔎 Google Search API Key", type="password",
                               placeholder="AIza… (optional)")
    google_cx  = st.text_input("🔎 Google CX (Search Engine ID)",
                               placeholder="optional")

    st.markdown("---")
    st.markdown('<div style="color:#8b8ba8;font-size:0.8rem;">Model cascade: llama-3.1-8b-instant → Gemini-1.5-flash → Groq mixtral</div>',
                unsafe_allow_html=True)

# ─── STEP 1: UPLOAD & LINKS ──────────────────────────────────────────────────
st.markdown('<div class="step-badge">1</div> **Upload your CV & Profile Links**',
            unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    uploaded_cv = st.file_uploader("📄 Upload CV (PDF)", type=["pdf"])
with col2:
    github_url  = st.text_input("🐙 GitHub Profile URL",
                                placeholder="https://github.com/username")
    kaggle_url  = st.text_input("📊 Kaggle Profile URL",
                                placeholder="https://www.kaggle.com/username")

analyse_btn = st.button("🧠 Analyse My Profile", use_container_width=True)

# ─── ANALYSIS ────────────────────────────────────────────────────────────────
if analyse_btn:
    if not uploaded_cv:
        st.error("Please upload your CV first.")
    elif not (groq_key or gemini_key):
        st.error("Please enter at least one API key (Groq or Gemini).")
    else:
        with st.spinner("Extracting CV text…"):
            cv_text = extract_pdf_text(uploaded_cv)

        github_data = {}
        if github_url.strip():
            uname = extract_github_username(github_url)
            if uname:
                with st.spinner(f"Scraping GitHub: {uname}…"):
                    github_data = scrape_github_profile(uname)

        kaggle_data = {}
        if kaggle_url.strip():
            uname = extract_kaggle_username(kaggle_url)
            if uname and tavily_key:
                with st.spinner(f"Scraping Kaggle: {uname}…"):
                    kaggle_data = scrape_kaggle_public(uname, tavily_key)

        with st.spinner("Analysing profile with AI…"):
            profile = analyse_cv_and_profiles(cv_text, github_data,
                                               kaggle_data, groq_key,
                                               gemini_key)
        st.session_state["profile"]     = profile
        st.session_state["cv_text"]     = cv_text
        st.session_state["github_data"] = github_data
        st.session_state["kaggle_data"] = kaggle_data


if "profile" in st.session_state:
    profile = st.session_state["profile"]

    st.markdown("---")
    st.markdown('<div class="step-badge">2</div> **Profile Analysis Results**',
                unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**📝 Summary**\n\n{profile.get('summary','')}")
        st.markdown(f"**Level:** `{profile.get('experience_level','')}`")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**🛠️ Skills**")
        skills_html = " ".join(
            f'<span class="tag chip-purple">{s}</span>'
            for s in profile.get("skills", []))
        st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**🎯 Domains**")
        domains_html = " ".join(
            f'<span class="tag chip-cyan">{d}</span>'
            for d in profile.get("domains", []))
        st.markdown(domains_html, unsafe_allow_html=True)
        st.markdown("**🔬 Research Interests**")
        ri_html = " ".join(
            f'<span class="tag chip-green">{r}</span>'
            for r in profile.get("research_interests", []))
        st.markdown(ri_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # GitHub display
    gd = st.session_state.get("github_data", {})
    if gd and not gd.get("error"):
        with st.expander("🐙 GitHub Profile Details"):
            st.write(f"**{gd.get('name','')}** — {gd.get('bio','')}")
            st.write(f"📍 {gd.get('location','')} | ⭐ {gd.get('followers',0)} followers | 📦 {gd.get('public_repos',0)} repos")
            if gd.get("top_repos"):
                for repo in gd["top_repos"][:5]:
                    st.markdown(
                        f'<div class="highlight-box">🗂️ <b>{repo["name"]}</b> '
                        f'({repo.get("language","")}) ⭐{repo.get("stars",0)}<br>'
                        f'<span style="color:#8b8ba8">{repo.get("description","")}</span><br>'
                        f'<a href="{repo.get("url","")}" style="color:#06b6d4">{repo.get("url","")}</a></div>',
                        unsafe_allow_html=True)

    # Kaggle display
    kd = st.session_state.get("kaggle_data", {})
    if kd.get("notebooks") or kd.get("competitions"):
        with st.expander("📊 Kaggle Profile Details"):
            if kd["notebooks"]:
                st.markdown("**Notebooks found:**")
                for n in kd["notebooks"][:5]:
                    st.markdown(f'<div class="highlight-box">📓 <b>{n["title"]}</b><br>'
                                f'<a href="{n["url"]}" style="color:#06b6d4">{n["url"]}</a></div>',
                                unsafe_allow_html=True)

    # ── STEP 3: ACTION BUTTONS ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="step-badge">3</div> **Choose Your Action**',
                unsafe_allow_html=True)

    target_country = st.text_input("🌍 Enter target country / region",
                                   placeholder="e.g. Germany, USA, Remote, Pakistan…")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        find_researchers_btn = st.button("🔬 Find Researchers for Collaboration",
                                         use_container_width=True)
    with col_btn2:
        find_jobs_btn = st.button("💼 Find Jobs Worldwide",
                                  use_container_width=True)

    # ── RESEARCHERS ─────────────────────────────────────────────────────────
    if find_researchers_btn:
        if not tavily_key and not (google_key and google_cx):
            st.error("Please provide Tavily or Google Search API keys.")
        else:
            with st.spinner("🔍 Searching for matching researchers…"):
                researchers = find_researchers(
                    profile, target_country or "worldwide",
                    tavily_key, google_key, google_cx,
                    groq_key, gemini_key)
            st.session_state["researchers"] = researchers

    if "researchers" in st.session_state:
        researchers = st.session_state["researchers"]
        st.markdown(f"### 🔬 Found {len(researchers)} Matching Researchers")

        if not researchers:
            st.info("No researchers found. Try different country or ensure search keys are valid.")
        for i, r in enumerate(researchers, 1):
            with st.expander(f"#{i} {r.get('name','Unknown')} — {r.get('affiliation','')}"):
                st.markdown(
                    f'<div class="card">'
                    f'<b>🏛️ Affiliation:</b> {r.get("affiliation","")}<br>'
                    f'<b>📧 Email:</b> <span class="email-badge">{r.get("email","Not found")}</span><br>'
                    f'<b>🔗 Profile:</b> <a href="{r.get("profile_url","")}" style="color:#06b6d4">{r.get("profile_url","")}</a><br>'
                    f'<b>🎯 Match Reason:</b> {r.get("match_reason","")}<br>'
                    f'<b>🔬 Research Areas:</b> '
                    + " ".join(f'<span class="tag chip-green">{a}</span>'
                               for a in r.get("research_areas", []))
                    + '</div>', unsafe_allow_html=True)

    # ── JOBS ────────────────────────────────────────────────────────────────
    if find_jobs_btn:
        if not tavily_key and not (google_key and google_cx):
            st.error("Please provide Tavily or Google Search API keys.")
        else:
            with st.spinner("💼 Searching for matching jobs worldwide…"):
                jobs = find_jobs(
                    profile, target_country or "",
                    tavily_key, google_key, google_cx,
                    groq_key, gemini_key)
            st.session_state["jobs"] = jobs

    if "jobs" in st.session_state:
        jobs = st.session_state["jobs"]
        st.markdown(f"### 💼 Found {len(jobs)} Matching Jobs")

        if not jobs:
            st.info("No jobs found. Try a different region or broader keywords.")

        for i, job in enumerate(sorted(jobs,
                                       key=lambda x: x.get("match_score", 0),
                                       reverse=True), 1):
            score = job.get("match_score", 0)
            color = "#10b981" if score >= 8 else "#f59e0b" if score >= 5 else "#ef4444"
            with st.expander(f"#{i} {job.get('title','')} @ {job.get('company','')}  |  Match: {score}/10"):
                apply_url   = job.get("apply_url", "")
                founder_url = job.get("founder_or_hr_linkedin", "Not found")
                st.markdown(
                    f'<div class="card">'
                    f'<b>🏢 Company:</b> {job.get("company","")}<br>'
                    f'<b>📍 Location:</b> {job.get("location","")}<br>'
                    f'<b>💰 Salary:</b> {job.get("salary","Not specified")}<br>'
                    f'<b>🎯 Match Score:</b> <span style="color:{color};font-weight:700">{score}/10</span><br>'
                    + (f'<b>🔗 Apply Link:</b> <a href="{apply_url}" target="_blank" '
                       f'style="color:#06b6d4;font-weight:600">👉 Apply Now</a><br>'
                       if apply_url else "")
                    + (f'<b>👤 Founder/HR:</b> <a href="{founder_url}" target="_blank" '
                       f'style="color:#c4b5fd">{founder_url}</a><br>'
                       if founder_url != "Not found" else "")
                    + '<b>🛠️ Skills Needed:</b> '
                    + " ".join(f'<span class="tag chip-purple">{s}</span>'
                               for s in job.get("skills_needed", []))
                    + '</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="card" style="text-align:center;padding:2.5rem;">
        <div style="font-size:3rem;margin-bottom:1rem;">🚀</div>
        <h3 style="color:#c4b5fd;">Get Started</h3>
        <p style="color:#8b8ba8;">
        Fill in your API keys in the sidebar, upload your CV, add your GitHub
        and Kaggle links, then click <b>Analyse My Profile</b> to begin.
        </p>
    </div>
    """, unsafe_allow_html=True)

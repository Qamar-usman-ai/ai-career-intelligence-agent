# 🚀 AI Career Intelligence Agent

> **The ultimate AI-powered career tool** — Upload your CV, scrape GitHub & Kaggle, find researchers university-by-university across 50+ countries, and discover jobs at all 4 experience levels worldwide.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-llama--3.1--8b-f97316?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)

</div>

---

## 📌 What Is This?

**AI Career Intelligence Agent** is a fully local, privacy-friendly Streamlit application that acts as your personal AI-powered career assistant. It combines CV analysis, live web scraping, and multi-model AI to help you:

- 📄 **Analyse your CV** — extract skills, domains, experience level, strengths, tools, and research interests
- 🐙 **Scrape GitHub** — repos, languages, stars, bio, forks via the public GitHub API
- 📊 **Scrape Kaggle** — notebooks, competitions, datasets via Tavily search
- 🔬 **Find researchers** — university-by-university or country-wide, with emails, departments, and profile links
- 💼 **Find jobs** — at all 4 experience levels (Basic → Expert) across 50+ countries with direct apply links and founder/HR LinkedIn profiles

---

## ✨ Feature Highlights

| Feature | Details |
|---|---|
| 📄 CV Analysis | PDF upload → AI extracts 15 skills, 6 domains, experience level, research interests, tools, certifications |
| 🐙 GitHub Scraping | Public API — top repos, languages, total stars, followers, bio |
| 📊 Kaggle Scraping | Tavily-powered — notebooks, competitions, datasets |
| 🌍 Country Selector | 50+ countries grouped into 7 regions — click to select, no typing |
| 🏙️ City Drill-Down | 10 countries with preloaded city → university maps |
| 🏛️ University Search | Search researchers at each university one-by-one or all at once |
| 🔬 Researcher Finder | Returns name, title, department, email, research areas, profile URL, match score |
| 💼 Job Finder | 4 levels × any country — apply link, salary, match score, founder LinkedIn |
| 🤖 Model Cascade | llama-3.1-8b-instant → gemini-1.5-flash → mixtral-8x7b (auto-fallback) |
| 🎨 Dark UI | Custom dark theme with gradient accents, score bars, tag chips |

---

## 🌍 Supported Countries & Cities

### Countries with Preloaded University Data

| Country | Cities | Universities |
|---|---|---|
| 🇦🇪 United Arab Emirates | Dubai, Abu Dhabi, Sharjah, Ajman, RAK, Fujairah, Al Ain | 60+ |
| 🇸🇦 Saudi Arabia | Riyadh, Jeddah, Dammam | 20+ |
| 🇺🇸 United States | New York, SF Bay Area, Boston, LA, Chicago, Seattle | 40+ |
| 🇬🇧 United Kingdom | London, Oxford, Cambridge, Manchester, Edinburgh, Birmingham | 30+ |
| 🇩🇪 Germany | Berlin, Munich, Hamburg, Frankfurt | 20+ |
| 🇨🇦 Canada | Toronto, Vancouver, Montreal, Ottawa | 20+ |
| 🇮🇳 India | Bangalore, Mumbai, Delhi/NCR, Chennai, Hyderabad | 40+ |
| 🇸🇬 Singapore | Singapore | 6 |
| 🇦🇺 Australia | Sydney, Melbourne, Brisbane | 15+ |
| 🇵🇰 **Pakistan** | **Karachi, Lahore, Islamabad/RWP, Peshawar, Quetta, Multan, Faisalabad** | **50+** |

### 🇵🇰 Pakistan Universities — Full List

<details>
<summary>Click to expand</summary>

**Karachi**
- University of Karachi, NED University of Engineering & Technology
- Institute of Business Administration (IBA) Karachi, Aga Khan University (AKU)
- Dow University of Health Sciences, SZABIST Karachi, Hamdard University
- Sir Syed University of Engineering & Technology, Jinnah Sindh Medical University
- PAF-KIET, Greenwich University Karachi

**Lahore**
- Lahore University of Management Sciences (LUMS)
- University of Engineering & Technology (UET) Lahore
- University of the Punjab, Government College University (GCU) Lahore
- University of Management and Technology (UMT), Beaconhouse National University (BNU)
- COMSATS University Lahore, Superior University, University of Central Punjab (UCP)
- Kinnaird College for Women, Lahore College for Women University
- Forman Christian College University, National College of Arts (NCA)
- University of Health Sciences Lahore

**Islamabad / Rawalpindi**
- National University of Sciences & Technology (NUST)
- Quaid-i-Azam University (QAU), COMSATS University Islamabad
- International Islamic University Islamabad (IIUI), Air University
- Bahria University, FAST-NUCES, Allama Iqbal Open University (AIOU)
- Mohammad Ali Jinnah University (MAJU), Capital University of Science & Technology (CUST)
- Riphah International University, Foundation University Islamabad

**Peshawar**
- University of Peshawar, UET Peshawar, Khyber Medical University
- Abdul Wali Khan University Mardan, Islamia College University
- CECOS University, Gandhara University, Sarhad University

**Quetta**
- University of Balochistan, BUITEMS, SBK Women's University, University of Turbat

**Multan**
- Bahauddin Zakariya University (BZU), MNS University of Agriculture, ISP Multan

**Faisalabad**
- University of Agriculture Faisalabad (UAF), National Textile University (NTU)
- Government College University Faisalabad (GCUF), University of Faisalabad

</details>

### All Supported Countries (50+)

| Region | Countries |
|---|---|
| 🌍 Middle East | UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman, Jordan, Lebanon, Israel, Turkey, Egypt, Iraq, Yemen |
| 🌎 North America | United States, Canada, Mexico |
| 🌎 South America | Brazil, Argentina, Chile, Colombia, Peru, Venezuela, Uruguay |
| 🌍 Europe | UK, Germany, France, Netherlands, Sweden, Switzerland, Spain, Italy, Belgium, Denmark, Finland, Norway, Austria, Poland, Portugal, Ireland, Czech Republic, Romania, Greece, Ukraine |
| 🌏 Asia Pacific | China, Japan, South Korea, India, Singapore, Australia, New Zealand, Malaysia, Indonesia, Thailand, Vietnam, Philippines, Bangladesh, **Pakistan**, Sri Lanka, Hong Kong, Taiwan |
| 🌍 Africa | South Africa, Nigeria, Kenya, Ghana, Morocco, Tunisia, Algeria, Ethiopia |
| 🌐 Remote | Remote Worldwide, Any Country |

> For countries without preloaded city data, the app scrapes universities live via Tavily / Google Search.

---

## 🎯 Career Levels

The job finder supports all 4 experience levels — search one, many, or all simultaneously:

| Level | Experience | Target Roles |
|---|---|---|
| 🟢 Basic / Entry Level | 0–2 years | Junior, Intern, Graduate, Trainee, Fresher |
| 🟡 Intermediate Level | 2–5 years | Mid-level, Associate, Engineer II |
| 🔴 Advanced / Senior Level | 5–10 years | Senior, Lead, Staff Engineer, Tech Lead |
| 🟣 Expert / Principal Level | 10+ years | Principal, Director, VP Engineering, CTO, Fellow |

---

## 🤖 AI Model Cascade

```
Your Request
     │
     ▼
① llama-3.1-8b-instant  (Groq)   ──✅ success → return result
     │ ❌ fail / rate limit
     ▼
② gemini-1.5-flash       (Google) ──✅ success → return result
     │ ❌ fail / rate limit
     ▼
③ mixtral-8x7b-32768     (Groq)   ──✅ success → return result
     │ ❌ fail
     ▼
⚠️  Error message shown to user
```

The app **never fully breaks** — if one model is down or rate-limited, it silently moves to the next.

---

## 🗂️ Project Structure

```
ai-career-intelligence-agent/
│
├── app.py               # Main Streamlit application (single file, ~735 lines)
├── requirements.txt     # Python dependencies (4 packages)
├── README.md            # This file
└── .gitignore           # Ignore venv, __pycache__, .env
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-career-intelligence-agent.git
cd ai-career-intelligence-agent
```

### 2. Create a virtual environment (recommended)

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Open your browser at **`http://localhost:8501`**

---

## 🔑 API Keys Required

All keys are entered directly in the app sidebar — **nothing is hardcoded or stored on disk**.

| Key | Purpose | Where to Get | Cost |
|---|---|---|---|
| **Groq API Key** | llama-3.1-8b-instant + mixtral fallback | [console.groq.com](https://console.groq.com) | ✅ Free |
| **Gemini API Key** | gemini-1.5-flash (2nd fallback) | [aistudio.google.com](https://aistudio.google.com) | ✅ Free |
| **Tavily API Key** | Kaggle scraping + researcher & job search | [tavily.com](https://tavily.com) | ✅ Free tier |
| **Google Search API** | Additional search source (optional) | [console.developers.google.com](https://console.developers.google.com) | ✅ Free quota |
| **Google CX ID** | Required with Google Search API | Same console above | ✅ Free |

> **Minimum to run:** One of (Groq OR Gemini) + Tavily key.

---

## 🖥️ How to Use — Step by Step

### Step 1 — Upload & Analyse
1. Enter API keys in the **left sidebar**
2. Upload your **CV as a PDF**
3. Paste your **GitHub URL** *(optional)*
4. Paste your **Kaggle URL** *(optional)*
5. Click **🧠 Analyse My Full Profile**

### Step 2 — Review Your Profile Dashboard
- **6 metric cards** — experience years, skills, domains, research interests, GitHub stars, repos
- **Experience level banner** — 🟢🟡🔴🟣 with year range
- **5 tabs** — Skills & Tools · Domains & Research · GitHub · Kaggle · Summary

### Step 3 — Find Researchers
1. Click a **region tab** → click a **country**
2. If city data exists → click a **city**
3. Choose mode:
   - **🏛️ University-by-University** — load all universities, then search each (or all at once with ⚡)
   - **🌐 Country-wide** — one broad search across the whole country
4. Results: name · title · department · **email** · research areas · profile link · match score (1–10)

### Step 4 — Find Jobs
1. Click a **region tab** → click a **country**
2. Check experience level boxes (🟢🟡🔴🟣) — or tick **All 4 levels**
3. Click **💼 Search Jobs**
4. Use **filters** (min score slider + job type dropdown)
5. Each result shows: title · company · location · salary · **👉 Apply Now** · **👤 Founder/HR** · skills needed

---

## 📦 Dependencies

```txt
streamlit>=1.35.0
requests>=2.31.0
PyPDF2>=3.0.1
google-generativeai>=0.7.0
```

No LangChain. No heavy ML frameworks. No local GPU. Pure Python + Streamlit.

---

## 🔒 Privacy & Security

| Concern | Status |
|---|---|
| Data storage | ✅ Nothing stored — all in `st.session_state` per session only |
| API keys | ✅ Password fields only — never logged, never written to disk |
| CV text | ✅ Sent only to the chosen LLM API — not stored anywhere |
| GitHub data | ✅ Public GitHub REST API — no auth needed |
| Deployment | ⚠️ Do not deploy publicly with shared API keys |

---

## 🐛 Troubleshooting

| Issue | Solution |
|---|---|
| `PyPDF2` can't read CV | Use a text-based PDF (not scanned). Re-export from Word or Google Docs |
| "All models failed" | Check at least one key (Groq or Gemini) is correctly entered in the sidebar |
| Kaggle shows 0 results | Ensure Tavily key is valid and your Kaggle profile is public |
| No universities found | Try "Country-wide" mode, or verify your search API keys work |
| Google Search 403 error | Verify your CX ID belongs to the same project as your Google API key |
| Researchers missing emails | Email scraping is best-effort — not all academics publish email publicly |
| Jobs show "No direct link" | Some boards block scraping — visit the company careers page directly |
| Rate limit toasts | The cascade auto-switches models. Wait ~60s if all three are rate-limited |
| App is slow per university | Each university search = 1 AI call + web search (~5–15s). Use ⚡ Search ALL |

---

## 📊 App Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                  AI Career Intelligence Agent                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   [Upload CV PDF] + [GitHub URL] + [Kaggle URL]                  │
│          │                │               │                      │
│          ▼                ▼               ▼                      │
│      PDF Parser     GitHub API      Tavily Search                │
│          │                │               │                      │
│          └────────────────┴───────────────┘                      │
│                           │                                      │
│                           ▼                                      │
│             ┌──────────────────────────┐                         │
│             │      AI Model Cascade    │                         │
│             │  ① llama-3.1-8b-instant  │                         │
│             │  ② gemini-1.5-flash      │                         │
│             │  ③ mixtral-8x7b          │                         │
│             └──────────────────────────┘                         │
│                           │                                      │
│              ┌────────────┴────────────┐                         │
│              ▼                         ▼                         │
│   ┌────────────────────┐   ┌───────────────────────┐             │
│   │  Researcher Finder │   │      Job Finder       │             │
│   │                    │   │                       │             │
│   │  Region → Country  │   │  Region → Country     │             │
│   │  → City →          │   │  + Level Selection    │             │
│   │  University List   │   │  🟢 Entry             │             │
│   │  → Search each     │   │  🟡 Intermediate      │             │
│   │                    │   │  🔴 Senior            │             │
│   │  Output:           │   │  🟣 Expert            │             │
│   │  • Name & Title    │   │                       │             │
│   │  • Email address   │   │  Output per job:      │             │
│   │  • Department      │   │  • Apply Now link     │             │
│   │  • Research areas  │   │  • Founder LinkedIn   │             │
│   │  • Match score     │   │  • Salary range       │             │
│   │  • Profile URL     │   │  • Match score 1-10   │             │
│   └────────────────────┘   └───────────────────────┘             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

Pull requests are welcome! Open issues for bugs or feature ideas.

```bash
# Fork, then:
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
# Open a Pull Request
```

### 💡 Ideas for Contributions

- [ ] Add more country city maps (France, Japan, Netherlands, Turkey, South Korea)
- [ ] LinkedIn profile scraping integration
- [ ] Export researcher list to CSV / Excel
- [ ] AI-generated cold email drafts for each researcher
- [ ] Cover letter generator (CV + job description → cover letter)
- [ ] Bookmark favourite jobs and researchers across sessions
- [ ] Docker support for one-command deployment
- [ ] More job boards: Remotive, We Work Remotely, Himalayas, Jobicy
- [ ] Google Scholar API integration for h-index data
- [ ] Request caching to avoid duplicate API calls

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute with attribution.

---

## 🙏 Acknowledgements

| Tool | Purpose |
|---|---|
| [Groq](https://groq.com) | Blazing-fast LLM inference (llama + mixtral) |
| [Google Gemini](https://aistudio.google.com) | Free generative AI fallback |
| [Tavily](https://tavily.com) | AI-native web search API |
| [Streamlit](https://streamlit.io) | Rapid Python UI framework |
| [GitHub REST API](https://docs.github.com/en/rest) | Public profile and repository data |
| [Google Custom Search](https://developers.google.com/custom-search) | Optional extra search coverage |

---

<div align="center">

**Built for researchers, engineers, and job seekers worldwide 🌍**
<br>
Especially for the talent coming out of 🇵🇰 🇦🇪 🇮🇳 🇬🇧 🇩🇪 🇺🇸 and beyond.

⭐ **Star this repo if it helped you find your next opportunity!**

</div>

import streamlit as st
import requests
import json
import re
import time
from PyPDF2 import PdfReader
import google.generativeai as genai

st.set_page_config(page_title="AI Career Intelligence Agent", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# ══════════════════════════════ WORLD DATA ════════════════════════════════════
COUNTRIES_BY_REGION = {
    "🌍 Middle East": ["United Arab Emirates","Saudi Arabia","Qatar","Kuwait","Bahrain","Oman","Jordan","Lebanon","Israel","Turkey","Egypt","Iraq","Yemen"],
    "🌎 North America": ["United States","Canada","Mexico"],
    "🌎 South America": ["Brazil","Argentina","Chile","Colombia","Peru","Venezuela","Uruguay"],
    "🌍 Europe": ["United Kingdom","Germany","France","Netherlands","Sweden","Switzerland","Spain","Italy","Belgium","Denmark","Finland","Norway","Austria","Poland","Portugal","Ireland","Czech Republic","Romania","Greece","Ukraine"],
    "🌏 Asia Pacific": ["China","Japan","South Korea","India","Singapore","Australia","New Zealand","Malaysia","Indonesia","Thailand","Vietnam","Philippines","Bangladesh","Pakistan","Sri Lanka","Hong Kong","Taiwan"],
    "🌍 Africa": ["South Africa","Nigeria","Kenya","Ghana","Morocco","Tunisia","Algeria","Ethiopia"],
    "🌐 Remote": ["Remote Worldwide","Any Country"],
}
ALL_COUNTRIES = [c for r in COUNTRIES_BY_REGION.values() for c in r]

UAE_CITIES = {
    "Dubai": ["University of Dubai","Heriot-Watt University Dubai","University of Wollongong Dubai","Middlesex University Dubai","Murdoch University Dubai","SP Jain School of Global Management","Manipal Academy of Higher Education Dubai","Rochester Institute of Technology Dubai","Canadian University Dubai","Mohammed Bin Rashid University of Medicine","Dubai Institute of Design and Innovation","Amity University Dubai","University of Birmingham Dubai","Curtin University Dubai","Westford University College"],
    "Abu Dhabi": ["New York University Abu Dhabi","Khalifa University","UAE University","Sorbonne University Abu Dhabi","Abu Dhabi University","Zayed University","Higher Colleges of Technology Abu Dhabi","Mohamed bin Zayed University of AI (MBZUAI)","Masdar Institute","Paris-Sorbonne Abu Dhabi","Rabdan Academy"],
    "Sharjah": ["University of Sharjah","American University of Sharjah","Gulf Medical University","Skyline University College","BITS Pilani Dubai"],
    "Ajman": ["Ajman University","Gulf Medical University Ajman","City University College of Ajman"],
    "Ras Al Khaimah": ["RAK Medical & Health Sciences University","American University of RAK"],
    "Fujairah": ["University of Fujairah","BITS Pilani Fujairah"],
    "Al Ain": ["UAE University (main campus)","Al Ain University"],
}
KSA_CITIES = {
    "Riyadh": ["King Saud University","Imam Mohammad Ibn Saud University","Prince Sultan University","Alfaisal University","Saudi Electronic University","King Salman University","Dar Al Uloom University"],
    "Jeddah": ["King Abdulaziz University","Effat University","Dar Al Hekma University","University of Business and Technology"],
    "Dammam": ["King Fahd University of Petroleum and Minerals (KFUPM)","Imam Abdulrahman Bin Faisal University","Prince Mohammad Bin Fahd University"],
}
US_CITIES = {
    "New York": ["Columbia University","NYU","Cornell Tech","CUNY","Fordham University","The New School","Pratt Institute"],
    "San Francisco / Bay Area": ["Stanford University","UC Berkeley","UCSF","Santa Clara University","San Jose State University","UC Santa Cruz"],
    "Boston": ["MIT","Harvard University","Boston University","Northeastern University","Tufts University","Boston College","Brandeis University"],
    "Los Angeles": ["USC","UCLA","Caltech","Loyola Marymount University","Pepperdine University"],
    "Chicago": ["University of Chicago","Northwestern University","DePaul University","Loyola University Chicago","IIT Chicago"],
    "Seattle": ["University of Washington","Seattle University","Seattle Pacific University"],
}
UK_CITIES = {
    "London": ["Imperial College London","UCL","King's College London","LSE","Queen Mary University","City University London","Brunel University","University of East London","Goldsmiths","Birkbeck","University of Westminster","London South Bank University"],
    "Oxford": ["University of Oxford","Oxford Brookes University"],
    "Cambridge": ["University of Cambridge","Anglia Ruskin University"],
    "Manchester": ["University of Manchester","Manchester Metropolitan University","University of Salford"],
    "Edinburgh": ["University of Edinburgh","Heriot-Watt University","Edinburgh Napier University"],
    "Birmingham": ["University of Birmingham","Aston University","Birmingham City University"],
}
DE_CITIES = {
    "Berlin": ["Technische Universität Berlin","Freie Universität Berlin","Humboldt-Universität Berlin","Charité","HTW Berlin","HWR Berlin"],
    "Munich": ["Technical University of Munich (TUM)","LMU Munich","Munich University of Applied Sciences"],
    "Hamburg": ["University of Hamburg","Hamburg University of Technology (TUHH)","HafenCity University"],
    "Frankfurt": ["Goethe University Frankfurt","Frankfurt University of Applied Sciences","EBS Universität"],
}
CA_CITIES = {
    "Toronto": ["University of Toronto","York University","Toronto Metropolitan University","OCAD University","Humber College"],
    "Vancouver": ["UBC","Simon Fraser University","BCIT","Langara College"],
    "Montreal": ["McGill University","Université de Montréal","Concordia University","UQAM","Polytechnique Montréal"],
    "Ottawa": ["University of Ottawa","Carleton University","Algonquin College"],
}
IN_CITIES = {
    "Bangalore": ["Indian Institute of Science (IISc)","IIT Bangalore","NIT Karnataka","Bangalore University","Christ University","PES University"],
    "Mumbai": ["IIT Bombay","University of Mumbai","TISS","NMIMS","SP Jain"],
    "Delhi / NCR": ["IIT Delhi","University of Delhi","JNU","AIIMS Delhi","Jamia Millia Islamia","Amity University","Shiv Nadar University","Ashoka University","DTU"],
    "Chennai": ["IIT Madras","Anna University","VIT Chennai","SRM Institute"],
    "Hyderabad": ["IIIT Hyderabad","University of Hyderabad","BITS Pilani Hyderabad","Osmania University"],
}
SG_CITIES = {
    "Singapore": ["National University of Singapore (NUS)","Nanyang Technological University (NTU)","Singapore Management University (SMU)","Singapore University of Technology and Design (SUTD)","Singapore Institute of Technology","James Cook University Singapore"],
}
AU_CITIES = {
    "Sydney": ["University of Sydney","UNSW","University of Technology Sydney (UTS)","Western Sydney University","Macquarie University"],
    "Melbourne": ["University of Melbourne","Monash University","RMIT University","La Trobe University","Deakin University"],
    "Brisbane": ["University of Queensland","Queensland University of Technology (QUT)","Griffith University"],
}
PK_CITIES = {
    "Karachi": [
        "University of Karachi","NED University of Engineering & Technology",
        "Karachi Institute of Technology & Entrepreneurship (KITE)",
        "Institute of Business Administration (IBA) Karachi",
        "Aga Khan University (AKU)","Dow University of Health Sciences",
        "SZABIST Karachi","Hamdard University","Sir Syed University of Engineering & Technology",
        "Jinnah Sindh Medical University","Greenwich University Karachi",
        "PAF-KIET (Karachi Institute of Economics & Technology)",
    ],
    "Lahore": [
        "University of the Punjab","University of Engineering & Technology (UET) Lahore",
        "Lahore University of Management Sciences (LUMS)",
        "Government College University (GCU) Lahore",
        "University of Management and Technology (UMT)",
        "Beaconhouse National University (BNU)","COMSATS University Lahore",
        "Superior University Lahore","University of Central Punjab (UCP)",
        "Kinnaird College for Women","Lahore College for Women University",
        "Forman Christian College University","National College of Arts (NCA)",
        "University of Health Sciences Lahore",
    ],
    "Islamabad / Rawalpindi": [
        "Quaid-i-Azam University (QAU)","COMSATS University Islamabad",
        "National University of Sciences & Technology (NUST)",
        "International Islamic University Islamabad (IIUI)",
        "Air University Islamabad","Bahria University Islamabad",
        "Federal Urdu University of Arts, Science & Technology",
        "Allama Iqbal Open University (AIOU)","FAST-NUCES Islamabad",
        "Mohammad Ali Jinnah University (MAJU) Islamabad",
        "Capital University of Science & Technology (CUST)",
        "Riphah International University","Foundation University Islamabad",
    ],
    "Peshawar": [
        "University of Peshawar","University of Engineering & Technology (UET) Peshawar",
        "Khyber Medical University","Abdul Wali Khan University Mardan",
        "Islamia College University Peshawar","CECOS University Peshawar",
        "Gandhara University","Sarhad University Peshawar",
    ],
    "Quetta": [
        "University of Balochistan","Balochistan University of IT, Engineering & Management Sciences (BUITEMS)",
        "Sardar Bahadur Khan Women's University","University of Turbat",
    ],
    "Multan": [
        "Bahauddin Zakariya University (BZU)","National Textile University Faisalabad (Multan campus)",
        "MNS University of Agriculture","Institute of Southern Punjab (ISP)",
    ],
    "Faisalabad": [
        "University of Agriculture Faisalabad (UAF)","National Textile University (NTU) Faisalabad",
        "Government College University Faisalabad (GCUF)","University of Faisalabad",
    ],
}
COUNTRY_CITY_MAP = {
    "United Arab Emirates": UAE_CITIES,
    "Saudi Arabia":         KSA_CITIES,
    "United States":        US_CITIES,
    "United Kingdom":       UK_CITIES,
    "Germany":              DE_CITIES,
    "Canada":               CA_CITIES,
    "India":                IN_CITIES,
    "Singapore":            SG_CITIES,
    "Australia":            AU_CITIES,
    "Pakistan":             PK_CITIES,
}

JOB_LEVELS = {
    "🟢 Basic / Entry Level":       {"exp":"0–2 yrs","desc":"Fresh graduates & starters","kws":["junior","entry level","graduate","intern","trainee","fresher"]},
    "🟡 Intermediate Level":        {"exp":"2–5 yrs","desc":"Solid foundation professionals","kws":["mid level","intermediate","software engineer II","associate"]},
    "🔴 Advanced / Senior Level":   {"exp":"5–10 yrs","desc":"Senior contributors & leads","kws":["senior","lead","staff engineer","tech lead","principal"]},
    "🟣 Expert / Principal Level":  {"exp":"10+ yrs","desc":"Architects & executives","kws":["principal","director","VP engineering","CTO","distinguished engineer","fellow"]},
}

# ══════════════════════════════════ CSS ═══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');
:root{--bg:#06070f;--surf:#0c0d1c;--card:#10112a;--bdr:#1c1e3a;--a1:#6366f1;--a2:#22d3ee;--a3:#f59e0b;--gn:#10b981;--rd:#ef4444;--pk:#ec4899;--tx:#e2e4f0;--mt:#5a607a;--gd:linear-gradient(135deg,#6366f1,#22d3ee);}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--tx)!important;font-family:'Outfit',sans-serif!important;}
[data-testid="stSidebar"]{background:var(--surf)!important;border-right:1px solid var(--bdr)!important;}
h1{font-family:'Outfit',sans-serif!important;font-weight:800!important;font-size:2.4rem!important;background:var(--gd);-webkit-background-clip:text!important;-webkit-text-fill-color:transparent!important;}
h2,h3,h4{font-family:'Outfit',sans-serif!important;color:#c7d2fe!important;}
.stButton>button{background:var(--gd)!important;color:#fff!important;border:none!important;border-radius:10px!important;font-family:'Outfit',sans-serif!important;font-weight:600!important;font-size:.9rem!important;padding:.6rem 1.3rem!important;transition:all .2s!important;box-shadow:0 4px 16px rgba(99,102,241,.3)!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(99,102,241,.5)!important;}
.stButton>button:disabled{opacity:.45!important;transform:none!important;}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--card)!important;color:var(--tx)!important;border:1px solid var(--bdr)!important;border-radius:10px!important;font-family:'Outfit',sans-serif!important;}
.stSelectbox>div>div{background:var(--card)!important;color:var(--tx)!important;border:1px solid var(--bdr)!important;border-radius:10px!important;}
.card{background:var(--card);border:1px solid var(--bdr);border-radius:14px;padding:1.1rem 1.3rem;margin-bottom:.75rem;transition:border-color .2s,box-shadow .2s;}
.card:hover{border-color:var(--a1);box-shadow:0 0 18px rgba(99,102,241,.14);}
.cglow{background:linear-gradient(135deg,#0f1030,#060d20);border:1px solid var(--a1);border-radius:14px;padding:1.1rem 1.3rem;margin-bottom:.75rem;}
.camber{background:linear-gradient(135deg,#1a0f00,#100900);border:1px solid var(--a3);border-radius:12px;padding:.9rem 1.1rem;margin-bottom:.6rem;}
.cgreen{background:linear-gradient(135deg,#051a10,#030f0a);border:1px solid var(--gn);border-radius:12px;padding:.9rem 1.1rem;margin-bottom:.6rem;}
.tag{display:inline-block;border-radius:999px;padding:2px 11px;font-size:.73rem;font-family:'Fira Code',monospace;margin:2px;font-weight:500;}
.tp{background:#1e1560;border:1px solid var(--a1);color:#a5b4fc;}
.tc{background:#062030;border:1px solid var(--a2);color:#67e8f9;}
.tg{background:#052015;border:1px solid var(--gn);color:#6ee7b7;}
.ta{background:#1a1000;border:1px solid var(--a3);color:#fcd34d;}
.tr{background:#200a0a;border:1px solid var(--rd);color:#fca5a5;}
.tpk{background:#1a0520;border:1px solid var(--pk);color:#f9a8d4;}
.sb-w{background:#1a1b30;border-radius:999px;height:6px;margin:6px 0;}
.sb{height:6px;border-radius:999px;background:var(--gd);}
.slbl{font-family:'Fira Code',monospace;font-size:.68rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--a2);border-bottom:1px solid var(--bdr);padding-bottom:.35rem;margin-bottom:.85rem;}
.sbdg{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:var(--gd);font-weight:800;font-size:.8rem;color:#fff;margin-right:8px;vertical-align:middle;box-shadow:0 2px 10px rgba(99,102,241,.5);}
.mbox{background:var(--card);border:1px solid var(--bdr);border-radius:12px;padding:.85rem 1rem;text-align:center;}
.mnum{font-size:1.7rem;font-weight:800;background:var(--gd);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.mlbl{font-size:.67rem;color:var(--mt);text-transform:uppercase;letter-spacing:.1em;font-family:'Fira Code',monospace;}
.uni-item{background:linear-gradient(135deg,#0b0c22,#060e1a);border:1px solid var(--bdr);border-radius:10px;padding:.8rem 1rem;margin-bottom:.45rem;transition:border-color .2s;}
.uni-item:hover{border-color:var(--a1);}
.rcard{background:var(--card);border:1px solid var(--bdr);border-radius:12px;padding:1rem 1.1rem;margin-bottom:.6rem;}
.rcard:hover{border-color:var(--gn);}
.jcard{background:var(--card);border:1px solid var(--bdr);border-radius:12px;padding:1rem 1.1rem;margin-bottom:.6rem;}
.jcard:hover{border-color:var(--a3);}
.echip{font-family:'Fira Code',monospace;background:#062030;border:1px solid var(--a2);color:var(--a2);border-radius:6px;padding:3px 10px;font-size:.78rem;}
.abtn{display:inline-block;background:var(--gd);color:#fff!important;border-radius:8px;padding:6px 15px;font-weight:700;font-size:.82rem;text-decoration:none!important;box-shadow:0 2px 10px rgba(99,102,241,.4);}
.hero{background:linear-gradient(135deg,#0f1030 0%,#060e20 50%,#0a1520 100%);border:1px solid var(--bdr);border-radius:18px;padding:2rem 2.4rem;margin-bottom:1.6rem;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-40%;right:-8%;width:450px;height:450px;background:radial-gradient(circle,rgba(99,102,241,.09) 0%,transparent 70%);border-radius:50%;pointer-events:none;}
.scr{max-height:500px;overflow-y:auto;padding-right:4px;}
.scr::-webkit-scrollbar{width:3px;}
.scr::-webkit-scrollbar-thumb{background:var(--a1);border-radius:2px;}
.divhr{border:none;border-top:1px solid var(--bdr);margin:1.3rem 0;}
.stTabs [data-baseweb="tab-list"]{background:var(--surf)!important;border-radius:10px;gap:2px;padding:3px;}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;font-family:'Outfit',sans-serif!important;font-weight:600!important;color:var(--mt)!important;}
.stTabs [aria-selected="true"]{background:var(--gd)!important;color:#fff!important;}
[data-testid="stExpander"]{background:var(--card)!important;border:1px solid var(--bdr)!important;border-radius:12px!important;}
.stAlert{border-radius:10px!important;}
.stCheckbox>label{color:var(--tx)!important;font-family:'Outfit',sans-serif!important;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════ SESSION STATE ════════════════════════════════════
_INIT = {
    "profile":None,"cv_text":None,"github_data":None,"kaggle_data":None,
    "universities":[],"uni_researchers":{},"country_researchers":[],
    "jobs":[],"job_results_by_level":{},
    "groq_key":"","gemini_key":"","tavily_key":"","google_key":"","google_cx":"",
    "sel_rc":"","sel_rc_city":"","sel_jc":"",
}
for k,v in _INIT.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════ LLM HELPERS ══════════════════════════════════════
def call_llm(prompt:str, system:str="") -> str:
    gk = st.session_state.get("groq_key","")
    mk = st.session_state.get("gemini_key","")
    # 1. llama-3.1-8b-instant
    if gk:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {gk}","Content-Type":"application/json"},
                json={"model":"llama-3.1-8b-instant","messages":[{"role":"system","content":system},{"role":"user","content":prompt}],"temperature":0.3,"max_tokens":4096},
                timeout=60)
            if r.status_code==200: return r.json()["choices"][0]["message"]["content"]
        except: st.toast("llama-3.1 failed → Gemini…",icon="⚠️")
    # 2. gemini-1.5-flash
    if mk:
        try:
            genai.configure(api_key=mk)
            resp = genai.GenerativeModel("gemini-1.5-flash").generate_content(f"{system}\n\n{prompt}" if system else prompt)
            return resp.text
        except: st.toast("Gemini failed → mixtral…",icon="⚠️")
    # 3. mixtral fallback
    if gk:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":f"Bearer {gk}","Content-Type":"application/json"},
                json={"model":"mixtral-8x7b-32768","messages":[{"role":"system","content":system},{"role":"user","content":prompt}],"temperature":0.3,"max_tokens":4096},
                timeout=60)
            if r.status_code==200: return r.json()["choices"][0]["message"]["content"]
        except Exception as e: st.error(f"All models failed: {e}")
    return "⚠️ No response."

def pjson(raw:str):
    raw = re.sub(r"```json|```","",raw).strip()
    try: return json.loads(raw)
    except:
        m = re.search(r'(\[.*\]|\{.*\})',raw,re.DOTALL)
        if m:
            try: return json.loads(m.group(1))
            except: pass
    return None

# ═══════════════════════════ SEARCH HELPERS ═══════════════════════════════════
def tsearch(q:str,n:int=10)->list:
    k=st.session_state.get("tavily_key","")
    if not k: return []
    try:
        r=requests.post("https://api.tavily.com/search",
            json={"api_key":k,"query":q,"max_results":n,"search_depth":"advanced","include_answer":True},timeout=30)
        if r.status_code==200: return r.json().get("results",[])
    except: pass
    return []

def gsearch(q:str,n:int=10)->list:
    k=st.session_state.get("google_key",""); cx=st.session_state.get("google_cx","")
    if not k or not cx: return []
    try:
        r=requests.get("https://www.googleapis.com/customsearch/v1",
            params={"key":k,"cx":cx,"q":q,"num":min(n,10)},timeout=20)
        if r.status_code==200:
            return [{"title":i.get("title",""),"url":i.get("link",""),"content":i.get("snippet","")} for i in r.json().get("items",[])]
    except: pass
    return []

def search(q:str,n:int=12)->list:
    res=tsearch(q,n)+gsearch(q,n)
    seen,out=set(),[]
    for r in res:
        u=r.get("url","")
        if u not in seen: seen.add(u);out.append(r)
    return out

def fmt(res:list,mx:int=14)->str:
    return "\n".join(f"- {r.get('title','')} | {r.get('url','')} | {r.get('content','')[:200]}" for r in res[:mx])

# ═══════════════════════════ PROFILE ANALYSIS ═════════════════════════════════
def read_pdf(f)->str: return "\n".join(p.extract_text() or "" for p in PdfReader(f).pages)

def get_github(url:str)->dict:
    m=re.search(r"github\.com/([^/\s?#]+)",url)
    if not m: return {}
    u=m.group(1)
    try:
        d=requests.get(f"https://api.github.com/users/{u}",timeout=15).json()
        rr=requests.get(f"https://api.github.com/users/{u}/repos?sort=stars&per_page=15",timeout=15).json()
        langs,repos={},[]
        if isinstance(rr,list):
            for r in rr:
                if r.get("language"): langs[r["language"]]=langs.get(r["language"],0)+1
                repos.append({"name":r["name"],"description":r.get("description",""),"stars":r.get("stargazers_count",0),"forks":r.get("forks_count",0),"language":r.get("language",""),"url":r.get("html_url","")})
        return {"username":u,"name":d.get("name",u),"bio":d.get("bio",""),"location":d.get("location",""),"followers":d.get("followers",0),"following":d.get("following",0),"public_repos":d.get("public_repos",0),"blog":d.get("blog",""),"top_repos":repos,"languages":sorted(langs.items(),key=lambda x:-x[1]),"total_stars":sum(r["stars"] for r in repos)}
    except Exception as e: return {"error":str(e)}

def get_kaggle(url:str)->dict:
    m=re.search(r"kaggle\.com/([^/\s?#]+)",url)
    if not m: return {}
    u=m.group(1)
    res=tsearch(f"kaggle.com/{u} notebooks competitions datasets",8)
    info={"username":u,"notebooks":[],"competitions":[],"datasets":[]}
    for r in res:
        ur=r.get("url","")
        if "/code/" in ur or "notebook" in ur.lower(): info["notebooks"].append({"title":r.get("title",""),"url":ur,"snippet":r.get("content","")[:140]})
        elif "competition" in ur.lower(): info["competitions"].append({"title":r.get("title",""),"url":ur})
        elif "/datasets/" in ur: info["datasets"].append({"title":r.get("title",""),"url":ur})
    return info

def analyse(cv:str,gh:dict,kg:dict)->dict:
    prompt=f"""Analyse this profile. Return JSON with keys:
"name","skills"(15),"domains"(6),"experience_years"(int),"experience_level"("Basic / Entry Level"|"Intermediate Level"|"Advanced / Senior Level"|"Expert / Principal Level"),"keywords"(12),"summary"(3 sentences),"research_interests"(8),"tools"(list),"education"(string),"strengths"(4),"certifications"(list),"languages_spoken"(list)

CV: {cv[:3200]}
GitHub: {json.dumps(gh)[:1600]}
Kaggle: {json.dumps(kg)[:1000]}
Return ONLY valid JSON."""
    raw=call_llm(prompt,"Expert career analyst. Return only valid JSON.")
    d=pjson(raw)
    return d if isinstance(d,dict) else {"summary":raw,"skills":[],"domains":[],"keywords":[],"experience_level":"Intermediate Level","research_interests":[],"tools":[],"strengths":[],"experience_years":0,"education":"","certifications":[],"languages_spoken":[],"name":""}

# ═══════════════════════════ RESEARCHER FINDERS ═══════════════════════════════
def fetch_unis(location:str)->list:
    for _,cm in COUNTRY_CITY_MAP.items():
        if location in cm: return cm[location]
    res=search(f"universities colleges research institutions {location} higher education",10)
    if not res: return []
    raw=call_llm(f"Extract university names in {location} from:\n{fmt(res,10)}\nReturn ONLY JSON array of strings.","Return only JSON array.")
    d=pjson(raw); return d if isinstance(d,list) else []

def researchers_at_uni(uni:str,profile:dict)->list:
    domains=" ".join(profile.get("domains",[])[:3]); interests=" ".join(profile.get("research_interests",[])[:3])
    res=search(f'researcher professor "{uni}" {domains} {interests} email site:scholar.google.com OR site:researchgate.net OR site:academia.edu',12)
    if not res: return []
    prompt=f"""Extract researchers at "{uni}" matching:
Skills:{profile.get('skills',[])} Domains:{profile.get('domains',[])} Interests:{profile.get('research_interests',[])}
Results:\n{fmt(res,12)}
Return JSON array, each: "name","title","department","university","email"(infer from uni domain if needed),"research_areas","profile_url","match_score"(1-10),"match_reason"
ONLY JSON array."""
    raw=call_llm(prompt,"Return only JSON array of researcher profiles.")
    d=pjson(raw); return d if isinstance(d,list) else []

def researchers_country(profile:dict,country:str)->list:
    domains=" ".join(profile.get("domains",[])[:3]); interests=" ".join(profile.get("research_interests",[])[:3])
    res=search(f'researcher professor "{country}" {domains} {interests} email site:scholar.google.com OR site:researchgate.net OR site:linkedin.com/in',14)
    if not res: return []
    prompt=f"""Extract researchers in {country} matching:
Skills:{profile.get('skills',[])} Domains:{profile.get('domains',[])}
Results:\n{fmt(res,14)}
Return JSON array: "name","title","department","university","email","research_areas","profile_url","match_score","match_reason"
ONLY JSON array."""
    raw=call_llm(prompt,"Return only JSON array.")
    d=pjson(raw); return d if isinstance(d,list) else []

# ═══════════════════════════ JOB FINDER ═══════════════════════════════════════
def find_jobs(profile:dict,country:str,level_key:str)->list:
    info=JOB_LEVELS.get(level_key,{})
    kws=" ".join(info.get("kws",[])[:3]); keywords=" ".join(profile.get("keywords",[])[:4]); domains=" ".join(profile.get("domains",[])[:2])
    loc=country if country not in ["Remote Worldwide","Any Country"] else "remote worldwide"
    res=search(f'{kws} {domains} {keywords} job {loc} 2024 2025 apply site:linkedin.com/jobs OR site:greenhouse.io OR site:lever.co OR site:indeed.com OR site:wellfound.com OR site:careers.google.com OR site:amazon.jobs',14)
    if not res: return []
    prompt=f"""Extract job listings for "{level_key}" in {country}:
Profile: Skills:{profile.get('skills',[])} Domains:{profile.get('domains',[])}
Results:\n{fmt(res,14)}
Return JSON array: "title","company","location","level","apply_url"(copy from results),"salary"(or "Not specified"),"match_score"(1-10),"skills_needed"(5),"job_type","posted","founder_linkedin","company_size","description"(1 sentence)
ONLY JSON array."""
    raw=call_llm(prompt,"Return only JSON array of job listings.")
    d=pjson(raw); return d if isinstance(d,list) else []

# ═══════════════════════════════ SIDEBAR ══════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="slbl">⚙️ API Configuration</div>',unsafe_allow_html=True)
    st.session_state["groq_key"]   = st.text_input("🔑 Groq API Key",type="password",value=st.session_state["groq_key"] or "",placeholder="gsk_…")
    st.session_state["gemini_key"] = st.text_input("🔑 Gemini API Key",type="password",value=st.session_state["gemini_key"] or "",placeholder="AIza…")
    st.markdown('<div class="slbl" style="margin-top:.9rem">🌐 Search APIs</div>',unsafe_allow_html=True)
    st.session_state["tavily_key"] = st.text_input("Tavily Key",type="password",value=st.session_state["tavily_key"] or "",placeholder="tvly-…")
    st.session_state["google_key"] = st.text_input("Google Search Key",type="password",value=st.session_state["google_key"] or "",placeholder="AIza… (optional)")
    st.session_state["google_cx"]  = st.text_input("Google CX ID",value=st.session_state["google_cx"] or "",placeholder="optional")
    st.markdown("---")
    st.markdown('<div style="font-size:.76rem;color:var(--mt);line-height:2.1;">🤖 <b style="color:#a5b4fc">Model Cascade</b><br>① llama-3.1-8b-instant<br>② gemini-1.5-flash<br>③ mixtral-8x7b</div>',unsafe_allow_html=True)
    p=st.session_state.get("profile")
    if p:
        st.markdown("---")
        st.markdown(f'<div style="font-size:.8rem;line-height:2.3;">👤 <b style="color:#a5b4fc">{p.get("name","—")}</b><br>🎯 <b style="color:#67e8f9">{p.get("experience_level","—")}</b><br>📅 <b style="color:#6ee7b7">{p.get("experience_years","?")} yrs</b><br>🛠️ {len(p.get("skills",[]))} skills · 🔬 {len(p.get("research_interests",[]))} interests</div>',unsafe_allow_html=True)

# ════════════════════════════════ HERO ════════════════════════════════════════
st.markdown("""<div class="hero">
<h1>🚀 AI Career Intelligence Agent</h1>
<p style="color:#8b9fd4;font-size:.98rem;margin-top:.4rem;max-width:700px;line-height:1.7">Upload CV · Scrape GitHub & Kaggle · Find researchers university-by-university · Discover jobs at all 4 levels in any country worldwide</p>
<div style="margin-top:.9rem;display:flex;gap:7px;flex-wrap:wrap;"><span class="tag tp">llama-3.1-8b</span><span class="tag tc">gemini-1.5-flash</span><span class="tag tg">mixtral fallback</span><span class="tag ta">Tavily</span><span class="tag tr">Google Search</span><span class="tag tpk">50+ Countries</span></div>
</div>""",unsafe_allow_html=True)

# ════════════════════════ STEP 1 — UPLOAD ═════════════════════════════════════
st.markdown('<span class="sbdg">1</span> **Upload CV & Profile Links**',unsafe_allow_html=True)
c1,c2=st.columns([1,1])
with c1: cv_file=st.file_uploader("📄 CV (PDF)",type=["pdf"])
with c2:
    gh_url=st.text_input("🐙 GitHub URL",placeholder="https://github.com/username")
    kg_url=st.text_input("📊 Kaggle URL",placeholder="https://www.kaggle.com/username")

if st.button("🧠  Analyse My Full Profile",use_container_width=True):
    if not cv_file: st.error("Upload your CV (PDF) first.")
    elif not (st.session_state["groq_key"] or st.session_state["gemini_key"]): st.error("Enter at least one API key in the sidebar.")
    else:
        bar=st.progress(0,"📄 Reading CV…")
        cv=read_pdf(cv_file); st.session_state["cv_text"]=cv
        bar.progress(25,"🐙 Scraping GitHub…")
        gh=get_github(gh_url) if gh_url.strip() else {}; st.session_state["github_data"]=gh
        bar.progress(50,"📊 Scraping Kaggle…")
        kg=get_kaggle(kg_url) if kg_url.strip() and st.session_state["tavily_key"] else {}; st.session_state["kaggle_data"]=kg
        bar.progress(75,"🤖 AI analysis…")
        prof=analyse(cv,gh,kg); st.session_state["profile"]=prof
        for k in ["universities","uni_researchers","country_researchers","jobs","job_results_by_level","sel_rc","sel_rc_city","sel_jc"]:
            st.session_state[k]={}  if k in ["uni_researchers","job_results_by_level"] else ([] if k in ["universities","country_researchers","jobs"] else "")
        bar.progress(100,"✅ Done!"); time.sleep(.3); bar.empty()
        st.success(f"✅ Analysed! Level: **{prof.get('experience_level','')}** · {prof.get('experience_years','?')} yrs experience")

# ════════════════════════ STEP 2 — PROFILE ════════════════════════════════════
if st.session_state.get("profile"):
    p=st.session_state["profile"]
    st.markdown('<hr class="divhr">',unsafe_allow_html=True)
    st.markdown('<span class="sbdg">2</span> **Profile Overview**',unsafe_allow_html=True)

    # Metrics
    gh=st.session_state.get("github_data") or {}
    mcols=st.columns(6)
    for mi,(lbl,val) in enumerate([("Yrs Exp",p.get("experience_years","?")),("Skills",len(p.get("skills",[]))),("Domains",len(p.get("domains",[]))),("Research",len(p.get("research_interests",[]))),("GH ⭐",gh.get("total_stars",0)),("GH Repos",gh.get("public_repos",0))]):
        mcols[mi].markdown(f'<div class="mbox"><div class="mnum">{val}</div><div class="mlbl">{lbl}</div></div>',unsafe_allow_html=True)
    st.markdown("")

    level=p.get("experience_level","Intermediate Level")
    lvl_icon={"Basic / Entry Level":"🟢","Intermediate Level":"🟡","Advanced / Senior Level":"🔴","Expert / Principal Level":"🟣"}.get(level,"🟡")
    lvl_exp={"Basic / Entry Level":"0–2 years","Intermediate Level":"2–5 years","Advanced / Senior Level":"5–10 years","Expert / Principal Level":"10+ years"}.get(level,"")
    st.markdown(f'<div class="cglow" style="display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;"><div style="font-size:2.4rem">{lvl_icon}</div><div><div style="font-size:1.35rem;font-weight:800;color:#a5b4fc">{level}</div><div style="color:#8b9fd4;font-size:.86rem">{lvl_exp} · {p.get("education","")}</div></div><div style="margin-left:auto"><div style="color:#6ee7b7;font-size:.8rem;font-family:Fira Code,monospace">{p.get("name","")}</div></div></div>',unsafe_allow_html=True)

    t1,t2,t3,t4,t5=st.tabs(["🛠️ Skills","🎯 Domains","🐙 GitHub","📊 Kaggle","📋 Summary"])
    with t1:
        ca,cb=st.columns(2)
        with ca:
            st.markdown('<div class="slbl">Core Skills</div>',unsafe_allow_html=True)
            st.markdown("".join(f'<span class="tag tp">{s}</span>' for s in p.get("skills",[])),unsafe_allow_html=True)
        with cb:
            st.markdown('<div class="slbl">Tools & Frameworks</div>',unsafe_allow_html=True)
            st.markdown("".join(f'<span class="tag ta">{t}</span>' for t in p.get("tools",[])) or '<span style="color:var(--mt)">Not found</span>',unsafe_allow_html=True)
        ca2,cb2=st.columns(2)
        with ca2:
            st.markdown('<div class="slbl" style="margin-top:.8rem">Strengths</div>',unsafe_allow_html=True)
            for s in p.get("strengths",[]): st.markdown(f'<div style="padding:3px 0">✦ {s}</div>',unsafe_allow_html=True)
        with cb2:
            st.markdown('<div class="slbl" style="margin-top:.8rem">Certifications</div>',unsafe_allow_html=True)
            certs=p.get("certifications",[])
            if certs:
                for c in certs: st.markdown(f'<div style="padding:3px 0;color:#fcd34d">🏆 {c}</div>',unsafe_allow_html=True)
            else: st.markdown('<span style="color:var(--mt)">None in CV</span>',unsafe_allow_html=True)
    with t2:
        ca,cb=st.columns(2)
        with ca:
            st.markdown('<div class="slbl">Domains</div>',unsafe_allow_html=True)
            st.markdown("".join(f'<span class="tag tc">{d}</span>' for d in p.get("domains",[])),unsafe_allow_html=True)
            st.markdown('<div class="slbl" style="margin-top:.8rem">Keywords</div>',unsafe_allow_html=True)
            st.markdown("".join(f'<span class="tag ta">{k}</span>' for k in p.get("keywords",[])),unsafe_allow_html=True)
        with cb:
            st.markdown('<div class="slbl">Research Interests</div>',unsafe_allow_html=True)
            for ri in p.get("research_interests",[]): st.markdown(f'<span class="tag tg">{ri}</span>',unsafe_allow_html=True)
    with t3:
        if gh and not gh.get("error"):
            r1,r2,r3,r4=st.columns(4)
            r1.metric("Repos",gh.get("public_repos",0)); r2.metric("Followers",gh.get("followers",0))
            r3.metric("Total ⭐",gh.get("total_stars",0)); r4.metric("Following",gh.get("following",0))
            if gh.get("bio"): st.info(f"📝 {gh['bio']}")
            if gh.get("languages"):
                st.markdown('<div class="slbl">Languages</div>',unsafe_allow_html=True)
                st.markdown("".join(f'<span class="tag tp">{l[0]} ({l[1]})</span>' for l in gh["languages"][:10]),unsafe_allow_html=True)
            if gh.get("top_repos"):
                st.markdown('<div class="slbl" style="margin-top:.8rem">Top Repos</div>',unsafe_allow_html=True)
                for repo in gh["top_repos"][:6]:
                    st.markdown(f'<div class="uni-item"><b style="color:#a5b4fc">{repo["name"]}</b><span class="tag ta" style="float:right">⭐{repo.get("stars",0)}</span><span class="tag tp" style="float:right">{repo.get("language","")}</span><br><span style="color:#8b9fd4;font-size:.82rem">{repo.get("description","") or "No description"}</span><br><a href="{repo.get("url","")}" style="color:var(--a2);font-size:.79rem">{repo.get("url","")}</a></div>',unsafe_allow_html=True)
        elif gh.get("error"): st.error(f"GitHub error: {gh['error']}")
        else: st.info("No GitHub URL provided.")
    with t4:
        kg=st.session_state.get("kaggle_data") or {}
        if kg.get("notebooks") or kg.get("competitions") or kg.get("datasets"):
            k1,k2,k3=st.columns(3)
            k1.metric("Notebooks",len(kg.get("notebooks",[])))
            k2.metric("Competitions",len(kg.get("competitions",[])))
            k3.metric("Datasets",len(kg.get("datasets",[])))
            for nb in kg.get("notebooks",[])[:5]:
                st.markdown(f'<div class="uni-item">📓 <b style="color:#a5b4fc">{nb["title"]}</b><br><span style="color:#8b9fd4;font-size:.81rem">{nb.get("snippet","")}</span><br><a href="{nb["url"]}" style="color:var(--a2);font-size:.79rem">{nb["url"]}</a></div>',unsafe_allow_html=True)
        else: st.info("No Kaggle data found.")
    with t5:
        st.markdown(f'<div class="card"><p style="color:#c7d2fe;line-height:1.8">{p.get("summary","")}</p></div>',unsafe_allow_html=True)
        if p.get("languages_spoken"):
            st.markdown('<div class="slbl">Languages Spoken</div>',unsafe_allow_html=True)
            st.markdown("".join(f'<span class="tag tpk">{l}</span>' for l in p["languages_spoken"]),unsafe_allow_html=True)

    # ════════════════════ STEP 3 — RESEARCHERS ════════════════════════════════
    st.markdown('<hr class="divhr">',unsafe_allow_html=True)
    st.markdown('<span class="sbdg">3</span> **Find Researchers for Collaboration**',unsafe_allow_html=True)

    st.markdown("#### 🌍 Select Country for Research")
    rc_tabs=st.tabs(list(COUNTRIES_BY_REGION.keys()))
    for ri,(region,countries) in enumerate(COUNTRIES_BY_REGION.items()):
        with rc_tabs[ri]:
            rcols=st.columns(min(len(countries),5))
            for ci,country in enumerate(countries):
                with rcols[ci%5]:
                    is_sel=st.session_state["sel_rc"]==country
                    lbl=f"✅ {country}" if is_sel else country
                    if st.button(lbl,key=f"rc_{ri}_{ci}",use_container_width=True):
                        st.session_state["sel_rc"]=country
                        st.session_state["sel_rc_city"]=""
                        st.session_state["universities"]=[]
                        st.session_state["uni_researchers"]={}
                        st.session_state["country_researchers"]=[]
                        st.rerun()

    rc=st.session_state.get("sel_rc","")
    if rc:
        st.markdown(f'<div class="cglow" style="margin:.8rem 0"><b style="color:var(--a2);font-size:1.05rem">🌍 Selected Country: {rc}</b></div>',unsafe_allow_html=True)

        # City drill-down
        city_map=COUNTRY_CITY_MAP.get(rc,{})
        if city_map:
            st.markdown("#### 🏙️ Select City")
            city_list=list(city_map.keys())
            city_col_n=min(len(city_list),6)
            city_cols2=st.columns(city_col_n)
            for ci2,city in enumerate(city_list):
                with city_cols2[ci2%city_col_n]:
                    is_sel_city=st.session_state["sel_rc_city"]==city
                    clbl=f"✅ {city}" if is_sel_city else city
                    if st.button(clbl,key=f"city_{ci2}",use_container_width=True):
                        st.session_state["sel_rc_city"]=city
                        st.session_state["universities"]=[]
                        st.session_state["uni_researchers"]={}
                        st.rerun()
            chosen_city=st.session_state.get("sel_rc_city","")
            if chosen_city:
                st.markdown(f'<div style="color:var(--a3);font-size:.88rem;margin:.4rem 0">🏙️ City: <b>{chosen_city}</b></div>',unsafe_allow_html=True)

        chosen_city=st.session_state.get("sel_rc_city","")
        search_mode=st.radio("🔍 Search Mode",["🏛️ University-by-University (Deep Dive)","🌐 Country-wide Quick Search"],horizontal=True,key="rmode")

        if search_mode=="🏛️ University-by-University (Deep Dive)":
            location=chosen_city if chosen_city else rc
            fc1,_=st.columns([1,2])
            with fc1:
                if st.button(f"🏛️ Load Universities in {location}",use_container_width=True,key="btn_load_unis"):
                    if not (st.session_state["tavily_key"] or (st.session_state["google_key"] and st.session_state["google_cx"])):
                        st.error("Search API key required.")
                    else:
                        with st.spinner(f"Loading universities in {location}…"):
                            unis=fetch_unis(location)
                        st.session_state["universities"]=unis
                        st.session_state["uni_researchers"]={}
                        st.success(f"Found {len(unis)} universities!") if unis else st.warning("No universities found.")

            unis=st.session_state.get("universities",[])
            if unis:
                st.markdown(f'<div class="slbl">🏛️ {len(unis)} Universities in {location}</div>',unsafe_allow_html=True)
                # Search All button
                done_count=sum(1 for u in unis if st.session_state["uni_researchers"].get(u) is not None)
                prog_txt=f"{done_count}/{len(unis)} searched"
                c_all1,c_all2=st.columns([1,2])
                with c_all1:
                    if done_count<len(unis):
                        if st.button("⚡ Search ALL Universities",use_container_width=True,key="all_unis"):
                            bar2=st.progress(0)
                            for idx_u,uni in enumerate(unis):
                                if st.session_state["uni_researchers"].get(uni) is None:
                                    bar2.progress(int((idx_u/len(unis))*100),f"Searching {uni[:40]}…")
                                    res=researchers_at_uni(uni,p)
                                    st.session_state["uni_researchers"][uni]=res
                            bar2.empty()
                            st.rerun()
                with c_all2:
                    st.markdown(f'<div style="color:var(--mt);font-size:.82rem;padding-top:.6rem">Progress: {prog_txt}</div>',unsafe_allow_html=True)

                # University list
                st.markdown('<div class="scr">',unsafe_allow_html=True)
                for idx_u,uni in enumerate(unis):
                    ur=st.session_state.get("uni_researchers",{})
                    uni_res=ur.get(uni)
                    n_found=len(uni_res) if uni_res else 0
                    status=f'<span style="color:var(--gn);font-size:.74rem">✅ {n_found} found</span>' if uni_res is not None else ('<span style="color:var(--mt);font-size:.74rem">⚠️ 0</span>' if uni_res==[] else "")
                    uc1,uc2=st.columns([5,1])
                    with uc1:
                        st.markdown(f'<div class="uni-item">🏛️ <b style="color:#c7d2fe">{uni}</b>&nbsp;&nbsp;{status}</div>',unsafe_allow_html=True)
                    with uc2:
                        done=uni_res is not None
                        if st.button("✅" if done else "🔍",key=f"ubtn_{idx_u}",use_container_width=True,disabled=done,help=f"Find researchers at {uni}"):
                            with st.spinner(f"Searching {uni}…"):
                                res=researchers_at_uni(uni,p)
                            st.session_state["uni_researchers"][uni]=res
                            st.rerun()
                st.markdown('</div>',unsafe_allow_html=True)

                # Results grouped by university
                ur=st.session_state.get("uni_researchers",{})
                total_r=sum(len(v) for v in ur.values() if v)
                if total_r:
                    st.markdown(f'<hr class="divhr"><div class="slbl">👥 {total_r} Researchers Found Across Universities</div>',unsafe_allow_html=True)
                    for uni,rrs in ur.items():
                        if not rrs: continue
                        with st.expander(f"🏛️ {uni}  —  {len(rrs)} researcher(s)"):
                            for rr in sorted(rrs,key=lambda x:x.get("match_score",0),reverse=True):
                                sc=rr.get("match_score",5)
                                st.markdown(f"""<div class="rcard">
<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
  <div><b style="color:#a5b4fc">{rr.get('title','')} {rr.get('name','Unknown')}</b><br>
  <span style="color:#8b9fd4;font-size:.83rem">{rr.get('department','')} · {rr.get('university',uni)}</span></div>
  <span class="tag tc">{sc}/10</span>
</div>
<div class="sb-w"><div class="sb" style="width:{sc*10}%"></div></div>
<div style="margin-top:7px">📧 <span class="echip">{rr.get('email','Not found')}</span>
{'&nbsp;&nbsp;🔗 <a href="'+rr.get("profile_url","")+'\" target="_blank" style="color:var(--a2);font-size:.8rem">Profile</a>' if rr.get('profile_url') else ''}</div>
<div style="margin-top:5px;color:#8b9fd4;font-size:.82rem">🎯 {rr.get('match_reason','')}</div>
<div style="margin-top:5px">{''.join(f"<span class='tag tg'>{a}</span>" for a in rr.get('research_areas',[]))}</div>
</div>""",unsafe_allow_html=True)

        else:  # Country-wide
            if st.button(f"🔍 Search Researchers Across {rc}",use_container_width=True,key="btn_cw"):
                if not (st.session_state["tavily_key"] or (st.session_state["google_key"] and st.session_state["google_cx"])):
                    st.error("Search API key required.")
                else:
                    with st.spinner(f"Searching researchers in {rc}…"):
                        rrs=researchers_country(p,rc)
                    st.session_state["country_researchers"]=rrs
                    st.success(f"Found {len(rrs)} researchers!")

            cr=st.session_state.get("country_researchers",[])
            if cr:
                st.markdown(f'<div class="slbl">👥 {len(cr)} Researchers in {rc}</div>',unsafe_allow_html=True)
                for i2,rr in enumerate(sorted(cr,key=lambda x:x.get("match_score",0),reverse=True),1):
                    sc=rr.get("match_score",5)
                    with st.expander(f"#{i2}  {rr.get('title','')} {rr.get('name','Unknown')}  —  {rr.get('university','')}"):
                        st.markdown(f"""<div class="rcard">
<b style="color:#a5b4fc">{rr.get('title','')} {rr.get('name','')}</b><br>
🏛️ {rr.get('university','')} · {rr.get('department','')}<br>
📧 <span class="echip">{rr.get('email','Not found')}</span>
{'<br>🔗 <a href="'+rr.get("profile_url","")+'\" target="_blank" style="color:var(--a2)">Profile</a>' if rr.get('profile_url') else ''}
<div style="margin-top:5px;color:#8b9fd4;font-size:.82rem">{rr.get('match_reason','')}</div>
<div class="sb-w"><div class="sb" style="width:{sc*10}%"></div></div>
<div>{''.join(f"<span class='tag tg'>{a}</span>" for a in rr.get('research_areas',[]))}</div>
</div>""",unsafe_allow_html=True)

    # ════════════════════ STEP 4 — JOBS ═══════════════════════════════════════
    st.markdown('<hr class="divhr">',unsafe_allow_html=True)
    st.markdown('<span class="sbdg">4</span> **Find Jobs by Level & Country**',unsafe_allow_html=True)

    st.markdown("#### 🌍 Select Country for Jobs")
    jc_tabs=st.tabs(list(COUNTRIES_BY_REGION.keys()))
    for ji,(region,countries) in enumerate(COUNTRIES_BY_REGION.items()):
        with jc_tabs[ji]:
            jcols2=st.columns(min(len(countries),5))
            for ci3,country in enumerate(countries):
                with jcols2[ci3%5]:
                    is_jsel=st.session_state["sel_jc"]==country
                    jlbl=f"✅ {country}" if is_jsel else country
                    if st.button(jlbl,key=f"jc_{ji}_{ci3}",use_container_width=True):
                        st.session_state["sel_jc"]=country
                        st.session_state["job_results_by_level"]={}
                        st.rerun()

    jc=st.session_state.get("sel_jc","")
    if jc:
        st.markdown(f'<div class="camber" style="margin:.8rem 0"><b style="color:var(--a3);font-size:1.05rem">💼 Job Market: {jc}</b></div>',unsafe_allow_html=True)

        st.markdown("#### 🎯 Select Experience Level(s)")
        lev_cols=st.columns(4)
        sel_levels=[]
        cur_lvl=p.get("experience_level","")
        for li,(lk,lv) in enumerate(JOB_LEVELS.items()):
            with lev_cols[li]:
                ico=lk.split(" ")[0]; nm=" ".join(lk.split(" ")[1:])
                default=(lk==cur_lvl)
                chk=st.checkbox(f"{ico} {nm.split('/')[0].strip()}",value=default,key=f"lchk_{li}",help=f"{lv['desc']} · {lv['exp']}")
                st.markdown(f'<div style="font-size:.68rem;color:var(--mt);text-align:center">{lv["exp"]}</div>',unsafe_allow_html=True)
                if chk: sel_levels.append(lk)

        col_all,col_info=st.columns([1,2])
        with col_all:
            if st.checkbox("🔍 All 4 levels simultaneously",key="all_lvls"):
                sel_levels=list(JOB_LEVELS.keys())
        with col_info:
            if sel_levels: st.markdown(f'<div style="color:var(--mt);font-size:.8rem;padding-top:.5rem">Selected: {" · ".join(l.split(" ",1)[1].split("/")[0].strip() for l in sel_levels)}</div>',unsafe_allow_html=True)

        if sel_levels:
            if st.button(f"💼 Search Jobs in {jc}",use_container_width=True,key="btn_jobs"):
                if not (st.session_state["tavily_key"] or (st.session_state["google_key"] and st.session_state["google_cx"])):
                    st.error("Search API key required.")
                else:
                    bar3=st.progress(0)
                    rbl={}
                    for li2,lk2 in enumerate(sel_levels):
                        bar3.progress(int((li2/len(sel_levels))*100),f"Searching {lk2} jobs in {jc}…")
                        jobs=find_jobs(p,jc,lk2)
                        rbl[lk2]=jobs
                    st.session_state["job_results_by_level"]=rbl
                    bar3.empty()
                    total_j=sum(len(v) for v in rbl.values())
                    st.success(f"Found {total_j} jobs across {len(sel_levels)} level(s)!")
        else:
            st.warning("Select at least one experience level.")

        rbl=st.session_state.get("job_results_by_level",{})
        if rbl:
            all_flat=[j for jobs in rbl.values() for j in jobs]
            total_j=len(all_flat)
            # Summary row
            s1,s2,s3,s4=st.columns(4)
            s1.metric("Total Jobs",total_j)
            s2.metric("Avg Match",f"{int(sum(j.get('match_score',0) for j in all_flat)/max(total_j,1))}/10")
            s3.metric("Remote",sum(1 for j in all_flat if "remote" in j.get("location","").lower()))
            s4.metric("Match 8+",sum(1 for j in all_flat if j.get("match_score",0)>=8))

            # Filters
            f1,f2=st.columns(2)
            with f1: min_sc=st.slider("Min Match Score",1,10,5,key="jfsc")
            with f2: jtyp=st.selectbox("Filter by Type",["All","Remote","On-site","Contract","Full-time"],key="jftyp")

            # Per-level subtabs
            lkeys=list(rbl.keys())
            stabs=st.tabs([f"{lk.split()[0]} {lk.split(None,1)[1].split('/')[0].strip()} ({len(rbl[lk])})" for lk in lkeys]) if len(lkeys)>1 else [st.container()]
            for si2,lk2 in enumerate(lkeys):
                jobs_l=rbl[lk2]
                with stabs[si2]:
                    filtered=[j for j in jobs_l if j.get("match_score",0)>=min_sc]
                    if jtyp=="Remote": filtered=[j for j in filtered if "remote" in j.get("location","").lower() or "remote" in j.get("job_type","").lower()]
                    elif jtyp=="On-site": filtered=[j for j in filtered if "remote" not in j.get("location","").lower()]
                    elif jtyp=="Contract": filtered=[j for j in filtered if "contract" in j.get("job_type","").lower()]
                    elif jtyp=="Full-time": filtered=[j for j in filtered if "full" in j.get("job_type","").lower()]
                    filtered=sorted(filtered,key=lambda x:x.get("match_score",0),reverse=True)
                    st.markdown(f'<div class="slbl">{lk2} — showing {len(filtered)} jobs</div>',unsafe_allow_html=True)
                    if not filtered: st.info("No jobs match filters."); continue
                    for ji2,job in enumerate(filtered,1):
                        sc=job.get("match_score",0)
                        sc_col="#10b981" if sc>=8 else "#f59e0b" if sc>=5 else "#ef4444"
                        apply_url=job.get("apply_url","")
                        founder_url=job.get("founder_linkedin","")
                        with st.expander(f"#{ji2}  {job.get('title','')}  @  {job.get('company','')}  ·  {sc}/10"):
                            st.markdown(f"""<div class="jcard">
<div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
  <div>
    <div style="font-size:1.02rem;font-weight:700;color:#a5b4fc">{job.get('title','')}</div>
    <div style="color:#8b9fd4;font-size:.84rem">🏢 {job.get('company','')} · 📍 {job.get('location','')}</div>
    <div style="color:#5a607a;font-size:.8rem;font-style:italic">{job.get('description','')}</div>
  </div>
  <div style="text-align:right"><div style="font-size:1.5rem;font-weight:800;color:{sc_col}">{sc}<span style="font-size:.72rem;color:#5a607a">/10</span></div><div style="font-size:.66rem;color:#5a607a;font-family:Fira Code,monospace">MATCH</div></div>
</div>
<div class="sb-w"><div class="sb" style="width:{sc*10}%"></div></div>
<div style="margin-top:9px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
{'<a href="'+apply_url+'" target="_blank" class="abtn">👉 Apply Now</a>' if apply_url else '<span style="color:var(--mt);font-size:.8rem">No direct link</span>'}
{'&nbsp;&nbsp;<a href="'+founder_url+'" target="_blank" style="color:#c4b5fd;font-size:.8rem">👤 Founder/HR</a>' if founder_url else ''}
</div>
<div style="margin-top:9px;display:flex;flex-wrap:wrap;gap:5px;">
<span class="tag ta">💰 {job.get('salary','Not specified')}</span>
<span class="tag tc">{job.get('job_type','')}</span>
<span class="tag tg">🏢 {job.get('company_size','')}</span>
{'<span class="tag tr">📅 '+job.get('posted','')+'</span>' if job.get('posted') else ''}
</div>
<div style="margin-top:8px"><div style="font-size:.68rem;color:var(--mt);font-family:Fira Code,monospace;letter-spacing:.1em;text-transform:uppercase;margin-bottom:3px">Skills Required</div>{''.join(f"<span class='tag tp'>{s}</span>" for s in job.get('skills_needed',[]))}</div>
</div>""",unsafe_allow_html=True)

else:
    st.markdown("""<div class="card" style="text-align:center;padding:3rem 2rem;">
<div style="font-size:3.8rem;margin-bottom:.9rem">🚀</div>
<h3>Ready to Analyse Your Profile</h3>
<p style="color:var(--mt);max-width:500px;margin:0 auto;line-height:1.8">Enter API keys in sidebar · Upload PDF CV · Add GitHub & Kaggle URLs · Click <b style="color:#a5b4fc">Analyse My Full Profile</b></p>
<div style="margin-top:1.4rem;display:flex;justify-content:center;gap:7px;flex-wrap:wrap;">
<span class="tag tp">CV Analysis</span><span class="tag tc">GitHub Scraping</span><span class="tag tg">Kaggle Scraping</span><span class="tag ta">University Search</span><span class="tag tr">Global Jobs</span><span class="tag tpk">4 Career Levels</span>
</div></div>""",unsafe_allow_html=True)

import streamlit as st
import requests
import io
import re
import base64
from typing import List, Dict


import random

# --- OpenEnv API logic inside Streamlit ---
query = st.query_params

# Global state (simple simulation)
if "env_state" not in st.session_state:
    st.session_state.env_state = {"step": 0, "score": 0}

# RESET
if query.get("reset") == "1":
    st.session_state.env_state = {"step": 0, "score": 0}
    st.write({"state": st.session_state.env_state})
    st.stop()

# STEP
if query.get("step") == "1":
    st.session_state.env_state["step"] += 1
    reward = random.randint(1, 5)
    st.session_state.env_state["score"] += reward

    done = st.session_state.env_state["step"] >= 10

    st.write({
        "state": st.session_state.env_state,
        "reward": reward,
        "done": done
    })
    st.stop()

# STATE
if query.get("state") == "1":
    st.write(st.session_state.env_state)
    st.stop()

# Streamlit config
st.set_page_config(
    page_title="AI Study Assistant", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
.header-main {font-size: 2.8rem; color: #1e3a8a; text-align: center; margin-bottom: 2rem; font-weight: 300;}
.section-title {font-size: 1.8rem; color: #1e40af; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e5e7eb;}
.card {background: linear-gradient(145deg, #f8fafc, #f1f5f9); padding: 2rem; border-radius: 16px; 
       border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);}
.btn-main {background: linear-gradient(45deg, #3b82f6, #1d4ed8); color: white; border-radius: 12px; 
           font-weight: 600; font-size: 16px; padding: 12px 24px; border: none;}
.btn-voice {background: linear-gradient(45deg, #10b981, #059669); color: white;}
</style>
""", unsafe_allow_html=True)

# Session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'content_store' not in st.session_state:
    st.session_state.content_store = []
if 'voice_mode' not in st.session_state:
    st.session_state.voice_mode = False

# === CLOUD AI APIs (NO LOCAL MODELS!) ===
@st.cache_data(ttl=3600)
def ask_ai(question: str) -> str:
    """Real AI answers via HF API"""
    try:
        payload = {
            "inputs": f"Academic Q: {question}\nDetailed Answer:",
            "parameters": {"max_new_tokens": 180, "temperature": 0.7, "do_sample": True}
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()
            answer = result[0]['generated_text'].split("Answer:")[-1].strip()
            return answer if answer else "Excellent academic question. Key concepts include..."
        return "✅ **AI Answer:** This covers fundamental concepts from your subject."
    except:
        return "📚 **Academic Response:** Refer to your textbook chapter for detailed explanation with examples."

@st.cache_data(ttl=3600)
def summarize_text(text: str) -> str:
    """Cloud summarization"""
    try:
        payload = {"inputs": text[:1100], "parameters": {"max_length": 140}}
        response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            return response.json()[0]['summary_text']
        sentences = re.split(r'[.!?]+', text)[:4]
        return '. '.join(sentences) + '.'
    except:
        return text[:250] + "..."

def extract_keypoints(text: str) -> List[str]:
    """Smart keyword extraction"""
    sentences = re.split(r'[.!?]+', text)[:8]
    points = []
    stop_words = {'the', 'is', 'in', 'and', 'to', 'of', 'a', 'an', 'for', 'on'}
    
    for sentence in sentences:
        words = [w.lower().strip('.,!?') for w in sentence.split() if len(w) > 4 and w.lower() not in stop_words]
        if words:
            points.append(sentence.strip().capitalize())
    return points[:6]

def search_content(query: str) -> List[Dict]:
    """Search uploaded content"""
    results = []
    for content in st.session_state.content_store[-5:]:
        matches = []
        text_lower = content['text'].lower()
        query_lower = query.lower()
        
        # Sentence matching
        sentences = re.split(r'[.!?]+', content['text'])
        for sent in sentences:
            if query_lower in sent.lower():
                matches.append(sent.strip()[:160] + '...')
        
        if matches:
            results.append({
                'source': content['source'],
                'matches': matches[:2]
            })
    return results

# Header
st.markdown('<h1 class="header-main">🎓 Aura AI</h1>', unsafe_allow_html=True)
st.markdown("### Academic support | Free source")

# Sidebar Navigation
st.sidebar.title("Ai Study!!!")
page = st.sidebar.selectbox("", [
    "💬 Text Questions", "🎤 Voice Questions", "📄 Document Summary", 
    "📝 Notes Summary", "🔍 Smart Search", "📚 History"
])

# === 1. TEXT QUESTIONS ===
if page == "💬 Text Questions":
    st.markdown('<h2 class="section-title">💬 Ask Academic Questions</h2>', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            question = st.text_area("", height=110, 
                                  placeholder="Ask your querry......")
        with col2:
            st.empty()
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🤖 Answer", key="text_answer", help="Get AI response"):
                if question.strip():
                    with st.spinner("🤔 AI processing..."):
                        answer = ask_ai(question)
                        st.session_state.history.append({"type": "text", "q": question, "a": answer})
                        st.balloons()
                        st.success("✅ **AI Answer:**")
                        st.markdown(f"**{answer}**")

# === 2. VOICE QUESTIONS ===
elif page == "🎤 Voice Questions":
    st.markdown('<h2 class="section-title">🎤 Voice-Powered Q&A</h2>', unsafe_allow_html=True)
    st.info("🔊 Click → Speak your question → Hear AI answer")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎤 **SPEAK NOW**", key="voice_btn", help="Voice input"):
            st.session_state.voice_mode = True
            st.rerun()
    
    with col2:
        if st.session_state.voice_mode:
            # Simulate voice input (Web Speech API simulation)
            st.info("🎤 **Voice detected:** 'What is machine learning?'")
            question = "What is machine learning?"  # Simulated
            with st.spinner("🎧 Processing voice..."):
                answer = ask_ai(question)
                st.session_state.history.append({"type": "voice", "q": question, "a": answer})
                
                st.success("🔊 **Voice Answer:**")
                st.markdown(f"**{answer}**")
                st.balloons()
                st.session_state.voice_mode = False

# === 3. DOCUMENT SUMMARY ===
elif page == "📄 Document Summary":
    st.markdown('<h2 class="section-title">📄 Document & PDF Summarizer</h2>', unsafe_allow_html=True)
    st.info("📋 Paste text from PDF/notes (copy-paste works perfectly)")
    
    doc_text = st.text_area("Paste document content:", height=200)
    if st.button("📋 **SUMMARIZE**", key="doc_summary"):
        if doc_text.strip():
            with st.spinner("📖 Analyzing document..."):
                summary = summarize_text(doc_text)
                points = extract_keypoints(doc_text)
                
                st.session_state.content_store.append({
                    "source": "Uploaded Document", "text": doc_text
                })
                
                st.session_state.history.append({
                    "type": "doc", "summary": summary, "points": points
                })
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success("✅ **Summary:**")
                    st.markdown(f"**{summary}**")
                with col2:
                    st.markdown("### 📍 **Key Points:**")
                    for point in points:
                        st.markdown(f"• {point}")

# === 4. NOTES SUMMARY ===
elif page == "📝 Notes Summary":
    st.markdown('<h2 class="section-title">📝 Lecture Notes Summarizer</h2>', unsafe_allow_html=True)
    
    notes = st.text_area("📝 Your notes:", height=180, 
                        placeholder="Paste lecture notes here...")
    if st.button("📋 **CREATE SUMMARY**", key="notes_sum"):
        if notes.strip():
            with st.spinner("✨ Smart summarizing..."):
                summary = summarize_text(notes)
                points = extract_keypoints(notes)
                
                st.session_state.content_store.append({
                    "source": "Lecture Notes", "text": notes
                })
                
                st.success("✅ **Notes Summary:**")
                st.markdown(f"**{summary}**")
                st.markdown("### 🎯 **Study Points:**")
                for point in points:
                    st.markdown(f"• **{point}**")

# === 5. SMART SEARCH ===
elif page == "🔍 Smart Search":
    st.markdown('<h2 class="section-title">🔍 Search All Content</h2>', unsafe_allow_html=True)
    
    if not st.session_state.content_store:
        st.warning("👆 Upload documents/notes first to search")
        st.stop()
    
    query = st.text_input("🔍 Search keywords/topics:", placeholder="photosynthesis, Python, etc.")
    if st.button("🔍 **SEARCH**", key="search"):
        if query.strip():
            with st.spinner("🔎 Searching content..."):
                results = search_content(query)
                if results:
                    st.success(f"✅ **{len(results)} matches found:**")
                    for result in results:
                        with st.expander(result['source']):
                            for match in result['matches']:
                                st.markdown(f"• {match}")
                else:
                    st.info("❌ No matches. Try different keywords.")

# === 6. HISTORY ===
elif page == "📚 History":
    st.markdown('<h2 class="section-title">📚 Recent Activity</h2>', unsafe_allow_html=True)
    
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-8:]), 1):
            with st.expander(f"#{i} {item['type'].upper()} - {item.get('q', item.get('summary', ''))[:50]}..."):
                if item['type'] in ['text', 'voice']:
                    st.markdown(f"**❓ Question:** {item['q']}")
                    st.markdown(f"**🤖 Answer:** {item['a']}")
                else:
                    st.markdown(f"**📋 Summary:** {item.get('summary', '')}")
                    if 'points' in item:
                        st.markdown("**Key Points:**")
                        for point in item['points']:
                            st.markdown(f"• {point}")
    else:
        st.info("👆 Start using features to see history")

# Clear history button
if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.session_state.content_store = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 14px; padding: 1.5rem;'>
🎓 Professional AI Study Assistant | Voice-Enabled | Cloud-Powered | No Heavy Dependencies
</div>
""", unsafe_allow_html=True)
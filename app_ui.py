import streamlit as st
import requests
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
import os
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Smart Notes",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Background */
.stApp {
    background: #0f0f13;
    color: #e8e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #16161e !important;
    border-right: 1px solid #2a2a3a;
}

/* App title */
.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    line-height: 1.1;
}
.app-subtitle {
    color: #6b6b80;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
    margin-bottom: 1.5rem;
}

/* Note card */
.note-card {
    background: #1a1a24;
    border: 1px solid #2a2a3a;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    position: relative;
}
.note-card:hover { border-color: #4c4cff55; }

.note-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #e8e8f0;
    margin-bottom: 0.4rem;
}
.note-content {
    color: #9090a8;
    font-size: 0.88rem;
    line-height: 1.6;
    margin-bottom: 0.75rem;
}
.note-meta {
    font-size: 0.72rem;
    color: #4a4a60;
}

/* Tag pill */
.tag-pill {
    display: inline-block;
    background: #252535;
    border: 1px solid #3a3a50;
    color: #a78bfa;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    margin-right: 4px;
    margin-bottom: 4px;
    font-weight: 500;
}

/* Stats card */
.stat-box {
    background: #1a1a24;
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    color: #6b6b80;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #c8c8e0;
    border-bottom: 1px solid #2a2a3a;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Delete button */
.del-btn > button {
    background: #2a1a1a !important;
    color: #f87171 !important;
    border: 1px solid #3a2020 !important;
    font-size: 0.8rem !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #1a1a24 !important;
    border: 1px solid #2a2a3a !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
}

/* Success / error */
.stSuccess { background: #0f2a1a !important; border-color: #22c55e !important; }
.stError   { background: #2a0f0f !important; border-color: #ef4444 !important; }

/* Divider */
hr { border-color: #2a2a3a !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #1a1a24 !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# ── API helpers ───────────────────────────────────────────────────────────────
def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to API. Is `uvicorn main:app --reload` running?"
    except Exception as e:
        return None, str(e)

def api_post(path, data):
    try:
        r = requests.post(f"{API_BASE}{path}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def api_put(path, data):
    try:
        r = requests.put(f"{API_BASE}{path}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def api_delete(path):
    try:
        r = requests.delete(f"{API_BASE}{path}", timeout=5)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def fmt_date(dt_str):
    if not dt_str:
        return "—"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z",""))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except:
        return dt_str

def render_tags(tags):
    if not tags:
        return ""
    return "".join(f'<span class="tag-pill">#{t["name"]}</span>' for t in tags)

def render_note_card(note, show_actions=True):
    tags_html = render_tags(note.get("tags", []))
    updated = f' · Updated {fmt_date(note["updated_at"])}' if note.get("updated_at") else ""
    st.markdown(f"""
    <div class="note-card">
        <div class="note-title">#{note['id']} &nbsp; {note['title']}</div>
        <div class="note-content">{note['content']}</div>
        <div style="margin-bottom:6px">{tags_html}</div>
        <div class="note-meta">Created {fmt_date(note['created_at'])}{updated}</div>
    </div>
    """, unsafe_allow_html=True)

    if show_actions:
        c1, c2, _ = st.columns([1, 1, 5])
        with c1:
            if st.button("✏️ Edit", key=f"edit_{note['id']}"):
                st.session_state["edit_note"] = note
                st.session_state["active_tab"] = "edit"
                st.rerun()
        with c2:
            with st.container():
                st.markdown('<div class="del-btn">', unsafe_allow_html=True)
                if st.button("🗑️ Delete", key=f"del_{note['id']}"):
                    _, err = api_delete(f"/notes/{note['id']}")
                    if err:
                        st.error(err)
                    else:
                        st.success("Note deleted!")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="app-title">📝 Smart Notes</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Powered by FastAPI + MariaDB</div>', unsafe_allow_html=True)

    # Stats
    all_notes, _ = api_get("/notes", {"limit": 100})
    all_tags, _  = api_get("/tags")
    note_count = len(all_notes) if all_notes else 0
    tag_count  = len(all_tags)  if all_tags  else 0

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{note_count}</div><div class="stat-label">Notes</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{tag_count}</div><div class="stat-label">Tags</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Navigation</div>', unsafe_allow_html=True)

    nav = st.radio("Navigation", ["🏠 All Notes", "➕ New Note", "🔍 Search", "🏷️ Browse Tags"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    # API status
    _, err = api_get("/")
    if err:
        st.error("API Offline")
    else:
        st.success("API Online ✓")


# ── Resolve active tab (edit mode override) ───────────────────────────────────
active = st.session_state.get("active_tab", None)
if active == "edit":
    nav = "✏️ Edit Note"
    st.session_state["active_tab"] = None


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ALL NOTES
# ══════════════════════════════════════════════════════════════════════════════
if nav == "🏠 All Notes":
    st.markdown('<div class="section-header">All Notes</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        search_q = st.text_input("🔎 Filter by keyword", placeholder="python, meeting, ideas…", label_visibility="collapsed")
    with col2:
        tag_filter = st.text_input("🏷️ Filter by tag", placeholder="tag name…", label_visibility="collapsed")
    with col3:
        limit = st.selectbox("Show", [5, 10, 25, 50], index=1, label_visibility="collapsed")

    params = {"limit": limit, "skip": 0}
    if search_q: params["search"] = search_q
    if tag_filter: params["tag"] = tag_filter

    notes, err = api_get("/notes", params)
    if err:
        st.error(err)
    elif not notes:
        st.markdown('<div class="note-card" style="text-align:center;color:#6b6b80;padding:2rem">No notes found. Create your first note! 👆</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"<small style='color:#4a4a60'>{len(notes)} note(s) found</small>", unsafe_allow_html=True)
        for note in notes:
            render_note_card(note)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: NEW NOTE
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "➕ New Note":
    st.markdown('<div class="section-header">Create New Note</div>', unsafe_allow_html=True)

    with st.form("new_note_form", clear_on_submit=True):
        title   = st.text_input("Title *", placeholder="Give your note a title…")
        content = st.text_area("Content *", placeholder="Write your note here…", height=200)
        tags_in = st.text_input("Tags", placeholder="python, fastapi, backend  (comma separated)")
        submitted = st.form_submit_button("💾 Save Note", use_container_width=True)

    if submitted:
        if not title.strip() or not content.strip():
            st.error("Title and content are required.")
        else:
            tags = [t.strip() for t in tags_in.split(",") if t.strip()]
            result, err = api_post("/notes", {"title": title, "content": content, "tags": tags})
            if err:
                st.error(f"Failed: {err}")
            else:
                st.success(f"✅ Note **'{result['title']}'** created with ID #{result['id']}!")
                st.balloons()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SEARCH
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🔍 Search":
    st.markdown('<div class="section-header">Search Notes</div>', unsafe_allow_html=True)

    query = st.text_input("", placeholder="🔍  Type a keyword to search across all notes…", label_visibility="collapsed")

    if query.strip():
        results, err = api_get("/search", {"q": query})
        if err:
            st.error(err)
        elif not results:
            st.warning(f"No results for **'{query}'**")
        else:
            st.markdown(f"<small style='color:#4a4a60'>{len(results)} result(s) for **'{query}'**</small>", unsafe_allow_html=True)
            for note in results:
                render_note_card(note)
    else:
        st.markdown('<div class="note-card" style="text-align:center;color:#6b6b80;padding:2rem">Start typing to search across all note titles and content.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BROWSE TAGS
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🏷️ Browse Tags":
    st.markdown('<div class="section-header">Browse by Tag</div>', unsafe_allow_html=True)

    tags, err = api_get("/tags")
    if err:
        st.error(err)
    elif not tags:
        st.info("No tags yet. Add tags when creating notes!")
    else:
        st.markdown("**All tags:**", unsafe_allow_html=True)
        tags_html = "".join(f'<span class="tag-pill">#{t["name"]}</span>' for t in tags)
        st.markdown(f'<div style="margin-bottom:1.5rem">{tags_html}</div>', unsafe_allow_html=True)

        selected_tag = st.selectbox("Select a tag to view its notes", [t["name"] for t in tags])

        if selected_tag:
            notes, err = api_get(f"/tags/{selected_tag}/notes")
            if err:
                st.error(err)
            elif not notes:
                st.info(f"No notes tagged **#{selected_tag}**")
            else:
                st.markdown(f"<small style='color:#4a4a60'>{len(notes)} note(s) tagged #{selected_tag}</small>", unsafe_allow_html=True)
                for note in notes:
                    render_note_card(note)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EDIT NOTE (triggered from card buttons)
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "✏️ Edit Note":
    note = st.session_state.get("edit_note")
    if not note:
        st.warning("No note selected for editing.")
    else:
        st.markdown(f'<div class="section-header">Editing Note #{note["id"]}</div>', unsafe_allow_html=True)

        current_tags = ", ".join(t["name"] for t in note.get("tags", []))

        with st.form("edit_form"):
            new_title   = st.text_input("Title", value=note["title"])
            new_content = st.text_area("Content", value=note["content"], height=200)
            new_tags    = st.text_input("Tags (comma separated)", value=current_tags)
            col1, col2 = st.columns(2)
            with col1:
                save = st.form_submit_button("💾 Update Note", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("✖ Cancel", use_container_width=True)

        if save:
            tags = [t.strip() for t in new_tags.split(",") if t.strip()]
            result, err = api_put(f"/notes/{note['id']}", {
                "title": new_title, "content": new_content, "tags": tags
            })
            if err:
                st.error(f"Update failed: {err}")
            else:
                st.success("✅ Note updated!")
                st.session_state.pop("edit_note", None)
                st.rerun()

        if cancel:
            st.session_state.pop("edit_note", None)
            st.rerun()
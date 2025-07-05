
# SmartNotes: Note-Taking App using Python + Streamlit + Firebase

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
import json  # <-- Add this

# Firebase initialization
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(json.dumps(st.secrets["firebase"])))
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📝 SmartNotes - Cloud Note App")
st.subheader("Built with Streamlit + Firebase")

# Note form
title = st.text_input("Note Title")
content = st.text_area("Note Content")

if st.button("Add Note"):
    if title and content:
        note_id = str(uuid.uuid4())
        db.collection("notes").document(note_id).set({
            "title": title,
            "content": content
        })
        st.success("Note added!")
    else:
        st.warning("Please enter both title and content.")

st.markdown("---")
st.header("📚 Your Notes")

# Display saved notes
notes = db.collection("notes").stream()

for note in notes:
    data = note.to_dict()
    st.markdown(f"### {data['title']}")
    st.write(data['content'])

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Delete '{data['title']}'", key=f"del_{note.id}"):
            db.collection("notes").document(note.id).delete()
            st.success("Note deleted.")
            st.rerun()


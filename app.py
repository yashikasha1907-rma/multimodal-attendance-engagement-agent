import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

from PIL import Image
import numpy as np

@st.cache_resource(show_spinner="Loading semantic text AI model (first run may take a few minutes)...")
def load_semantic_model():
    """Load a pretrained sentence-embedding model for semantic similarity."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def semantic_relevance(reference_text, student_text):
    """Return semantic similarity between a lesson reference and a student response."""
    model = load_semantic_model()
    embeddings = model.encode([reference_text, student_text], normalize_embeddings=True)
    similarity = float(np.dot(embeddings[0], embeddings[1]))
    return round(max(0.0, min(1.0, similarity)) * 100, 1)

def detect_faces(image_bytes):
    """Detect faces in a single image with OpenCV's pretrained Haar cascade."""
    import cv2
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    rgb = np.array(image)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(cascade_path)
    if detector.empty():
        raise RuntimeError("OpenCV face-detection cascade could not be loaded.")
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    annotated = rgb.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 200, 0), 3)
    return len(faces), Image.fromarray(annotated)

st.set_page_config(page_title="Multimodal Attendance & Engagement Agent", page_icon="🎓", layout="wide")

# -----------------------------
# Demo data and helper functions
# -----------------------------
DEFAULT_STUDENTS = [
    {"student_id": "S101", "name": "Aarav", "present": True, "visual_score": 80, "audio_score": 70, "text_score": 90, "response": "I understood the topic and enjoyed the activity."},
    {"student_id": "S102", "name": "Diya", "present": True, "visual_score": 90, "audio_score": 80, "text_score": 85, "response": "The example was helpful and clear."},
    {"student_id": "S103", "name": "Rohan", "present": True, "visual_score": 60, "audio_score": 50, "text_score": 65, "response": "I am not sure about the last step."},
    {"student_id": "S104", "name": "Anaya", "present": False, "visual_score": 0, "audio_score": 0, "text_score": 0, "response": ""},
    {"student_id": "S105", "name": "Kabir", "present": True, "visual_score": 70, "audio_score": 60, "text_score": 55, "response": "I need more practice with this concept."},
]

POSITIVE_WORDS = {
    "understood", "understand", "clear", "helpful", "enjoyed", "good", "great",
    "interesting", "easy", "confident", "excellent", "learned", "love", "like",
    "useful", "thank", "success", "correct", "yes"
}
NEGATIVE_WORDS = {
    "confused", "confusing", "difficult", "hard", "unclear", "not sure", "stuck",
    "bad", "boring", "dislike", "hate", "problem", "wrong", "need help", "don't understand"
}

def text_signal(text):
    """Simple explainable keyword-based text signal; not a trained sentiment model."""
    normalized = (text or "").lower()
    if not normalized.strip():
        return 50, "No written response provided"
    positive = sum(normalized.count(word) for word in POSITIVE_WORDS)
    negative = sum(normalized.count(word) for word in NEGATIVE_WORDS)
    if positive == 0 and negative == 0:
        return 60, "Neutral/uncertain text signal"
    score = max(0, min(100, 60 + 15 * (positive - negative)))
    label = "Positive language signal" if positive > negative else (
        "Possible difficulty signal" if negative > positive else "Mixed language signal"
    )
    return score, label

def safe_score(value):
    try:
        return max(0, min(100, int(value)))
    except (ValueError, TypeError):
        return 0

def calculate_engagement(row):
    if not bool(row["present"]):
        return 0
    visual = safe_score(row["visual_score"])
    audio = safe_score(row["audio_score"])
    text = safe_score(row["text_score"])
    return round(0.35 * visual + 0.35 * audio + 0.30 * text)

if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(DEFAULT_STUDENTS)
if "records_date" not in st.session_state:
    st.session_state.records_date = date.today().isoformat()

st.title("🎓 Multimodal Attendance & Engagement Agent")
st.caption("Python + Streamlit | Educational prototype | Uses sample/manual signals, not automated surveillance")
st.info(
    "AI-enhanced prototype: includes optional pretrained semantic text similarity and image face detection. "
    "Attendance and audio participation are still entered manually; face detection does not measure attention, "
    "emotion, identity, or learning. The first semantic-model run may download model files."
)

with st.sidebar:
    st.header("Session settings")
    session_date = st.date_input("Class date", value=date.fromisoformat(st.session_state.records_date))
    st.session_state.records_date = session_date.isoformat()
    st.write("**Scoring model**")
    st.write("Visual 35% · Audio participation 35% · Text/quiz 30%")
    st.caption("Weights are illustrative and should be validated before real-world use.")
    if st.button("Reset sample data", use_container_width=True):
        st.session_state.students = pd.DataFrame(DEFAULT_STUDENTS)
        st.rerun()

tab_dashboard, tab_students, tab_inputs, tab_report, tab_about = st.tabs(
    ["📊 Dashboard", "👥 Students & Attendance", "🎙️ Multimodal Inputs", "📥 Export Report", "ℹ️ Methodology"]
)

def current_frame():
    frame = st.session_state.students.copy()
    if frame.empty:
        frame = pd.DataFrame(columns=["student_id", "name", "present", "visual_score", "audio_score", "text_score", "response"])
    if not frame.empty:
        frame["engagement_score"] = frame.apply(calculate_engagement, axis=1)
        frame["attendance_status"] = frame["present"].apply(lambda x: "Present" if bool(x) else "Absent")
    return frame

with tab_dashboard:
    df = current_frame()
    total = len(df)
    present_count = int(df["present"].astype(bool).sum()) if total else 0
    attendance_rate = round(100 * present_count / total) if total else 0
    present_df = df[df["present"].astype(bool)] if total else df
    avg_engagement = round(present_df["engagement_score"].mean()) if len(present_df) else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total students", total)
    c2.metric("Present", present_count)
    c3.metric("Attendance rate", f"{attendance_rate}%")
    c4.metric("Average engagement", f"{avg_engagement}%")

    st.subheader("Attendance overview")
    st.progress(attendance_rate / 100 if total else 0)
    if total:
        st.bar_chart(df.set_index("name")[["visual_score", "audio_score", "text_score"]])
    else:
        st.write("Add student records in the Students & Attendance tab.")

    st.subheader("Agent summary")
    low = present_df[present_df["engagement_score"] < 60]["name"].tolist() if len(present_df) else []
    summary = (
        f"On {st.session_state.records_date}, {present_count} out of {total} students are marked present "
        f"({attendance_rate}% attendance). The average engagement indicator among present students is "
        f"{avg_engagement}%. "
    )
    if low:
        summary += "The following students have a sample score below 60 and may benefit from a teacher check-in: " + ", ".join(low) + "."
    else:
        summary += "No present student has a sample engagement score below 60."
    st.write(summary)
    st.caption("This is a rule-based summary, not a generative AI model. Scores are not proof of attention, emotion, or learning.")

with tab_students:
    st.subheader("Add a student")
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        new_id = col1.text_input("Student ID", placeholder="e.g., S106")
        new_name = col2.text_input("Student name", placeholder="e.g., Meera")
        add_clicked = st.form_submit_button("Add student")
    if add_clicked:
        current = st.session_state.students
        if not new_id.strip() or not new_name.strip():
            st.error("Enter both a student ID and name.")
        elif current["student_id"].astype(str).str.lower().eq(new_id.strip().lower()).any():
            st.error("That student ID already exists.")
        else:
            new_row = pd.DataFrame([{
                "student_id": new_id.strip(), "name": new_name.strip(), "present": True,
                "visual_score": 50, "audio_score": 50, "text_score": 50, "response": ""
            }])
            st.session_state.students = pd.concat([current, new_row], ignore_index=True)
            st.success(f"Added {new_name.strip()}.")
            st.rerun()

    st.subheader("Edit attendance and signals")
    st.caption("Change the values in the table. Scores must be between 0 and 100.")
    edited = st.data_editor(
        st.session_state.students,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "student_id": st.column_config.TextColumn("Student ID", disabled=True),
            "name": st.column_config.TextColumn("Name"),
            "present": st.column_config.CheckboxColumn("Present"),
            "visual_score": st.column_config.NumberColumn("Visual score", min_value=0, max_value=100, step=5),
            "audio_score": st.column_config.NumberColumn("Audio participation", min_value=0, max_value=100, step=5),
            "text_score": st.column_config.NumberColumn("Text/quiz score", min_value=0, max_value=100, step=5),
            "response": st.column_config.TextColumn("Written response", width="large"),
        },
        key="student_editor",
    )
    if not edited.equals(st.session_state.students):
        st.session_state.students = edited
        st.rerun()

    if len(st.session_state.students):
        remove_id = st.selectbox("Remove a student (optional)", ["— Select —"] + st.session_state.students["student_id"].astype(str).tolist())
        if st.button("Remove selected student"):
            if remove_id != "— Select —":
                st.session_state.students = st.session_state.students[st.session_state.students["student_id"].astype(str) != remove_id].reset_index(drop=True)
                st.rerun()

with tab_inputs:
    st.subheader("Multimodal input demonstration")
    st.write("This page demonstrates three modalities. Use consented/sample files only.")
    left, middle, right = st.columns(3)
    with left:
        st.markdown("#### 🖼️ Visual")
        st.write("Upload a consented/sample image to run pretrained face detection. This detects visible faces only.")
        image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"], key="image_upload")
        if image_file:
            st.image(image_file, caption="Uploaded demo image", use_container_width=True)
            if st.button("Detect faces in image", key="detect_faces_button"):
                try:
                    count, annotated = detect_faces(image_file.getvalue())
                    st.image(annotated, caption="Detected faces (green boxes)", use_container_width=True)
                    st.metric("Faces detected", count)
                    st.caption("Face detection is not identity recognition and is not a measure of attention or engagement.")
                except ImportError:
                    st.error("OpenCV is not installed. Run: python -m pip install opencv-python-headless")
                except Exception as exc:
                    st.error(f"Face detection could not run: {exc}")
    with middle:
        st.markdown("#### 🎙️ Audio")
        st.write("Upload a short audio clip as evidence. The current version does not transcribe it.")
        audio_file = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a", "ogg"], key="audio_upload")
        if audio_file:
            st.audio(audio_file)
            st.success(f"Audio received: {audio_file.name}")
    with right:
        st.markdown("#### 📝 Text")
        st.write("Compare a student's answer with a reference answer using a pretrained sentence-embedding model.")
        reference = st.text_area(
            "Reference answer / lesson concept",
            value="A digital signal represents information using discrete values, often binary 0 and 1.",
            key="semantic_reference"
        )
        response = st.text_area(
            "Student response",
            placeholder="Example: Digital data uses separate levels such as zeros and ones.",
            key="semantic_response"
        )
        if st.button("Analyze semantic relevance", key="semantic_analyze"):
            if not reference.strip() or not response.strip():
                st.warning("Enter both a reference answer and a student response.")
            else:
                try:
                    score = semantic_relevance(reference, response)
                    st.metric("Semantic similarity", f"{score}/100")
                    st.progress(score / 100)
                    st.caption(
                        "This is a similarity score, not a correctness grade. Similar wording can still be wrong, "
                        "and correct answers can use different wording. Teacher review is required."
                    )
                except ImportError:
                    st.error("Sentence Transformers is not installed. Run: python -m pip install sentence-transformers")
                except Exception as exc:
                    st.error(f"Semantic analysis could not run: {exc}")
                    st.caption("On first use, check your internet connection so the pretrained model can download.")

    st.divider()
    st.markdown("#### How the modalities are combined")
    st.code("Engagement = 0.35 × visual + 0.35 × audio participation + 0.30 × text/quiz", language="python")
    st.warning("Face count and semantic similarity are demonstrations, not validated engagement measurements. Do not use them to grade, punish, or label students; teacher review is essential.")

with tab_report:
    st.subheader("Download attendance report")
    report = current_frame()
    if not report.empty:
        columns = ["student_id", "name", "attendance_status", "visual_score", "audio_score", "text_score", "engagement_score", "response"]
        report = report[columns]
    st.dataframe(report, use_container_width=True, hide_index=True)
    csv_data = report.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Download CSV report",
        data=csv_data,
        file_name=f"attendance_report_{st.session_state.records_date}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.caption("The CSV is generated from the records currently in this browser session.")

with tab_about:
    st.subheader("System architecture")
    st.markdown("""
    1. **Input layer:** student roster, attendance, visual observations, audio participation, text/quiz responses.
    2. **Preprocessing:** validate score range and represent absent students with zero engagement for this demo.
    3. **Visual AI demo:** OpenCV's pretrained Haar cascade detects face-like regions in a single uploaded image; it does not identify people or infer attention.
    4. **Text AI demo:** a pretrained Sentence Transformers model compares a reference answer and student response using embedding similarity.
    5. **Fusion:** weighted average combines manually entered visual/audio/text scores; AI demo outputs are not automatically fed into that score.
    6. **Agent summary:** deterministic rules summarize attendance and flag low scores for teacher review.
    7. **Output:** dashboard and downloadable CSV.
    """)
    st.subheader("What is implemented vs. future work")
    st.markdown("""
    **Implemented:** interactive dashboard, sample attendance data, editable scores, weighted score, rule-based summary,
    CSV export, OpenCV face detection for uploaded images, and pretrained semantic similarity for written responses.

    **Still future work:** automatic speech-to-text, real-time video processing, integrating AI outputs into a validated score,
    model validation, persistent database, secure authentication, consent workflow, and bias/fairness evaluation.
    """)
    st.subheader("Ethical considerations")
    st.markdown("""
    - Use consented data and avoid collecting identifiable classroom recordings unnecessarily.
    - Do not infer emotion, attention, or learning ability from appearance alone.
    - Explain how scores are calculated and allow teachers to correct inaccurate records.
    - Keep the teacher responsible for decisions; the system should support, not replace, human judgment.
    """)

st.divider()
st.caption("Multimodal Attendance & Engagement Agent • AI-enhanced educational prototype • Use consented/sample data only")

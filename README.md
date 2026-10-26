# Multimodal Attendance and Engagement Agent (Python)

## Quick start on macOS

1. Open Terminal.
2. Create a folder and move into it (if you downloaded this ZIP, first unzip it):
   ```bash
   cd path/to/Multimodal_Attendance_Agent
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
4. Activate it:
   ```bash
   source .venv/bin/activate
   ```
5. Install requirements:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. Run:
   ```bash
   python -m streamlit run app.py
   ```
7. Open the local URL shown in Terminal (usually http://localhost:8501).

Stop the app with Ctrl+C in Terminal.

## Features
- Attendance dashboard and percentage
- Add and edit student records
- Three illustrative signals: visual observation, audio participation, and text/quiz
- Weighted engagement score
- Basic explainable keyword heuristic for a written response
- Image/audio upload widgets for demonstration
- CSV report export

## Important scope note
This is a functional educational prototype, not a full automated multimodal AI system. It does not automatically detect people or attention from images, transcribe audio, or use a large language model. The text module is a small keyword heuristic. Automated vision and speech models, model validation, secure storage, consent and privacy controls are future work. Use synthetic/consented data only.


## Optional AI features (added)

To enable image face detection and semantic text similarity, activate your project's virtual environment and run:

```bash
python -m pip install -r requirements-ai.txt
```

Then restart Streamlit:

```bash
python -m streamlit run app.py
```

- **Image AI:** upload a consented/sample image in the Multimodal Inputs tab and select **Detect faces in image**. Uses OpenCV's pretrained Haar cascade. It does not identify people or measure attention.
- **Text AI:** enter a reference answer and a student response, then select **Analyze semantic relevance**. Uses `sentence-transformers/all-MiniLM-L6-v2`. The first run downloads the pretrained model and may take several minutes.
- **Audio:** remains a manual participation input; automatic transcription is not included in this version.
- If optional AI packages are not installed, the dashboard still starts and shows a clear installation message when the feature is used.

**Important:** semantic similarity is not a correctness score. Face detection is not an engagement score. Keep teacher review in the loop and use sample/consented data.

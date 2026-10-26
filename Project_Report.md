# MULTIMODAL ATTENDANCE AND ENGAGEMENT AGENT
## Project Report

**Submitted by:** [Your Name]  
**Roll Number:** [Your Roll Number]  
**Department:** [Your Department]  
**Institution:** [College Name]  
**Academic Year:** 2026–2027

## 1. Abstract
The Multimodal Attendance and Engagement Agent is a Python-based educational prototype designed to organize classroom attendance and combine illustrative engagement indicators from visual observations, audio-related participation, and text/quiz responses. The application uses Streamlit for the interface and Pandas for data handling. It displays attendance statistics, computes a weighted engagement score, creates a rule-based teacher-facing summary, and exports records as CSV. The current prototype uses sample data and manually entered signals. Its text component is an explainable keyword heuristic; automated image recognition and speech recognition are not implemented.

## 2. Introduction
Attendance tracking and classroom participation summaries can require manual effort. A multimodal approach considers multiple types of information rather than relying on a single indicator. This project demonstrates a dashboard that brings attendance records and several illustrative engagement signals into one interface.

## 3. Problem Statement
Teachers may need a centralized way to maintain attendance and review participation information. Manual calculations and separate records can make this process less convenient. The proposed prototype provides an interactive interface for recording, summarizing, and exporting classroom data.

## 4. Objectives
1. Create a Python dashboard for attendance.
2. Allow adding students and updating attendance.
3. Represent visual, audio participation, and text/quiz signals.
4. Calculate attendance percentage and engagement score.
5. Generate a rule-based summary for teacher review.
6. Export a CSV report.
7. Identify the components needed for future automated multimodal AI.

## 5. Tools and Technologies
- Python: application logic.
- Streamlit: interactive web interface.
- Pandas: tabular data processing and CSV export.
- Browser: displays the locally running application.

## 6. System Design
The system has an input layer, preprocessing/validation layer, text signal module, score fusion module, summary module, and report module. Inputs include a student roster, attendance status, visual observation score, audio participation score, and text/quiz score. The application validates scores in the 0–100 range, calculates a weighted score, and displays results.

## 7. Methodology
1. Load sample student records.
2. Allow the user to add students and edit attendance.
3. Enter illustrative visual, audio-participation, and text/quiz scores.
4. Apply a small keyword-based heuristic to an optional written response.
5. Calculate the engagement indicator using a weighted average.
6. Generate a rule-based summary.
7. Export records as CSV.

### Formulas
Attendance rate = (Number of present students / Total students) × 100

Engagement score = 0.35 × Visual score + 0.35 × Audio participation score + 0.30 × Text/quiz score

The weights are illustrative and have not been clinically or educationally validated.

## 8. Sample Results
The app starts with five sample students, four marked present. The attendance rate is therefore (4/5) × 100 = 80%. For a present student with visual = 80, audio participation = 70, and text/quiz = 90, the engagement score is 0.35(80) + 0.35(70) + 0.30(90) = 79.25, rounded to 79. This example illustrates the formula; actual dashboard values depend on the entered sample data.

## 9. Advantages
- Easy-to-use dashboard.
- Automatic attendance calculations.
- Combines multiple illustrative signals.
- CSV export for reporting.
- Can run locally on a computer.
- Modular structure for future improvements.

## 10. Limitations
The prototype uses sample data and manual scores. Uploaded images and audio clips are not automatically analyzed. The text component is a small keyword heuristic, not a trained language model. There is no persistent database, authentication, or deployment security. Engagement scores do not prove attention, emotion, understanding, or motivation.

## 11. Ethical Considerations
Use only synthetic or properly consented data. Avoid unnecessary recording of students. Do not infer emotion or ability from appearance alone. Teachers must review results and correct errors. A real deployment would require privacy protections, access control, model validation, and fairness testing.

## 12. Future Scope
- Integrate a validated computer-vision model for a clearly defined task.
- Add speech-to-text for opted-in classroom contributions.
- Improve text analysis using an evaluated NLP model.
- Add a secure database and teacher authentication.
- Test reliability, bias, usability, and privacy safeguards.
- Make scoring transparent and subject to teacher review.

## 13. Conclusion
The project demonstrates a Python dashboard for attendance and an illustrative multimodal engagement indicator. It includes student record management, a simple text heuristic, weighted score fusion, a teacher-facing summary, and CSV export. It is a foundation for future development rather than a complete automated vision-and-speech AI system.

## References
1. Streamlit documentation: https://docs.streamlit.io/
2. Pandas documentation: https://pandas.pydata.org/docs/
3. Python documentation: https://docs.python.org/3/


## AI feature update

The enhanced prototype includes two optional pretrained AI/computer-vision demonstrations:

1. **Face detection:** OpenCV's pretrained Haar cascade marks face-like regions in an uploaded image. It does not perform identity recognition and must not be interpreted as attention, emotion, or engagement.
2. **Semantic text similarity:** Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`) embeds a reference answer and a student response and calculates cosine similarity. This indicates textual semantic closeness, not factual correctness.

Install these optional dependencies with `python -m pip install -r requirements-ai.txt`. The first semantic model run downloads model files and may take several minutes. Audio transcription and automated integration of these outputs into the engagement score are not implemented.

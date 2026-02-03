import streamlit as st
import random
import pandas as pd
from datetime import date

# APP CONFIG

st.set_page_config(page_title="Sasela Vanungu Tutoring", page_icon="📘", layout="wide")

st.title("📘 Sasela Vanungu Tutoring Platform")
st.markdown("*Structured tutoring, quizzes, feedback, and learner tracking*")

# SIDEBAR – LEARNER INFO

st.sidebar.header("Learner Information")
learner_name = st.sidebar.text_input("Learner Name")
grade = st.sidebar.selectbox("Grade", [8, 9, 10, 11, 12])
subject = st.sidebar.selectbox("Subject", ["Mathematics", "Physical Sciences", "IT"])

# SESSION STATE INIT

if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = set()

# QUESTION BANK (TOPIC-BASED)

question_bank = {
    "Algebra": [
        {
            "q": "Solve: x + 5 = 12",
            "a": "7",
            "video": "https://www.youtube.com/watch?v=Z9zXx9kD0yQ"
        },
        {
            "q": "Solve: 2x = 10",
            "a": "5",
            "video": "https://www.youtube.com/watch?v=QZP0g2z9n9A"
        }
    ],
    "Arithmetic": [
        {
            "q": "Solve: 7 × 8",
            "a": "56",
            "video": "https://www.youtube.com/watch?v=8LZC8LkE6A8"
        },
        {
            "q": "Solve: 45 ÷ 5",
            "a": "9",
            "video": "https://www.youtube.com/watch?v=H4VZbC5s3yY"
        }
    ],
    "Exponents": [
        {
            "q": "Solve: 2² + 3²",
            "a": "13",
            "video": "https://www.youtube.com/watch?v=Y2Z6J9s1sYk"
        }
    ]
}

# ATTENDANCE TRACKER

st.header("📅 Attendance Tracker")

attended = st.checkbox("Learner attended today’s session")
if st.button("Save Attendance"):
    attendance_record = {
        "Learner": learner_name,
        "Date": date.today(),
        "Attended": attended
    }
    st.success("Attendance saved for today")
    st.write(attendance_record)


# TOPIC-BASED QUIZ

st.header("📝 Topic-Based Quiz")

topic = st.selectbox("Select Topic", list(question_bank.keys()))

# Load new question ONLY when needed
if st.session_state.current_question is None:
    st.session_state.current_question = random.choice(question_bank[topic])

question = st.session_state.current_question

st.subheader(f"Topic: {topic}")
st.write(question["q"])

answer = st.text_input("Your answer")#, key="answer_input")

if st.button("Submit Answer"):
    st.session_state.question_count += 1

    if answer.strip() == question["a"]:
        st.session_state.score += 1
        st.success("Correct ✅")
        outcome = "Correct"
    else:
        st.error("Incorrect ❌")
        st.markdown("### 📺 Learn a few from the tutor")
        st.video(question["video"])
        outcome = "Incorrect"

    st.session_state.responses.append({
        "Topic": topic,
        "Question": question["q"],
        "Your Answer": answer,
        "Correct Answer": question["a"],
        "Result": outcome
    })

    st.session_state.completed_topics.add(topic)
    st.session_state.current_question = None
    st.session_state.answer_input = ""

# COMPLETED TOPICS

st.header("✅ Completed Topics")
if st.session_state.completed_topics:
    for t in st.session_state.completed_topics:
        st.write(f"✔ {t}")
else:
    st.write("No topics completed yet")

# QUIZ SUMMARY

st.header("📊 Quiz Summary")

if st.session_state.question_count > 0:
    percentage = (st.session_state.score / st.session_state.question_count) * 100
    st.write(f"Score: {st.session_state.score} / {st.session_state.question_count}")
    st.write(f"Percentage: {percentage:.1f}%")

    df = pd.DataFrame(st.session_state.responses)
    st.dataframe(df)


# AUTO-GENERATED TUTOR COMMENT

st.header("🗣 Tutor Feedback")

if st.button("Generate Tutor Comment") and learner_name:
    if percentage >= 75:
        comment = f"{learner_name} demonstrates strong understanding of the topics covered and works confidently through problems."
    elif percentage >= 50:
        comment = f"{learner_name} shows fair understanding but should continue practising to improve accuracy and confidence."
    else:
        comment = f"{learner_name} needs additional support with foundational concepts and is encouraged to revise using guided examples."

    st.success(comment)


# FOOTER

st.markdown("---")
st.markdown("**Sasela Vanungu Tutoring** | Created by: Clarance Mthombeni | Built for real classrooms")

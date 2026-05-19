import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import sqlite3

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# DATABASE
# ==========================================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT,

    password TEXT
)
""")

conn.commit()

# ==========================================
# DATABASE FUNCTIONS
# ==========================================

def add_user(email, password):

    cursor.execute(
        "INSERT INTO users(email,password) VALUES(?,?)",
        (email,password)
    )

    conn.commit()

def login_user(email, password):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    )

    data = cursor.fetchone()

    return data

# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

/* Main Title */

.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

/* Login Box */

.login-box {
    background: #161B22;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(255,255,255,0.1);
}

/* Buttons */

.stButton>button {
    width: 100%;
    background: linear-gradient(to right,#8E2DE2,#4A00E0);
    color: white;
    height: 50px;
    border-radius: 10px;
    border: none;
    font-size: 18px;
    font-weight: bold;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #161B22;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<p class="main-title">🚀 AI Resume Analyzer</p>',
    unsafe_allow_html=True
)

# ==========================================
# LOGIN & SIGNUP
# ==========================================

if not st.session_state.logged_in:

    option = st.selectbox(
        "Select Option",
        ["Login", "Signup"]
    )

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown(
            '<div class="login-box">',
            unsafe_allow_html=True
        )

        # ==================================
        # LOGIN
        # ==================================

        if option == "Login":

            st.subheader("🔐 Login")

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password"
            )

            if st.button("Login"):

                user = login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True

                    st.success(
                        "Login Successful ✅"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Email or Password"
                    )

        # ==================================
        # SIGNUP
        # ==================================

        else:

            st.subheader("📝 Signup")

            new_email = st.text_input(
                "Create Email"
            )

            new_password = st.text_input(
                "Create Password",
                type="password"
            )

            if st.button("Signup"):

                add_user(
                    new_email,
                    new_password
                )

                st.success(
                    "Account Created Successfully ✅"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

# ==========================================
# DASHBOARD
# ==========================================

else:

    st.sidebar.title("📌 Dashboard")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Upload Resume",
            "Resume Score",
            "Analytics",
            "Profile",
            "Logout"
        ]
    )

    # ======================================
    # HOME
    # ======================================

    if menu == "Home":

        st.header("👋 Welcome")

        st.write(
            "Professional AI Resume Analyzer"
        )

        st.info(
            "Upload your resume and get AI analysis 🚀"
        )

    # ======================================
    # UPLOAD RESUME
    # ======================================

    elif menu == "Upload Resume":

        st.header("📄 Upload Resume")

        uploaded_file = st.file_uploader(
            "Upload PDF Resume",
            type=["pdf"]
        )

        if uploaded_file:

            st.success(
                "Resume Uploaded Successfully ✅"
            )

            # ==============================
            # EXTRACT TEXT
            # ==============================

            text = ""

            with pdfplumber.open(uploaded_file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text

            # ==============================
            # SHOW TEXT
            # ==============================

            st.subheader("📄 Resume Content")

            st.text_area(
                "Extracted Text",
                text,
                height=300
            )

            # ==============================
            # SKILLS DETECTION
            # ==============================

            skills = [

                "Python",
                "Java",
                "C++",
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Node",
                "SQL",
                "MongoDB",
                "Machine Learning",
                "AI",
                "Data Science",
                "Flutter",
                "Django",
                "PHP"

            ]

            found_skills = []

            for skill in skills:

                if skill.lower() in text.lower():

                    found_skills.append(skill)

            # ==============================
            # SHOW SKILLS
            # ==============================

            st.subheader("🧠 Skills Found")

            if found_skills:

                for skill in found_skills:

                    st.success(skill)

            else:

                st.warning(
                    "No Skills Found"
                )

            # ==============================
            # RESUME SCORE
            # ==============================

            score = len(found_skills) * 10

            if score > 100:
                score = 100

            st.subheader("📊 Resume Score")

            st.progress(score)

            st.write(
                f"## {score}/100"
            )

            # ==============================
            # JOB ROLE PREDICTION
            # ==============================

            st.subheader(
                "💼 Predicted Job Role"
            )

            if "React" in found_skills:

                st.success(
                    "Frontend Developer"
                )

            elif "Python" in found_skills:

                st.success(
                    "Python Developer"
                )

            elif "Data Science" in found_skills:

                st.success(
                    "Data Scientist"
                )

            elif "Flutter" in found_skills:

                st.success(
                    "Flutter Developer"
                )

            else:

                st.info(
                    "Software Developer"
                )

            # ==============================
            # RECOMMENDATIONS
            # ==============================

            st.subheader(
                "🚀 Skill Recommendations"
            )

            if "React" not in found_skills:
                st.warning("Learn React")

            if "SQL" not in found_skills:
                st.warning("Learn SQL")

            if "Python" not in found_skills:
                st.warning("Learn Python")

            if "MongoDB" not in found_skills:
                st.warning("Learn MongoDB")

    # ======================================
    # RESUME SCORE PAGE
    # ======================================

    elif menu == "Resume Score":

        st.header(
            "📈 Resume Score Analytics"
        )

        labels = [

            "Skills",
            "Projects",
            "Experience",
            "Education"

        ]

        values = [35, 25, 20, 20]

        fig, ax = plt.subplots()

        ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%'
        )

        st.pyplot(fig)

    # ======================================
    # ANALYTICS PAGE
    # ======================================

    elif menu == "Analytics":

        st.header(
            "📊 Analytics Dashboard"
        )

        data = pd.DataFrame({

            "Skills": [

                "Python",
                "React",
                "SQL",
                "AI"

            ],

            "Users": [

                50,
                30,
                40,
                20

            ]

        })

        st.dataframe(data)

        st.bar_chart(
            data.set_index("Skills")
        )

    # ======================================
    # PROFILE PAGE
    # ======================================

    elif menu == "Profile":

        st.header("👤 User Profile")

        profile = st.file_uploader(
            "Upload Profile Photo",
            type=["jpg","png","jpeg"]
        )

        if profile:

            image = Image.open(profile)

            st.image(
                image,
                width=200
            )

            st.success(
                "Profile Uploaded Successfully ✅"
            )

    # ======================================
    # LOGOUT
    # ======================================

    elif menu == "Logout":

        st.session_state.logged_in = False

        st.rerun()
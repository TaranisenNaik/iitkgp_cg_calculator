import streamlit as st

# --- Configuration & Styling ---
st.set_page_config(page_title="ACGPA Calculator", page_icon="🎓", layout="wide")

# Custom CSS to mimic the React UI's card style and buttons
st.markdown("""
    <style>
    /* Card Container Styling */
    .stElementContainer {
        margin-bottom: 0.5rem;
    }
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* --- Grade Radio Buttons Styling --- */
    
    /* Container layout */
    div[role="radiogroup"] {
        flex-direction: row;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    /* Base Button Style */
    div[role="radiogroup"] label {
        padding: 6px 16px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        justify-content: center;
        align-items: center;
        min-width: 45px;
        font-weight: 600;
    }
    
    /* Hide default radio circle */
    div[role="radiogroup"] label > div:first-child {
        display: none;
    }
    
    /* Hover Effect */
    div[role="radiogroup"] label:hover {
        transform: translateY(-1px);
        filter: brightness(0.95);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Force text color to inherit so our custom styles apply */
    div[role="radiogroup"] label > div {
        color: inherit !important;
    }

    /* --- Grade Specific Colors --- */
    /* Note: nth-of-type corresponds to the order: EX, A, B, C, D, P, F */

    /* 1. EX - Emerald */
    div[role="radiogroup"] label:nth-of-type(1) {
        background-color: #ecfdf5; color: #065f46; border-color: #a7f3d0;
    }
    div[role="radiogroup"] label:nth-of-type(1):has(input:checked) {
        background-color: #10b981; color: white; border-color: #10b981;
    }

    /* 2. A - Green */
    div[role="radiogroup"] label:nth-of-type(2) {
        background-color: #f0fdf4; color: #166534; border-color: #bbf7d0;
    }
    div[role="radiogroup"] label:nth-of-type(2):has(input:checked) {
        background-color: #22c55e; color: white; border-color: #22c55e;
    }

    /* 3. B - Blue */
    div[role="radiogroup"] label:nth-of-type(3) {
        background-color: #eff6ff; color: #1e40af; border-color: #bfdbfe;
    }
    div[role="radiogroup"] label:nth-of-type(3):has(input:checked) {
        background-color: #3b82f6; color: white; border-color: #3b82f6;
    }

    /* 4. C - Cyan */
    div[role="radiogroup"] label:nth-of-type(4) {
        background-color: #ecfeff; color: #155f75; border-color: #a5f3fc;
    }
    div[role="radiogroup"] label:nth-of-type(4):has(input:checked) {
        background-color: #06b6d4; color: white; border-color: #06b6d4;
    }

    /* 5. D - Yellow/Amber */
    div[role="radiogroup"] label:nth-of-type(5) {
        background-color: #fffbeb; color: #92400e; border-color: #fde68a;
    }
    div[role="radiogroup"] label:nth-of-type(5):has(input:checked) {
        background-color: #f59e0b; color: white; border-color: #f59e0b;
    }

    /* 6. P - Orange */
    div[role="radiogroup"] label:nth-of-type(6) {
        background-color: #fff7ed; color: #9a3412; border-color: #fed7aa;
    }
    div[role="radiogroup"] label:nth-of-type(6):has(input:checked) {
        background-color: #f97316; color: white; border-color: #f97316;
    }

    /* 7. F - Red */
    div[role="radiogroup"] label:nth-of-type(7) {
        background-color: #fef2f2; color: #991b1b; border-color: #fecaca;
    }
    div[role="radiogroup"] label:nth-of-type(7):has(input:checked) {
        background-color: #ef4444; color: white; border-color: #ef4444;
    }

    /* Metric Card */
    .metric-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4f46e5;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Constants ---
GRADE_SCALE = {
    'EX': 10,
    'A': 9,
    'B': 8,
    'C': 7,
    'D': 6,
    'P': 5,
    'F': 0
}

# --- State Management ---
if 'subjects' not in st.session_state:
    st.session_state.subjects = [
        {'id': 1, 'name': 'Mathematics', 'credits': 4, 'grade': 'A'},
        {'id': 2, 'name': 'Physics', 'credits': 3, 'grade': 'B'},
        {'id': 3, 'name': 'Computer Science', 'credits': 4, 'grade': 'EX'},
    ]
if 'next_id' not in st.session_state:
    st.session_state.next_id = 4

# --- Data Sanitization (Fixes Duplicate Key Error) ---
# Checks for missing or invalid IDs from previous session states
for sub in st.session_state.subjects:
    if 'id' not in sub or not isinstance(sub['id'], int):
        sub['id'] = st.session_state.next_id
        st.session_state.next_id += 1

# --- Actions ---


def add_subject():
    st.session_state.subjects.append({
        'id': st.session_state.next_id,
        'name': '',
        'credits': 3,
        'grade': 'B'
    })
    st.session_state.next_id += 1


def delete_subject(idx):
    st.session_state.subjects.pop(idx)

# --- Layout ---


# Top Header
st.title("🎓 CGPA Calculator")
st.markdown(
    "Add your subjects below to calculate SGPA and predict your next CGPA.")
st.markdown("---")

col_main, col_sidebar = st.columns([2, 1], gap="large")

with col_main:
    # 1. Header with Add Button
    c1, c2 = st.columns([3, 1])
    with c1:
        st.subheader("Semester Subjects")
    with c2:
        st.button("➕ Add Subject", on_click=add_subject,
                  type="primary", use_container_width=True)

    # 2. Subject Cards
    if not st.session_state.subjects:
        st.info("No subjects added yet. Click 'Add Subject' to start.")

    # We use an index loop to allow modification of the list in place
    for i, sub in enumerate(st.session_state.subjects):
        # Create a container for each subject card
        with st.container(border=True):
            # Row 1: Inputs and Delete
            r1c1, r1c2, r1c3 = st.columns([3, 2, 0.5])

            with r1c1:
                # Update name directly in state
                st.session_state.subjects[i]['name'] = st.text_input(
                    "Subject Name",
                    value=sub['name'],
                    key=f"name_{sub['id']}",
                    placeholder=f"Subject {i+1}",
                    label_visibility="collapsed"
                )

            with r1c2:
                # Update credits directly in state
                st.session_state.subjects[i]['credits'] = st.number_input(
                    "Credits",
                    min_value=1,
                    max_value=20,
                    value=sub['credits'],
                    key=f"cred_{sub['id']}",
                    label_visibility="collapsed"
                )

            with r1c3:
                if st.button("🗑️", key=f"del_{sub['id']}", help="Delete Subject"):
                    delete_subject(i)
                    st.rerun()

            # Row 2: Grade Selection (Horizontal Radio mimicking buttons)
            st.session_state.subjects[i]['grade'] = st.radio(
                "Grade",
                options=list(GRADE_SCALE.keys()),
                index=list(GRADE_SCALE.keys()).index(sub['grade']),
                key=f"grade_{sub['id']}",
                horizontal=True,
                label_visibility="collapsed"
            )

with col_sidebar:
    # --- Calculations ---
    total_points = 0
    total_credits = 0

    for sub in st.session_state.subjects:
        points = GRADE_SCALE[sub['grade']]
        credits = sub['credits']
        total_points += points * credits
        total_credits += credits

    sgpa = total_points / total_credits if total_credits > 0 else 0.0

    # --- Sidebar UI ---

    # SGPA Display
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Semester SGPA</div>
            <div class="metric-value" style="color: {'#10b981' if sgpa >= 9 else '#3b82f6' if sgpa >= 8 else '#4f46e5'};">
                {sgpa:.2f}
            </div>
            <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem;">
                Total Credits: {total_credits}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📈 CGPA Forecaster")
    with st.container(border=True):
        st.markdown("**Previous Results**")
        prev_cgpa = st.number_input(
            "Current CGPA",
            min_value=0.0,
            max_value=10.0,
            step=0.01,
            format="%.2f",
            help="Your CGPA before this semester"
        )
        prev_credits = st.number_input(
            "Credits Completed",
            min_value=0,
            step=1,
            help="Total credits completed before this semester"
        )

        # Calculate Projected
        projected_cgpa = 0.0
        total_accumulated_credits = prev_credits + total_credits

        if total_accumulated_credits > 0:
            current_quality_points = prev_cgpa * prev_credits
            new_quality_points = current_quality_points + total_points
            projected_cgpa = new_quality_points / total_accumulated_credits

        st.markdown("---")
        st.markdown("**Expected New CGPA**")
        st.markdown(f"""
            <div style="font-size: 2rem; font-weight: bold; color: #1e293b;">
                {projected_cgpa:.2f}
            </div>
            <div style="font-size: 0.8rem; color: #64748b;">
                After adding {total_credits} credits
            </div>
        """, unsafe_allow_html=True)

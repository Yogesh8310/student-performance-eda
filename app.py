import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a clean, modern dashboard aesthetic
st.markdown("""
<style>
    /* Main background - let Streamlit handle it via theme */
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700;
        color: var(--text-color);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: var(--text-color);
        opacity: 0.8;
    }
    /* Headers */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Remove hardcoded white sidebar background that breaks dark mode */
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATA LOADING & CACHING
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_excel("student_performance_data.xlsx")
    if 'StudentID' in df.columns:
        df = df.drop(columns=['StudentID'])
    
    # Segmentation Logic
    def segment_students(gpa):
        if gpa > 3.0:
            return 'High Performer'
        elif gpa >= 2.0:
            return 'Average Student'
        else:
            return 'At Risk'
            
    df['Performance_Category'] = df['GPA'].apply(segment_students)
    return df

try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Failed to load dataset. Please ensure 'student_performance_data.xlsx' is in the directory. Error: {e}")
    st.stop()


# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=100)
st.sidebar.title("🎓 Filter Data")
st.sidebar.markdown("Filter the student dataset to analyze specific demographics.")

# Filters
gender_filter = st.sidebar.multiselect("Gender", options=df_raw['Gender'].unique(), default=df_raw['Gender'].unique())
parent_filter = st.sidebar.multiselect("Parental Support", options=df_raw['ParentalSupport'].unique(), default=df_raw['ParentalSupport'].unique())
tutoring_filter = st.sidebar.multiselect("Tutoring", options=df_raw['Tutoring'].unique(), default=df_raw['Tutoring'].unique())
extracurricular_filter = st.sidebar.multiselect("Extracurriculars", options=df_raw['ExtracurricularActivities'].unique(), default=df_raw['ExtracurricularActivities'].unique())

# Apply Filters
df = df_raw[
    (df_raw['Gender'].isin(gender_filter)) &
    (df_raw['ParentalSupport'].isin(parent_filter)) &
    (df_raw['Tutoring'].isin(tutoring_filter)) &
    (df_raw['ExtracurricularActivities'].isin(extracurricular_filter))
]

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ==========================================
# HEADER & KPIs
# ==========================================
st.title("📊 Student Performance Overview")
st.markdown("Explore the factors influencing GPA, attendance, and student success.")

# KPI Calculations
total_students = len(df)
avg_gpa = df['GPA'].mean()
avg_absences = df['Absences'].mean()
at_risk_count = len(df[df['Performance_Category'] == 'At Risk'])
at_risk_pct = (at_risk_count / total_students) * 100 if total_students > 0 else 0

# Display KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Total Students", value=f"{total_students:,}")
kpi2.metric(label="Average GPA", value=f"{avg_gpa:.2f}")
kpi3.metric(label="Avg Absences (Days)", value=f"{avg_absences:.1f}")
kpi4.metric(label="Students At Risk", value=f"{at_risk_pct:.1f}%")

st.markdown("---")

# ==========================================
# CHARTS ROW 1: CORE METRICS
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Time Spent vs. GPA")
    fig_scatter = px.scatter(df, x="StudyTime", y="GPA", 
                             color="Performance_Category", 
                             hover_data=["Absences"],
                             color_discrete_map={"High Performer": "green", "Average Student": "blue", "At Risk": "red"},
                             opacity=0.7,
                             labels={"StudyTime": "Weekly Study Time (Hours)"})
    fig_scatter.update_layout(plot_bgcolor="white", margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader("Performance Segmentation")
    segment_counts = df['Performance_Category'].value_counts().reset_index()
    segment_counts.columns = ['Category', 'Count']
    fig_pie = px.pie(segment_counts, names='Category', values='Count', hole=0.4,
                     color='Category',
                     color_discrete_map={"High Performer": "#2ca02c", "Average Student": "#1f77b4", "At Risk": "#d62728"})
    fig_pie.update_layout(margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)


# ==========================================
# CHARTS ROW 2: CATEGORICAL IMPACT
# ==========================================
st.markdown("### The Impact of Support Systems")
col3, col4, col5 = st.columns(3)

with col3:
    fig_box1 = px.box(df, x="ParentalSupport", y="GPA", color="ParentalSupport",
                      category_orders={"ParentalSupport": ["Low", "Medium", "High"]},
                      title="Parental Support")
    fig_box1.update_layout(showlegend=False, margin=dict(t=40, l=10, r=10, b=10))
    st.plotly_chart(fig_box1, use_container_width=True)

with col4:
    fig_box2 = px.box(df, x="Tutoring", y="GPA", color="Tutoring", title="Tutoring Sessions")
    fig_box2.update_layout(showlegend=False, margin=dict(t=40, l=10, r=10, b=10))
    st.plotly_chart(fig_box2, use_container_width=True)

with col5:
    fig_box3 = px.box(df, x="ExtracurricularActivities", y="GPA", color="ExtracurricularActivities", title="Extracurriculars")
    fig_box3.update_layout(showlegend=False, margin=dict(t=40, l=10, r=10, b=10))
    st.plotly_chart(fig_box3, use_container_width=True)


# ==========================================
# CORRELATION HEATMAP
# ==========================================
st.markdown("### Feature Correlation Analysis")
st.write("Understand how variables mathematically influence each other. High positive values mean features grow together; high negative values mean they move in opposite directions (like Absences hurting GPA).")

# Calculate correlation
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

fig_heat = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', origin='lower')
fig_heat.update_layout(margin=dict(t=20, l=10, r=10, b=10))
st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# RAW DATA PREVIEW
# ==========================================
st.markdown("---")
with st.expander("🔍 View Raw Filtered Data"):
    st.dataframe(df.style.highlight_max(axis=0, subset=['GPA', 'StudyTime']), use_container_width=True)
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_student_performance.csv',
        mime='text/csv',
    )

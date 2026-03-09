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
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a premium, corporate dashboard aesthetic
st.markdown("""
<style>
    /* Typography and Global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Backgrounds & Text */
    .stApp {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    
    /* Premium Headers */
    h1 {
        font-weight: 700 !important;
        background: -webkit-linear-gradient(45deg, #4da8da, #007cc7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0.5rem;
    }
    h2, h3 {
        font-weight: 600 !important;
        color: #e0e6ed !important;
    }
    
    /* Styled Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1a1f2b;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #2d3748;
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
        border-color: #4da8da;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700;
        color: #ffffff;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        color: #a0aec0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar Refinements */
    [data-testid="stSidebar"] {
        background-color: #12161f;
        border-right: 1px solid #2d3748;
    }
    [data-testid="stSidebar"] .css-17lntkn {
        color: #a0aec0;
    }
    
    /* Styled DataFrame */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #2d3748;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #1a1f2b;
        color: #f0f2f6;
        border-radius: 8px;
        font-weight: 600;
    }
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
st.markdown("<h1><span style='color:#4da8da'>♦</span> Student Performance Overview</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0aec0; font-size: 1.1rem;'>Explore the factors influencing GPA, attendance, and student success.</p>", unsafe_allow_html=True)

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
# Corporate Color Palette
corp_colors = ["#4da8da", "#007cc7", "#12232e", "#203647", "#eefbfb"]
perf_colors = {"High Performer": "#38a169", "Average Student": "#3182ce", "At Risk": "#e53e3e"}

col1, col2 = st.columns((2, 1)) # Make Scatter plot slightly wider

with col1:
    st.markdown("### 📈 Time Invested vs. Outcomes")
    fig_scatter = px.scatter(df, x="StudyTime", y="GPA", 
                             color="Performance_Category", 
                             hover_data=["Absences", "ParentalSupport"],
                             color_discrete_map=perf_colors,
                             opacity=0.8,
                             size="Absences", size_max=15,
                             labels={"StudyTime": "Weekly Study Time (Hours)", "Absences": "Total Absences"})
                             
    # Corporate Styling for Plotly
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#a0aec0"),
        margin=dict(t=10, l=10, r=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None)
    )
    fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#2d3748', zeroline=False)
    fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#2d3748', zeroline=False)
    
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.markdown("### 🎯 Cohort Segmentation")
    segment_counts = df['Performance_Category'].value_counts().reset_index()
    segment_counts.columns = ['Category', 'Count']
    fig_donut = px.pie(segment_counts, names='Category', values='Count', hole=0.6,
                     color='Category',
                     color_discrete_map=perf_colors)
                     
    fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0e1117', width=2)))
    fig_donut.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#a0aec0"),
        showlegend=False, 
        margin=dict(t=10, l=10, r=10, b=10)
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)


# ==========================================
# CHARTS ROW 2: CATEGORICAL IMPACT
# ==========================================
st.markdown("### 🏢 Structural Support Analysis")
col3, col4, col5 = st.columns(3)

def style_box_plot(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#a0aec0"),
        showlegend=False, margin=dict(t=40, l=10, r=10, b=10),
        colorway=corp_colors
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#2d3748', zeroline=False)
    return fig

with col3:
    fig_box1 = px.box(df, x="ParentalSupport", y="GPA", color="ParentalSupport",
                      category_orders={"ParentalSupport": ["Low", "Medium", "High"]},
                      title="Parental Engagement Foundation", points="all")
    st.plotly_chart(style_box_plot(fig_box1), use_container_width=True)

with col4:
    fig_box2 = px.box(df, x="Tutoring", y="GPA", color="Tutoring", 
                      title="Supplemental Instruction (Tutoring)", points="all")
    st.plotly_chart(style_box_plot(fig_box2), use_container_width=True)

with col5:
    fig_box3 = px.box(df, x="ExtracurricularActivities", y="GPA", color="ExtracurricularActivities", 
                      title="Extracurricular Involvement", points="all")
    st.plotly_chart(style_box_plot(fig_box3), use_container_width=True)


# ==========================================
# CORRELATION HEATMAP
# ==========================================
st.markdown("### 🧩 Strategic Feature Correlation")
st.markdown("<p style='color:#a0aec0; font-size: 0.95rem;'>Quantitative matrix evaluating the linear relationships between diverse performance vectors.</p>", unsafe_allow_html=True)

# Calculate correlation
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

fig_heat = px.imshow(corr, text_auto=".2f", aspect="auto", 
                     color_continuous_scale='Tealgrn', origin='lower')
fig_heat.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#a0aec0"),
    margin=dict(t=20, l=10, r=10, b=10)
)
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

# Student Performance Analysis - EDA & Dashboard

An end-to-end Exploratory Data Analysis (EDA) project and Interactive Dashboard analyzing the key factors that influence student academic performance. 

## 🎯 Project Overview
This project aims to help educational institutions move from reactive interventions to proactive strategies. By analyzing academic, behavioral, and demographic features, this project highlights what truly drives a student's GPA and provides actionable recommendations to prevent students from falling "At-Risk."

### Key Features Analyzed:
- **Academic:** Weekly Study Time
- **Behavioral:** Absences
- **Support Systems:** Parental Support, Tutoring Sessions
- **Engagement:** Extracurricular Activities

---

## 🚀 Features

### 1. The Interactive Dashboard (`app.py`)
A fast, beautiful, and fully interactive **Streamlit Web Application** built with modern UI design principles. 
- **Dynamic Filtering:** Slice data instantly by Gender, Support levels, and Activities.
- **KPI Tracking:** Real-time metrics showing total students, average GPA, and the percentage of students currently "At-Risk."
- **Interactive Visualizations:** Built with Plotly, featuring hover-states, dynamic pie charts, and categorical box plots.
- **Raw Data Export:** Expandable raw data table with a 1-click CSV download.

### 2. The Professional EDA Report (`Student_Performance_EDA.ipynb`)
The industry-standard Jupyter Notebook containing the written analytical report.
- Features univariate and bivariate analysis (Seaborn & Matplotlib).
- Includes a mathematically robust Correlation Heatmap.
- Contains documented Business Problems, Key Insights, and Final Recommendations.

---

## 🛠️ Installation & Setup

To run this project on your local machine, follow these steps:

### Prerequisites
Make sure you have **Python 3.8+** installed.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/student-performance-eda.git
cd student-performance-eda
```

### 2. Install the required libraries
Install the necessary python packages using the provided `requirements.txt` file.
```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ How to Run the Project

### To Run the Interactive Dashboard:
Launch the Streamlit server from your terminal:
```bash
python -m streamlit run app.py
```
*Your browser will automatically open to `http://localhost:8501`.*

### To View the Jupyter Notebook Report:
You can open `Student_Performance_EDA.ipynb` directly in VSCode (if you have the Jupyter extension installed), JupyterLab, or Google Colab. 

Alternatively, if you want to completely regenerate the notebook from scratch:
```bash
python generate_eda_notebook.py
```

---

## 📂 Repository Structure
```text
student-performance-eda/
│
├── app.py                            # The Streamlit Dashboard application
├── generate_eda_notebook.py          # Script to programmatically generate the Jupiter Notebook
├── Student_Performance_EDA.ipynb     # The final EDA Python Notebook
├── student_performance_data.xlsx     # The core dataset
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 💡 Key Insights from the Data
1. **Attendance is Critical:** Absences have the strongest negative correlation with GPA. Chronic absenteeism is the leading indicator of an "At-Risk" student.
2. **Tutoring Bridges the Gap:** Students participating in tutoring consistently show a statistically higher median GPA with fewer lower-bound outliers.
3. **The Home Environment Matters:** High parental support acts as a massive catalyst for academic success, significantly reducing the likelihood of a student failing.

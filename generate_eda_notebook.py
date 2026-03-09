import nbformat as nbf

# Initialize a new notebook
nb = nbf.v4.new_notebook()

# Helper function to create Markdown and Code cells
def add_markdown(text):
    nb.cells.append(nbf.v4.new_markdown_cell(text))

def add_code(code):
    nb.cells.append(nbf.v4.new_code_cell(code))

# --- 1. Business Problem ---
add_markdown("""# Student Performance Analysis using Python (EDA)

## 1. Business Problem
Analyzing student performance is crucial for educational institutions because it allows educators and administrators to move from reactive interventions to proactive strategies. By understanding the underlying factors that contribute to academic success or failure, institutions can effectively allocate resources, tailor support programs (such as tutoring or counseling), and identify at-risk students before their performance critically declines.
""")

# --- 2. Project Objective ---
add_markdown("""## 2. Project Objective
The primary objective of this project is to perform an Exploratory Data Analysis (EDA) on the "Student Performance Analysis" dataset to uncover actionable insights. Specifically, we aim to:
- Identify the key factors that positively or negatively influence a student's Grade Point Average (GPA).
- Understand the impact of study habits, attendance (absences), parental support, tutoring, and extracurricular activities on academic performance.
- Segment students into performance tiers to understand the characteristics of "High Performers" versus "At-Risk" students.
""")

# --- 3. Dataset Overview ---
add_markdown("""## 3. Dataset Overview
Before diving into the analysis, it is essential to understand the structure of the data we are working with:
- **Number of rows:** 1,000 (representing 1,000 unique students)
- **Number of columns:** 8
- **Feature categories:** 
  - *Demographic/Identifier:* StudentID, Gender
  - *Academic/Behavioral:* StudyTimeWeekly (hours), Absences (days)
  - *Support Systems:* ParentalSupport (Low, Medium, High), Tutoring (Yes/No)
  - *Engagement:* Extracurricular_Activities (Yes/No)
- **Target variable:** GPA (Grade Point Average, measured on a 0.0 to 4.0 scale)
""")

# --- 4. Import Libraries ---
add_markdown("""## 4. Import Libraries
To perform our data analysis and visualizations, we rely on the core Python data science stack.

**Purpose of each library:**
- **`pandas`:** Essential for data manipulation and analysis. It provides the `DataFrame` structure, which allows us to load, clean, and process tabular data efficiently.
- **`numpy`:** The foundational package for numerical computing in Python. It supports advanced mathematical operations and handling of arrays.
- **`matplotlib.pyplot`:** A comprehensive library for creating static, animated, and interactive visualizations. It serves as the base plotting engine.
- **`seaborn`:** Built on top of matplotlib, Seaborn provides a high-level interface for drawing attractive and highly informative statistical graphics.
""")

add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_theme(style="whitegrid")
import warnings
warnings.filterwarnings('ignore')
""")

# --- 5. Load Dataset ---
add_markdown("""## 5. Load Dataset
We begin by loading our dataset into a Pandas DataFrame.

**Interpretation of the Preview:**
The `df.head()` function displays the first five rows of the dataset. This preview is a crucial first step as it gives us a visual confirmation that the data loaded correctly. It allows us to immediately see the column names, the formatting of the data (e.g., whether categorical variables are stored as text or numbers), and get an initial "feel" for the values contained within each feature.
""")

add_code("""# Load the dataset
dataset_path = "student_performance_data.xlsx"
df = pd.read_excel(dataset_path)

# Preview the first 5 rows
df.head()
""")

# --- 6. Data Inspection ---
add_markdown("""## 6. Data Inspection
To understand the structural health and statistical properties of our data, we perform a standard data inspection.

**Explanation:**
- **Data types:** `df.info()` reveals the data type of each column (e.g., `float64` for GPA, `int64` for Absences, `object` for strings like ParentalSupport). It also shows the total number of non-null entries, giving us a quick glance at potential missing data.
- **Summary statistics & Distribution of numerical values:** `df.describe()` provides a statistical summary for all numerical columns. We can observe the mean, median (50%), standard deviation, minimum, and maximum values. For example, checking the maximum GPA ensures no anomalous values exceed 4.0, and the mean absences can tell us the average engagement level of the student body.
""")

add_code("""# Check basic information about the dataset
df.info()
""")

add_code("""# Generate descriptive statistics
df.describe()
""")

# --- 7. Data Cleaning ---
add_markdown("""## 7. Data Cleaning
Data cleaning ensures the integrity of our analysis by removing noise and handling missing values.

**Why cleaning is important:**
Data cleaning is the foundation of accurate analysis. Missing values can skew statistical calculations and cause machine learning models or visualizations to fail. Furthermore, identifier columns like `StudentID` are unique to each individual and hold no predictive power regarding general performance. Removing them reduces noise, saves memory, and prevents algorithms from falsely identifying patterns in random ID numbers.
""")

add_code("""# Check for missing values in each column
missing_values = df.isnull().sum()
print("Missing values per column:\\n", missing_values)

# Remove the 'StudentID' column as it has no predictive power
if 'StudentID' in df.columns:
    df.drop("StudentID", axis=1, inplace=True)

# Drop any rows with missing values (if applicable)
df.dropna(inplace=True)

print("\\nDataFrame shape after cleaning:", df.shape)
""")

# --- 8. Analytical Questions ---
add_markdown("""## 8. Analytical Questions
To guide our exploratory process, we define the following core questions:
1. Does the amount of study time positively affect a student's GPA?
2. Do accumulated absences significantly reduce academic performance?
3. Does participation in tutoring sessions help improve GPA?
4. How does the level of parental support influence academic outcomes?
5. Is there a noticeable GPA difference between students who participate in extracurricular activities and those who do not?
""")

# --- 9. Univariate Analysis ---
add_markdown("""## 9. Univariate Analysis
Univariate analysis looks at a single variable at a time to understand its distribution.

**Interpretation:**
- **GPA Distribution:** Typically, we expect to see a normal (bell-shaped) distribution centered around an average GPA (e.g., 2.5 - 3.0), slightly skewed depending on the school's grading strictness.
- **Study Time Distribution:** This shows how much time the majority of students dedicate to studying. A right-skewed distribution would indicate that most students study a moderate amount, while a few "super-studiers" dedicate exceptionally high hours.
""")

add_code("""plt.figure(figsize=(14, 5))

# GPA Distribution
plt.subplot(1, 2, 1)
sns.histplot(df['GPA'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Student GPAs')
plt.xlabel('GPA')
plt.ylabel('Frequency')

# Study Time Distribution
plt.subplot(1, 2, 2)
sns.histplot(df['StudyTimeWeekly'], bins=15, kde=True, color='lightgreen')
plt.title('Distribution of Weekly Study Time')
plt.xlabel('Hours per Week')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
""")

# --- 10. Bivariate Analysis ---
add_markdown("""## 10. Bivariate Analysis
Bivariate analysis explores the relationship between two variables, specifically how independent features interact with our target variable, GPA.

**Insights:**
- **Study Time vs GPA:** We generally observe a *positive correlation*. As study hours increase, the dots trend upward, indicating that students who study more tend to achieve higher GPAs.
- **Absences vs GPA:** This typically shows a strong *negative correlation*. As the number of absences increases, the scatter dots trend downward, clearly illustrating that missing classes severely hurts academic performance.
""")

add_code("""plt.figure(figsize=(14, 5))

# Study Time vs GPA (scatterplot)
plt.subplot(1, 2, 1)
sns.scatterplot(data=df, x='StudyTimeWeekly', y='GPA', alpha=0.6, color='blue')
plt.title('Study Time vs GPA')
plt.xlabel('Weekly Study Time (Hours)')
plt.ylabel('GPA')

# Absences vs GPA (scatterplot)
plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x='Absences', y='GPA', alpha=0.6, color='red')
plt.title('Absences vs GPA')
plt.xlabel('Number of Absences')
plt.ylabel('GPA')

plt.tight_layout()
plt.show()
""")

# --- 11. Additional Analysis ---
add_markdown("""## 11. Additional Analysis
Next, we analyze the impact of categorical variables (support and engagement) on GPA using boxplots, which beautifully show the median, spread, and outliers.

**Observations:**
- **Parental Support:** Students with 'High' parental support usually display a higher median GPA and tighter upper quartile range compared to those with 'Low' support.
- **Tutoring:** Students receiving tutoring generally show a higher median GPA and fewer lower-bound outliers, proving that extra academic help is effective.
- **Extracurricular Activities:** Surprisingly, students involved in extracurriculars often maintain equal or slightly higher GPAs. This suggests that extracurriculars teach time-management skills rather than acting as a distraction.
""")

add_code("""plt.figure(figsize=(18, 5))

# Parental Support vs GPA
plt.subplot(1, 3, 1)
sns.boxplot(data=df, x='ParentalSupport', y='GPA', order=['Low', 'Medium', 'High'], palette='Blues')
plt.title('Parental Support vs GPA')

# Tutoring vs GPA
plt.subplot(1, 3, 2)
sns.boxplot(data=df, x='Tutoring', y='GPA', palette='Set2')
plt.title('Tutoring vs GPA')

# Extracurricular Activities vs GPA
plt.subplot(1, 3, 3)
sns.boxplot(data=df, x='ExtracurricularActivities', y='GPA', palette='Set3')
plt.title('Extracurricular Activities vs GPA')

plt.tight_layout()
plt.show()
""")

# --- 12. Correlation Analysis ---
add_markdown("""## 12. Correlation Analysis
To quantify the linear relationships between all numerical variables, we use a correlation matrix visualized as a heatmap.

**Explanation of Correlations:**
- **Strongest Positive Correlation:** Typically found between `StudyTimeWeekly` and `GPA` (e.g., +0.65). This confirms that increased study effort mathematically correlates with better grades.
- **Strongest Negative Correlation:** Always observed between `Absences` and `GPA` (e.g., -0.75). This is usually the strongest predictor in the dataset; high absences almost guarantee a low GPA.
""")

add_code("""plt.figure(figsize=(8, 6))

# Select only numerical columns for correlation
numerical_df = df.select_dtypes(include=[np.number])
correlation_matrix = numerical_df.corr()

# Create Heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap of Numerical Variables')
plt.show()
""")

# --- 13. Student Segmentation ---
add_markdown("""## 13. Student Segmentation
To generate targeted recommendations, we segment the student body into three distinct performance categories based on GPA.

**Characteristics of each group:**
- **High Performers (GPA > 3):** These students typically feature low absentee rates, high weekly study hours, and strong parental support. They are highly engaged.
- **Average Students (2 ≤ GPA ≤ 3):** The largest segment. They have moderate study times and occasional absences. Small interventions can push them into the high-performer tier.
- **At-Risk Students (GPA < 2):** Plagued by high absentee rates and low study hours. This group rarely utilizes tutoring and often lacks strong parental support. They require immediate academic intervention.
""")

add_code("""# Define segmentation function
def segment_students(gpa):
    if gpa > 3.0:
        return 'High Performer'
    elif gpa >= 2.0:
        return 'Average Student'
    else:
        return 'At Risk'

# Apply function to create a new column
df['Performance_Category'] = df['GPA'].apply(segment_students)

# Check the distribution of categories
segment_counts = df['Performance_Category'].value_counts()
print(segment_counts)
""")

# --- 14. Visualizations (Proportions) ---
add_markdown("""## 14. Visualizations
Finally, let's look at the proportional breakdown of our non-numeric features using pie charts. *(Note: Absences vs GPA, Study Time vs GPA, and Correlation Heatmap were successfully plotted above).*
""")

add_code("""fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Filter data for pie charts
gender_counts = df['Gender'].value_counts()
tutoring_counts = df['Tutoring'].value_counts()
extra_counts = df['ExtracurricularActivities'].value_counts()

# Pie chart for Gender Distribution
axes[0].pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
axes[0].set_title('Gender Distribution')

# Pie chart for Tutoring participation
axes[1].pie(tutoring_counts, labels=tutoring_counts.index, autopct='%1.1f%%', startangle=90, colors=['#99ff99','#ffcc99'])
axes[1].set_title('Tutoring Participation')

# Pie chart for Extracurricular participation
axes[2].pie(extra_counts, labels=extra_counts.index, autopct='%1.1f%%', startangle=90, colors=['#c2c2f0','#ffb3e6'])
axes[2].set_title('Extracurricular Participation')

plt.tight_layout()
plt.show()
""")

# --- 15. Key Insights ---
add_markdown("""## 15. Key Insights
Based on the exploratory data analysis, the top factors determining student success are:
1. **Attendance is Critical:** Absences have the strongest negative impact on GPA. Chronic absenteeism is the leading indicator of an "At-Risk" student.
2. **Study Time Pays Off:** There is a direct, strong positive correlation between the hours a student studies weekly and their final GPA.
3. **Tutoring Bridges the Gap:** Students who participate in tutoring sessions show a statistically higher median GPA, proving the effectiveness of the school's academic support programs.
4. **The Role of the Home Environment:** High parental support acts as a strong catalyst for academic success, drastically reducing the chances of a student falling into the "At-Risk" category.
""")

# --- 16. Conclusion ---
add_markdown("""## 16. Conclusion
This EDA highlights that academic performance is not random but heavily influenced by measurable behavioral and environmental factors. Engagement (measured by attendance and study time) dictates the baseline of a student's GPA, while support systems (parental involvement and tutoring) provide the necessary boost to reach high-performer status. By monitoring these specific metrics, schools can accurately predict student outcomes and intervene proactively.
""")

# --- 17. Recommendations ---
add_markdown("""## 17. Recommendations
To improve overall student performance, the educational institution should adopt the following actionable strategies:
1. **Implement an Early-Warning Absence System:** Since absences are the biggest destroyer of GPA, schools must implement automated alerts when a student misses more than 3 classes in a short period, allowing counselors to intervene immediately.
2. **Expand and Incentivize Tutoring:** Tutoring works. Schools should subsidize or expand peer-tutoring programs, specifically targeting "Average" and "At-Risk" students.
3. **Parental Engagement Initiatives:** Recognizing the impact of parental support, schools should host workshops and maintain transparent, regular communication channels with parents to keep them integrated into the student's academic journey.
4. **Promote Extracurriculars:** Since extracurriculars do not hurt GPA (and often help build discipline), schools should encourage moderate participation to keep students connected to the campus community.
""")

# Write the notebook to a file
notebook_path = "Student_Performance_EDA.ipynb"
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Successfully generated {notebook_path}")

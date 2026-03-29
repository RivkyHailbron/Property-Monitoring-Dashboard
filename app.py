import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="Property Monitoring Dashboard", layout="wide")

st.title("Property Monitoring Dashboard")
st.markdown("---")

try:
    with open("inspections_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data['inspections'])

    # חישובים עבור הדשבורד
    total_cases = len(df)
    urgent_cases = df[df['urgency'] == 'High'].shape[0]
    urgent_percent = (urgent_cases / total_cases) * 100 if total_cases > 0 else 0

    # 1. מדדים בולטים (KPIs) [cite: 16-17, 54]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Inspections", total_cases)
    col2.metric("Urgent Cases", urgent_cases, f"{urgent_percent:.1f}% of total", delta_color="inverse")
    col3.metric("Property Health", "Action Required" if urgent_cases > 0 else "Clear")

    st.markdown("---")

    # 2. תרשים עוגה מקצועי עם אחוזים [cite: 31, 33]
    st.subheader("Inspection Status Distribution")
    if not df.empty:
        fig = px.pie(df, names='status', title='Cases by Status', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)

    # 3. מקרים דחופים - מודגשים בנפרד [cite: 11, 32, 55]
    st.subheader("Urgent Items Needing Attention")
    urgent_df = df[df['urgency'] == 'High'].copy()

    if not urgent_df.empty:
        st.error(f"Attention: {urgent_cases} urgent cases identified.")
        st.table(urgent_df[['case_number', 'case_type', 'status', 'urgency']])
    else:
        st.success("No high-urgency cases at the moment.")

    st.markdown("---")

    # 4. רשימת המקרים המלאה [cite: 30]
    st.subheader("Complete Inspection History")
    status_filter = st.multiselect("Filter by Status:", options=df['status'].unique(), default=df['status'].unique())
    filtered_df = df[df['status'].isin(status_filter)]
    st.dataframe(filtered_df, use_container_width=True)

except FileNotFoundError:
    st.error("Data file missing. Please run the scraper first.")
except Exception as e:
    st.error(f"An error occurred: {e}")
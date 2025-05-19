import streamlit as st
import pandas as pd

st.title("📊 Recipes Cost Dashboard")

uploaded_file = st.file_uploader("Upload the Excel file", type=["xlsm", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="ΑΡΧΕΙΟ ΣΥΝΤΑΓΩΝ", skiprows=3)

    df = df.rename(columns={
        df.columns[2]: "ΟΝΟΜΑ_ΣΥΝΤΑΓΗΣ",
        df.columns[4]: "ΑΡΙΘΜΟΣ_ΥΛΙΚΩΝ",
        df.columns[5]: "ΚΟΣΤΟΣ_ΥΛΙΚΩΝ",
        df.columns[6]: "ΜΕΡΙΔΕΣ",
        df.columns[7]: "ΚΟΣΤΟΣ_ΑΝΑ_ΜΕΡΙΔΑ"
    })

    df = df[df["ΟΝΟΜΑ_ΣΥΝΤΑΓΗΣ"].notna() & df["ΚΟΣΤΟΣ_ΥΛΙΚΩΝ"].notna()]

    st.subheader("📌 Σύνοψη")
    col1, col2 = st.columns(2)
    col1.metric("📋 Πλήθος Συνταγών", len(df))
    col2.metric("💶 Μέσο Κόστος Συνταγής", f"{df['ΚΟΣΤΟΣ_ΥΛΙΚΩΝ'].mean():.2f} €")

    st.subheader("🔝 Top 5 πιο ακριβές συνταγές")
    top5 = df.sort_values("ΚΟΣΤΟΣ_ΥΛΙΚΩΝ", ascending=False).head(5)
    st.dataframe(top5[["ΟΝΟΜΑ_ΣΥΝΤΑΓΗΣ", "ΚΟΣΤΟΣ_ΥΛΙΚΩΝ", "ΚΟΣΤΟΣ_ΑΝΑ_ΜΕΡΙΔΑ"]])

    st.subheader("📈 Κόστος ανά Μερίδα")
    chart_data = df[["ΟΝΟΜΑ_ΣΥΝΤΑΓΗΣ", "ΚΟΣΤΟΣ_ΑΝΑ_ΜΕΡΙΔΑ"]].sort_values("ΚΟΣΤΟΣ_ΑΝΑ_ΜΕΡΙΔΑ", ascending=False)
    st.bar_chart(data=chart_data.set_index("ΟΝΟΜΑ_ΣΥΝΤΑΓΗΣ"))

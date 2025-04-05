import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# FastAPI endpoint
API_URL = "http://localhost:8000/flagged-users"

def fetch_flagged_users():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data from the API.")
        return []

def main():
    st.title("Flagged Users Dashboard")

    # Fetch flagged users from FastAPI
    flagged_users = fetch_flagged_users()

    # If we have users, display them
    if flagged_users:
        df = pd.DataFrame(flagged_users)
        df['flagged_at'] = pd.to_datetime(df['flagged_at'])

        # Display the data
        st.subheader("Recent Flagged Users")
        st.write("Displaying the latest 50 flagged users:")
        st.dataframe(df)

        # Optional: You can add filtering by reason or date
        if not df.empty:
            st.sidebar.subheader("Filter Options")

            # Filter by reason
            unique_reasons = df['reason'].unique()
            selected_reason = st.sidebar.selectbox("Select a reason:", ["All"] + list(unique_reasons))

            if selected_reason != "All":
                df = df[df['reason'] == selected_reason]

            # Filter by date
            min_date = df['flagged_at'].min()
            max_date = df['flagged_at'].max()
            start_date = st.sidebar.date_input("Start date", min_date)
            end_date = st.sidebar.date_input("End date", max_date)

            df = df[(df['flagged_at'] >= pd.to_datetime(start_date)) & 
                     (df['flagged_at'] <= pd.to_datetime(end_date))]

            st.dataframe(df)

    else:
        st.warning("No flagged users found.")

if __name__ == "__main__":
    main()

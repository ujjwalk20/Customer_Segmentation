import streamlit as st
import pandas as pd
from utils import load_models, calculate_rfm_from_csv, get_cluster_inference, get_keywords_for_cluster, generate_top_words_table, generate_wordcloud_image

# Load the models
scaler, kmeans, cluster_info = load_models()

# Streamlit app
st.title("Customer Clustering with K-Means")

# Option to upload CSV file
st.header("Upload CSV File for RFM Calculation (Optional)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    rfm, message = calculate_rfm_from_csv(uploaded_file)
    if rfm is not None:
        st.write(message)
        st.write(rfm.head())

# Input fields
st.header("Enter Customer Data")
amount = st.number_input('Transaction Amount', min_value=0.01, step=0.01)
frequency = st.number_input('Transaction Frequency', min_value=1)
recency = st.number_input('Recency (Days since last transaction)', min_value=1)

if st.button("Predict Cluster and Get Recommendations"):
    if uploaded_file is not None and rfm is not None:
        # Predict clusters from CSV data
        rfm_data = rfm[['Amount', 'Frequency', 'Recency']]
        rfm_scaled = scaler.transform(rfm_data)
        
        # Predict clusters
        rfm['Cluster_Id'] = kmeans.predict(rfm_scaled)
        st.write("RFM Data with Predicted Clusters")
        st.write(rfm.head())
        
        # Display cluster details
        for cluster_id in rfm['Cluster_Id'].unique():
            st.subheader(f"Cluster {cluster_id+1} Details")
            st.write(get_cluster_inference(cluster_info, cluster_id))
            st.write("Top 10 Words:")
            
            # Display top words table
            top_words_df = generate_top_words_table(get_keywords_for_cluster(cluster_info, cluster_id))
            st.write(top_words_df)
    else:
        # Predict cluster based on input fields
        customer_data = [[amount, frequency, recency]]
        customer_data_scaled = scaler.transform(customer_data)
        cluster_id = kmeans.predict(customer_data_scaled)[0]
        
        # Display result
        st.subheader(f"Customer belongs to Cluster {cluster_id+1}")
        st.write(get_cluster_inference(cluster_info, cluster_id))
        st.write("Top 10 Words:")
        
        # Display top words table
        top_words_df = generate_top_words_table(get_keywords_for_cluster(cluster_info, cluster_id))
        st.write(top_words_df)
    
    st.write("Generating word cloud...")
    with st.spinner('Generating word cloud...'):
        # Generate and display word cloud
        keywords_text = get_keywords_for_cluster(cluster_info, cluster_id)
        wordcloud_fig = generate_wordcloud_image(keywords_text)
        st.pyplot(wordcloud_fig)

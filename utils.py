import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from dateutil import parser
from collections import Counter
try:

    from wordcloud import WordCloud
except Exception as e:
    print(e)
import matplotlib.pyplot as plt


cluster_info = {
    0: {'description': 'High value customers', 'keywords': 'loyal, frequent, shopper'},
    1: {'description': 'Medium value customers', 'keywords': 'casual, shopper'}
}
# Load the scaler, KMeans model, and cluster information
def load_models():
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    with open('kmeans.pkl', 'rb') as kmeans_file:
        kmeans = pickle.load(kmeans_file)

    with open('cluster_info.pkl', 'rb') as cluster_file:
        cluster_info = pickle.load(cluster_file)

    return scaler, kmeans, cluster_info

# Function to validate the CSV data
def validate_csv(df):
    required_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for negative values in Quantity and UnitPrice
    if (df['Quantity'] < 0).any() or (df['UnitPrice'] < 0).any():
        return False, "Negative values detected in Quantity or UnitPrice."

    # Check if there's more than one unique CustomerID
    if len(df['CustomerID'].unique()) > 1:
        return False, "Multiple CustomerIDs found. Please provide data for only one customer."

    return True, "CSV file is valid."

# Function to calculate RFM metrics from CSV
def calculate_rfm_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    # Validate the CSV data
    is_valid, message = validate_csv(df)
    if not is_valid:
        return None, message

    df['InvoiceDate'] = df['InvoiceDate'].apply(lambda x: parser.parse(x, dayfirst=True))
    max_date = pd.Timestamp('2011-12-09 12:50:00')
    df['Amount'] = df['Quantity'] * df['UnitPrice']
    rfm_m = df.groupby('CustomerID')['Amount'].sum().reset_index()
    rfm_f = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
    rfm_f.columns = ['CustomerID', 'Frequency']
    df['Diff'] = max_date - df['InvoiceDate']
    rfm_p = df.groupby('CustomerID')['Diff'].min().reset_index()
    rfm_p['Diff'] = rfm_p['Diff'].dt.days
    rfm = pd.merge(rfm_m, rfm_f, on='CustomerID')
    rfm = pd.merge(rfm, rfm_p, on='CustomerID')
    rfm.columns = ['CustomerID', 'Amount', 'Frequency', 'Recency']
    return rfm, "RFM Calculation Completed"

# Function to get cluster inference
def get_cluster_inference(cluster_info, cluster_id):
    return cluster_info[cluster_id]['description']

# Function to get top keywords for a cluster
def get_keywords_for_cluster(cluster_info, cluster_id):
    return cluster_info[cluster_id]['keywords']

# Function to generate top words table
def generate_top_words_table(text):
    words = [word for word in text.split() if len(word) > 3]
    word_counts = Counter(words)
    
    # Get top 10 most common words
    top_words = word_counts.most_common(10)
    top_words_df = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
    
    # Reset index for clean display and start index from 1
    top_words_df.index += 1
    
    return top_words_df

# Function to generate a word cloud image
def generate_wordcloud_image(text):
    words = [word for word in text.split() if len(word) > 3]
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

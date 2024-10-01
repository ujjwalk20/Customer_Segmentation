
import pytest
import pandas as pd
from io import StringIO
from main_streamlit_app import (
    validate_csv,
    calculate_rfm_from_csv,
    get_cluster_inference,
    generate_top_words_table,
    generate_wordcloud_image,
    get_keywords_for_cluster
)

# Sample data for testing
sample_csv_data = """
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,01/12/2010 08:26,2.55,17850,United Kingdom
536365,71053,WHITE METAL LANTERN,6,01/12/2010 08:26,3.39,17850,United Kingdom
536366,22633,HAND WARMER UNION JACK,6,01/12/2010 08:28,1.85,17850,United Kingdom
536366,22632,HAND WARMER RED POLKA DOT,6,01/12/2010 08:28,1.85,17850,United Kingdom
"""

sample_invalid_csv_data = """
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,-6,01/12/2010 08:26,-2.55,United Kingdom
536365,71053,WHITE METAL LANTERN,6,01/12/2010 08:26,3.39,United Kingdom
"""

# Sample CSV with missing columns
sample_missing_columns_csv_data = """
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,01/12/2010 08:26,2.55,United Kingdom
"""

@pytest.fixture
def valid_csv_df():
    return pd.read_csv(StringIO(sample_csv_data))

@pytest.fixture
def invalid_csv_df():
    return pd.read_csv(StringIO(sample_invalid_csv_data))

@pytest.fixture
def missing_columns_csv_df():
    return pd.read_csv(StringIO(sample_missing_columns_csv_data))

def test_validate_csv_valid(valid_csv_df):
    is_valid, message = validate_csv(valid_csv_df)
    assert is_valid == True
    assert message == "CSV file is valid."

def test_validate_csv_invalid(invalid_csv_df):
    is_valid, message = validate_csv(invalid_csv_df)
    assert is_valid == False
    assert message == "Negative values detected in Quantity or UnitPrice."

def test_validate_csv_missing_columns(missing_columns_csv_df):
    is_valid, message = validate_csv(missing_columns_csv_df)
    assert is_valid == False
    assert "Missing required columns" in message

def test_calculate_rfm(valid_csv_df):
    rfm = calculate_rfm_from_csv(StringIO(sample_csv_data))
    assert rfm is not None
    assert list(rfm.columns) == ['CustomerID', 'Amount', 'Frequency', 'Recency']
    assert len(rfm) == 1

def test_generate_top_words_table():
    sample_text = "apple banana apple orange apple banana fruit"
    top_words_df = generate_top_words_table(sample_text)
    
    expected_keywords = ['apple', 'banana', 'orange', 'fruit']
    assert top_words_df is not None
    assert len(top_words_df) == 4
    assert all(word in expected_keywords for word in top_words_df['Keyword'].tolist())

def test_generate_wordcloud_image():
    sample_text = "apple banana apple orange apple banana fruit"
    fig = generate_wordcloud_image(sample_text)
    
    assert fig is not None

def test_get_cluster_inference():
    cluster_id = 0  # Adjust this as per your data
    inference = get_cluster_inference(cluster_id)
    
    assert inference is not None
    assert isinstance(inference, str)

def test_get_keywords_for_cluster():
    cluster_id = 0  # Adjust this as per your data
    keywords = get_keywords_for_cluster(cluster_id)
    
    assert keywords is not None
    assert isinstance(keywords, str)

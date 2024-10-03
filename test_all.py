import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch
from utils import validate_csv, calculate_rfm_from_csv, get_cluster_inference, get_keywords_for_cluster, generate_top_words_table

# Sample data for testing
sample_csv = """
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,01-12-10 08:28,2.55,17850,United Kingdom
536365,71053,WHITE METAL LANTERN,6,01-12-10 08:28,3.39,17850,United Kingdom
"""

# Test validate_csv function
def test_validate_csv():
    # Valid CSV test case
    df = pd.read_csv(StringIO(sample_csv))
    is_valid, message = validate_csv(df)
    assert is_valid is True
    assert message == "CSV file is valid."
    
    # Missing column test case
    df_invalid = df.drop(columns=['CustomerID'])
    is_valid, message = validate_csv(df_invalid)
    assert is_valid is False
    assert "Missing required columns" in message
    
    # Negative value test case
    df_invalid = df.copy()
    df_invalid['Quantity'] = -1
    is_valid, message = validate_csv(df_invalid)
    assert is_valid is False
    assert "Negative values detected in Quantity or UnitPrice." in message

    # Multiple CustomerID test case
    df_invalid = df.copy()
    df_invalid['CustomerID'] = [17850, 17851]  # Changing CustomerID to trigger multiple customers
    is_valid, message = validate_csv(df_invalid)
    assert is_valid is False
    assert "Multiple CustomerIDs found. Please provide data for only one customer." in message

# Test calculate_rfm_from_csv function
@patch('utils.validate_csv', return_value=(True, "CSV file is valid."))
def test_calculate_rfm_from_csv(mock_validate_csv):
    csv_file = StringIO(sample_csv)
    rfm, message = calculate_rfm_from_csv(csv_file)  # Ensure your calculate_rfm_from_csv returns a tuple
    
    assert rfm is not None
    assert list(rfm.columns) == ['CustomerID', 'Amount', 'Frequency', 'Recency']
    assert message == "RFM Calculation Completed"  # Check if the message is also returned

# Test get_cluster_inference function
def test_get_cluster_inference():
    cluster_info = {0: {'description': 'High value customers'}}
    with patch('utils.cluster_info', new=cluster_info):  # Correctly patch the cluster_info
        description = get_cluster_inference(cluster_info, 0)  # Pass cluster_info to the function
        assert description == 'High value customers'

# Test get_keywords_for_cluster function
def test_get_keywords_for_cluster():
    cluster_info = {0: {'keywords': 'loyal frequent shopper'}}
    with patch('utils.cluster_info', new=cluster_info):  # Correctly patch the cluster_info
        keywords = get_keywords_for_cluster(cluster_info, 0)  # Pass cluster_info to the function
        assert keywords == 'loyal frequent shopper'

# Test generate_top_words_table function
def test_generate_top_words_table():
    text = "loyal frequent shopper loyal buyer"
    top_words_df = generate_top_words_table(text)
    
    assert list(top_words_df.columns) == ['Keyword', 'Frequency']
    assert top_words_df.index[0] == 1  # Check if the index starts from 1
    assert top_words_df['Keyword'].iloc[0] == 'loyal'  # Check if 'loyal' is one of the top words

if __name__ == "__main__":
    pytest.main()


from ingestion.src.filters import extract_filter_names

test_cases = [
    """Filter Name: Test Center Name
Registration Number: 123456789""",

    """Column: Confidence Index
Status Code: ACTIVE
Device Name: iPhone 14""",

    """This is just random text without any filter
Page 5 of 10""",

    """Test Start Date: 2025-01-15
Sent to Scoring Date: 2025-02-01"""
]

for i, text in enumerate(test_cases, 1):
    filters = extract_filter_names(text)
    print(f"\nTest {i}:")
    print("Input text:")
    print(text)
    print("Extracted filters:", filters)
    print("-" * 50)
import re

def extract_filter_names(text: str) -> list:
    filters = set()

    important_keywords = ['name', 'date', 'code', 'id', 'status', 'index', 'number', 'flag']

    # Pattern 1: Keep as-is (good for "Filter Name:")
    matches = re.findall(r"Filter Name[:\s]+([A-Za-z0-9\s\(\)#&-]+?)(?:\n|$)", text, re.IGNORECASE)
    for m in matches:
        cleaned = m.strip().split('\n')[0]
        if len(cleaned) < 50:
            filters.add(cleaned.strip())

    # Pattern 2: Much better - capture anything before colon that looks like a column/filter name
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line:
            # Split on first colon only
            parts = line.split(':', 1)
            if len(parts) == 2:
                potential_name = parts[0].strip()
               
                if any(word in potential_name.lower() for word in important_keywords ):
                    if 3 < len(potential_name) < 60:  
                        filters.add(potential_name.strip())

    return sorted(list(filters))  
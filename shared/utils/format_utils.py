from bs4 import BeautifulSoup

def truncate_html(html, max_length=30)->tuple[str, int]:
    if not html or not isinstance(html, str):
        return None, 0
    soup = BeautifulSoup(html, "html.parser")
    text_content = soup.get_text(" ")
    truncated_text = text_content[:max_length].strip() 
    
    if len(text_content) > max_length:
        truncated_text = truncated_text+"..."
    return truncated_text, len(text_content)


def truncate_text(text, max_length=30)->str:
    return text[:max_length] + "..." if len(text) > max_length else text
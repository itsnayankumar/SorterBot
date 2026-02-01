import re

MEDIA_EXTENSIONS = {'mkv', 'mp4', 'avi', 'mov', 'flv', 'wmv', 'webm', 'srt', 'ass'}
SPAM_TLDS = {'com', 'net', 'org', 'info', 'biz', 'xyz', 'club', 'pro', 'dad', 'leech', 'fuck', 'bot', 'link'}

def robust_cleaner(text):
    if not text: return ""

    # Remove URL schemes
    text = re.sub(r'(https?://|www\.|t\.me/|telegram\.me/|magnet:\?)[^\s]+', '', text, flags=re.IGNORECASE)
    # Remove Usernames
    text = re.sub(r'@[a-zA-Z0-9_]+', '', text)

    # Domain Filter Logic
    def domain_filter(match):
        ext = match.group(2).lower()
        if ext in MEDIA_EXTENSIONS: return match.group(0) # Keep .mkv
        if ext in SPAM_TLDS or len(ext) <= 3: return ""   # Delete .com
        return match.group(0)

    text = re.sub(r'\b([\w-]+)\.([a-zA-Z]{2,10})\b', domain_filter, text)
    return re.sub(r'\s+', ' ', text).strip()

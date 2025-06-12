import regex

# Bạn không cần thay đổi gì ở hàm này, nó đã khá tốt
def remove_headers_footers(text, header_patterns=None, footer_patterns=None):
    """Xóa các dòng header/footer dựa trên các mẫu regex."""
    if header_patterns is None:
        # Mẫu thực tế hơn: xóa các dòng chứa "Trang X", "Số hiệu: Y"
        header_patterns = [r'^(Trang|Page)\s+\d+', r'^(Số hiệu|Ref No):.*$']
    if footer_patterns is None:
        footer_patterns = [r'^.*Footer.*$'] # Giữ lại mẫu footer cũ

    for pattern in header_patterns + footer_patterns:
        text = regex.sub(pattern, '', text, flags=regex.MULTILINE | regex.IGNORECASE)

    return text.strip()


def remove_special_characters_vietnamese_safe(text):
    """
    Xóa các ký tự đặc biệt không mong muốn nhưng giữ lại toàn bộ chữ cái và số của mọi ngôn ngữ (bao gồm tiếng Việt).
    \p{L} -> Bất kỳ chữ cái Unicode nào (a, b, c, á, à, ậ, đ...)
    \p{N} -> Bất kỳ chữ số Unicode nào (1, 2, 3...)
    \s -> Khoảng trắng
    Dấu câu được liệt kê tường minh: .,;:'"?!-
    """
    # Regex này giữ lại chữ cái, số, khoảng trắng và các dấu câu cần thiết
    pattern = r'[^\p{L}\p{N}\s.,;:\'"?!-]'
    
    # Thay thế các ký tự không mong muốn (ví dụ: emoji, ký tự khối,...) bằng một khoảng trắng
    text = regex.sub(pattern, ' ', text)
    return text.strip()

def normalize_repeated_punctuation(text):
    """
    Chuẩn hóa các dấu câu bị lặp lại (ví dụ: ... thành ., ?? thành ?, !! thành !)
    ([.?!]) -> Bắt giữ một trong các dấu ., ?, ! vào group 1.
    \1+ -> Tìm kiếm thêm 1 hoặc nhiều lần ký tự đã bị bắt giữ ở group 1.
    r'\1' -> Thay thế toàn bộ chuỗi tìm thấy bằng chỉ một ký tự của group 1.
    """
    text = regex.sub(r'([.?!])\1+', r'\1', text)
    return text.strip()

def normalize_whitespace(text):
    """Chuẩn hóa các khoảng trắng và dòng mới thừa."""
    # Thay thế nhiều dòng mới liên tiếp bằng một dòng mới duy nhất (để giữ lại cấu trúc đoạn)
    text = regex.sub(r'\n{3,}', '\n\n', text)
    # Thay thế nhiều khoảng trắng/tab bằng một khoảng trắng duy nhất
    text = regex.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def preprocess_text(text: str) -> str:
    """
    Pipeline hoàn chỉnh để tiền xử lý văn bản, an toàn cho tiếng Việt.
    """
    if not isinstance(text, str):
        return ""

    # 1. Xóa các khối lớn không cần thiết như header/footer
    text = remove_headers_footers(text)
    
    # 2. Xóa các ký tự đặc biệt không mong muốn một cách an toàn
    text = remove_special_characters_vietnamese_safe(text)

    # 3. Chuẩn hóa các dấu câu lặp lại
    text = normalize_repeated_punctuation(text)

    # 4. Chuẩn hóa khoảng trắng (thường làm cuối cùng để dọn dẹp)
    text = normalize_whitespace(text)

    return text.strip()

import yaml
import os

def switch_voice_language(target_language: str) -> str:
    """
    Hàm gọi tự động giúp AI sửa cấu hình bộ lọc đơn ngữ của bộ nghe ASR.
    Hỗ trợ 3 ngôn ngữ mục tiêu: 'vi' (Tiếng Việt), 'en' (Tiếng Anh), 'fi' (Tiếng Phần Lan)
    """
    config_path = "config.yaml"
    valid_langs = {
        'vi': 'vi', 'vietnam': 'vi', 'tiếng việt': 'vi',
        'en': 'en', 'english': 'en', 'tiếng anh': 'en',
        'fi': 'fi', 'finnish': 'fi', 'suomi': 'fi', 'tiếng phần lan': 'fi'
    }
    
    lang_code = valid_langs.get(target_language.lower())
    if not lang_code:
        return f"Ngôn ngữ '{target_language}' hiện chưa được cấu hình bộ lọc Native."
        
    if not os.path.exists(config_path):
        return "Lỗi hệ thống: Không tìm thấy file config.yaml."
        
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # Cập nhật ngôn ngữ nhận diện đơn ngữ
        config['ASR']['language'] = lang_code
        
        # Đồng bộ giọng đọc phản hồi tương ứng của Microsoft Edge
        if lang_code == 'en':
            config['TTS']['language'] = 'en-US'
            config['TTS']['voice'] = 'en-US-BrianNeural'
        elif lang_code == 'fi':
            config['TTS']['language'] = 'fi-FI'
            config['TTS']['voice'] = 'fi-FI-HarriNeural'
        else:
            config['TTS']['language'] = 'vi-VN'
            config['TTS']['voice'] = 'vi-VN-NamMinhNeural'
            
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
        return f"SUCCESS: Đã đồng bộ toàn bộ hệ thống sang Chế độ ngôn ngữ Native: {lang_code.upper()}."
    except Exception as e:
        return f"Lỗi cập nhật cấu hình: {str(e)}"

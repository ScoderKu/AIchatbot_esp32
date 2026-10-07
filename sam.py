# -*- coding: utf-8 -*-
import os

def setup_project():
    print("=== Khởi tạo cấu trúc dự án AI Chatbot Local Xiaozhi ===")
    
    # 1. Tạo file cấu hình khởi động Docker cho bộ nghe ASR Faster-Whisper
    with open("docker-compose.yml", "w", encoding="utf-8") as f:
        f.write('''version: '3.8'

services:
  faster-whisper:
    image: fedirz/faster-whisper-server:latest
    container_name: xiaozhi-asr-whisper
    ports:
      - "10095:10095"
    volumes:
      - ./whisper_models:/root/.cache/huggingface
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    command: --model small --device cuda --port 10095
    restart: unless-stopped
''')
    print("[+] Đã tạo file: docker-compose.yml (Bộ nghe ASR GPU)")

    # 2. Tạo file cấu hình tham số cốt lõi kết nối thiết bị với bộ não Ollama 14B
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write('''# ====================================================================
# CONFIG LÕI TỐI ƯU CHO HỆ THỐNG GIAO TIẾP GIỌNG NÓI GIÁO DỤC TRẺ EM
# Phần cứng yêu cầu: RTX 2070 Super 8GB VRAM / 32GB RAM hệ thống
# ====================================================================

LLM:
  type: "Ollama"
  base_url: "http://localhost:11434"
  model_name: "qwen2.5:14b-instruct"
  system_prompt: >
    Bạn là một trợ lý giáo dục thông minh, vui tính, tràn đầy năng lượng và cực kỳ kiên nhẫn dành cho trẻ em.
    Bạn thành thạo Tiếng Việt, Tiếng Anh và Tiếng Phần Lan. 
    Hãy sử dụng ngôn ngữ đơn giản, ẩn dụ dễ hiểu để giải thích kiến thức khoa học, giải toán đố và chơi trò chơi tương tác giọng nói cùng bé.
    Khi chơi trò chơi, không được nói thẳng đáp án mà hãy gợi ý từ từ và luôn khen ngợi để khích lệ tinh thần của bé.

ASR:
  type: "FasterWhisper"
  url: "ws://localhost:10095" 
  language: "vi"       # Ngôn ngữ lọc mặc định ban đầu là tiếng Việt

TTS:
  type: "EdgeTTS"
  language: "vi-VN"
  voice: "vi-VN-NamMinhNeural"
''')
    print("[+] Đã tạo file: config.yaml (Cấu hình tham số lõi)")

    # 3. Tạo script Python gọi hàm để AI tự can thiệp đổi ngôn ngữ hệ thống
    with open("switch_lang.py", "w", encoding="utf-8") as f:
        f.write('''import yaml
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
''')
    print("[+] Đã tạo file: switch_lang.py (Plugin gọi hàm đổi ngôn ngữ)")
    print("\\n=== HOÀN THÀNH KHỞI TẠO DỰ ÁN MIỄN PHÍ OMNI LOCAL ===")

if __name__ == "__main__":
    setup_project()

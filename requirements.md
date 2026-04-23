# Requirements

Dựa trên các thư viện bạn đã import và các phiên bản hiện có trong môi trường ảo `.venv`, dưới đây là danh sách chi tiết các thư viện cần cài đặt.

Bạn có thể tạo một file tên là `requirements.txt` và copy nội dung sau vào:

```text
python-dotenv==1.2.1
gradio==4.44.0
requests==2.32.5
langchain==0.1.20
langchain-community==0.0.38
langchain-chroma==0.1.1
langchain-ollama==0.1.0
ollama==0.1.8
chromadb==0.5.23
numpy==1.26.4
scikit-learn==1.3.2
plotly==5.18.0
SQLAlchemy==2.0.23
```

*(Các thư viện như `functools`, `concurrent.futures`, `time`, `json`, và `pathlib` là thư viện chuẩn của Python nên không cần phải cài đặt qua pip).*

## Cài đặt

Để cài đặt các thư viện trên, bạn hãy mở terminal và chạy lệnh:

```bash
pip install -r requirements.txt
```

Hoặc nếu bạn muốn cài đặt nhanh trực tiếp bằng một dòng lệnh:

```bash
pip install python-dotenv==1.2.1 gradio==4.44.0 requests==2.32.5 langchain==0.1.20 langchain-community==0.0.38 langchain-chroma==0.1.1 langchain-ollama==0.1.0 ollama==0.1.8 chromadb==0.5.23 numpy==1.26.4 scikit-learn==1.3.2 plotly==5.18.0 SQLAlchemy==2.0.23
```
from typing import List, Dict, Optional
from transformers import AutoTokenizer
import re

# ====== Cấu hình ======
BASE_MODEL    = "Qwen/Qwen2.5-3B-Instruct"  # tokenizer mở, không bị gate
MIN_TOKENS    = 150                         # tối thiểu token (sau tokenize)
MAX_TOKENS    = 3000                         # truncate theo tokens
MIN_CHARS     = 300                         # tối thiểu ký tự “thô”
MAX_CHARS     = 8000                        # GIỚI HẠN: chỉ lấy hội thoại ≤ 8000 ký tự

class ConversationItem:
    """
    Mẫu hội thoại đã clean để fine-tune / phân tích.
    """
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    id: Optional[str]
    messages: List[Dict[str, str]]
    token_count: int = 0
    text: Optional[str] = None
    length_chars: int = 0
    include: bool = False

    def __init__(self, data: Dict):
        self.id = str(data.get("id")) if data.get("id") is not None else None
        self.messages = []
        self.parse(data)

    # --- clean text giữ dấu câu cơ bản ---
    def clean_text(self, s) -> str:
        if not s:
            return ""
        s = str(s)
        s = re.sub(r"[^\w\s.,?!:;()/%\-\"'…]", " ", s)  # bỏ ký tự lạ
        s = re.sub(r"\s+", " ", s).strip()
        s = re.sub(r"([.!?])\1{1,}", r"\1", s)          # gom !!!??? -> ! ?
        return s

    def parse(self, data: Dict):
        convs = data.get("conversations") or []
        msgs: List[Dict[str, str]] = []

        for turn in convs:
            role_raw = (turn.get("from") or turn.get("role") or "").lower()
            role = "user" if role_raw in ("human", "user") else "assistant"
            content = self.clean_text(turn.get("value") or turn.get("content") or "")
            if content:
                msgs.append({"role": role, "content": content})

        # đảm bảo mở đầu bằng user
        if msgs and msgs[0]["role"] != "user":
            msgs = [{"role": "user", "content": ""}] + msgs

        # ghép text để đo độ dài & lọc theo ký tự
        raw_text = "\n".join(m["content"] for m in msgs)
        self.length_chars = len(raw_text)

        # lọc theo ký tự tối thiểu & tối đa (KHÔNG truncate về MAX_CHARS)
        if self.length_chars < MIN_CHARS or self.length_chars > MAX_CHARS:
            self.include = False
            return

        # tokenize để lọc theo tokens
        ids = self.tokenizer.encode(raw_text, add_special_tokens=False)
        if len(ids) < MIN_TOKENS:
            self.include = False
            return

        # truncate theo MAX_TOKENS (theo token, không phải ký tự)
        ids = ids[:MAX_TOKENS]
        self.text = self.tokenizer.decode(ids, skip_special_tokens=True)

        # gán dữ liệu cuối
        self.messages = msgs
        self.token_count = len(ids)
        self.include = True

    def to_sft(self) -> Dict:
        return {"id": self.id, "messages": self.messages}

    def __repr__(self):
        return (f"<Conversation id={self.id} chars={self.length_chars} "
                f"tokens={self.token_count} include={self.include}>")

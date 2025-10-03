from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from ConversationItems import ConversationItem  # giống cấu trúc BookLoader

CHUNK_SIZE = 1000  # để tương tự BookLoader

def from_datapoint(dp):
    try:
        item = ConversationItem(dp)
        return item if item.include else None
    except Exception:
        return None

def from_chunk(chunk):
    return [it for it in (from_datapoint(dp) for dp in chunk) if it]

def chunk_generator(rawdata, chunk_size=CHUNK_SIZE):
    size = len(rawdata)
    for i in range(0, size, chunk_size):
        yield rawdata.select(range(i, min(i + chunk_size, size)))

def load_conversations_from_rawdata(rawdata, workers=8):
    results = []
    total = (len(rawdata) + CHUNK_SIZE - 1) // CHUNK_SIZE
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for batch in tqdm(
            pool.map(from_chunk, chunk_generator(rawdata)),
            total=total,
            desc="Loading conversations"
        ):
            results.extend(batch)
    return results

# Windows lưu ý khi gọi trực tiếp file này:
# if __name__ == "__main__":
#     ... gọi load_conversations_from_rawdata(...) ở đây để tránh lỗi ProcessPool

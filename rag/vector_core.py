import os
import json
import hashlib
import numpy as np
from core.settings import VECTOR_DB_PATH

# 向量维度
VECTOR_DIM = 384


class SimpleVectorStore:
    """纯Python本地向量存储，零外部依赖，跨平台"""

    def __init__(self, path: str):
        self.path = path
        self.data_file = os.path.join(path, "vectors.json")
        os.makedirs(path, exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.vectors = data.get("vectors", [])
            self.metadata_list = data.get("metadata", [])
            self.ids = data.get("ids", [])
        else:
            self.vectors = []
            self.metadata_list = []
            self.ids = []
            self._save()

    def _save(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump({
                "vectors": self.vectors,
                "metadata": self.metadata_list,
                "ids": self.ids
            }, f, ensure_ascii=False)

    def _text_to_vector(self, text: str) -> list:
        """简易文本向量化（生产环境替换为embedding API）"""
        seed = hashlib.md5(text.encode()).digest()
        np.random.seed(int.from_bytes(seed[:4], 'big'))
        vec = np.random.randn(VECTOR_DIM).astype(np.float32)
        vec = vec / (np.linalg.norm(vec) + 1e-8)
        return vec.tolist()

    def add(self, doc_id: str, text: str, metadata: dict):
        """添加文档"""
        # 先删除旧记录
        if doc_id in self.ids:
            idx = self.ids.index(doc_id)
            self.vectors.pop(idx)
            self.metadata_list.pop(idx)
            self.ids.pop(idx)

        vec = self._text_to_vector(text)
        self.vectors.append(vec)
        self.metadata_list.append({**metadata, "content": text})
        self.ids.append(doc_id)
        self._save()

    def search(self, query_text: str, top_k: int = 5, avatar_id: int = None,
               emotion_type: str = "", social_type: str = "") -> list:
        """向量检索"""
        if not self.vectors:
            return []

        query_vec = np.array(self._text_to_vector(query_text), dtype=np.float32)
        all_vecs = np.array(self.vectors, dtype=np.float32)

        # 余弦相似度
        similarities = np.dot(all_vecs, query_vec)

        scored = []
        for i, sim in enumerate(similarities):
            meta = self.metadata_list[i]
            # 过滤
            if avatar_id is not None and str(meta.get("avatar_id", "")) != str(avatar_id):
                continue
            if emotion_type and meta.get("emotion_type", "") != emotion_type:
                continue
            if social_type and meta.get("social_type", "") != social_type:
                continue
            weight = meta.get("weight", 1)
            scored.append((weight, meta.get("content", ""), float(sim)))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

    def delete_by_avatar(self, avatar_id: int):
        """删除指定分身的所有数据"""
        indices_to_remove = []
        for i, meta in enumerate(self.metadata_list):
            if str(meta.get("avatar_id", "")) == str(avatar_id):
                indices_to_remove.append(i)

        for i in reversed(indices_to_remove):
            self.vectors.pop(i)
            self.metadata_list.pop(i)
            self.ids.pop(i)

        self._save()

    def count(self) -> int:
        return len(self.ids)


# 全局单例
_store = None


def get_store() -> SimpleVectorStore:
    global _store
    if _store is None:
        _store = SimpleVectorStore(VECTOR_DB_PATH)
    return _store


def init_vector_store():
    """初始化向量存储（应用启动时调用）"""
    store = get_store()
    print(f"[VectorStore] 本地向量库已就绪，当前 {store.count()} 条记录。路径: {VECTOR_DB_PATH}")
    return store


def insert_rag_sample(user_id: int, avatar_id: int, emotion_type: str, social_type: str,
                      content: str, weight: int = 1):
    """入库RAG样本"""
    store = get_store()
    point_id = hashlib.md5(f"{avatar_id}_{content}".encode()).hexdigest()
    store.add(point_id, content, {
        "user_id": user_id,
        "avatar_id": avatar_id,
        "emotion_type": emotion_type,
        "social_type": social_type,
        "weight": weight
    })


def search_rag(avatar_id: int, query_text: str, emotion_type: str = "",
               social_type: str = "", top_k: int = 5) -> list:
    """分层RAG检索"""
    store = get_store()
    return store.search(query_text, top_k, avatar_id, emotion_type, social_type)


def clear_avatar_rag(avatar_id: int):
    """清空指定分身的所有RAG数据"""
    store = get_store()
    store.delete_by_avatar(avatar_id)

import json
import sqlite3
from typing import Optional, Dict
from infrastructure.db.connection import get_connection


class WeightRepository:
    def save(self, user_id: int, raw_weights: Dict[str, float]) -> None:
        total = sum(raw_weights.values())
        if total == 0:
            raise ValueError("Сумма весов не может быть нулевой")
        normalized = {k: v / total for k, v in raw_weights.items()}
        raw_json = json.dumps(raw_weights, ensure_ascii=False)
        norm_json = json.dumps(normalized, ensure_ascii=False)

        conn = get_connection()
        try:
            # Удаляем старую запись, если есть
            conn.execute("DELETE FROM user_weights WHERE user_id = ?", (user_id,))
            # Вставляем новую
            conn.execute(
                "INSERT INTO user_weights (user_id, weights, raw_weights) VALUES (?, ?, ?)",
                (user_id, norm_json, raw_json)
            )
            conn.commit()
            print(f"[SAVE SUCCESS] user_id={user_id} raw={raw_weights}")
        except Exception as e:
            print(f"[SAVE ERROR] {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_raw(self, user_id: int) -> Optional[Dict[str, float]]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT raw_weights FROM user_weights WHERE user_id = ?", (user_id,)).fetchone()
            if row:
                return json.loads(row["raw_weights"])
        except Exception as e:
            print(f"[GET ERROR] {e}")
        finally:
            conn.close()
        return None

    def get_normalized(self, user_id: int) -> Optional[Dict[str, float]]:
        conn = get_connection()
        try:
            row = conn.execute("SELECT weights FROM user_weights WHERE user_id = ?", (user_id,)).fetchone()
            if row:
                return json.loads(row["weights"])
        except Exception as e:
            print(f"[GET ERROR] {e}")
        finally:
            conn.close()
        return None
import sqlite3
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from infrastructure.db.connection import get_connection


@dataclass
class CommentRow:
    id: int
    user_id: int
    user_name: str          
    target_user_id: int
    text: str
    created_at: str


class CommentRepository:
    def add(self, user_id: int, target_user_id: int, text: str) -> int:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO comments (user_id, target_user_id, text) VALUES (?, ?, ?)",
            (user_id, target_user_id, text)
        )
        conn.commit()
        comment_id = cursor.lastrowid
        conn.close()
        return comment_id

    def get_by_target(self, target_user_id: int) -> List[CommentRow]:
        conn = get_connection()
        rows = conn.execute("""
            SELECT c.id, c.user_id, u.name as user_name, c.target_user_id, c.text, c.created_at
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.target_user_id = ?
            ORDER BY c.created_at DESC
        """, (target_user_id,)).fetchall()
        conn.close()
        return [
            CommentRow(
                id=row["id"],
                user_id=row["user_id"],
                user_name=row["user_name"],
                target_user_id=row["target_user_id"],
                text=row["text"],
                created_at=row["created_at"]
            )
            for row in rows
        ]

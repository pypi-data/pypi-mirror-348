"""
Tiny persistence layer for *programs* and their KPI metrics.

Schema
------
programs(id TEXT PK,
         code TEXT NOT NULL,
         parent_id TEXT,
         metrics TEXT,           -- JSON string (nullable until eval completed)
         created REAL)           -- Unix seconds
"""

import os, sqlite3, uuid, json, time, random
from pathlib import Path
from typing import Optional, Dict, Any, List

from pwb_alphaevolve.config import settings


class ProgramStore:
    def __init__(self, db_path: str | os.PathLike = "~/.pwb_alphaevolve/programs.db"):
        db_path = Path(db_path).expanduser()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(
            db_path, check_same_thread=False, isolation_level=None  # autocommit
        )
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS programs(
                 id TEXT PRIMARY KEY,
                 code TEXT NOT NULL,
                 parent_id TEXT,
                 metrics TEXT,
                 created REAL
               )"""
        )

    # -------------------------------------------------------------- #
    # basic CRUD
    # -------------------------------------------------------------- #
    def insert(
        self,
        code: str,
        metrics: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
        prog_id: Optional[str] = None,
    ) -> str:
        prog_id = prog_id or str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO programs(id, code, parent_id, metrics, created) VALUES (?,?,?,?,?)",
            (
                prog_id,
                code,
                parent_id,
                json.dumps(metrics) if metrics is not None else None,
                time.time(),
            ),
        )
        return prog_id

    def update_metrics(self, prog_id: str, metrics: Dict[str, Any]) -> None:
        self.conn.execute(
            "UPDATE programs SET metrics=? WHERE id=?",
            (json.dumps(metrics), prog_id),
        )

    def get(self, prog_id: str) -> Optional[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM programs WHERE id=?", (prog_id,))
        row = cur.fetchone()
        return self._row_to_dict(row) if row else None

    def sample(self, prog_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if prog_id:
            return self.get(prog_id)
        # random row (weighted toward evaluated programs)
        cur = self.conn.execute("SELECT * FROM programs ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
        return self._row_to_dict(row) if row else None

    def top_k(
        self, k: int = 5, metric: str = settings.hof_metric
    ) -> List[Dict[str, Any]]:
        cur = self.conn.execute("SELECT * FROM programs WHERE metrics IS NOT NULL")
        rows = [self._row_to_dict(r) for r in cur.fetchall()]
        rows.sort(key=lambda r: r["metrics"].get(metric, 0.0), reverse=True)
        return rows[:k]

    # -------------------------------------------------------------- #
    # helpers
    # -------------------------------------------------------------- #
    @staticmethod
    def _row_to_dict(row) -> Dict[str, Any]:
        (
            prog_id,
            code,
            parent_id,
            metrics_json,
            created,
        ) = row
        return {
            "id": prog_id,
            "code": code,
            "parent_id": parent_id,
            "metrics": json.loads(metrics_json) if metrics_json else None,
            "created": created,
        }

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any

class BancoDados:
    """Módulo simples de banco de dados SQLite para persistência local."""
    
    def __init__(self):
        # Cria a pasta data se não existir
        self.db_path = Path(__file__).parent.parent / "data" / "profaplanner.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabela de alunos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    faixa TEXT NOT NULL,
                    evolucao TEXT NOT NULL
                )
            ''')
            conn.commit()

    # --- Alunos ---
    def get_alunos(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nome, faixa, evolucao FROM alunos')
            rows = cursor.fetchall()
            alunos = []
            for row in rows:
                alunos.append({
                    "id": row[0],
                    "nome": row[1],
                    "faixa": row[2],
                    "evolucao": json.loads(row[3]) if row[3] else {}
                })
            return alunos

    def add_aluno(self, nome: str, faixa: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO alunos (nome, faixa, evolucao) VALUES (?, ?, ?)',
                (nome, faixa, "{}")
            )
            conn.commit()
            return cursor.lastrowid

    def delete_aluno(self, aluno_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM alunos WHERE id = ?', (aluno_id,))
            conn.commit()

    def update_evolucao(self, aluno_id: int, evolucao: Dict[str, str]):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE alunos SET evolucao = ? WHERE id = ?',
                (json.dumps(evolucao), aluno_id)
            )
            conn.commit()

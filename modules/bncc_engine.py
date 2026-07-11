import json
from pathlib import Path
from typing import Optional


class BNCCEngine:
    """Motor de busca e filtragem dos objetivos BNCC de Educação Infantil."""

    def __init__(self):
        data_path = Path(__file__).parent.parent / "data" / "bncc_ei.json"
        with open(data_path, "r", encoding="utf-8") as f:
            self.dados = json.load(f)
        self._indexar()

    def _indexar(self):
        """Cria índice plano de todos os objetivos para busca eficiente."""
        self.indice = []
        for campo in self.dados["campos_de_experiencia"]:
            for faixa in campo["faixas"]:
                for obj in faixa["objetivos"]:
                    self.indice.append(
                        {
                            "codigo": obj["codigo"],
                            "descricao": obj["descricao"],
                            "palavras_chave": obj["palavras_chave"],
                            "campo_codigo": campo["codigo"],
                            "campo_nome": campo["nome"],
                            "faixa": faixa["faixa"],
                            "faixa_descricao": faixa["descricao"],
                        }
                    )

    def buscar(
        self,
        texto: str,
        faixa: Optional[str] = None,
        campo: Optional[str] = None,
    ) -> list:
        """Busca objetivos BNCC por palavras-chave no texto informado."""
        palavras = [p.lower() for p in texto.split() if len(p) >= 3]
        scores: dict[str, int] = {}
        candidatos = []

        for obj in self.indice:
            # Aplicar filtros
            if faixa and obj["faixa"] != faixa:
                continue
            if campo and obj["campo_codigo"] != campo:
                continue

            score = 0
            descricao_lower = obj["descricao"].lower()
            chaves_lower = [pk.lower() for pk in obj["palavras_chave"]]

            for palavra in palavras:
                # Match exato na descrição
                if palavra in descricao_lower:
                    score += 3
                # Match exato em palavras-chave
                for chave in chaves_lower:
                    if palavra == chave:
                        score += 2
                    elif palavra in chave or chave in palavra:
                        score += 1

            if score > 0:
                scores[obj["codigo"]] = score
                candidatos.append(obj)

        # Fallback: se nenhum resultado, retorna até 5 objetivos da faixa/campo
        if not candidatos:
            for obj in self.indice:
                if faixa and obj["faixa"] != faixa:
                    continue
                if campo and obj["campo_codigo"] != campo:
                    continue
                candidatos.append(obj)
            return candidatos[:5]

        # Ordena por relevância e retorna até 10
        candidatos.sort(key=lambda x: scores.get(x["codigo"], 0), reverse=True)
        return candidatos[:10]

    def get_objetivos_por_faixa(self, faixa: str) -> dict:
        """Retorna todos os objetivos de uma faixa, agrupados por campo de experiência."""
        resultado: dict[str, list] = {}
        for campo in self.dados["campos_de_experiencia"]:
            for f in campo["faixas"]:
                if f["faixa"] == faixa:
                    resultado[campo["nome"]] = f["objetivos"]
        return resultado

    def get_objetivo(self, codigo: str) -> Optional[dict]:
        """Retorna um objetivo específico pelo código alfanumérico."""
        for obj in self.indice:
            if obj["codigo"] == codigo:
                return obj
        return None

    def get_campos(self) -> list[tuple[str, str]]:
        """Retorna lista de (codigo, nome) dos campos de experiência."""
        return [
            (c["codigo"], c["nome"]) for c in self.dados["campos_de_experiencia"]
        ]

    def get_todos_objetivos(
        self, faixa: Optional[str] = None, campo: Optional[str] = None
    ) -> list:
        """Retorna todos os objetivos, com filtros opcionais."""
        resultado = []
        for obj in self.indice:
            if faixa and obj["faixa"] != faixa:
                continue
            if campo and obj["campo_codigo"] != campo:
                continue
            resultado.append(obj)
        return resultado

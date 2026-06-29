"""
Cliente da API TMDB (The Movie Database) — gratuita com cadastro.
Docs: https://developer.themoviedb.org/docs
"""
import os

import requests

TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"
IMG_BASE_ORIGINAL = "https://image.tmdb.org/t/p/original"

# Demo quando não há chave (aula funciona offline)
_DEMO_FILMES = [
    {
        "id": 550,
        "title": "Clube da Luta",
        "overview": "Um homem solitário conhece um vendedor de sabonete e forma um clube de luta clandestino.",
        "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
        "vote_average": 8.4,
        "release_date": "1999-10-15",
    },
    {
        "id": 27205,
        "title": "A Origem",
        "overview": "Um ladrão invade sonhos para plantar uma ideia na mente de um CEO.",
        "poster_path": "/oYu0037M7541PxH2N22L6Q26Ia.jpg",
        "vote_average": 8.8,
        "release_date": "2010-07-16",
    },
    {
        "id": 155,
        "title": "Batman: O Cavaleiro das Trevas",
        "overview": "Batman enfrenta o Coringa, criminoso que mergulha Gotham no caos.",
        "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
        "vote_average": 9.0,
        "release_date": "2008-07-18",
    },
]

_DEMO_STREAMING = {
    550: {
        "flatrate": [{"provider_name": "Netflix", "logo_path": "/t2yyOvP6iX0U6R9MvL3w8x9x9x9x.jpg"}],
        "rent": [{"provider_name": "Apple TV", "logo_path": None}],
    },
    27205: {
        "flatrate": [{"provider_name": "HBO Max", "logo_path": None}],
        "rent": [{"provider_name": "Google Play", "logo_path": None}],
    },
    155: {
        "flatrate": [{"provider_name": "Prime Video", "logo_path": None}],
        "buy": [{"provider_name": "YouTube", "logo_path": None}],
    },
}


class TmdbApi:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY", "").strip()
        self.region = os.getenv("TMDB_REGION", "BR")
        self.language = os.getenv("TMDB_LANGUAGE", "pt-BR")
        self.modo_demo = not self.api_key or self.api_key == "sua_chave_aqui"

    @property
    def usando_demo(self):
        return self.modo_demo

    def _get(self, endpoint, params=None):
        if self.modo_demo:
            return None
        params = params or {}
        params["api_key"] = self.api_key
        params.setdefault("language", self.language)
        url = f"{TMDB_BASE}{endpoint}"
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None

    @staticmethod
    def poster_url(poster_path, tamanho="w500"):
        if not poster_path:
            return None
        base = IMG_BASE if tamanho == "w500" else IMG_BASE_ORIGINAL
        return f"{base}{poster_path}"

    @staticmethod
    def logo_url(logo_path):
        if not logo_path:
            return None
        return f"https://image.tmdb.org/t/p/w45{logo_path}"

    def _normalizar_filme(self, item):
        return {
            "id": item.get("id"),
            "titulo": item.get("title") or item.get("name", "Sem título"),
            "sinopse": item.get("overview") or "Sinopse não disponível.",
            "poster_path": item.get("poster_path"),
            "poster_url": self.poster_url(item.get("poster_path")),
            "nota": round(item.get("vote_average") or 0, 1),
            "ano": (item.get("release_date") or "")[:4] or "—",
            "data_lancamento": item.get("release_date") or "",
        }

    def filmes_populares(self, pagina=1):
        if self.modo_demo:
            return [self._normalizar_filme(f) for f in _DEMO_FILMES], True
        data = self._get("/movie/popular", {"page": pagina})
        if not data:
            return [], False
        return [self._normalizar_filme(f) for f in data.get("results", [])], False

    def filmes_melhores(self, pagina=1):
        if self.modo_demo:
            return [self._normalizar_filme(f) for f in reversed(_DEMO_FILMES)], True
        data = self._get("/movie/top_rated", {"page": pagina})
        if not data:
            return [], False
        return [self._normalizar_filme(f) for f in data.get("results", [])], False

    def buscar(self, termo, pagina=1):
        if not termo.strip():
            return [], False
        if self.modo_demo:
            termo_lower = termo.lower()
            resultados = [
                self._normalizar_filme(f)
                for f in _DEMO_FILMES
                if termo_lower in f["title"].lower()
            ]
            return resultados, True
        data = self._get("/search/movie", {"query": termo, "page": pagina})
        if not data:
            return [], False
        return [self._normalizar_filme(f) for f in data.get("results", [])], False

    def detalhe(self, filme_id):
        if self.modo_demo:
            raw = next((f for f in _DEMO_FILMES if f["id"] == filme_id), None)
            if not raw:
                return None
            filme = self._normalizar_filme(raw)
            filme["generos"] = ["Drama", "Ação"]
            filme["duracao"] = 120
            return filme
        data = self._get(f"/movie/{filme_id}")
        if not data:
            return None
        filme = self._normalizar_filme(data)
        filme["generos"] = [g["name"] for g in data.get("genres", [])]
        filme["duracao"] = data.get("runtime") or 0
        return filme

    def streaming(self, filme_id):
        """Onde assistir no Brasil: flatrate (assinatura), rent, buy."""
        if self.modo_demo:
            br = _DEMO_STREAMING.get(filme_id, {})
            return self._formatar_provedores(br), True
        data = self._get(f"/movie/{filme_id}/watch/providers")
        if not data:
            return {"flatrate": [], "rent": [], "buy": []}, False
        br = data.get("results", {}).get(self.region, {})
        return self._formatar_provedores(br), False

    def _formatar_provedores(self, regiao):
        def map_lista(chave):
            itens = regiao.get(chave, []) or []
            return [
                {
                    "nome": p.get("provider_name", "Streaming"),
                    "logo_url": self.logo_url(p.get("logo_path")),
                }
                for p in itens
            ]

        return {
            "flatrate": map_lista("flatrate"),
            "rent": map_lista("rent"),
            "buy": map_lista("buy"),
        }

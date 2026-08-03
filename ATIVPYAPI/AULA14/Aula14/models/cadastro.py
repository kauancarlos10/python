from . import db
from .base import ModeloBase


class Cadastro(ModeloBase):
    __tablename__ = "cadastros"

    nome = db.Column(db.String(120), nullable=False)
    profissao = db.Column(db.String(80), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    logradouro = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100), default="")
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)

    CAMPOS_OBRIGATORIOS = (
        "nome", "profissao", "cep", "logradouro",
        "numero", "bairro", "cidade", "estado",
    )

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()

    @classmethod
    def a_partir_de_dict(cls, dados):
        """Monta um Cadastro a partir de um dict (form HTML ou JSON da API)."""
        try:
            return cls(
                nome=str(dados["nome"]).strip(),
                profissao=str(dados["profissao"]).strip(),
                cep=str(dados["cep"]).strip(),
                logradouro=str(dados["logradouro"]).strip(),
                numero=str(dados["numero"]).strip(),
                complemento=str(dados.get("complemento", "")).strip(),
                bairro=str(dados["bairro"]).strip(),
                cidade=str(dados["cidade"]).strip(),
                estado=str(dados["estado"]).strip().upper(),
            )
        except (KeyError, ValueError, TypeError) as erro:
            campos = ", ".join(cls.CAMPOS_OBRIGATORIOS)
            raise ValueError(f"Campos obrigatórios: {campos}") from erro

    def atualizar_de_dict(self, dados):
        """Atualiza só os campos que vierem no dict."""
        for campo in self.CAMPOS_OBRIGATORIOS + ("complemento",):
            if campo in dados:
                valor = str(dados[campo]).strip()
                if campo == "estado":
                    valor = valor.upper()
                setattr(self, campo, valor)

    def endereco_completo(self):
        partes = [
            f"{self.logradouro}, {self.numero}",
            self.complemento,
            self.bairro,
            f"{self.cidade}/{self.estado}",
            f"CEP {self.cep}",
        ]
        return " — ".join(p for p in partes if p)

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "profissao": self.profissao,
            "cep": self.cep,
            "logradouro": self.logradouro,
            "numero": self.numero,
            "complemento": self.complemento,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "estado": self.estado,
            "endereco_completo": self.endereco_completo(),
            "data_criacao": str(self.data_criacao),
        }

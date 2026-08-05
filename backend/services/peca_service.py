from decimal import Decimal, InvalidOperation

from backend.repositories import PecaRepository


class ValidacaoPecaError(ValueError):
    pass


class PecaService:
    CAMPOS_PERMITIDOS = {
        "nome", "descricao", "codigo", "fabricante", "categoria",
        "quantidade_estoque", "quantidade_minima", "localizacao",
        "preco_unitario",
    }

    CAMPOS_OBRIGATORIOS = {
        "nome", "codigo", "quantidade_estoque",
        "quantidade_minima", "preco_unitario",
    }

    def __init__(self, repository=None):
        self.repository = repository or PecaRepository()

    def criar(self, dados):
        dados = self._normalizar_dados(dados, criar=True)
        self._validar_codigo_unico(dados["codigo"])
        return self.repository.criar(dados)

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(self, peca_id):
        return self.repository.buscar_por_id(peca_id)

    def atualizar(self, peca_id, dados):
        peca = self.buscar_por_id(peca_id)
        if not peca:
            return None

        dados = self._normalizar_dados(dados, criar=False)

        if "codigo" in dados and dados["codigo"] != peca.codigo:
            self._validar_codigo_unico(dados["codigo"])

        return self.repository.atualizar(peca, dados)

    def excluir(self, peca_id):
        peca = self.buscar_por_id(peca_id)
        if not peca:
            return False

        self.repository.excluir(peca)
        return True

    def _normalizar_dados(self, dados, criar):
        if not isinstance(dados, dict):
            raise ValidacaoPecaError(
                "O corpo da requisição deve ser um objeto JSON."
            )

        desconhecidos = set(dados) - self.CAMPOS_PERMITIDOS
        if desconhecidos:
            campos = ", ".join(sorted(desconhecidos))
            raise ValidacaoPecaError(f"Campos não permitidos: {campos}.")

        if criar:
            ausentes = self.CAMPOS_OBRIGATORIOS - set(dados)
            if ausentes:
                campos = ", ".join(sorted(ausentes))
                raise ValidacaoPecaError(
                    f"Campos obrigatórios ausentes: {campos}."
                )
        elif not dados:
            raise ValidacaoPecaError(
                "Informe ao menos um campo para atualização."
            )

        normalizados = dict(dados)

        for campo in ("nome", "codigo"):
            if campo in normalizados:
                valor = normalizados[campo]
                if not isinstance(valor, str) or not valor.strip():
                    raise ValidacaoPecaError(f"{campo} é obrigatório.")
                normalizados[campo] = valor.strip()

        for campo in ("quantidade_estoque", "quantidade_minima"):
            if campo in normalizados:
                valor = normalizados[campo]
                if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
                    raise ValidacaoPecaError(
                        f"{campo} deve ser um inteiro maior ou igual a zero."
                    )

        if "preco_unitario" in normalizados:
            try:
                preco = Decimal(str(normalizados["preco_unitario"]))
            except (InvalidOperation, ValueError):
                raise ValidacaoPecaError(
                    "preco_unitario deve ser um número válido."
                ) from None

            if not preco.is_finite() or preco < 0:
                raise ValidacaoPecaError(
                    "preco_unitario deve ser maior ou igual a zero."
                )

            normalizados["preco_unitario"] = preco

        return normalizados

    def _validar_codigo_unico(self, codigo):
        if self.repository.buscar_por_codigo(codigo):
            raise ValidacaoPecaError(
                "Já existe uma peça cadastrada com este código."
            )

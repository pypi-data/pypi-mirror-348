
import requests

class LegiswebClient:
    BASE_URL = "https://www.legisweb.com.br/api"

    def __init__(self, token: str, codigo_cliente: str):
        self.token = token
        self.codigo_cliente = codigo_cliente

    def _get(self, endpoint: str, params: dict) -> dict:
        params["t"] = self.token
        params["c"] = self.codigo_cliente
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def consulta_ii(self, ncm: str) -> dict:
        return self._get("ii", {"ncm": ncm})

    def consulta_ipi(self, ncm: str) -> dict:
        return self._get("ipi", {"ncm": ncm})

    def consulta_icms(self, ncm: str, estado: str) -> dict:
        return self._get("icms", {"ncm": ncm, "estado": estado})

    def consulta_piscofins(self, ncm: str, regime: int, atividade: int) -> dict:
        return self._get("piscofins", {
            "ncm": ncm,
            "regime_tributario_origem": regime,
            "atividade_origem": atividade
        })

    def consulta_piscofins_importacao(self, ncm: str) -> dict:
        return self._get("piscofins-importacao", {"ncm": ncm})

    def consulta_tipi(self, ncm: str) -> dict:
        return self._get("tipi", {"ncm": ncm})

    def consulta_st_interna(self, ncm: str, estado: str) -> dict:
        return self._get("st-interna", {"ncm": ncm, "estado": estado})

    def consulta_st_interestadual(self, ncm: str, uf_origem: str, uf_destino: str, destinacao: int) -> dict:
        return self._get("st-interestadual", {
            "ncm": ncm,
            "estado_origem": uf_origem,
            "estado_destino": uf_destino,
            "destinacao_mercadoria": destinacao
        })

    def consulta_preferencia_tarifaria(self, codigo: str, operacao: int, pais: int) -> dict:
        return self._get("preferencia-tarifaria", {
            "codigo": codigo,
            "operacao": operacao,
            "pais": pais,
            "codigo_exato": 1
        })

    def consulta_nve(self, ncm: str) -> dict:
        return self._get("nve", {"ncm": ncm})

    def consulta_ptax(self, moeda: str, data: str) -> dict:
        return self._get("ptax", {"moeda": moeda, "data": data})

    def consulta_defesa_comercial(self, ncm: str) -> dict:
        return self._get("defesa-comercial", {"ncm": ncm})

    def consulta_cide_combustivel(self, ncm: str) -> dict:
        return self._get("cide-combustivel", {"ncm": ncm})

    def consulta_tratamento_adm_importacao(self, ncm: str) -> dict:
        return self._get("tratamento-administrativo-importacao", {"ncm": ncm, "grupo_busca": "ncm"})

    def consulta_tratamento_adm_exportacao(self, ncm: str) -> dict:
        return self._get("tratamento-administrativo-exportacao", {"ncm": ncm, "grupo_busca": "ncm"})

    def consulta_produto_ssn(self, ncm: str) -> dict:
        return self._get("produto-ssn", {"ncm": ncm})

    def consulta_correlacao_ncm(self, codigo: str, de: str, para: str) -> dict:
        return self._get("correlacao-nbm-ncm-naladi", {
            "codigo": codigo,
            "de": de,
            "para": para
        })

    def consulta_pauta_fiscal(self, estado: str, busca: str) -> dict:
        return self._get("pauta-fiscal", {"estado": estado, "busca": busca})

    def consulta_agenda_tributaria(self, data: str, estado: str) -> dict:
        return self._get("agenda-tributaria", {"data": data, "estadual": 1, "estado": estado})

    def consulta_beneficio_fiscal(self, descricao: str, estado: str, categoria: int) -> dict:
        return self._get("beneficio-fiscal", {
            "descricao": descricao,
            "estado": estado,
            "categoria": categoria
        })

    def consulta_empresa(self, cnpj: str) -> dict:
        return self._get("empresas", {"empresa": cnpj})

    def consulta_cfop(self, codigo: str) -> dict:
        return self._get("cfop", {"codigo": codigo})

    def consulta_aliquota_padrao(self, estado: str) -> dict:
        return self._get("aliquota-padrao", {"estado": estado})

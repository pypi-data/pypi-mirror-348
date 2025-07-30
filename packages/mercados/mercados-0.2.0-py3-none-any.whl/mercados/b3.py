import base64
import csv
import datetime
import io
import json
import zipfile
from dataclasses import asdict, dataclass
from decimal import Decimal
from functools import lru_cache
from typing import Optional
from urllib.parse import urljoin

from .utils import (
    clean_string,
    create_session,
    parse_br_date,
    parse_br_decimal,
    parse_date,
    parse_datetime_force_timezone,
    parse_iso_date,
)

UM_CENTAVO = Decimal("0.01")
UM_MILESIMO = Decimal("0.001")
UM_PONTO_BASE = Decimal("0.0001")

def parse_float(value):
    if value is None or value == "":
        return None
    return float(value)


def parse_decimal(value, places=2):
    if value is None or value == "":
        return None
    quantization = {2: UM_CENTAVO, 3: UM_MILESIMO, 4: UM_PONTO_BASE}[places]
    return Decimal(value).quantize(quantization)


# TODO: baixar e tratar vários arquivos de <https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/pesquisa-por-pregao/>
#       Descrição: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/descricao-dos-arquivos/
#       Layout: https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/boletins-diarios/pesquisa-por-pregao/layout-dos-arquivos/
# TODO: 'Arquivo de Índices' https://www.b3.com.br/pesquisapregao/download?filelist=IR241210.zip,
# TODO: 'Mercado de Títulos Públicos - Preços Referenciais para Títulos Públicos' https://www.b3.com.br/pesquisapregao/download?filelist=PU241210.ex_,
# TODO: 'Mercado de Câmbio - Taxas Praticadas, Parâmetros de Abertura e Operações Contratadas' https://www.b3.com.br/pesquisapregao/download?filelist=CT241210.zip,
# TODO: 'Mercado de Derivativos - Indicadores Econômicos e Agropecuários - Final' https://www.b3.com.br/pesquisapregao/download?filelist=ID241210.ex_,
# TODO: 'Mercado de Derivativos - Negócios Realizados no Mercado de Balcão' https://www.b3.com.br/pesquisapregao/download?filelist=BE241210.ex_,
# TODO: 'Mercado de Derivativos - Negócios Registrados em Leilão BACEN' https://www.b3.com.br/pesquisapregao/download?filelist=LB180802.zip,
# TODO: 'Renda Fixa Privada' https://www.b3.com.br/pesquisapregao/download?filelist=RF241210.ex_,
# TODO: 'Taxas do Mercado de Renda Variável' https://www.b3.com.br/pesquisapregao/download?filelist=TX241202.zip,

# TODO: pegar negociações after market de
# <https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/dados-publicos-de-produtos-listados-e-de-balcao/>
# ou de lugar parecido com as de balcão?

# TODO: pegar plantão de notícias <https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/plantao-de-noticias/>


@lru_cache(maxsize=16 * 1024)
def converte_centavos_para_decimal(valor: str) -> Optional[Decimal]:
    """Converte um valor em centavos em str para Decimal em Reais com 2 casas decimais

    >>> print(converte_centavos_para_decimal(""))
    None
    >>> print(converte_centavos_para_decimal(None))
    None
    >>> converte_centavos_para_decimal("0")
    Decimal('0.00')
    >>> converte_centavos_para_decimal("1")
    Decimal('0.01')
    >>> converte_centavos_para_decimal("10")
    Decimal('0.10')
    >>> converte_centavos_para_decimal("100")
    Decimal('1.00')
    >>> converte_centavos_para_decimal("12356")
    Decimal('123.56')
    """
    return (Decimal(valor) / 100).quantize(UM_CENTAVO) if valor else None


@lru_cache(maxsize=16 * 1024)
def converte_decimal(valor: str) -> Optional[Decimal]:
    """
    >>> print(converte_decimal(""))
    None
    >>> print(converte_decimal("   \\t\\n "))
    None
    >>> print(converte_decimal(None))
    None
    >>> converte_decimal("1.23")
    Decimal('1.23')
    >>> converte_decimal("1.23456789")
    Decimal('1.23456789')
    >>> converte_decimal("1.2")
    Decimal('1.20')
    """
    valor = str(valor or "").strip()
    if not valor:
        return None
    valor = Decimal(valor)
    if len(str(valor - int(valor))) < 4:
        valor = valor.quantize(UM_CENTAVO)
    return valor


@dataclass
class NegociacaoBolsa:
    quantidade: Optional[int]
    pontos_strike: Optional[int]
    data: datetime.date
    data_vencimento: Optional[datetime.date]
    negociacoes: Optional[int]
    lote: Optional[int]
    indice_correcao: Optional[int]
    distribuicao: Optional[int]
    codigo_bdi: Optional[int]
    codigo_tipo_mercado: Optional[int]
    prazo_termo: Optional[int]
    codigo_isin: str
    codigo_negociacao: str
    moeda: str
    nome_pregao: str
    tipo_papel: str
    preco_abertura: Optional[Decimal]
    preco_maximo: Optional[Decimal]
    preco_minimo: Optional[Decimal]
    preco_medio: Optional[Decimal]
    preco_ultimo: Optional[Decimal]
    preco_melhor_oferta_compra: Optional[Decimal]
    preco_melhor_oferta_venda: Optional[Decimal]
    volume: Optional[Decimal]
    preco_execucao: Optional[Decimal]

    @classmethod
    def _line_to_dict(cls, line):
        return {
            "date_of_exchange": line[2:10].strip(),
            "codbdi": line[10:12].strip(),
            "codneg": line[12:24].strip(),
            "tpmerc": line[24:27].strip(),
            "nomres": line[27:39].strip(),
            "especi": line[39:49].strip(),
            "prazot": line[49:52].strip(),
            "modref": line[52:56].strip(),
            "preabe": line[56:69].strip(),
            "premax": line[69:82].strip(),
            "premin": line[82:95].strip(),
            "premed": line[95:108].strip(),
            "preult": line[108:121].strip(),
            "preofc": line[121:134].strip(),
            "preofv": line[134:147].strip(),
            "totneg": line[147:152].strip(),
            "quatot": line[152:170].strip(),
            "voltot": line[170:188].strip(),
            "preexe": line[188:201].strip(),
            "indopc": line[201:202].strip(),
            "datven": line[202:210].strip(),
            "fatcot": line[210:217].strip(),
            "ptoexe": line[217:230].strip(),
            "codisi": line[230:242].strip(),
            "dismes": line[242:245].strip(),
        }

    @classmethod
    def from_line(cls, line: str):
        assert len(line) == 246 and line[:2] == "01"
        row = cls._line_to_dict(line)
        return cls(
            quantidade=int(row["quatot"]) if row["quatot"] else None,
            pontos_strike=int(row["ptoexe"]) if row["ptoexe"] != "0000000000000" else None,
            data=datetime.datetime.strptime(row["date_of_exchange"], "%Y%m%d").date(),
            data_vencimento=(
                None if row["datven"] == "99991231" else datetime.datetime.strptime(row["datven"], "%Y%m%d").date()
            ),
            negociacoes=int(row["totneg"]) if row["totneg"] else None,
            lote=int(row["fatcot"]) if row["fatcot"] else None,
            indice_correcao=int(row["indopc"]) if row["indopc"] else None,
            distribuicao=int(row["dismes"]) if row["dismes"] else None,
            codigo_bdi=int(row["codbdi"]) if row["codbdi"] else None,
            codigo_tipo_mercado=int(row["tpmerc"]) if row["tpmerc"] else None,
            prazo_termo=None if row["prazot"] == "" else int(row["prazot"]),
            codigo_isin=row["codisi"],
            codigo_negociacao=row["codneg"].strip(),
            moeda=row["modref"],
            nome_pregao=row["nomres"],
            tipo_papel=row["especi"],
            preco_abertura=converte_centavos_para_decimal(row["preabe"]),
            preco_maximo=converte_centavos_para_decimal(row["premax"]),
            preco_minimo=converte_centavos_para_decimal(row["premin"]),
            preco_medio=converte_centavos_para_decimal(row["premed"]),
            preco_ultimo=converte_centavos_para_decimal(row["preult"]),
            preco_melhor_oferta_compra=converte_centavos_para_decimal(row["preofc"]),
            preco_melhor_oferta_venda=converte_centavos_para_decimal(row["preofv"]),
            volume=converte_centavos_para_decimal(row["voltot"]),
            preco_execucao=converte_centavos_para_decimal(row["preexe"]),
        )


@dataclass
class Dividendo:
    tipo: str
    codigo_isin: str
    data_aprovacao: datetime.date
    data_base: datetime.date
    data_pagamento: datetime.date
    valor_por_cota: Decimal
    periodo_referencia: str

    @classmethod
    def from_dict(cls, row):
        tipo_mapping = {
            "AMORTIZACAO RF": "Amortização RF",
            "DIVIDENDO": "Dividendo",
            "RENDIMENTO": "Rendimento",
        }
        return cls(
            codigo_isin=row["isinCode"],
            data_aprovacao=parse_br_date(row["approvedOn"]),
            data_base=parse_br_date(row["lastDatePrior"]),
            data_pagamento=parse_br_date(row["paymentDate"]),
            valor_por_cota=converte_decimal(row["rate"].replace(".", "").replace(",", ".")),
            periodo_referencia=row["relatedTo"],
            tipo=tipo_mapping.get(row["label"], row["label"]),
        )

    def serialize(self):
        return asdict(self)


@dataclass
class FundoDocumento:
    acronimo: str
    fundo: str
    tipo: str
    datahora_entrega: datetime.datetime
    url: str
    data_referencia: datetime.date = None
    data_ordem: datetime.date = None

    @classmethod
    def from_dict(cls, acronimo, row):
        """
        >>> FundoDocumento.from_dict('XPID', {'name': 'Regulamento', 'date': '2021-05-05T11:29:59.46', 'referenceDate': '', 'companyName': 'XP FDO INV. COTAS FDO INC. INV. EM INFR. R. FIXA  ', 'dateOrder': '0001-01-01T00:00:00'})
        FundoDocumento(acronimo='XPID', fundo='XP FDO INV. COTAS FDO INC. INV. EM INFR. R. FIXA', tipo='Regulamento', datahora_entrega=datetime.datetime(2021, 5, 5, 11, 29, 59, 460000, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=75600))), url='https://bvmf.bmfbovespa.com.br/sig/FormConsultaPdfDocumentoFundos.asp?strSigla=XPID&strData=2021-05-05T11:29:59.46', data_referencia=None, data_ordem=None)
        """
        return cls(
            acronimo=acronimo,
            fundo=clean_string(row["companyName"]),
            tipo=row["name"],
            datahora_entrega=parse_datetime_force_timezone(row["date"]),
            data_referencia=parse_br_date(row["referenceDate"]),
            data_ordem=parse_date("iso-date", row["dateOrder"].replace("T00:00:00", "")),
            url=f"https://bvmf.bmfbovespa.com.br/sig/FormConsultaPdfDocumentoFundos.asp?strSigla={acronimo}&strData={row['date']}",
        )

    def serialize(self):
        return asdict(self)


@dataclass
class FundoB3:
    tipo: str
    acronimo: str
    nome_negociacao: str
    cnpj: str
    classificacao: str
    endereco: str
    ddd: str
    telefone: str
    fax: str
    empresa_endereco: str
    empresa_ddd: str
    empresa_telefone: str
    empresa_fax: str
    empresa_email: str
    empresa_razao_social: str
    cotas: float
    data_aprovacao_cotas: datetime.date
    administrador: str
    administrador_endereco: str
    administrador_ddd: str
    administrador_telefone: str
    administrador_fax: str
    administrador_responsavel: str
    administrador_responsavel_cargo: str
    administrador_email: str = None
    website: str = None
    tipo_fnet: str = None
    codigos_negociacao: list[str] = None
    segmento: str = None

    @property
    def codigo_negociacao(self):
        return self.codigos_negociacao[0] if self.codigos_negociacao else f"{self.acronimo}11"

    def to_dict(self):
        return {"codigo_negociacao": self.codigo_negociacao, **asdict(self)}

    def serialize(self):
        obj = self.to_dict()
        if obj["data_aprovacao_cotas"]:
            obj["data_aprovacao_cotas"] = obj["data_aprovacao_cotas"].isoformat()
        if obj["codigos_negociacao"]:
            obj["codigos_negociacao"] = json.dumps(obj["codigos_negociacao"])
        return obj

    @classmethod
    def from_dict(cls, type_name, obj):
        detail = obj["detailFund"]
        shareholder = obj["shareHolder"] or {}
        codigos_negociacao = []
        if detail["codes"]:
            codigos_negociacao = [clean_string(item) for item in detail["codes"]]
        if detail["codesOther"]:
            for item in detail["codesOther"]:
                item = clean_string(item)
                if item not in codigos_negociacao:
                    codigos_negociacao.append(item)
        fax = clean_string(detail["fundPhoneNumberFax"])
        fax = fax if fax != "0" else None
        empresa_fax = clean_string(detail["companyPhoneNumberFax"])
        empresa_fax = empresa_fax if empresa_fax != "0" else None
        administrador_fax = clean_string(shareholder.get("shareHolderFaxNumber"))
        administrador_fax = administrador_fax if administrador_fax != "0" else None
        website = clean_string(detail["webSite"])
        if website and not website.lower().startswith("https:") and not website.lower().startswith("http:"):
            website = f"https://{website}"
        return cls(
            tipo=type_name,
            acronimo=clean_string(detail["acronym"]),
            nome_negociacao=clean_string(detail["tradingName"]),
            cnpj=clean_string(detail["cnpj"]),
            classificacao=clean_string(detail["classification"]),
            cotas=parse_float(clean_string(detail["quotaCount"])),
            data_aprovacao_cotas=parse_br_date(clean_string(detail["quotaDateApproved"])),
            tipo_fnet=clean_string(detail["typeFNET"]),
            segmento=clean_string(detail["segment"]),
            codigos_negociacao=codigos_negociacao,
            website=website,
            endereco=clean_string(detail["fundAddress"]),
            ddd=clean_string(detail["fundPhoneNumberDDD"]),
            telefone=clean_string(detail["fundPhoneNumber"]),
            fax=fax,
            empresa_endereco=clean_string(detail["companyAddress"]),
            empresa_ddd=clean_string(detail["companyPhoneNumberDDD"]),
            empresa_telefone=clean_string(detail["companyPhoneNumber"]),
            empresa_fax=empresa_fax,
            empresa_email=clean_string(detail["companyEmail"]),
            empresa_razao_social=clean_string(detail["companyName"]),
            administrador=clean_string(shareholder.get("shareHolderName")),
            administrador_endereco=clean_string(shareholder.get("shareHolderAddress")),
            administrador_ddd=clean_string(shareholder.get("shareHolderPhoneNumberDDD")),
            administrador_telefone=clean_string(shareholder.get("shareHolderPhoneNumber")),
            administrador_fax=administrador_fax,
            administrador_email=clean_string(shareholder.get("shareHolderEmail")),
            administrador_responsavel=clean_string(detail["managerName"]),
            administrador_responsavel_cargo=clean_string(detail["positionManager"]),
        )


@dataclass
class NegociacaoBalcao:
    codigo: str
    codigo_if: str
    instrumento: str
    datahora: datetime.date
    quantidade: Decimal
    preco: Decimal
    volume: Decimal
    origem: str
    codigo_isin: str = None
    data_liquidacao: datetime.date = None
    emissor: str = None
    situacao: str = None
    taxa: Decimal = None

    @classmethod
    def from_dict(cls, row):
        day, month, year = row.pop("Data Negocio").split("/")
        date = f"{year}-{int(month):02d}-{int(day):02d}"
        quantidade = parse_br_decimal(row.pop("Quantidade Negociada"))
        preco = parse_br_decimal(row.pop("Preco Negocio"))
        volume = parse_br_decimal(row.pop("Volume Financeiro R$").replace("################", ""))
        if volume is None:  # Only in 2 cases in 2021
            volume = quantidade * preco
        data_liquidacao = str(row.pop("Data Liquidacao") or "").strip()
        data_liquidacao = data_liquidacao.split()[0] if data_liquidacao else None
        data_liquidacao = parse_date("br-date", data_liquidacao)
        obj = cls(
            codigo=row.pop("Cod. Identificador do Negocio"),
            codigo_if=row.pop("Codigo IF"),
            codigo_isin=row.pop("Cod. Isin"),
            data_liquidacao=data_liquidacao,
            datahora=parse_date("iso-datetime-tz", f"{date}T{row.pop('Horario Negocio')}-03:00"),
            emissor=row.pop("Emissor"),
            instrumento=row.pop("Instrumento Financeiro"),
            taxa=parse_br_decimal(row.pop("Taxa Negocio")),
            quantidade=quantidade,
            preco=preco,
            volume=volume,
            origem=row.pop("Origem Negocio"),
            situacao=row.pop("Situacao Negocio", None),
        )
        assert not row
        return obj

    @classmethod
    def from_converted_dict(cls, row):
        data_liquidacao = row.pop("data_liquidacao")
        taxa = row.pop("taxa")
        obj = cls(
            codigo=row.pop("codigo"),
            codigo_if=row.pop("codigo_if"),
            instrumento=row.pop("instrumento"),
            datahora=parse_date("iso-datetime-tz", row.pop("datahora")),
            quantidade=converte_decimal(row.pop("quantidade")),
            preco=converte_decimal(row.pop("preco")),
            volume=converte_decimal(row.pop("volume")),
            origem=row.pop("origem"),
            codigo_isin=row.pop("codigo_isin") or None,
            data_liquidacao=parse_date("iso-date", data_liquidacao) if data_liquidacao else None,
            emissor=row.pop("emissor") or None,
            taxa=converte_decimal(taxa) if taxa else None,
        )
        assert not row
        return obj


@dataclass
class EmprestimoAtivo:
    data: datetime.date
    ticker: str
    codigo_isin: str
    nome: str
    mercado: str
    contratos: int
    quantidade: int
    minima: float
    media_ponderada: float
    maxima: float
    valor: Decimal
    taxa_doador: float
    taxa_tomador: float

    @classmethod
    def from_dict(cls, row):
        key = "Data"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            data=row.pop("Data"),
            ticker=row.pop("Ticker"),
            codigo_isin=row.pop("ISIN"),
            nome=row.pop("Empresa ou Fundo"),
            mercado=row.pop("Mercado"),
            contratos=int(row.pop("Número de Contratos")),
            quantidade=int(row.pop("Quantidade de Ativos")),
            minima=parse_float(row.pop("Mínima")),
            media_ponderada=parse_float(row.pop("Média Ponderada")),
            maxima=parse_float(row.pop("Máxima")),
            valor=parse_decimal(row.pop("Valor em R$")),
            taxa_doador=parse_float(row.pop("Taxa Doador")),
            taxa_tomador=parse_float(row.pop("Taxa Tomador")),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class EmprestimoNegociado:
    data_referencia: datetime.date
    ticker: str
    quantidade: int
    taxa_remuneracao: float
    numero_negocio: int
    mercado: str
    data_hora: datetime.datetime
    codigo: int
    doador: str
    tomador: str
    acao_atualizacao: str
    tipo_sessao_pregao: str
    participante_doador: str
    participante_tomador: str

    @classmethod
    def from_dict(cls, row):
        key = "Data de referência"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            data_referencia=row.pop("Data de referência"),
            ticker=row.pop("Papel"),
            quantidade=int(row.pop("Quantidade")),
            codigo=int(row.pop("Código")),
            taxa_remuneracao=parse_float(row.pop("Taxa % Remuneração")),
            numero_negocio=int(row.pop("Número do negócio")),
            mercado=row.pop("Mercado"),
            data_hora=parse_datetime_force_timezone(row.pop("Hora")),
            doador=row.pop("Nome Doador"),
            tomador=row.pop("Nome Tomador"),
            acao_atualizacao=row.pop("Ação de Atualização"),
            tipo_sessao_pregao=row.pop("Tipo Sessão do Pregão"),
            participante_doador=row.pop("Participante Doador"),
            participante_tomador=row.pop("Participante Tomador"),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class EmprestimoEmAberto:
    data: datetime.date
    ticker: str
    codigo_isin: str
    empresa: str
    tipo: str
    mercado: str
    saldo_quantidade: int
    saldo: Decimal
    preco_medio: Decimal = None

    @classmethod
    def from_dict(cls, row):
        key = "Data"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            data=row.pop("Data"),
            ticker=row.pop("Ticker"),
            codigo_isin=row.pop("ISIN"),
            empresa=row.pop("Empresa ou Fundo"),
            tipo=row.pop("Tipo"),
            mercado=row.pop("Mercado"),
            saldo_quantidade=int(row.pop("Saldo em quantidade do ativo")),
            preco_medio=parse_decimal(row.pop("Preço Médio")),
            saldo=parse_decimal(row.pop("Saldo em R$")),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class OpcaoFlexivel:
    ticker: str
    operacao: str
    descricao: str
    vencimento: datetime.date
    negocios: int
    volume: Decimal
    premio_medio: Decimal
    preco_exercicio_medio: Decimal

    @classmethod
    def from_dict(cls, row):
        key = "Vencimento"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            ticker=row.pop("Código"),
            operacao=row.pop("Tipo de opção"),
            descricao=row.pop("Opção"),
            vencimento=row.pop("Vencimento"),
            negocios=int(row.pop("Número de negócios")),
            volume=parse_decimal(row.pop("Volume (R$)")),
            premio_medio=parse_decimal(row.pop("Prêmio médio (R$)"), places=4),
            preco_exercicio_medio=parse_decimal(row.pop("Preço exercício médio (R$)"), places=4),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class PrazoDeposito:
    data: datetime.date
    empresa: str
    codigo: str
    tipo: str

    @classmethod
    def from_dict(cls, row):
        key = "Data"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            data=row.pop("Data"),
            empresa=row.pop("Empresa"),
            codigo=row.pop("Código"),
            tipo=row.pop("Provento"),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class PosicaoEmAberto:
    data: datetime.date
    mercado: str
    contratos: int
    valor_milhares: Decimal
    ordenacao: int

    @classmethod
    def from_dict(cls, row):
        key = "Data"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            data=row.pop("Data"),
            mercado=row.pop("Mercado"),
            contratos=int(row.pop("Número de contratos")),
            valor_milhares=parse_decimal(row.pop("Valor Referencial (mil R$)")),
            ordenacao=int(row.pop("OrderCol")),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class Swap:
    codigo: str
    vencimento: datetime.date
    negocios: int
    volume: Decimal
    taxa_media_diaria: Decimal

    @classmethod
    def from_dict(cls, row):
        key = "Vencimento"
        if key in row:
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            codigo=row.pop("Código"),
            vencimento=row.pop("Vencimento"),
            negocios=int(row.pop("Número de negócios")),
            volume=parse_decimal(row.pop("Volume (R$)")),
            taxa_media_diaria=parse_decimal(row.pop("Taxa média diária"), places=4),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class AcaoCustodiada:
    empresa: str
    tipo: str
    quantidade: int

    @classmethod
    def from_dict(cls, row):
        obj = cls(
            empresa=row.pop("Empresa"),
            tipo=row.pop("Tipo"),
            quantidade=row.pop("Quantidade de ações"),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class CreditoProvento:
    emissor: str
    codigo_isin: str
    tipo: str
    data_aprovacao: datetime.date
    valor: Decimal
    data_credito: datetime.date

    @classmethod
    def from_dict(cls, row):
        for key in ("Data de aprovação", "Data de crédito"):
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            emissor=row.pop("Emissor"),
            codigo_isin=row.pop("Código ISIN"),
            tipo=row.pop("Tipo de provento"),
            data_aprovacao=row.pop("Data de aprovação"),
            data_credito=row.pop("Data de crédito"),
            valor=parse_decimal(row.pop("Valor (R$)")),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


@dataclass
class CustodiaFungivel:
    prazo_final_subscricao: datetime.date
    prazo_final_cessao: datetime.date
    emissor: str
    codigo_isin_origem: str
    codigo_isin_direito: str
    codigo_isin_subscricao: str

    @classmethod
    def from_dict(cls, row):
        for key in ("Prazo final subscrição", "Prazo final cessão"):
            assert row[key].endswith("T00:00:00"), f"Data para coluna {key} em formato inválido: {repr(row[key])}"
            row[key] = parse_iso_date(row[key].replace("T00:00:00", ""))
        obj = cls(
            prazo_final_subscricao=row.pop("Prazo final subscrição"),
            prazo_final_cessao=row.pop("Prazo final cessão"),
            emissor=row.pop("Emissor"),
            codigo_isin_origem=row.pop("Código ISIN origem"),
            codigo_isin_direito=row.pop("Código ISIN direito"),
            codigo_isin_subscricao=row.pop("Código ISIN subscrição"),
        )
        assert not row, f"Dados sobraram e não foram extraídos para {cls.__name__}: {row}"
        return obj

    def serialize(self):
        return asdict(self)


class B3:
    funds_call_url = "https://sistemaswebb3-listados.b3.com.br/fundsProxy/fundsCall/"
    indexes_call_url = "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/"
    companies_call_url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/"

    def __init__(self):
        self.session = create_session()
        # Requisição para guardar cookies:
        self.request(
            "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimento-imobiliario-fii.htm",
            decode_json=False,
        )

    def _make_url_params(self, params):
        return base64.b64encode(json.dumps(params).encode("utf-8")).decode("ascii")

    def url_negociacao_bolsa(self, frequencia: str, data: datetime.date):
        """
        :param frequencia: deve ser "dia", "mês" ou "ano"
        :param data: data desejada (use o dia "01" caso frequência seja "mês" e o dia e mês "01" caso frequência seja
        "ano")
        """
        if frequencia == "dia":
            date = data.strftime("%d%m%Y")
            return f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D{date}.ZIP"
        elif frequencia == "mês":
            date = data.strftime("%m%Y")
            return f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_M{date}.ZIP"
        elif frequencia == "ano":
            date = data.strftime("%Y")
            return f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{date}.ZIP"

    def negociacao_bolsa(self, frequencia: str, data: datetime.date):
        """
        Baixa cotação para uma determinada data (dia, mês ou ano)

        :param frequencia: deve ser "dia", "mês" ou "ano"
        :param data: data das cotações a serem baixadas (use o dia "01" caso frequência seja "mês" e o dia e mês "01"
        caso frequência seja "ano")

        Horários de atualização, de acordo com meus testes:
        - Diária: 23:31:45 GMT
        - Mensal: 00:20:56 GMT
        - Anual: 23:32:31 GMT
        """
        assert frequencia in ("dia", "mês", "ano")

        url = self.url_negociacao_bolsa(frequencia, data)
        response = self.session.get(url, verify=False)
        if len(response.content) == 0:  # Arquivo vazio (provavelmente dia sem pregão)
            return ValueError(
                f"Data {data} possui arquivo de cotação vazio (provavelmente não teve pregão ou data no futuro)"
            )
        zf = zipfile.ZipFile(io.BytesIO(response.content))
        assert len(zf.filelist) == 1
        fobj = io.TextIOWrapper(zf.open(zf.filelist[0].filename), encoding="iso-8859-1")
        for line in fobj:
            if line[:2] != "01":  # Não é um registro de fato
                continue
            yield NegociacaoBolsa.from_line(line)

    def url_intraday_zip(self, data: datetime.date):
        data_str = data.strftime("%Y-%m-%d")
        url = f"https://arquivos.b3.com.br/rapinegocios/tickercsv/{data_str}"
        return url

    def _le_zip_intraday(self, fobj):
        zf = zipfile.ZipFile(fobj)
        assert len(zf.filelist) == 1
        filename = zf.filelist[0].filename
        assert "_NEGOCIOSAVISTA.txt" in filename
        fobj = io.TextIOWrapper(zf.open(zf.filelist[0].filename), encoding="iso-8859-1")
        reader = csv.DictReader(fobj, delimiter=";")
        # TODO: criar dataclass e converter valores em objetos Python
        yield from reader

    def negociacao_intraday(self, data: datetime.date):
        url = self.url_intraday_zip(data)
        response = self.session.get(url)
        yield from self._le_zip_intraday(io.BytesIO(response.content))

    def request(
        self,
        url,
        url_params=None,
        params=None,
        method="GET",
        timeout=10,
        decode_json=True,
        verify_ssl=False,
        json_data=None,
    ):
        if url_params is not None:
            url_params = self._make_url_params(url_params)
            url = urljoin(url, url_params)
        response = self.session.request(method, url, params=params, timeout=timeout, verify=verify_ssl, json=json_data)
        if decode_json:
            text = response.text
            if text and text[0] == text[-1] == '"':  # WTF, B3?
                text = json.loads(text)
            return json.loads(text) if text else {}
        return response

    def paginate(self, base_url, url_params=None, params=None, method="GET"):
        url_params = url_params or {}
        if "pageNumber" not in url_params:
            url_params["pageNumber"] = 1
        if "pageSize" not in url_params:
            url_params["pageSize"] = 100
        finished = False
        while not finished:
            response = self.request(base_url, url_params, params=params, method=method)
            if isinstance(response, list):
                yield from response
                finished = True
            elif isinstance(response, dict):
                if "results" in response:
                    yield from response["results"]
                    finished = url_params["pageNumber"] >= response["page"]["totalPages"]
                    url_params["pageNumber"] += 1
                else:
                    yield response

    def _funds_by_type(self, type_name, type_id):
        objs = self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedFundsSIG/"),
            url_params={"typeFund": type_id},
        )
        for obj in objs:
            yield self._fund_detail(type_name, type_id, obj["acronym"])

    def _fund_detail(self, type_name, type_id, identifier):
        return FundoB3.from_dict(
            type_name,
            self.request(
                method="GET",
                url=urljoin(self.funds_call_url, "GetDetailFundSIG/"),
                url_params={"typeFund": type_id, "identifierFund": identifier},
            ),
        )

    def _fund_dividends(self, type_id, cnpj, identifier):
        data = self.request(
            url=urljoin(self.funds_call_url, "GetListedSupplementFunds/"),
            url_params={"cnpj": cnpj, "identifierFund": identifier, "typeFund": type_id},
        )
        dividends = data.get("cashDividends") if data else []
        return [Dividendo.from_dict(row) for row in dividends]

    # TODO: implement stockDividends

    def _fund_subscriptions(self, type_id, cnpj, identifier):
        # TODO: parse/convert to dataclass:
        # assetIssued	percentage	priceUnit	tradingPeriod	subscriptionDate	approvedOn	isinCode	label	lastDatePrior	remarks
        # BRAFHICTF005	31,33913825813	95,80000000000	31/12/9999 a 06/06/2024	11/06/2024	20/05/2024	BRAFHICTF005	SUBSCRICAO	23/05/2024
        # BRAFHICTF005	31,01981846164	96,43000000000	31/12/9999 a 24/01/2024	29/01/2024	08/01/2024	BRAFHICTF005	SUBSCRICAO	11/01/2024
        # BRAFHICTF005	20,66255046858	96,17000000000	31/12/9999 a 02/08/2023	07/08/2023	18/07/2023	BRAFHICTF005	SUBSCRICAO	21/07/2023
        # BRALZCCTF016	128,40431952130	100,51000000000	31/12/9999 a 27/05/2024	31/05/2024	10/05/2024	BRALZCCTF016	SUBSCRICAO	15/05/2024

        return self.request(
            url=urljoin(self.funds_call_url, "GetListedSupplementFunds/"),
            url_params={"cnpj": cnpj, "identifierFund": identifier, "typeFund": type_id},
        )["subscriptions"]

    def _fundo_comunicados(self, identificador):
        "Comunicados"
        result = self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedPreviousDocuments/"),
            url_params={"identifierFund": identificador, "type": 1},
        )
        for row in result:
            yield FundoDocumento.from_dict(identificador, row)

    def _fundo_demonstrativos(self, identificador):
        "Demonstrativos financeiros e relatórios"
        result = self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedPreviousDocuments/"),
            url_params={"identifierFund": identificador, "type": 2},
        )
        for row in result:
            yield FundoDocumento.from_dict(identificador, row)

    def _fundo_outros_documentos(self, identificador):
        "Demonstrativos financeiros e relatórios"
        result = self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedPreviousDocuments/"),
            url_params={"identifierFund": identificador, "type": 3},
        )
        for row in result:
            yield FundoDocumento.from_dict(identificador, row)

    def _fund_documents(self, type_id, cnpj, identifier, start_date: datetime.date, end_date: datetime.date):
        # TODO: parse/convert to dataclass:
        iterator = self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedDocuments/"),
            url_params={
                "identifierFund": identifier,
                "typeFund": type_id,
                "cnpj": cnpj,
                "dateInitial": start_date.strftime("%Y-%m-%d"),
                "dateFinal": end_date.strftime("%Y-%m-%d"),
            },
        )
        for row in iterator:
            yield row

    # TODO: GetListedHeadLines/ b'{"agency":"18","identifierFund":"CPTR","dateInitial":"2023-06-10","dateFinal":"2024-06-05"}'
    # TODO: GetListedByType/ b'{"cnpj":"42537579000176","identifierFund":"CPTR","typeFund":34,"dateInitial":"2024-01-01","dateFinal":"2024-12-31"}'
    # TODO: GetListedCategory/ b'{"cnpj":"42537579000176"}'
    # TODO: GetListedDocuments/ b'{"pageNumber":1,"pageSize":4,"cnpj":"42537579000176","identifierFund":"CPTR","typeFund":34,"dateInitial":"2024-01-01","dateFinal":"2024-12-31","category":7}'

    def bdrs(self):
        # TODO: retornar dataclass
        return self.paginate(
            base_url=urljoin(self.companies_call_url, "GetCompaniesBDR/"),
            url_params={"language": "pt-br"},
        )

    def fiis(self):
        yield from self._funds_by_type("FII", 7)

    def fii_detail(self, identificador):
        return self._fund_detail("FII", 7, identificador)

    def fii_dividends(self, cnpj, identificador):
        return self._fund_dividends(7, cnpj, identificador)

    def fii_subscriptions(self, cnpj, identificador):
        # TODO: Corrigir: `KeyError: 'subscriptions'`
        return self._fund_subscriptions(7, cnpj, identificador)

    def fii_documents(self, cnpj, identificador, data_inicial: datetime.date = None, data_final: datetime.date = None):
        today = datetime.datetime.now()
        if data_inicial is None:
            data_inicial = (today - datetime.timedelta(days=365)).date()
        if data_final is None:
            data_final = today.date()
        yield from self._fund_documents(7, cnpj, identificador, data_inicial, data_final)

    def fiinfras(self):
        yield from self._funds_by_type("FI-Infra", 27)

    def fiinfra_detail(self, identificador):
        return self._fund_detail("FI-Infra", 27, identificador)

    def fiinfra_dividends(self, cnpj, identificador):
        return self._fund_dividends(27, cnpj, identificador)

    def fiinfra_subscriptions(self, cnpj, identificador):
        return self._fund_subscriptions(27, cnpj, identificador)

    def fiinfra_documents(
        self, cnpj, identificador, data_inicial: datetime.date = None, data_final: datetime.date = None
    ):
        today = datetime.datetime.now()
        if data_inicial is None:
            data_inicial = (today - datetime.timedelta(days=365)).date()
        if data_final is None:
            data_final = today.date()
        yield from self._fund_documents(27, cnpj, identificador, data_inicial, data_final)

    def fips(self):
        yield from self._funds_by_type("FIP", 21)

    def fip_detail(self, identificador):
        return self._fund_detail("FIP", 21, identificador)

    def fip_dividends(self, cnpj, identificador):
        return self._fund_dividends(21, cnpj, identificador)

    def fip_subscriptions(self, cnpj, identificador):
        return self._fund_subscriptions(21, cnpj, identificador)

    def fip_documents(self, cnpj, identificador, data_inicial: datetime.date = None, data_final: datetime.date = None):
        today = datetime.datetime.now()
        if data_inicial is None:
            data_inicial = (today - datetime.timedelta(days=365)).date()
        if data_final is None:
            data_final = today.date()
        yield from self._fund_documents(21, cnpj, identificador, data_inicial, data_final)

    def fiagros(self):
        yield from self._funds_by_type("FI-Agro", 34)

    def fiagro_detail(self, identificador):
        return self._fund_detail("FI-Agro", 34, identificador)

    def fiagro_dividends(self, cnpj, identificador):
        return self._fund_dividends(34, cnpj, identificador)

    def fiagro_subscriptions(self, cnpj, identificador):
        return self._fund_subscriptions(34, cnpj, identificador)

    def fiagro_documents(
        self, cnpj, identificador, data_inicial: datetime.date = None, data_final: datetime.date = None
    ):
        today = datetime.datetime.now()
        if data_inicial is None:
            data_inicial = (today - datetime.timedelta(days=365)).date()
        if data_final is None:
            data_final = today.date()
        yield from self._fund_documents(34, cnpj, identificador, data_inicial, data_final)

    def securitizadoras(self):
        yield from self.paginate(urljoin(self.funds_call_url, "GetListedSecuritization/"))

    def cris(self, cnpj_securitizadora):
        yield from self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedCertified/"),
            url_params={"dateInitial": "", "cnpj": cnpj_securitizadora, "type": "CRI"},
        )

    def cras(self, cnpj_securitizadora):
        yield from self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedCertified/"),
            url_params={"dateInitial": "", "cnpj": cnpj_securitizadora, "type": "CRA"},
        )

    def certificate_documents(self, identificador, start_date: datetime.date, end_date: datetime.date):  # CRI or CRA
        yield from self.paginate(
            base_url=urljoin(self.funds_call_url, "GetListedDocumentsTypeHistory/"),
            url_params={
                "cnpj": identificador,
                "dateInitial": start_date.strftime("%Y-%m-%d"),
                "dateFinal": end_date.strftime("%Y-%m-%d"),
            },
        )

    def debentures(self):
        response = self.request(
            "https://sistemaswebb3-balcao.b3.com.br/featuresDebenturesProxy/DebenturesCall/GetDownload",
            decode_json=False,
        )
        decoded_data = base64.b64decode(response.text).decode("ISO-8859-1")
        reader = csv.DictReader(io.StringIO(decoded_data), delimiter=";")
        yield from reader

    def negociacao_balcao(self, date):
        response = self.request(
            "https://bvmf.bmfbovespa.com.br/NegociosRealizados/Registro/DownloadArquivoDiretorio",
            params={"data": date.strftime("%d-%m-%Y")},
            decode_json=False,
        )
        if response.status_code == 404:  # No data for this date
            return
        decoded_data = base64.b64decode(response.text).decode("ISO-8859-1")
        csv_data = decoded_data[decoded_data.find("\n") + 1 :]
        reader = csv.DictReader(io.StringIO(csv_data), delimiter=";")
        for row in reader:
            for field in ("Cod. Isin", "Data Liquidacao"):
                if field not in row:
                    row[field] = None
            yield NegociacaoBalcao.from_dict(row)

    # TODO: criar método para listar todos os índices

    def carteira_indice(self, indice):
        # TODO: seletor de tipo:
        # - GetTheoricalPortfolio/eyJwYWdlTnVtYmVyIjoxLCJwYWdlU2l6ZSI6MjAsImxhbmd1YWdlIjoicHQtYnIiLCJpbmRleCI6IklCT1YifQ==
        #   b'{"pageNumber":1,"pageSize":20,"language":"pt-br","index":"IBOV"}'
        # - GetPortfolioDay/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjIwLCJpbmRleCI6IklCT1YiLCJzZWdtZW50IjoiMSJ9
        #   b'{"language":"pt-br","pageNumber":1,"pageSize":20,"index":"IBOV","segment":"1"}'
        # - GetQuartelyPreview/eyJwYWdlTnVtYmVyIjoxLCJwYWdlU2l6ZSI6MjAsImxhbmd1YWdlIjoicHQtYnIiLCJpbmRleCI6IklCT1YifQ==
        #   b'{"pageNumber":1,"pageSize":20,"language":"pt-br","index":"IBOV"}'
        # - GetDownloadPortfolioDay/eyJpbmRleCI6IklCT1ZFU1BBIiwibGFuZ3VhZ2UiOiJwdC1iciIsInllYXIiOiIyMDIyIn0=
        #   b'{"index":"IBOVESPA","language":"pt-br","year":"2022"}'
        #
        # TODO: create dataclass:
        # {'segment': None,
        #  'cod': 'VINO11',
        #  'asset': 'FII VINCI OF',
        #  'type': 'CI  ER',
        #  'part': '0,814',
        #  'partAcum': None,
        #  'theoricalQty': '16.565.259'}
        # TODO: assert indice in XXX
        yield from self.paginate(
            base_url=urljoin(self.indexes_call_url, "GetPortfolioDay/"),
            url_params={"language": "pt-br", "index": indice, "segment": "1"},
        )

    def _tabela_clearing(self, url_template, url_params, query_params, json_data=None, data_class=None):
        """
        Baixa dados de Clearing do Boletim do Mercado da B3

        <https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/boletim-diario-do-mercado/>
        """
        page, page_size = 1, 1000
        json_data = json_data if json_data is not None else {}
        finished = False
        while not finished:
            url = url_template.format(page=page, page_size=page_size, **url_params)
            data = self.request(url, params=query_params, method="POST", json_data=json_data, decode_json=True)
            table = data["table"]
            header = [col["friendlyNamePt"] or col["name"] for col in table["columns"]]
            for item in table["values"]:
                row = dict(zip(header, item))
                if data_class is not None:
                    yield data_class.from_dict(row)
                else:
                    yield row
            finished = table["pageCount"] == page or len(table["values"]) == 0
            page += 1

    def clearing_acoes_custodiadas(self, data_inicial: datetime.date):
        """Clearing - Ações Custodiadas"""
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/Custody/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data_inicial.isoformat(), "data_final": data_inicial.isoformat()},
            query_params={"sort": "TckrSymb"},
            data_class=AcaoCustodiada,
        )

    def clearing_creditos_de_proventos(self, data_inicial: datetime.date, filtro_emissor=None):
        """Clearing - Créditos de Proventos - Renda Variável"""
        query_params = {"sort": "TckrSymb"}
        if filtro_emissor is not None:
            query_params["filter"] = base64.b64encode(filtro_emissor.encode("utf-8")).decode("ascii")
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/ProventionCreditVariable/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data_inicial.isoformat(), "data_final": data_inicial.isoformat()},
            query_params=query_params,
            data_class=CreditoProvento,
        )

    def clearing_custodia_fungivel(self, data: datetime.date):
        """Clearing - Custódia Fungível"""
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/FugibleCustody/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params={"sort": "TckrSymb"},
            data_class=CustodiaFungivel,
        )

    def clearing_emprestimos_registrados(
        self, data_inicial: datetime.date, data_final: datetime.date, filtro_ticker=None
    ):
        """Clearing - Empréstimos de Ativos - Empréstimos Registrados"""
        query_params = {"sort": "TckrSymb"}
        if filtro_ticker is not None:
            query_params["filter"] = base64.b64encode(filtro_ticker.encode("utf-8")).decode("ascii")
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/BTBLoanBalance/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data_inicial.isoformat(), "data_final": data_final.isoformat()},
            query_params=query_params,
            data_class=EmprestimoAtivo,
        )

    def clearing_emprestimos_negociados(
        self, data: datetime.date, filtro_tomador=None, filtro_doador=None, filtro_mercado=None, filtro_ticker=None
    ):
        """Clearing - Empréstimos de Ativos - Negócios"""
        query_params = {"sort": "TckrSymb"}
        json_data = {}
        if filtro_tomador is not None:
            json_data["EntryBuyerNm"] = filtro_tomador
        if filtro_doador is not None:
            json_data["EntrySellerNm"] = filtro_doador
        if filtro_mercado is not None:
            json_data["MarketBTB"] = filtro_mercado
        if filtro_ticker is not None:
            query_params["filter"] = base64.b64encode(filtro_ticker.encode("utf-8")).decode("ascii")
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/BTBTrade/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params=query_params,
            json_data=json_data,
            data_class=EmprestimoNegociado,
        )

    def clearing_filtros_emprestimos_negociados(self, data: datetime.date):
        """Lista valores disponíveis para filtros de empréstimos negociados"""
        data = data.isoformat()
        return self.request(f"https://arquivos.b3.com.br/bdi/table/BTBTrade/{data}/{data}/filters")

    def clearing_emprestimos_em_aberto(
        self, data_inicial: datetime.date, data_final: datetime.date, filtro_mercado=None, filtro_ticker=None
    ):
        """Clearing - Empréstimos de Ativos - Posições em Aberto"""
        query_params = {"sort": "TckrSymb"}
        if filtro_ticker is not None:
            query_params["filter"] = base64.b64encode(filtro_ticker.encode("utf-8")).decode("ascii")
        json_data = {}
        if filtro_mercado is not None:
            json_data["Market"] = filtro_mercado
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/BTBLendingOpenPosition/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data_inicial.isoformat(), "data_final": data_final.isoformat()},
            query_params=query_params,
            json_data=json_data,
            data_class=EmprestimoEmAberto,
        )

    def clearing_filtros_emprestimos_em_aberto(self, data_inicial: datetime.date, data_final: datetime.date):
        """Lista valores disponíveis para filtros de empréstimos em aberto"""
        data_inicial = data_inicial.isoformat()
        data_final = data_final.isoformat()
        return self.request(
            f"https://arquivos.b3.com.br/bdi/table/BTBLendingOpenPosition/{data_inicial}/{data_final}/filters"
        )

    def clearing_opcoes_flexiveis(self, data: datetime.date, filtro_ticker=None):
        """Clearing - Opções Flexíveis"""
        query_params = {"sort": "TckrSymb"}
        if filtro_ticker is not None:
            query_params["filter"] = base64.b64encode(filtro_ticker.encode("utf-8")).decode("ascii")
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/FlexibleOptions/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params=query_params,
            data_class=OpcaoFlexivel,
        )

    def clearing_prazo_deposito_titulos(self, data: datetime.date):
        """Clearing - Prazo para Depósito de Títulos"""
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/DeadlineDepositSecurities/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params={"sort": "TckrSymb"},
            data_class=PrazoDeposito,
        )

    def clearing_posicoes_em_aberto(self, data: datetime.date):
        """Clearing - Quadro Analítico das Posições em Aberto"""
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/AnalyticalFramework/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params={"sort": "TckrSymb"},
            data_class=PosicaoEmAberto,
        )

    def clearing_swap(self, data: datetime.date):
        """Clearing - Swap"""
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/SwapFlex/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params={"sort": "TckrSymb"},
            data_class=Swap,
        )

    def clearing_termo_eletronico(self, data: datetime.date):
        """Clearing - Termo Eletrônico"""
        yield from self._tabela_clearing(
            url_template="https://arquivos.b3.com.br/bdi/table/EletronicTerm/{data_inicial}/{data_final}/{page}/{page_size}",
            url_params={"data_inicial": data.isoformat(), "data_final": data.isoformat()},
            query_params={"sort": "TckrSymb"},
        )


if __name__ == "__main__":
    import argparse
    import datetime
    from pathlib import Path

    from .utils import day_range

    comandos_padrao = [
        "cra-documents",
        "cri-documents",
        "debentures",
        "fiagro-dividends",
        "fiagro-documents",
        "fiagro-subscriptions",
        "fii-dividends",
        "fii-documents",
        "fii-subscriptions",
        "fiinfra-dividends",
        "fiinfra-documents",
        "fiinfra-subscriptions",
        "fip-dividends",
        "fip-documents",
        "fip-subscriptions",
        "fundo-listado",
        "negociacao-balcao",
    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for comando in comandos_padrao:
        subparser = subparsers.add_parser(comando)
        subparser.add_argument("csv_filename", type=Path, help="Nome do arquivo CSV a ser salvo")

    subparser_negociacao_bolsa = subparsers.add_parser("negociacao-bolsa")
    subparser_negociacao_bolsa.add_argument(
        "frequencia", type=str, choices=["dia", "mês", "ano"], help="Frequência do arquivo de cotação disponível"
    )
    subparser_negociacao_bolsa.add_argument(
        "data",
        type=parse_iso_date,
        help="Data a ser baixada em formato YYYY-MM-DD (para frequência mensal, use dia = 01, para anual use mês e dia = 01)",
    )
    subparser_negociacao_bolsa.add_argument("csv_filename", type=Path, help="Nome do arquivo CSV a ser salvo")

    subparser_baixar = subparsers.add_parser("intraday-baixar", help="Baixa arquivo ZIP de intraday para uma data.")
    subparser_baixar.add_argument(
        "--chunk-size", "-c", type=int, default=256 * 1024, help="Tamanho do chunk no download"
    )
    subparser_baixar.add_argument("data", type=parse_iso_date, help="Data no formato YYYY-MM-DD")
    subparser_baixar.add_argument("zip_filename", type=Path, help="Nome do arquivo ZIP a ser salvo")

    subparser_converter = subparsers.add_parser("intraday-converter", help="Converte arquivo ZIP de intraday para CSV.")
    subparser_converter.add_argument("--codigo-ativo", "-c", action="append", help="Filtra pelo código de negociação")
    subparser_converter.add_argument(
        "zip_filename", type=Path, help="Nome do arquivo ZIP (já baixado) a ser convertido"
    )
    subparser_converter.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_acoes_custodiadas = subparsers.add_parser(
        "clearing-acoes-custodiadas", help="Coleta dados de Clearing - Ações Custodiadas"
    )
    subparser_clearing_acoes_custodiadas.add_argument(
        "data_inicial", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_acoes_custodiadas.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_creditos_de_proventos = subparsers.add_parser(
        "clearing-creditos-de-proventos", help="Coleta dados de Clearing - Créditos de Proventos - Renda Variável"
    )
    subparser_clearing_creditos_de_proventos.add_argument("--emissor", type=str, help="Filtra por emissor")
    subparser_clearing_creditos_de_proventos.add_argument(
        "data_inicial", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_creditos_de_proventos.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_custodia_fungivel = subparsers.add_parser(
        "clearing-custodia-fungivel", help="Coleta dados de Clearing - Custódia Fungível"
    )
    subparser_clearing_custodia_fungivel.add_argument("data", type=parse_iso_date, help="Data no formato YYYY-MM-DD")
    subparser_clearing_custodia_fungivel.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_emprestimos_registrados = subparsers.add_parser(
        "clearing-emprestimos-registrados",
        help="Coleta dados de Clearing - Empréstimos de Ativos - Empréstimos Registrados",
    )
    subparser_clearing_emprestimos_registrados.add_argument("--ticker", type=str, help="Filtra por ticker")
    subparser_clearing_emprestimos_registrados.add_argument(
        "data_inicial", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_emprestimos_registrados.add_argument(
        "data_final", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_emprestimos_registrados.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_emprestimos_negociados = subparsers.add_parser(
        "clearing-emprestimos-negociados", help="Coleta dados de Clearing - Empréstimos de Ativos - Negócios"
    )
    subparser_clearing_emprestimos_negociados.add_argument("--tomador", type=str, help="Filtra por tomador")
    subparser_clearing_emprestimos_negociados.add_argument("--doador", type=str, help="Filtra por doador")
    subparser_clearing_emprestimos_negociados.add_argument("--mercado", type=str, help="Filtra por mercado")
    subparser_clearing_emprestimos_negociados.add_argument("--ticker", type=str, help="Filtra por ticker")
    subparser_clearing_emprestimos_negociados.add_argument(
        "data", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_emprestimos_negociados.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_emprestimos_em_aberto = subparsers.add_parser(
        "clearing-emprestimos-em-aberto", help="Coleta dados de Clearing - Empréstimos de Ativos - Posições em Aberto"
    )
    subparser_clearing_emprestimos_em_aberto.add_argument("--mercado", type=str, help="Filtra por mercado")
    subparser_clearing_emprestimos_em_aberto.add_argument("--ticker", type=str, help="Filtra por ticker")
    subparser_clearing_emprestimos_em_aberto.add_argument(
        "data_inicial", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_emprestimos_em_aberto.add_argument(
        "data_final", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_emprestimos_em_aberto.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_opcoes_flexiveis = subparsers.add_parser(
        "clearing-opcoes-flexiveis", help="Coleta dados de Clearing - Opções Flexíveis"
    )
    subparser_clearing_opcoes_flexiveis.add_argument("--ticker", type=str, help="Filtra por ticker")
    subparser_clearing_opcoes_flexiveis.add_argument("data", type=parse_iso_date, help="Data no formato YYYY-MM-DD")
    subparser_clearing_opcoes_flexiveis.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_prazo_deposito_titulos = subparsers.add_parser(
        "clearing-prazo-deposito-titulos", help="Coleta dados de Clearing - Prazo para Depósito de Títulos"
    )
    subparser_clearing_prazo_deposito_titulos.add_argument(
        "data", type=parse_iso_date, help="Data no formato YYYY-MM-DD"
    )
    subparser_clearing_prazo_deposito_titulos.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_posicoes_em_aberto = subparsers.add_parser(
        "clearing-posicoes-em-aberto", help="Coleta dados de Clearing - Quadro Analítico das Posições em Aberto"
    )
    subparser_clearing_posicoes_em_aberto.add_argument("data", type=parse_iso_date, help="Data no formato YYYY-MM-DD")
    subparser_clearing_posicoes_em_aberto.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_swap = subparsers.add_parser("clearing-swap", help="Coleta dados de Clearing - Swap")
    subparser_clearing_swap.add_argument("data", type=parse_iso_date, help="Data no formato YYYY-MM-DD")
    subparser_clearing_swap.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    subparser_clearing_termo_eletronico = subparsers.add_parser(
        "clearing-termo-eletronico", help="Coleta dados de Clearing - Termo Eletrônico"
    )
    subparser_clearing_termo_eletronico.add_argument("data", type=parse_iso_date, help="Data no formato YYYY-MM-DD")
    subparser_clearing_termo_eletronico.add_argument("csv_filename", type=Path, help="Nome do CSV a ser criado")

    args = parser.parse_args()
    b3 = B3()
    command = args.command
    csv_filename = getattr(args, "csv_filename", None)
    if csv_filename:
        csv_filename.parent.mkdir(parents=True, exist_ok=True)

    if command == "cri-documents":
        current_year = datetime.datetime.now().year
        securitizadoras = b3.securitizadoras()
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for securitizadora in securitizadoras:
                for cri in b3.cris(securitizadora["cnpj"]):
                    start_date = parse_date("iso-datetime-tz", cri["issueDate"])
                    base_row = {**securitizadora, **cri}
                    for year in range(start_date.year, current_year + 1):
                        start, stop = datetime.date(year, 1, 1), datetime.date(year, 12, 31)
                        documents = list(
                            b3.certificate_documents(cri["identificationCode"], start_date=start, end_date=stop)
                        )
                        for doc in documents:
                            row = {**base_row, **doc}
                            if writer is None:
                                writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                                writer.writeheader()
                            writer.writerow(row)

    elif command == "cra-documents":
        current_year = datetime.datetime.now().year
        securitizadoras = b3.securitizadoras()
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for securitizadora in securitizadoras:
                for cra in b3.cras(securitizadora["cnpj"]):
                    start_date = parse_date("iso-datetime-tz", cra["issueDate"])
                    base_row = {**securitizadora, **cra}
                    for year in range(start_date.year, current_year + 1):
                        start, stop = datetime.date(year, 1, 1), datetime.date(year, 12, 31)
                        documents = list(
                            b3.certificate_documents(cra["identificationCode"], start_date=start, end_date=stop)
                        )
                        for doc in documents:
                            row = {**base_row, **doc}
                            if writer is None:
                                writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                                writer.writeheader()
                            writer.writerow(row)

    elif command == "fundo-listado":
        data_sources = (
            (b3.fiis(), "FII"),
            (b3.fiinfras(), "FI-Infra"),
            (b3.fips(), "FIP"),
            (b3.fiagros(), "FI-Agro"),
        )
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for iterator, type_name in data_sources:
                for obj in iterator:
                    row = obj.serialize()
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fii-dividends":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiis():
                base_fund_data = obj.serialize()
                for dividend in b3.fii_dividends(cnpj=obj.cnpj, identificador=obj.acronimo):
                    row = {**base_fund_data, **dividend.serialize()}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)
                    # TODO: include stock_dividends?

    elif command == "fii-subscriptions":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiis():
                base_fund_data = obj.serialize()
                data = b3.fii_subscriptions(cnpj=obj.cnpj, identificador=obj.acronimo)
                for subscription in data:
                    row = {**base_fund_data, **subscription}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fii-documents":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiis():
                base_fund_data = obj.serialize()
                data = b3.fii_documents(identificador=obj.acronimo, cnpj=obj.cnpj)
                for doc in data:
                    row = {**base_fund_data, **doc}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fiinfra-dividends":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiinfras():
                base_fund_data = obj.serialize()
                for dividend in b3.fiinfra_dividends(cnpj=obj.cnpj, identificador=obj.acronimo):
                    row = {**base_fund_data, **dividend.serialize()}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)
                    # TODO: include stock_dividends?

    elif command == "fiinfra-subscriptions":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiinfras():
                base_fund_data = obj.serialize()
                data = b3.fiinfra_subscriptions(cnpj=obj.cnpj, identificador=obj.acronimo)
                for subscription in data:
                    row = {**base_fund_data, **subscription}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fiinfra-documents":
        # TODO: o arquivo está ficando em branco, verificar
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiinfras():
                base_fund_data = obj.serialize()
                data = b3.fiinfra_documents(identificador=obj.acronimo, cnpj=obj.cnpj)
                for doc in data:
                    row = {**base_fund_data, **doc}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fiagro-dividends":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiagros():
                base_fund_data = obj.serialize()
                for dividend in b3.fiagro_dividends(cnpj=obj.cnpj, identificador=obj.acronimo):
                    row = {**base_fund_data, **dividend.serialize()}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)
                    # TODO: include stock_dividends?

    elif command == "fiagro-subscriptions":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiagros():
                base_fund_data = obj.serialize()
                data = b3.fiagro_subscriptions(cnpj=obj.cnpj, identificador=obj.acronimo)
                for subscription in data:
                    row = {**base_fund_data, **subscription}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fiagro-documents":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fiagros():
                base_fund_data = obj.serialize()
                data = b3.fiagro_documents(identificador=obj.acronimo, cnpj=obj.cnpj)
                for doc in data:
                    row = {**base_fund_data, **doc}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fip-dividends":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fips():
                base_fund_data = obj.serialize()
                for dividend in b3.fip_dividends(cnpj=obj.cnpj, identificador=obj.acronimo):
                    row = {**base_fund_data, **dividend.serialize()}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)
                    # TODO: include stock_dividends?

    elif command == "fip-documents":
        # TODO: o arquivo está ficando em branco, verificar
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fips():
                base_fund_data = obj.serialize()
                for doc in b3.fip_documents(identificador=obj.acronimo, cnpj=obj.cnpj):
                    row = {**base_fund_data, **doc}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "fip-subscriptions":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for obj in b3.fips():
                base_fund_data = obj.serialize()
                for subscription in b3.fip_subscriptions(cnpj=obj.cnpj, identificador=obj.acronimo):
                    row = {**base_fund_data, **subscription}
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "debentures":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for row in b3.debentures():
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "negociacao-balcao":
        today = datetime.datetime.now().date()
        start_date = datetime.date(today.year, 1, 1)
        end_date = today + datetime.timedelta(days=1)
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for date in day_range(start_date, end_date + datetime.timedelta(days=1)):
                for row in b3.negociacao_balcao(date):
                    row = asdict(row)
                    if writer is None:
                        writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                        writer.writeheader()
                    writer.writerow(row)

    elif command == "negociacao-bolsa":
        frequencia = args.frequencia
        data = args.data

        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for negociacao in b3.negociacao_bolsa(frequencia, data):
                row = asdict(negociacao)
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif args.command == "intraday-baixar":
        data = args.data
        chunk_size = args.chunk_size
        zip_filename = args.zip_filename
        zip_filename.parent.mkdir(parents=True, exist_ok=True)

        url = b3.url_intraday_zip(data)
        response = b3.session.get(url, stream=True)
        response.raise_for_status()
        with zip_filename.open("wb") as fobj:
            for chunk in response.iter_content(chunk_size):
                fobj.write(chunk)

    elif args.command == "intraday-converter":
        zip_filename = args.zip_filename
        zip_filename.parent.mkdir(parents=True, exist_ok=True)
        csv_filename = args.csv_filename
        codigo_ativo = set(args.codigo_ativo) if args.codigo_ativo else None

        with csv_filename.open(mode="w") as fobj, zip_filename.open(mode="rb") as zip_fobj:
            writer = None
            for row in b3._le_zip_intraday(zip_fobj):
                if writer is None:
                    writer = csv.DictWriter(fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                if codigo_ativo is None or row["CodigoInstrumento"] in codigo_ativo:
                    writer.writerow(row)

    elif command == "clearing-acoes-custodiadas":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_acoes_custodiadas(data_inicial=args.data_inicial):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-creditos-de-proventos":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_creditos_de_proventos(data_inicial=args.data_inicial, filtro_emissor=args.emissor):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-custodia-fungivel":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_custodia_fungivel(data=args.data):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-emprestimos-registrados":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_emprestimos_registrados(
                data_inicial=args.data_inicial, data_final=args.data_final, filtro_ticker=args.ticker
            ):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-emprestimos-negociados":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_emprestimos_negociados(
                data=args.data,
                filtro_tomador=args.tomador,
                filtro_doador=args.doador,
                filtro_mercado=args.mercado,
                filtro_ticker=args.ticker,
            ):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-emprestimos-em-aberto":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_emprestimos_em_aberto(
                data_inicial=args.data_inicial,
                data_final=args.data_final,
                filtro_mercado=args.mercado,
                filtro_ticker=args.ticker,
            ):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-opcoes-flexiveis":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_opcoes_flexiveis(data=args.data, filtro_ticker=args.ticker):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-prazo-deposito-titulos":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_prazo_deposito_titulos(data=args.data):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-posicoes-em-aberto":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_posicoes_em_aberto(data=args.data):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-swap":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for item in b3.clearing_swap(data=args.data):
                row = item.serialize()
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

    elif command == "clearing-termo-eletronico":
        with csv_filename.open(mode="w") as csv_fobj:
            writer = None
            for row in b3.clearing_termo_eletronico(data=args.data):
                if writer is None:
                    writer = csv.DictWriter(csv_fobj, fieldnames=list(row.keys()))
                    writer.writeheader()
                writer.writerow(row)

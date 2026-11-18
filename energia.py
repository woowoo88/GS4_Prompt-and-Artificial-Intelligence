"""Cenário didático de eficiência e geração residencial em São Paulo/SP."""

import re
import unicodedata


DIAS = 365
CONSUMO_ANUAL_KWH = 3000
LAMPADAS = 8
HORAS_DE_USO_DIA = 4
FLUXO_LUMINOSO_LM = 800
POTENCIA_FLUORESCENTE_W = 15
POTENCIA_LED_W = 9
PRECO_LED = 15.0
POTENCIA_SOLAR_KWP = 2.0
IRRADIACAO_KWH_M2_DIA = 4.671
FATOR_DESEMPENHO = 0.80
FRACAO_USO_DIRETO = 0.35
VALOR_IMPORTADO_KWH = 1.00
VALOR_CREDITO_KWH = 0.60
INVESTIMENTO_SOLAR = 8000.0
FATOR_EMISSAO_KG_CO2_KWH = 0.0385  # SIN, ano de 2023 (MCTI).

ATLAS = "https://labren.ccst.inpe.br/atlas2_tables/SP_inc.html"
ANEEL = "https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida"
INMETRO = "https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica/lampadas/"
SINIR = "https://www.sinir.gov.br/perfis/logistica-reversa/logistica-reversa/lampadas-fluorescentes-de-vapor-de-sodio-e-mercurio-e-de-luz-mista/"
MCTI = "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2024/02/fator-de-emissao-de-co2-na-geracao-de-energia-eletrica-no-brasil-em-2023-e-o-menor-em-12-anos"
CETEM = "https://mineralis.cetem.gov.br/bitstream/cetem/2378/1/manual-destinacao-residuos-eletroeletronicos-3ed.pdf"
FONTES_ENERGIA = {
    "Inmetro": INMETRO,
    "SINIR": SINIR,
    "Atlas do INPE": ATLAS,
    "ANEEL": ANEEL,
    "CETEM": CETEM,
    "MCTI": MCTI,
}

_LED = re.compile(r"\b(?:leds?|lampadas?|fluorescentes?|lumens?|iluminacao)\b")
_SOLAR = re.compile(
    r"\b(?:energia solar|fotovoltaic[oa]s?|paineis solares|painel solar|"
    r"placas? solares?|placa solar|geracao solar|sistema solar|kwp|microgeracao|"
    r"solar residencial|solar em casa|solar no telhado|solar zera)\b"
)
_GERAL = re.compile(
    r"\b(?:energias?|eletricidade|eletric[oa]s?|sustentabilidade|"
    r"renovaveis|renovavel|kwh|conta de luz|fatura de luz)\b"
)


def _normalizar_energia(consulta: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", consulta.casefold())
    return " ".join("".join(c for c in sem_acentos if not unicodedata.combining(c)).split())


def eh_consulta_energia(consulta: str) -> bool:
    """Identifica vocabulário de consumo, iluminação ou geração residencial."""
    normalizada = _normalizar_energia(consulta)
    return normalizada == "solar" or any(
        expressao.search(normalizada) for expressao in (_LED, _SOLAR, _GERAL)
    )


def calcular_cenario() -> dict[str, float]:
    """Aplica as premissas fixas do estudo e devolve resultados sem arredondar."""
    horas_anuais = HORAS_DE_USO_DIA * DIAS
    consumo_fluorescente = LAMPADAS * POTENCIA_FLUORESCENTE_W * horas_anuais / 1000
    consumo_led = LAMPADAS * POTENCIA_LED_W * horas_anuais / 1000
    economia_led = consumo_fluorescente - consumo_led
    geracao_solar = POTENCIA_SOLAR_KWP * IRRADIACAO_KWH_M2_DIA * DIAS * FATOR_DESEMPENHO
    uso_direto = geracao_solar * FRACAO_USO_DIRETO
    injecao = geracao_solar - uso_direto
    return {
        "consumo_fluorescente_kwh": consumo_fluorescente,
        "consumo_led_kwh": consumo_led,
        "economia_led_kwh": economia_led,
        "economia_led_reais": economia_led * VALOR_IMPORTADO_KWH,
        "investimento_led_reais": LAMPADAS * PRECO_LED,
        "geracao_solar_kwh": geracao_solar,
        "uso_direto_solar_kwh": uso_direto,
        "injecao_solar_kwh": injecao,
        "economia_solar_reais": uso_direto * VALOR_IMPORTADO_KWH + injecao * VALOR_CREDITO_KWH,
        "co2_led_kg": economia_led * FATOR_EMISSAO_KG_CO2_KWH,
        "co2_solar_kg": uso_direto * FATOR_EMISSAO_KG_CO2_KWH,
    }


def _pt(valor: float, casas: int = 2) -> str:
    inteiro, _, decimal = f"{valor:,.{casas}f}".partition(".")
    return inteiro.replace(",", ".") + (f",{decimal}" if casas else "")


def resposta_energia(consulta: str) -> str:
    """Oferece orientação verificável e proporcional ao tema da consulta."""
    dados = calcular_cenario()
    normalizada = _normalizar_energia(consulta)
    pergunta_led = bool(_LED.search(normalizada))
    pergunta_solar = bool(_SOLAR.search(normalizada)) or normalizada == "solar" or (
        pergunta_led and bool(re.search(r"\bsolar\b", normalizada))
    )
    introducao = (
        f"Estudo de caso ilustrativo de uma residência em São Paulo (SP), com consumo "
        f"estimado de {_pt(CONSUMO_ANUAL_KWH, 0)} kWh em {DIAS} dias. "
        "Os valores servem para comparar opções e variam de uma casa para outra."
    )
    if re.search(r"\b(?:banho|chuveiro)\b", normalizada):
        introducao += (
            " O estudo cobre lâmpadas e geração solar. Para estimar mudanças no banho, "
            "seria preciso conhecer a potência do chuveiro e o tempo de uso."
        )
    led = (
        f"Lâmpadas LED. Para {LAMPADAS} lâmpadas usadas {HORAS_DE_USO_DIA} h/dia, a troca "
        f"de fluorescentes de {POTENCIA_FLUORESCENTE_W} W por LEDs de {POTENCIA_LED_W} W "
        f"com brilho equivalente (cerca de {FLUXO_LUMINOSO_LM} lúmens cada) reduz o consumo de "
        f"iluminação de {_pt(dados['consumo_fluorescente_kwh'])} para "
        f"{_pt(dados['consumo_led_kwh'])} kWh/ano. A economia estimada é de "
        f"{_pt(dados['economia_led_kwh'])} kWh/ano, ou R$ {_pt(dados['economia_led_reais'])} "
        f"por ano a R$ {_pt(VALOR_IMPORTADO_KWH)}/kWh. O investimento hipotético é de "
        f"R$ {_pt(dados['investimento_led_reais'])}. Comece pela lâmpada que fica mais tempo acesa. "
        "Para manter o brilho, compare os lúmens (lm) nas embalagens. Confira também a etiqueta "
        "e a compatibilidade com a luminária. Entregue as fluorescentes "
        "usadas em pontos de coleta, pois contêm mercúrio."
    )
    proximo_passo_led = (
        "Para estimar sua economia em um mês, multiplique a quantidade de lâmpadas pela "
        "diferença de potência em watts e pelas horas de uso naquele mês. Divida por 1.000 "
        "para obter kWh e multiplique pelo valor variável do kWh na sua conta. Para recuperar "
        "o custo da troca em seis meses, um limite aproximado de gasto é seis vezes a economia "
        "mensal estimada, se uso e tarifa permanecerem parecidos."
    )
    solar = (
        f"Solar fotovoltaica. Um sistema de {_pt(POTENCIA_SOLAR_KWP, 0)} kWp (potência de pico) "
        f"sem bateria geraria cerca de {_pt(dados['geracao_solar_kwh'], 0)} kWh/ano no cenário. "
        f"O cálculo usa a irradiação local do INPE de {_pt(IRRADIACAO_KWH_M2_DIA, 3)} kWh/m²/dia "
        f"e um fator de desempenho de {_pt(FATOR_DESEMPENHO)} para representar perdas. "
        f"Consideramos {_pt(FRACAO_USO_DIRETO * 100, 0)}% de uso direto a "
        f"R$ {_pt(VALOR_IMPORTADO_KWH)}/kWh e o restante injetado na rede com créditos "
        f"totalmente aproveitados a R$ {_pt(VALOR_CREDITO_KWH)}/kWh. Isso resultaria em um "
        f"abatimento bruto estimado de R$ {_pt(dados['economia_solar_reais'])}/ano, com "
        f"investimento hipotético de R$ {_pt(INVESTIMENTO_SOLAR, 0)}. A fatura pode manter "
        "cobranças como o custo de disponibilidade, um valor mínimo pelo acesso à rede quando aplicável. "
        "O abatimento bruto não desconta manutenção nem financiamento. Planeje a destinação "
        "dos módulos e do inversor no fim da vida útil."
    )
    proximo_passo_solar = (
        "Antes de assinar, procure nas suas últimas 12 faturas o consumo de cada mês em kWh. "
        "Peça uma simulação que coloque lado a lado o consumo, a geração prevista, os créditos "
        "e o valor que ainda seria cobrado mês a mês. Peça também avaliação do telhado, "
        "do sombreamento e da conexão à distribuidora."
    )
    impacto_led = (
        f"A menor compra de eletricidade equivale a cerca de {_pt(dados['co2_led_kg'], 1)} kg de CO₂/ano "
        "pelo fator médio do Sistema Interligado Nacional em 2023. É um indicador operacional, "
        "sem incluir fabricação e descarte."
    )
    impacto_solar = (
        f"O uso direto da geração equivale a cerca de {_pt(dados['co2_solar_kg'], 1)} kg de CO₂/ano "
        "na eletricidade comprada, pelo fator médio do Sistema Interligado Nacional em 2023. "
        "A conta exclui a energia injetada, fabricação e descarte."
    )

    if pergunta_led and not pergunta_solar:
        fontes_led = f"Fontes: Inmetro {INMETRO}\nSINIR {SINIR}\nMCTI {MCTI}"
        return "\n\n".join((introducao, led, proximo_passo_led, impacto_led, fontes_led))
    if pergunta_solar and not pergunta_led:
        fontes_solar = f"Fontes: Atlas do INPE {ATLAS}\nANEEL {ANEEL}\nCETEM {CETEM}\nMCTI {MCTI}"
        return "\n\n".join((introducao, solar, proximo_passo_solar, impacto_solar, fontes_solar))

    orientacao = (
        "A troca por LED diminui o consumo mantendo o nível de iluminação. A geração solar "
        "mantém o consumo e substitui parte da energia comprada. Antes de escolher, confira "
        "12 meses de consumo e a tarifa na sua conta. Reavalie o tamanho do sistema solar "
        "se adotar as duas opções. As estimativas deixam de fora manutenção, financiamento e "
        "cobranças fixas."
    )
    fontes = "Fontes: " + "\n".join(f"{nome} {url}" for nome, url in FONTES_ENERGIA.items())
    return "\n\n".join((introducao, led, solar, proximo_passo_solar, orientacao,
                        impacto_led, impacto_solar, fontes))

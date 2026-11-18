# Energia residencial no Citizen Assist AI

## Público e necessidade

O módulo atende moradores de São Paulo (SP) que querem reduzir gastos com eletricidade mantendo o conforto da casa. Compara a troca de lâmpadas e a geração solar própria para uma mesma residência, no mesmo período de 365 dias. A energia solar fotovoltaica é a alternativa renovável. Os resultados ajudam a decidir qual ação merece investigação na residência real.

Para o caso didático, adotamos uma casa com consumo de 250 kWh/mês na média, ou 3.000 kWh/ano. É um perfil deliberadamente acima da média estadual de 188 kWh/mês por unidade consumidora no recorte de 2025 [1]. O consumo escolhido inclui a iluminação e representa um domicílio com uso relativamente alto. A simulação não utiliza faturas de moradores.

## Dados e premissas

| Variável | Valor | Origem e justificativa |
| --- | ---: | --- |
| Consumo total de referência | 3.000 kWh/ano | Premissa acima da média estadual para estudar a redução da despesa de uma casa com uso relativamente alto [1]. |
| Iluminação | 8 lâmpadas, 4 horas/dia cada | Perfil de uso estimado para oito pontos de luz de uso regular. |
| Potência e fluxo luminoso | Fluorescente 15 W e LED 9 W, ambas com cerca de 800 lm | Par estimado para comparar níveis equivalentes de luz. O Inmetro fornece dados por modelo [2]. |
| LED | R$ 15/unidade | Hipótese didática para explicitar o custo inicial de oito unidades. |
| Irradiação média diária anual no plano inclinado | 4.671 Wh/m²/dia = 4,671 kWh/m²/dia | Dado público do Atlas Brasileiro de Energia Solar, célula 5728, longitude −46,649 e latitude −23,5005. O Atlas usa estimativas modeladas com imagens de satélite de 1999 a 2015 [3]. |
| Sistema fotovoltaico | 2 kWp, conectado à rede, sem bateria | Potência de pico escolhida para aproximar a geração anual do consumo do cenário. |
| Fator de desempenho solar | 0,80 | Estimativa única para perdas, incluindo temperatura, conversão no inversor e cabeamento. |
| Uso direto da geração | 35% da geração | Premissa de coincidência parcial entre a carga residencial e as horas de sol. O saldo de 65% é injetado na rede. |
| Parcela variável evitada na compra | R$ 1,00/kWh | Valor redondo didático para comparar alternativas com a mesma referência. |
| Valor efetivo de compensação | R$ 0,60/kWh injetado e compensado | Hipótese abaixo do custo de compra para ilustrar que a valoração dos créditos depende das regras e da tarifa. No caso base, todo o excedente anual é aproveitado [4]. |
| Sistema solar instalado | R$ 8.000 | Hipótese didática de R$ 4.000/kWp para simular a diferença de investimento inicial. |
| Fator médio de CO₂ do SIN | 0,0385 kg CO₂/kWh | MCTI, ano-base de 2023. Corresponde a 0,0385 t CO₂/MWh [5]. |

As hipóteses de preço e tarifa são para simulação. Para uma decisão real, use as parcelas variáveis da fatura, confirme o regime de compensação e solicite cotações que incluam os componentes e a instalação.

## Cálculos reproduzíveis

**Alternativa A — eficiência com LED**

- Energia elétrica em kWh = quantidade de lâmpadas × potência em W × horas de uso ÷ 1.000.
- Linha de base da iluminação = `8 × 15 × 4 × 365 ÷ 1.000` = **175,20 kWh/ano**.
- Com LED = `8 × 9 × 4 × 365 ÷ 1.000` = **105,12 kWh/ano**.
- Economia = **70,08 kWh/ano**, ou **40% da iluminação** e **2,34% da demanda total**. As demais cargas usam 2.824,80 kWh/ano e permanecem constantes.
- A eficácia luminosa do exemplo passa de `800 ÷ 15 = 53,3 lm/W` para `800 ÷ 9 = 88,9 lm/W`. O lumen mede a quantidade de luz emitida e o watt mede a potência demandada.
- Redução variável da despesa = `70,08 × R$ 1,00` = **R$ 70,08/ano**. Investimento inicial = `8 × R$ 15` = **R$ 120**.

**Alternativa B — geração solar fotovoltaica**

- Irradiação diária ÷ irradiância de referência de 1 kW/m² = **4,671 horas de sol pleno equivalentes por dia**.
- Geração em kWh = potência de pico × horas de sol pleno × dias × fator de desempenho.
- Geração estimada = `2 × 4,671 × 365 × 0,80` = **2.727,86 kWh/ano**. A geração equivale a 90,93% da demanda ao comparar apenas os totais anuais.
- Uso direto = `2.727,864 × 0,35` = **954,75 kWh/ano**. A residência ainda importa **2.045,25 kWh/ano** antes dos créditos. Os **1.773,11 kWh/ano** restantes da produção são injetados.
- Abatimento bruto simulado = `(954,7524 × R$ 1,00) + (1.773,1116 × R$ 0,60)` = **R$ 2.018,62/ano**. Investimento inicial hipotético = **R$ 8.000**.
- Créditos alteram o faturamento. O uso direto altera a energia importada. Quando aplicáveis, o custo de disponibilidade e outras parcelas permanecem na fatura [4].

## Comparação para o primeiro ano

| Indicador | Sem intervenção | Alternativa A, LED | Alternativa B, fotovoltaica |
| --- | ---: | ---: | ---: |
| Consumo da residência (kWh/ano) | 3.000,00 | 2.929,92 | 3.000,00 |
| Geração local (kWh/ano) | 0,00 | 0,00 | 2.727,86 |
| Eletricidade importada, antes de créditos (kWh/ano) | 3.000,00 | 2.929,92 | 2.045,25 |
| Redução bruta modelada da despesa variável (R$/ano) | 0,00 | 70,08 | 2.018,62 |
| Desembolso inicial hipotético (R$) | 0,00 | 120,00 | 8.000,00 |
| Desembolso inicial menos redução do primeiro ano (R$) | 0,00 | 49,92 | 5.981,38 |
| CO₂ operacional associado à eletricidade comprada (kg CO₂/ano) | 115,50 | 112,80 | 78,74 |

Para o indicador ambiental, multiplicamos a eletricidade fisicamente importada pelo fator médio de 2023. A diferença corresponde a **2,70 kg CO₂/ano** no LED e **36,76 kg CO₂/ano** na solar. O cálculo tem fronteira residencial e exclui as injeções na rede. É uma aproximação da pegada operacional da compra de eletricidade. O efeito sobre a operação do sistema elétrico e as emissões de fabricação, transporte, manutenção e descarte exigem outro método [5].

## Decisão, viabilidade e limitações

- **LED.** Faz sentido começar pelos pontos mais usados se o orçamento for limitado. Compare o fluxo luminoso na embalagem e confira encaixe, tensão e compatibilidade com a luminária. Considere substituir as fluorescentes ao fim da vida útil e use um ponto da logística reversa por causa do mercúrio. A fabricação e o descarte de LEDs também demandam materiais e destinação adequada [2, 6].
- **Solar.** Vale solicitar avaliação se houver autorização para instalação, área disponível, insolação e telhado adequado. Peça a um profissional que estime a produção mensal, avalie estrutura e sombreamento e verifique a conexão com a distribuidora. O sistema exige equipamento, manutenção e destinação dos módulos e do inversor ao fim da vida útil [3, 4, 7].
- **Sensibilidade.** Com 2 h/dia de uso, a vantagem do LED cai a 35,04 kWh/ano e R$ 35,04/ano. Com geração solar 15% menor, mantendo as demais hipóteses, o abatimento bruto cai para R$ 1.715,83/ano. Se nenhum crédito do excedente da geração do caso base for utilizado, resta o valor do uso direto, R$ 954,75/ano.
- **Leitura financeira.** Se a redução anual do caso base permanecesse constante, o investimento dividido pela redução bruta daria 1,71 ano para LED e 3,96 anos para solar. Esses prazos são apenas quocientes do cenário, sem custos de manutenção e reposição, custo de disponibilidade, financiamento, variação de tarifa ou degradação. O modelo anual não simula o saldo de créditos mês a mês. Para avaliar um projeto real, compare os fluxos de caixa e os componentes da fatura.
- **Aplicação conjunta.** A comparação usa alternativas independentes sobre a mesma base. Ao adotar LED, recalcule a carga anual e horária antes de dimensionar um sistema solar. Usar menos energia durante o dia também pode alterar a fração de geração usada diretamente.

## Integração com o assistente

O módulo `energia.py` calcula os valores em `calcular_cenario()` e oferece respostas fundamentadas em `resposta_energia()`. A orientação mostra as estimativas e fontes da alternativa perguntada, ou compara as opções quando a pergunta é geral. Experimente no Citizen Assist AI:

- “Quanto economizo com lâmpadas LED?”
- “Energia solar zera a conta?”
- “Compare LED e solar.”
- “Quais são as fontes e limitações da análise de energia?”

Para reproduzir os números sem abrir o Colab, execute na pasta que contém `energia.py`:

```bash
python -c "from pprint import pprint; from energia import calcular_cenario; pprint(calcular_cenario())"
```

## Referências

1. ARSP. *Informações Energéticas, out–dez/2025*. Média residencial estadual compilada de dados da ANEEL até outubro. [Boletim com tabela estadual](https://arsp.es.gov.br/Media/arsi/Energia/Boletins/Boletins/4%20-%20INFORMACOES_ENERGETICAS_OUT_DEZ_2025.pdf)
2. Inmetro. *Programa Brasileiro de Etiquetagem, lâmpadas*. [Consulta por modelo](https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica/lampadas/) e [orientação sobre eficácia luminosa](https://www.gov.br/inmetro/pt-br/acesso-a-informacao/perguntas-frequentes/avaliacao-da-conformidade/lampadas-e-luminarias-led-portaria-inmetro-no-231-2026-consumidores/para-pagar-uma-conta-de-energia-mais-barata-devo-comprar-lampadas-e-luminarias-de-luz-201cfria201d).
3. LABREN/CCST/INPE, Brasil. *Atlas Brasileiro de Energia Solar*, 2ª edição, 2017. [Irradiação no plano inclinado, SP](https://labren.ccst.inpe.br/atlas2_tables/SP_inc.html) e [metadados do Atlas](https://labren.ccst.inpe.br/projetos/atlas_2017/atlas_solar_2017_metadados.pdf).
4. ANEEL. *Micro e Minigeração Distribuída*. [Orientações sobre compensação, adesão e faturamento](https://www.gov.br/aneel/pt-br/assuntos/geracao-distribuida) e [Lei nº 14.300/2022](https://www2.camara.leg.br/legin/fed/lei/2022/lei-14300-6-janeiro-2022-792217-normaatualizada-pl.html).
5. MCTI. *Fator de emissão de CO₂ na geração de energia elétrica no Brasil em 2023*. [Fator médio anual do SIN](https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/noticias/2024/02/fator-de-emissao-de-co2-na-geracao-de-energia-eletrica-no-brasil-em-2023-e-o-menor-em-12-anos).
6. SINIR. *Logística reversa de lâmpadas fluorescentes, de vapor de sódio e mercúrio e de luz mista*. [Condições e pontos de recebimento](https://www.sinir.gov.br/perfis/logistica-reversa/logistica-reversa/lampadas-fluorescentes-de-vapor-de-sodio-e-mercurio-e-de-luz-mista/).
7. CETEM. *Manual de Orientações sobre a Destinação de Resíduos Eletroeletrônicos*, 3ª edição, p. 41–42. [Cuidados com módulos fotovoltaicos](https://mineralis.cetem.gov.br/bitstream/cetem/2378/1/manual-destinacao-residuos-eletroeletronicos-3ed.pdf).

# Citizen Assist AI no Google Colab

**Angela Sousa Takezawa — RM 570797**  
**Mariana Carminato — RM 573258**  
**Turma 1CCPX**

O protótipo principal está em `Citizen_Assist_Colab.ipynb`. Ele reúne em um único arquivo:

- instalação do LangGraph, do Ollama e do modelo `llama3.2:1b`;
- sete fichas verificáveis FC-01 a FC-07;
- agente LangGraph `validar → recuperar → selecionar → compor`;
- menu por categorias e pergunta livre com `ipywidgets`;
- proteção de dados pessoais e recusa a prompt injection;
- testes automatizados;
- 26 casos do golden dataset e pipeline LLM as a Judge;
- comparação documentada antes/depois.

## Soluções em Energias Renováveis e Sustentáveis

A contribuição da disciplina atende moradores de São Paulo (SP) que querem reduzir o gasto de eletricidade em casa. O assistente compara duas opções para uma residência de referência durante um ano: substituir lâmpadas fluorescentes por LED de luminosidade equivalente e instalar um sistema fotovoltaico. A primeira reduz a demanda. A segunda gera eletricidade e pode reduzir a compra da rede.

Escolha **Energia residencial** no menu do notebook ou escreva uma pergunta como “Compare lâmpadas LED e energia solar”, “Quanto economizo com LED?” ou “Energia solar zera a conta?”. O assistente apresenta os resultados do cenário, as referências e as condições para interpretar custos e geração. A resposta de energia usa os cálculos de `energia.py` sem inferência do modelo.

- [Dados, premissas, cálculos e recomendações](ENERGIA.md)
- [Protocolo e registro dos testes com usuários](TESTES_COM_USUARIOS.md)

Para testar pela linha de comando, execute na pasta que contém `agente.py`:

```powershell
python -m pip install -r requirements.txt
python agente.py
python -m unittest -v test_agente
```

As consultas de energia e os testes automatizados dessa rota funcionam sem o Ollama. O notebook completo também roda os exemplos de documentação digital, que usam o modelo local.

## Execução

1. Envie `Citizen_Assist_Colab.ipynb` ao Google Drive ou abra-o diretamente no Google Colab.
2. Escolha **Ambiente de execução > Executar tudo**.
3. Aguarde a instalação e o download do modelo, que ocupa aproximadamente 1,3 GB.
4. Use a seção **Interface do agente** no próprio notebook.

Não é necessário abrir servidor, navegador local ou arquivo HTML. A interface é exibida nas células do Colab. O notebook não cria histórico de consultas nem solicita dados pessoais.

## Avaliação

A execução integral validada concluiu 26 casos antes e 26 depois da melhoria. O juiz híbrido aprovou 12/26 na versão inicial e 20/26 na versão melhorada. Esses números representam decisões do juiz e devem ser lidos junto da conferência manual.

A repetição completa fica desativada por padrão no notebook para não consumir todo o tempo do runtime. Para reproduzi-la, altere `EXECUTAR_AVALIACAO_COMPLETA` para `True` e execute a célula.

## Limitações

Para documentação digital, o assistente usa as fichas fictícias da Central do Cidadão de Aurora e orienta o usuário a confirmar as informações no órgão competente. As estimativas energéticas se referem à residência de exemplo. Para avaliar sua aplicação, confira seu consumo, as condições do imóvel, a tarifa e os orçamentos locais.

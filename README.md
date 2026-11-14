# Hábitos de saúde em Orlândia

Projeto de extensão do curso de Ciência de Dados (UNINTER), feito por Lucas Geloni Gonçalves.

A ideia é simples: perguntar para moradores de Orlândia – SP como andam seus hábitos de saúde e usar Python para entender o que os dados mostram. Isso pode ajudar a pensar em ações de conscientização na cidade.

## O que tem aqui

- `analise_habitos_saude.py`: script que limpa os dados e gera os gráficos
- `respostas_formulario.csv`: respostas originais do Google Forms (anônimas)
- `respostas_limpas.csv`: respostas depois da limpeza
- `graficos/`: gráficos gerados pela análise

## Como rodar

```
pip install pandas matplotlib
python analise_habitos_saude.py
```

O CSV precisa estar na mesma pasta do script.

## O que encontrei

Foram 28 respostas válidas:

- Idade média: 29,2 anos
- Sono médio: 7,3 horas por noite
- Atividade física mais comum: 3 a 4 vezes por semana (29%)
- Última consulta médica mais comum: entre 6 meses e 1 ano atrás (46%)
- Alimentação mais comum na autoavaliação: "Boa" (36%)

Obs.: a amostra é pequena e foi feita por conveniência, então não representa toda a cidade. É só um retrato do grupo que respondeu.

## Feito com

Python, Pandas, Matplotlib e Google Forms.

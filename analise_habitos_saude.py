import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

ARQUIVO_ENTRADA = "respostas_formulario.csv"
ARQUIVO_LIMPO = "respostas_limpas.csv"
PASTA_GRAFICOS = "graficos"

COLUNAS = {
    "Carimbo de data/hora": "data_resposta",
    "Qual a sua idade?": "idade",
    "Com que frequência você pratica atividade física?": "atividade_fisica",
    "Quantas horas você dorme por noite, em média?": "horas_sono",
    "Quando foi sua última consulta médica?": "ultima_consulta",
    "Como você avalia sua alimentação?": "alimentacao",
}

FAIXAS_LIMITES = [17, 29, 39, 49, 59, 120]
FAIXAS_NOMES = ["18-29", "30-39", "40-49", "50-59", "60+"]


def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    print(f"Respostas recebidas (bruto): {len(df)}")
    return df.rename(columns=COLUNAS)


def extrair_numero(serie):
    texto = serie.astype(str).str.extract(r"(\d+[.,]?\d*)")[0]
    return pd.to_numeric(texto.str.replace(",", ".", regex=False), errors="coerce")


def limpar_dados(df):
    df = df.copy()

    antes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicadas removidas: {antes - len(df)}")

    colunas_texto = df.select_dtypes(include=["object", "string"]).columns
    for col in colunas_texto:
        if col != "data_resposta":
            df[col] = df[col].astype(str).str.strip().str.capitalize()
            df[col] = df[col].replace("Nan", pd.NA)

    if "idade" in df.columns:
        df["idade"] = extrair_numero(df["idade"])
        df.loc[(df["idade"] < 18) | (df["idade"] > 110), "idade"] = pd.NA

    if "horas_sono" in df.columns:
        df["horas_sono"] = extrair_numero(df["horas_sono"])
        df.loc[(df["horas_sono"] <= 0) | (df["horas_sono"] > 16), "horas_sono"] = pd.NA

    if "data_resposta" in df.columns:
        df["data_resposta"] = pd.to_datetime(df["data_resposta"], errors="coerce")

    if "idade" in df.columns:
        df["faixa_etaria"] = pd.cut(df["idade"], bins=FAIXAS_LIMITES, labels=FAIXAS_NOMES)

    print("\nValores ausentes por coluna:")
    print(df.isna().sum())

    return df.reset_index(drop=True)


def grafico_barras(serie, titulo, nome_arquivo, rotulo_x=""):
    contagem = serie.value_counts(dropna=True)
    if contagem.empty:
        print(f"Sem dados para o gráfico: {titulo}")
        return

    percentuais = contagem / contagem.sum() * 100

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(contagem.index.astype(str), contagem.values, color="#2a7f62")

    for barra, pct in zip(barras, percentuais):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height(),
            f"{pct:.0f}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_title(titulo, fontsize=13)
    ax.set_xlabel(rotulo_x)
    ax.set_ylabel("Número de respostas")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(PASTA_GRAFICOS, nome_arquivo), dpi=150)
    plt.close(fig)


def grafico_histograma_sono(df):
    dados = df["horas_sono"].dropna()
    if dados.empty:
        print("Sem dados de sono para o histograma.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(dados, bins=range(2, 13), color="#534ab7", edgecolor="white")
    ax.axvline(dados.mean(), color="#a32d2d", linestyle="--",
               label=f"Média: {dados.mean():.1f} h")
    ax.set_title("Horas de sono por noite", fontsize=13)
    ax.set_xlabel("Horas de sono")
    ax.set_ylabel("Número de respostas")
    ax.legend()
    plt.tight_layout()
    fig.savefig(os.path.join(PASTA_GRAFICOS, "horas_sono.png"), dpi=150)
    plt.close(fig)


def gerar_graficos(df):
    os.makedirs(PASTA_GRAFICOS, exist_ok=True)

    if "faixa_etaria" in df.columns:
        grafico_barras(df["faixa_etaria"].astype("object"),
                       "Perfil dos participantes por faixa etária",
                       "faixa_etaria.png", "Faixa etária (anos)")

    if "atividade_fisica" in df.columns:
        grafico_barras(df["atividade_fisica"],
                       "Frequência de atividade física",
                       "atividade_fisica.png")

    if "horas_sono" in df.columns:
        grafico_histograma_sono(df)

    if "ultima_consulta" in df.columns:
        grafico_barras(df["ultima_consulta"],
                       "Última consulta médica",
                       "ultima_consulta.png")

    if "alimentacao" in df.columns:
        grafico_barras(df["alimentacao"],
                       "Autoavaliação da alimentação",
                       "alimentacao.png")

    print(f"\nGráficos salvos na pasta '{PASTA_GRAFICOS}'.")


def resumo(df):
    print("\n" + "=" * 50)
    print("RESUMO DA ANÁLISE")
    print("=" * 50)
    print(f"Total de respostas válidas: {len(df)}")

    if "idade" in df.columns:
        print(f"Idade média: {df['idade'].mean():.1f} anos")
    if "horas_sono" in df.columns:
        print(f"Média de sono: {df['horas_sono'].mean():.1f} horas por noite")

    for col in ["atividade_fisica", "ultima_consulta", "alimentacao"]:
        if col in df.columns and df[col].notna().any():
            moda = df[col].mode()[0]
            pct = (df[col] == moda).mean() * 100
            print(f"{col}: resposta mais comum = '{moda}' ({pct:.0f}%)")


if __name__ == "__main__":
    try:
        dados = carregar_dados(ARQUIVO_ENTRADA)
        dados_limpos = limpar_dados(dados)

        dados_limpos.to_csv(ARQUIVO_LIMPO, index=False, encoding="utf-8-sig")
        print(f"\nBase limpa salva em '{ARQUIVO_LIMPO}'.")

        gerar_graficos(dados_limpos)
        resumo(dados_limpos)

    except FileNotFoundError:
        print(f"Arquivo '{ARQUIVO_ENTRADA}' não encontrado. "
              "Coloque o CSV na mesma pasta do script.")
    except Exception as erro:
        print(f"Erro inesperado: {erro}")
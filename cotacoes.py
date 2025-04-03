import requests
from datetime import datetime
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def buscar_awesomeapi(moeda):
    try:
        url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"
        response = requests.get(url)
        data = response.json()
        preco = data[f"{moeda}BRL"]["bid"]
        return round(float(preco), 4)
    except:
        return None

def buscar_coingecko_btc():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl"
        response = requests.get(url)
        data = response.json()
        return round(float(data["bitcoin"]["brl"]), 2)
    except:
        return None

def buscar_bcb_usd():
    try:
        url = "https://www.bcb.gov.br/api/conteudo/pt-br/PAINEL_INDICADORES/cambio"
        response = requests.get(url, headers={
            "User-Agent": headers["User-Agent"],
            "Accept": "application/json"
        })
        data = response.json()

        for item in data["conteudo"]:
            if item["moeda"] == "Dólar":
                return round(float(item["valorVenda"]), 4)
        return None
    except:
        return None

def formatar_saida(data, usd, eur, btc, bcb):
    return (
        "📊 COTAÇÕES ATUALIZADAS:\n"
        f"data e hora: {data}\n"
        f"USD: {str(usd).replace('.', ',')}\n"
        f"EUR: {str(eur).replace('.', ',')}\n"
        f"BTC: {btc}\n"
        f"USD_BCB: {str(bcb).replace('.', ',')}\n"
    )

def salvar_txt(conteudo):
    with open("cotacoes.csv", "a", encoding="utf-8") as file:
        file.write(conteudo + "\n")

if __name__ == "__main__":
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")

    usd = buscar_awesomeapi("USD")
    eur = buscar_awesomeapi("EUR")
    btc = buscar_coingecko_btc()
    bcb = buscar_bcb_usd()

    texto = formatar_saida(agora, usd, eur, btc, bcb)

    print(texto)          # Exibe no terminal
    salvar_txt(texto)     # Grava no arquivo .csv (como se fosse um log/diário)

from django.shortcuts import render

import requests
from django.shortcuts import render

def converter_dolar_real(request):
    resultado = None
    taxas_disponiveis = ["USD", "EUR", "GBP", "CNY", "JPY", "BRL"]  # Moedas suportadas

    if request.method == 'POST':
        moeda_origem = request.POST.get('moeda_origem')
        moeda_destino = request.POST.get('moeda_destino')
        quantidade = request.POST.get('quantidade')

        if moeda_origem and moeda_destino and quantidade:
            try:

                chave_api = 'bb7015a02ab30e3e26a079fb'
                url = f"https://v6.exchangerate-api.com/v6/{chave_api}/latest/{moeda_origem}"
                response = requests.get(url)
                dados = response.json()

                if dados['result'] == 'success':
                    taxa = dados['conversion_rates'].get(moeda_destino)
                    if taxa:
                        resultado = round(float(quantidade) * taxa, 2)
                    else:
                        resultado = f"Erro: taxa de câmbio para {moeda_destino} não encontrada."
                else:
                    resultado = "Erro ao buscar os dados da API."
            except requests.exceptions.RequestException as e:
                resultado = f"Erro na requisição: {e}"

    return render(request, 'conversor/converter.html', {
        'resultado': resultado,
        'taxas_disponiveis': taxas_disponiveis
    })


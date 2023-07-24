from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


def pegarFotos(host, key, codigo):
    import requests

    url = host + "imoveis/detalhes?key=" + key + "&imovel=" + codigo + "&pesquisa={\"fields\":[{\"Foto\":[\"Foto\"]}]}"

    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers).json()

    return {
        "Foto1": response["Foto"]["1"]["Foto"],
        "Foto2": response["Foto"]["2"]["Foto"]
    }


@app.route("/requisicao", methods=["POST"])
def requisitar():
    payload = request.get_json()["payload"]

    fields = '["ValorVenda", "Bairro" ,"Dormitorios" , "AreaPrivativa" , "Vagas" , "Status", "Cidade" , "Categoria" ,  "FotoDestaque", "FotoDestaquePequena", "UF"]'

    key = payload["key"]
    host = payload["host"]
    filter = '{"Codigo": ' + str(payload["id_moveis"]).replace("'", '"') + '}'

    response = requests.get(
        headers={'Accept': 'application/json'},
        url=host + 'imoveis/listar?key=' + key +
            '&showtotal=1&pesquisa={"filter":' + filter +
            ', "fields":' + fields + ',"order":{"Bairro":"asc"},"paginacao":{"pagina":1,"quantidade":50}}'
    ).json()

    ids = [chave for chave in response.keys() if isinstance(response[chave], dict)]

    objetos_planilhas = []

    for id in ids:
        qtd_quartos = int(response[id]["Dormitorios"])
        qtd_vagas = int(response[id]["Vagas"])
        fotos = pegarFotos(host, key, id)

        objeto = {
            "Valor": response[id]["ValorVenda"],
            "Quartos": f'{qtd_quartos} quartos' if qtd_quartos > 1 or qtd_quartos == 0 else f'{qtd_quartos} quarto',
            "Metros": f'{response[id]["AreaPrivativa"]} m²',
            "Vagas": f'{qtd_vagas} vagas' if qtd_vagas > 1 or qtd_vagas == 0 else f'{qtd_vagas} vaga',
            "Operacao": response[id]["Status"],
            "Bairro": f"Bairro {response[id]['Bairro']}",
            "Tipo": response[id]['Categoria'],
            "Cidade": f"{response[id]['Cidade']}/{response[id]['UF']}",
            "Foto1": fotos["Foto1"],
            "Foto2": fotos["Foto2"]
        }
        objetos_planilhas.append(objeto)

    return jsonify(objetos_planilhas)


if __name__ == "__main__":
    app.run(debug=True)

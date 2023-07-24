from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/requisicao", methods=["POST"])
def requisitar():
    payload = request.get_json()["payload"]

    fields = '["ValorVenda", "Bairro" ,"Dormitorios" , "AreaPrivativa" , "Vagas" , "Status", "Cidade" , "Categoria" ,  "FotoDestaque", "FotoDestaquePequena"]'

    key = payload["key"]
    host = payload["host"]
    filter = '{"Codigo": ' + str(payload["id_moveis"]).replace("'", '"') + '}'

    response = requests.get(
        headers={'Accept': 'application/json'},
        url=host + 'imoveis/listar?key=' + key +
            '&showtotal=1&pesquisa={"filter":' + filter +
            ', "fields":' + fields + ',"order":{"Bairro":"asc"},"paginacao":{"pagina":1,"quantidade":50}}'
    ).json()

    # for imovel in payload["id_moveis"]:
    #     response2 = request.get(
    #         headers={'Accept': 'application/json'},
    #         url=host + 'imoveis/detalhes?key=' + key + '&imovel=' + imovel + '&pesquisa={"fields":' + fields
    #     )

    ids = [chave for chave in response.keys() if isinstance(response[chave], dict)]

    objetos_planilhas = []

    for id in ids:
        qtd_quartos = int(response[id]["Dormitorios"])
        qtd_vagas = int(response[id]["Vagas"])

        objeto = {
            "Valor": response[id]["ValorVenda"],
            "Quartos": f'{qtd_quartos} quartos' if qtd_quartos > 1 or qtd_quartos == 0 else f'{qtd_quartos} quarto',
            "Metros": f'{response[id]["AreaPrivativa"]} m²',
            "Vagas": f'{qtd_vagas} vagas' if qtd_vagas > 1 or qtd_vagas == 0 else f'{qtd_vagas} vaga',
            "Operacao": response[id]["Status"],
            "Bairro": f"Bairro {response[id]['Bairro']}",
            "Tipo": response[id]['Categoria'],
            "Cidade": response[id]['Cidade'],
            "Foto1": response[id]['FotoDestaque'],
            "Foto2": response[id]['FotoDestaquePequena']
        }
        objetos_planilhas.append(objeto)

    return jsonify(objetos_planilhas)


if __name__ == "__main__":
    app.run(debug=True)

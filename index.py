from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route("/requisicao", methods=["POST"])
def requisitar():

    payload = request.get_json()["payload"]

    fields = '["ValorVenda", "Bairro" ,"Dormitorios" , "AreaPrivativa" , "Vagas" , "Status", "Cidade" , "Categoria" ,  "FotoDestaque", "FotoDestaquePequena"]'

    key = payload["key"]
    host = payload["host"]
    filter = '{"Codigo": '+str(payload["id_moveis"]).replace("'",'"')+'}'

    response = requests.get(
        headers={'Accept': 'application/json'},
        url=host + 'imoveis/listar?key=' + key +
            '&showtotal=1&pesquisa={"filter":' + filter +
            ', "fields":' + fields + ',"order":{"Bairro":"asc"},"paginacao":{"pagina":1,"quantidade":50}}'
    ).json()

    ids = [chave for chave in response.keys() if isinstance(response[chave], dict)]

    objetos_planilhas = []

    for id in ids:
        objeto = {
            "Valor": response[id]["ValorVenda"],
            "Quartos": f'{response[id]["Dormitorios"]} quartos',
            "Metros": f'{response[id]["AreaPrivativa"]} m²',
            "Vagas": f'{response[id]["Vagas"]} vagas',
            "Operacao": response[id]["Status"],
            "Titulo": f"{response[id]['Categoria']} em {response[id]['Cidade']}",
            "Bairro": response[id]["Bairro"],
            "Foto1": response[id]['FotoDestaque'],
            "Foto2": response[id]['FotoDestaquePequena']
        }
        objetos_planilhas.append(objeto)

    return jsonify(objetos_planilhas)


if __name__ == "__main__":
    app.run()

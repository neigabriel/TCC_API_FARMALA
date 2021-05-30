from busca_pa import busca
from busca_ultrafarma import buscaultrafarma
from busca_drogaraia import buscadrogaraia
from flask_restx import Api,Resource,fields
from flask import Flask,request
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)
@app.route("/pesquisa", methods = ["POST"])
@cross_origin("*")
def buscar():
    if request.get_json():

        buscarUltra = buscaultrafarma(request.get_json())
        buscarPacheco = busca(request.get_json())
        buscarRaia = buscadrogaraia(request.get_json())
        return ("\n" + "{\n\n" + "Pacheco\n" + buscarPacheco +"\n\n" + "Ultrafarma\n" + buscarUltra + "\n" + "Drogaraia\n" + buscarRaia + "\n}"  )
    else:
        return {"Erro": "Um Nome Deve Ser Pesquisado"}

api = Api(app,
        version = '1.0',
        title = 'Famala_API',
        description = 'Busca de medicamento ',
        doc ='/doc')

template = api.model('template', {
'Nome do Medicamento' : fields.String(description = 'o nome do remedio')
})

@api.route("/pesquisa")
class documentation(Resource):
    @api.expect(template)
    def post(self, ):
        if request.get_json():

            buscarPacheco = busca(request.get_json())
            buscarUltra = buscaultrafarma(request.get_json())
            buscarRaia = buscadrogaraia(request.get_json())

            return ("\n" + "{\n\n" + "Pacheco\n" + buscarPacheco + "\n\n" + "Ultrafarma\n" + buscarUltra + "\n" + "Drogaraia\n" + buscarRaia + "\n}" )
        else:
            return {"Erro": "Um Nome Deve Ser Pesquisado"}
    
    
    
    
    

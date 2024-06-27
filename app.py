# app.py
from flask import Flask, request, jsonify
from config import Config
from models import db, Vaga

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/vagas', methods=['POST'])
def criar_vaga():
    data = request.get_json()
    nova_vaga = Vaga(
        descricao_cargo=data['descricao_cargo'],
        requisitos_obrigatorios=data['requisitos_obrigatorios'],
        requisitos_desejaveis=data.get('requisitos_desejaveis', ''),
        remuneracao_mensal=data['remuneracao_mensal'],
        beneficios=data.get('beneficios', ''),
        local_trabalho=data['local_trabalho']
    )
    db.session.add(nova_vaga)
    db.session.commit()
    return jsonify({'message': 'Vaga criada com sucesso!'}), 201

@app.route('/vagas/<int:id>', methods=['PUT'])
def alterar_vaga(id):
    data = request.get_json()
    vaga = Vaga.query.get(id)
    if not vaga:
        return jsonify({'message': 'Vaga não encontrada!'}), 404
    
    vaga.descricao_cargo = data['descricao_cargo']
    vaga.requisitos_obrigatorios = data['requisitos_obrigatorios']
    vaga.requisitos_desejaveis = data.get('requisitos_desejaveis', vaga.requisitos_desejaveis)
    vaga.remuneracao_mensal = data['remuneracao_mensal']
    vaga.beneficios = data.get('beneficios', vaga.beneficios)
    vaga.local_trabalho = data['local_trabalho']
    vaga.preenchida = data.get('preenchida', vaga.preenchida)

    db.session.commit()
    return jsonify({'message': 'Vaga alterada com sucesso!'}), 200

@app.route('/vagas/<int:id>', methods=['DELETE'])
def excluir_vaga(id):
    vaga = Vaga.query.get(id)
    if not vaga:
        return jsonify({'message': 'Vaga não encontrada!'}), 404
    
    db.session.delete(vaga)
    db.session.commit()
    return jsonify({'message': 'Vaga excluída com sucesso!'}), 200

@app.route('/vagas', methods=['GET'])
def listar_vagas():
    vagas = Vaga.query.all()
    vagas_list = [
        {
            'id': vaga.id,
            'descricao_cargo': vaga.descricao_cargo,
            'requisitos_obrigatorios': vaga.requisitos_obrigatorios,
            'requisitos_desejaveis': vaga.requisitos_desejaveis,
            'remuneracao_mensal': vaga.remuneracao_mensal,
            'beneficios': vaga.beneficios,
            'local_trabalho': vaga.local_trabalho,
            'preenchida': vaga.preenchida
        } for vaga in vagas
    ]
    return jsonify(vagas_list), 200

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import logging

# Configurar o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Inicializar o app Flask
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Log da requisição recebida
        logger.info("Requisição recebida!")

        # Pegar o corpo da requisição
        body = request.get_json()

        if not body:
            return jsonify({"message": "Requisição inválida. Sem dados no corpo."}), 400

        # Processar os dados
        ons_data = body.get("data")  # Substituir 'data' pelo formato exato que o ONS envia
        logger.info(f"Dados do ONS recebidos: {ons_data}")

        # Resposta de sucesso
        return jsonify({"message": "Dados processados com sucesso!", "data": ons_data}), 200

    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return jsonify({"message": "Erro interno do servidor."}), 500

if __name__ == '__main__':
    app.run(port=5000)



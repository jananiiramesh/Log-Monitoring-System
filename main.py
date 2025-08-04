from flask import Flask, jsonify
import logging

app = Flask(__name__)

# Optional: You can still write to a local file for internal server logging,
# but this file will not be used by the producer.
logging.basicConfig(
    filename='api_requests.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

@app.route('/endpoint1', methods=['GET'])
def endpoint1():
    logging.info("endpoint1 was called")
    return jsonify({"message": "Endpoint 1 - OK"}), 200

@app.route('/endpoint2', methods=['GET'])
def endpoint2():
    logging.info("endpoint2 was called")
    return jsonify({"message": "Endpoint 2 - OK"}), 200

@app.route('/endpoint3', methods=['GET'])
def endpoint3():
    logging.warning("endpoint3 triggered a warning")
    return jsonify({"message": "Endpoint 3 - Warning"}), 200

@app.route('/endpoint4', methods=['GET'])
def endpoint4():
    logging.error("endpoint4 triggered an error")
    return jsonify({"message": "Endpoint 4 - Error"}), 500

@app.route('/endpoint5', methods=['GET'])
def endpoint5():
    logging.info("endpoint5 was called")
    return jsonify({"message": "Endpoint 5 - Info"}), 200

@app.route('/endpoint6', methods=['GET'])
def endpoint6():
    logging.warning("endpoint6 triggered a warning")
    return jsonify({"message": "Endpoint 6 - Warning"}), 200

@app.route('/endpoint7', methods=['GET'])
def endpoint7():
    logging.error("endpoint7 triggered an error")
    return jsonify({"message": "Endpoint 7 - Error"}), 500

@app.route('/')
def root():
    return jsonify({"message": "Hello from the 7-endpoint API!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

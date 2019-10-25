from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def main():
    return jsonify()


@app.route('/sum')
def sum():
    # skip validations because reasons
    a = float(request.args.get('param1'))
    b = float(request.args.get('param2'))

    return jsonify(result=a+b)

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


@app.route('/sum2')
def sum2():
    # skip validations because reasons
    a = float(request.args.get('param1'))
    b = float(request.args.get('param2'))

    c = 0
    if 'param3' in request.args:
        c = float(request.args.get('param3'))

    return jsonify(result=a+b+c)

import json
import operator

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def main():
    return jsonify()


@app.route('/sum')
def sum():
    # skip validations because reasons
    a = float(request.args.get('param1'))
    b = float(request.args.get('param2'))

    return jsonify(result=a + b)


@app.route('/sum2')
def sum2():
    # skip validations because reasons
    a = float(request.args.get('param1'))
    b = float(request.args.get('param2'))

    c = 0
    if 'param3' in request.args:
        c = float(request.args.get('param3'))

    return jsonify(result=a + b + c)


def process_operation(operation):
    operators = {
        '*': operator.mul,
        '/': operator.truediv,
        '+': operator.add,
        '-': operator.sub
    }

    param1 = operation['param1']
    param2 = operation['param2']
    operator_function = operators[operation['operator']]

    if type(param1) is dict:
        param1 = process_operation(param1)

    if type(param2) is dict:
        param2 = process_operation(param2)

    return operator_function(param1, param2)


@app.route('/math')
def math():
    operation = json.loads(request.args.get('operation'))

    return jsonify(result=process_operation(operation))

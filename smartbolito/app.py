import os
from flask import Flask, render_template, request
from multiprocessing import Process
from smartbolito.behaviours import behaviours, turn_off


endpoint = os.getenv("ENDPOINT", "localhost:5000")

api = Flask(__name__)
current_process = None
dict_behaviours = dict((b['function_name'], b['function']) for b in behaviours)


@api.route('/', methods=['GET'])
def main():
    return render_template('home.html', behaviours=behaviours, endpoint=endpoint)


@api.route('/run', methods=['GET'])
def run():
    func_id = request.args.get('func')
    if not func_id:
        return 'Empty func parameter', 400

    if func_id not in dict_behaviours:
        return 'Function not found', 404

    global current_process
    if current_process is not None:
        current_process.kill()

    current_process = Process(target=dict_behaviours[func_id])
    current_process.daemon = True
    current_process.start()

    return 'running ' + func_id, 200


@api.route('/off', methods=['GET'])
def run():
    global current_process
    if current_process is not None:
        current_process.kill()

    turn_off()
    return 'turned off', 200

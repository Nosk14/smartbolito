import os
import logging
import signal
from flask import Flask, render_template, request
from multiprocessing import Process
from threading import Lock
from smartbolito.behaviours import behaviours, turn_off


endpoint = os.getenv("ENDPOINT", "localhost:5000")

api = Flask(__name__)
lock = Lock()

gunicorn_logger = logging.getLogger('gunicorn.error')
api.logger.handlers = gunicorn_logger.handlers
api.logger.setLevel(gunicorn_logger.level)

turn_off()
current_process = None
process_pid = None
dict_behaviours = dict((b['function_name'], b['function']) for b in behaviours)


@api.route('/', methods=['GET'])
def main():
    return render_template('home.html', behaviours=behaviours, endpoint=endpoint)


@api.route('/run', methods=['GET'])
def run():
    func_id = request.args.get('func')
    api.logger.info("[" + request.remote_addr + "] " + func_id)
    if not func_id:
        return 'Empty func parameter', 400

    if func_id not in dict_behaviours:
        return 'Function not found', 404

    with lock:
        stop_process()

        global current_process
        current_process = Process(target=dict_behaviours[func_id])
        current_process.daemon = True
        current_process.start()
        global process_pid
        process_pid = current_process.pid

        return 'running ' + func_id + ' on ' + str(current_process.pid), 200


@api.route('/off', methods=['GET'])
def off():
    stop_process()
    turn_off()
    return 'turned off', 200


def stop_process():
    global current_process
    global process_pid
    if current_process is not None:
        api.logger.warn("killing process " + str(current_process.pid))
        os.kill(process_pid, signal.SIGKILL)
        current_process.join(2)
        if current_process.is_alive():
            os.kill(process_pid, signal.SIGKILL)
            current_process.join(2)
        current_process = None
        process_pid = None

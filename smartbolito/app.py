from flask import Flask, render_template, request


api = Flask(__name__)


@api.route('/', methods=['GET'])
def main():
    print("aja")
    return render_template('home.html', functions=[])


@api.route('/run', methods=['GET'])
def run():
    func_id = request.args.get('func')
    if not func_id:
        return 'Empty func parameter', 400

    try:
        func = getattr(None, func_id)
        # stop previous function and run the actual in a thread
    except AttributeError:
        return 'Function does not exists', 404

    return 'running ' + func_id, 200

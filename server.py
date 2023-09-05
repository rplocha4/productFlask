import json

from flask import Flask, request, send_file

app = Flask(__name__)
ALLOWED_EXTENSIONS = {"json"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def valid_num(num):
    return type(num) == int and num > 0


@app.route("/product", methods=["POST"])
def add():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        data = json.load(file)
        token, first_num, second_num = data["token"], data["a"], data["b"]

        if not valid_num(first_num) or not valid_num(second_num):
            return "Bad Request", 400

        result = {"token": token, "product": data["a"] * data["b"]}
        with open("result.json", "w") as result_file:
            result_file.write(json.dumps(result))
        return send_file("result.json")
    else:
        return "Bad Request", 400


@app.errorhandler(405)
def method_not_allowed(e):
    return "Method not allowed", 405


if __name__ == "__main__":
    app.run(port=6060)

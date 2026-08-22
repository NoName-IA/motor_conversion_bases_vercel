from flask import Flask, request, jsonify

from converter import validar_y_convertir, alu_operation

app = Flask(__name__)

BASES = {"BIN": 2, "OCT": 8, "DEC": 10, "HEX": 16}


@app.route("/api/convert", methods=["POST"])
def convert():
    data = request.get_json(force=True)

    numero = data.get("numero", "")
    base_origen = data.get("base_origen")
    word_size = data.get("word_size")

    try:
        base = BASES[base_origen]
        word_size = int(word_size)
        resultado = validar_y_convertir(numero, base, word_size)
        return jsonify({"ok": True, "resultado": resultado})
    except (ValueError, OverflowError, KeyError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/alu", methods=["POST"])
def alu():
    data = request.get_json(force=True)

    bin1 = data.get("bin1", "")
    bin2 = data.get("bin2", "")
    operacion = data.get("operacion", "")
    word_size = data.get("word_size")

    try:
        word_size = int(word_size)
        resultado = alu_operation(bin1, bin2, operacion, word_size)
        return jsonify({"ok": True, "resultado": resultado})
    except (ValueError, OverflowError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400

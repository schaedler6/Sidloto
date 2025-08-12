import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from strategies.factory import StrategyFactory
from utils.filters import passes_parity, passes_sum, passes_repeat
from utils.optimizer import generate_batch

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, "config", ".env")
if os.path.exists(ENV_PATH): load_dotenv(ENV_PATH)

app = Flask(__name__,
    static_folder=os.path.join(PROJECT_ROOT, "frontend"),
    static_url_path=""
)
CORS(app, resources={r"/*": {"origins": os.getenv("CORS_ORIGINS","*")}})

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/status")
def status():
    return jsonify(ok=True, app="Sidloto2025", version="1.0")

@app.route("/api/strategies")
def strategies():
    return jsonify([
        {"id":"normal","name":"Normal","desc":"Sorteio balanceado"},
        {"id":"acima5","name":"Acima de 5","desc":"Favorece dezenas > 5"},
        {"id":"atraso_freq","name":"Atraso/Frequência 3–4+","desc":"Mock inicial"}
    ])

def _parse_int(x):
    try: return int(x)
    except: return None

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True) or {}
    strat_name = data.get("strategy","normal")
    qty = max(1, min(100, int(data.get("quantity", 1))))
    target_even = _parse_int(data.get("even"))
    min_sum     = _parse_int(data.get("min_sum"))
    max_sum     = _parse_int(data.get("max_sum"))
    ref         = data.get("reference") or []
    min_rep     = _parse_int(data.get("min_repeat"))
    max_rep     = _parse_int(data.get("max_repeat"))

    factory = StrategyFactory()
    strat = factory.get(strat_name)

    results = []
    ATTEMPT_CAP = 2000
    while len(results) < qty:
        tries = 0; ok = None
        while tries < ATTEMPT_CAP:
            cand = sorted(strat.generate_one())
            if not passes_parity(cand, target_even): tries += 1; continue
            if not passes_sum(cand, min_sum, max_sum): tries += 1; continue
            if not passes_repeat(cand, ref, min_rep, max_rep): tries += 1; continue
            ok = cand; break
        results.append(ok if ok else cand)

    return jsonify({
        "strategy": strat_name,
        "quantity": qty,
        "filters": {
            "even": target_even, "min_sum": min_sum, "max_sum": max_sum,
            "min_repeat": min_rep, "max_repeat": max_rep
        },
        "games": results
    })

@app.route("/api/generate_optimized", methods=["POST"])
def generate_optimized():
    data = request.get_json(force=True) or {}
    qty           = int(data.get("quantity", 10))
    last_result   = data.get("last_result", [])
    hot           = set(data.get("hot", []))
    cold          = set(data.get("cold", []))
    repeat_target = int(data.get("repeat_target", 9))
    even_target   = data.get("even_target", None)
    even_target   = int(even_target) if even_target is not None else None
    min_sum       = data.get("min_sum", None)
    max_sum       = data.get("max_sum", None)
    min_sum       = int(min_sum) if min_sum is not None else None
    max_sum       = int(max_sum) if max_sum is not None else None
    avoid         = set(data.get("avoid", []))
    must          = set(data.get("must", []))
    seed          = data.get("seed", None)

    games = generate_batch(
        quantity=qty,
        last_result=last_result,
        hot=hot, cold=cold,
        repeat_target=repeat_target,
        even_target=even_target,
        min_sum=min_sum, max_sum=max_sum,
        avoid=avoid, must=must,
        seed=seed
    )

    return jsonify({
        "quantity": qty,
        "games": games,
        "constraints": {
            "repeat_target": repeat_target,
            "even_target": even_target,
            "sum_range": [min_sum, max_sum],
            "hot": sorted(list(hot)),
            "cold": sorted(list(cold)),
            "avoid": sorted(list(avoid)),
            "must": sorted(list(must))
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT","5000")))

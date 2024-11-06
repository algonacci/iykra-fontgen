import os
from flask import Flask, Request, jsonify

from app.services.ingest_google_font import ingest_google_font
from app.services.transform_font import transform_google_fonts

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(
        {
            "status": {"code": 200, "message": "Success fetching the ETL API"},
            "data": None,
        }
    ), 200


@app.route("/ingest_google_fonts")
def ingest_google_fonts(request: Request):
    repo_dir = "./repo"
    tff_dir = "./tff"

    input_data = request.get_json()
    bucket_name = input_data["bucket_name"]
    prefix = input_data["prefix"]

    ingest_google_font(repo_dir, tff_dir, bucket_name, prefix)

    return jsonify(
        {
            "status": {"code": 200, "message": "Success doing data ingestion"},
            "data": None,
        }
    ), 200


@app.route("/transform_google_fonts")
def transform_google_fonts_service(request: Request):
    input_data = request.get_json()
    bucket_name = (input_data["bucket_name"],)
    raw_prefix = (input_data["raw_prefix"],)
    cleaned_prefix = (input_data["cleaned_prefix"],)
    font_dir = ("./fonts",)
    dataset_dir = "./datasets"
    transform_google_fonts(
        bucket_name,
        raw_prefix,
        cleaned_prefix,
        font_dir,
        dataset_dir,
    )

    return jsonify(
        {
            "status": {"code": 200, "message": "Success doing data transformation"},
            "data": None,
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

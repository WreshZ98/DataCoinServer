from flask import Flask, request, jsonify, send_file
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from supabase import create_client, Client
from typing import cast
import os
import numpy as np
import pandas as pd
from werkzeug.security import check_password_hash
np.random.seed(42)

random_matrix = np.random.rand(5, 3)

df = pd.DataFrame(random_matrix)

app = Flask(__name__)

url = os.environ.get("SUPABASE_URL")
url = cast(str, url)
key = os.environ.get("SUPABASE_KEY")
key = cast(str,key)
supabase: Client = create_client(url, key )

response = supabase.table('Users').select("*").execute()


@app.route('/login', methods=['GET'])
def get_data():
    # Get the integer parameter from the query string
    id = request.args.get('id', type=int)
    password = request.args.get('password', type=str)
    action = request.args.get('action', type=str)
    if id is not None and password is not None:
        response = supabase.table('Users').select('*').eq('id', id).execute()
        if response.data == []:
            return jsonify({'message': 'User ID not found'}), 404
        user = response.data[0]
        stored_password_hash = user['password']
        if password == str(stored_password_hash):
            if action is None:
                return jsonify({'message': 'Credentials are correct'}), 200
            else:
                if action == "GET_TASK":
                    df.to_csv("data.csv")
                    return send_file("data.csv", as_attachment=True, download_name="data.csv")
                else:
                    return jsonify({'message': 'Not an action'}), 400
        else:
            return jsonify({'message': 'Incorrect password'}), 401

    else:
        return jsonify({"error": "No credentials given."}), 400

@app.route('/upload', methods=['POST'])
def handle_file():
    print("file" in request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    print(file)
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = 'data.csv'
        file.save(filename)

    return jsonify({"error": "No selected file"}), 400
if __name__ == '__main__':
    app.run(debug=True)

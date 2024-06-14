from flask import Flask, request, jsonify, send_file
from supabase import create_client, Client
from typing import cast
import os
import numpy as np
import pandas as pd

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
    password = request.args.get('password', type=int)
    action = request.args.get('action', type=str)
    if id is not None and password is not None:
        response = supabase.table('Users').select("id, password").eq("id", id).execute()
        print(type(response.data))
        if password == response.data[0].get("password"):
            print("cascanueces")
            if action is not None and action != "NONE":
                print("doble cascanueces")
                if action == "GET_TASK":
                    df.to_csv("data.csv")
                    return send_file("data.csv", mimetype='text/csv', as_attachment=True, download_name='data.csv')
        return jsonify({"received_number": response.data[0]})
    else:
        return jsonify({"error": "No number provided"}), 400

@app.route("/")
def hello_world():
    return f'{response}\'s profile'

if __name__ == '__main__':
    print(response)
    app.run(debug=True)

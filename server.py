from flask import Flask, send_file, abort
import os
from supabase import create_client, Client
from typing import cast
app = Flask(__name__)

# Example mapping of keys to filenames
key_to_filename = {
    '01': 'file1.txt',
    '02': 'file2.txt',
}

url = os.environ.get("SUPABASE_URL")
url = cast(str, url)
key = os.environ.get("SUPABASE_KEY")
key = cast(str,key)
supabase: Client = create_client(url, key )

response = supabase.table('Users').select("*").execute()

@app.route('/getfile/<key>')
def get_file(key):
    filename = key_to_filename.get(key)
    if filename:
        path = "/workspaces/DataCoinServer/"+filename
        print(path)
        return send_file(filename, as_attachment = True)
        #return send_from_directory(directory='/', filename=filename)
    else:
        abort(404, description="Key not found")


@app.route("/")
def hello_world():
    return f'{response}\'s profile'
from markupsafe import escape

if __name__ == '__main__':
    print(response)
    app.run(debug=True)

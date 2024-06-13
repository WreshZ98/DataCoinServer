from flask import Flask, send_file, abort

app = Flask(__name__)

# Example mapping of keys to filenames
key_to_filename = {
    '01': 'file1.txt',
    '02': 'file2.txt',
}

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

if __name__ == '__main__':
    app.run(debug=True)
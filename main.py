from flask import Flask,current_app
app = Flask(__name__,static_url_path="/web")

@app.route("/")
def hello():
        return "xd"
if __name__ == '__main__':
    port = int(os.environ,get("PORT",5000))
    app.run(debug=True,port=port)

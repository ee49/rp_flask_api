from flask import render_template
import connexion

app = connexion.App(__name__, specification_dir="/Users/learn/pylearn/rp_flask_api/")
app.add_api("/Users/learn/pylearn/rp_flask_api/swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)


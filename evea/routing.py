from flask import render_template
from evea import app
from evea.routes.home import home  #ok
from evea.routes.sample import sample  #ok
from evea.routes.mirna import mirna  #ok
from evea.routes.stat import stat #ok
from evea.routes.target import target #ok
from evea.routes.search import search #ok
from evea.routes.drug import drug #ok

# routing
app.register_blueprint(home, url_prefix='/api/home')
app.register_blueprint(sample, url_prefix='/api/sample')
app.register_blueprint(mirna, url_prefix='/api/mirna')
app.register_blueprint(drug, url_prefix='/api/drug')
app.register_blueprint(stat, url_prefix='/api/stat')
app.register_blueprint(target, url_prefix='/api/target')



app.register_blueprint(search, url_prefix='/api/search')

# from evea.routes.sample import sample
# from evea.routes.home import home
# from evea.routes.mirna import mirna
# routing #
# app.register_blueprint(sample, url_prefix='/api/sample')
# app.register_blueprint(home, url_prefix='/api/home')
# app.register_blueprint(mirna, url_prefix='/api/mirna')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

from flask import Blueprint, render_template, url_for

index_blueprint = Blueprint('home', __name__, template_folder='templates')

@index_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

from flask import current_app, Blueprint


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Oláaaa'
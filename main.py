from website import create_app
from flask import render_template
from flask_login import current_user

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# obsluga bledu 404, czyli np kiedy uzytkownik chce sobie wpisac /rokoko
# to musi byc tu bo to jest po stronie przegladarki, inaczej nie dziala
@app.errorhandler(404)
def PageNotFound(error):
    return render_template('404.html', user=current_user)
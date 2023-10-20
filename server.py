from flask_app import app
from flask import render_template
#For every controller file, add below 
from flask_app.controllers import users_controller, routes, decks_controller, cards_controller #TODO replace with controller name

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)  
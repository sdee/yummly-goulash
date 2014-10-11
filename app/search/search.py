from flask import render_template, request, redirect, url_for
from wtforms import Form, TextField
from app.search.api import YummlyClient
from flask_bootstrap import Bootstrap
from flask import Flask

app = Flask(__name__)
Bootstrap(app)
app.config['DEBUG'] = True
app.config.from_envvar('GOULASH_SETTINGS')

class RecipeSearchForm(Form):
	recipe = TextField('Recipe')

@app.route('/search', methods=['GET', 'POST'])
def search():
	form = RecipeSearchForm(request.form)
	if request.method == 'POST':
		yc = YummlyClient(app.config['API_ID'], app.config['API_KEY'])
		result = yc.find_consensus(form.recipe.data)
		message = str(', '.join(result))
		return redirect(url_for('results', message=message))
	return render_template('search/search.html', form=form)

#canned search
# @app.route('/search/', methods=['GET', 'POST'])

@app.route('/results')
def results():
	message = request.args['message']
	return render_template('search/results.html', message=message)

if __name__ == "__main__":
    app.run()

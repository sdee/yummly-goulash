from flask import render_template, request, redirect, url_for
from wtforms import Form, TextField
from app.search.api import YummlyClient
from app.search.api import SearchResults
from flask_bootstrap import Bootstrap
from flask import Flask
import random

app = Flask(__name__)
Bootstrap(app)
app.config['DEBUG'] = True
app.config.from_envvar('GOULASH_SETTINGS')

class RecipeSearchForm(Form):
	recipe = TextField('Recipe')

@app.route('/search/<dish>')
def search_by_dish(dish):
	yc = YummlyClient(app.config['API_ID'], app.config['API_KEY'])
	core_ingreds, matches = yc.find_consensus(dish)
	message = str(', '.join(core_ingreds))
	photos = random.sample(matches.photos, 9)
	return redirect(url_for('results', message=message, num_matches=matches.num_matches, title=dish))

@app.route('/search', methods=['GET', 'POST'])
def search():
	form = RecipeSearchForm(request.form)
	if request.method == 'POST':
		dish = form.recipe.data
		return redirect(url_for('search_by_dish', dish=dish))
	examples = [('goulash', url_for('search_by_dish', dish='goulash')),
							('beef stroganoff', url_for('search_by_dish', dish='beef stroganoff')),
							('caprese salad', url_for('search_by_dish', dish='caprese salad')),
							('biscuits and gravy', url_for('search_by_dish', dish='biscuits and gravy')),
							('peach cobbler', url_for('search_by_dish', dish='peach cobbler'))]
	return render_template('search/search.html', form=form, examples=examples)

@app.route('/results')
def results():
	message = request.args['message']
	num_matches = request.args['num_matches']
	title = request.args['title']
	return render_template('search/results.html', message=message, title=title, num_matches=num_matches)

if __name__ == "__main__":
    app.run()

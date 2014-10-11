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

@app.route('/search/<dish>')
def canned_search(dish):
	yc = YummlyClient(app.config['API_ID'], app.config['API_KEY'])
	result, num_matches = yc.find_consensus(dish)
	message = str(', '.join(result))
	title = dish
	return redirect(url_for('results', message=message, num_matches=num_matches, title=title))

@app.route('/search', methods=['GET', 'POST'])
def search():
	form = RecipeSearchForm(request.form)
	if request.method == 'POST':
		yc = YummlyClient(app.config['API_ID'], app.config['API_KEY'])
		query = form.recipe.data
		result, num_matches= yc.find_consensus(query)
		num_matches = num_matches
		message = str(', '.join(result))
		return redirect(url_for('results', message=message, title=query, num_matches=num_matches))
	examples = [('goulash', url_for('canned_search', dish='goulash')),
							('beef stroganoff', url_for('canned_search', dish='beef stroganoff')),
							('caprese salad', url_for('canned_search', dish='caprese salad')),
							('biscuits and gravy', url_for('canned_search', dish='biscuits and gravy'))]
	return render_template('search/search.html', form=form, examples=examples)

@app.route('/results')
def results():
	message = request.args['message']
	num_matches = request.args['num_matches']
	title = request.args['title']
	return render_template('search/results.html', message=message, title=title, num_matches=num_matches)

if __name__ == "__main__":
    app.run()

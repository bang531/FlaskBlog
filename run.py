from flaskblog import create_app

app=create_app()

# for use in running from python
if __name__ == '__main__':
	app.run(debug=True)
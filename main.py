import connexion

app = connexion.FlaskApp(__name__, specification_dir='.')
app.add_api('spec.swagger.yaml')
app.run(port=8080)

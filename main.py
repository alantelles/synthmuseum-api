from flask import Flask
import services

app = Flask(__name__)

@app.route('/companies', methods=['GET'])
def get_companies():
    return services.get_company_list()

@app.route('/companies/<company>', methods=['GET'])
def get_company(company):
    return services.get_company(company)

@app.route('/companies/<company>/synths', methods=['GET'])
def get_company_synths(company):
    return services.get_company_synths(company)

app.run(debug=True)
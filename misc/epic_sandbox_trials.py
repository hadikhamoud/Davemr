import requests
#EPIC SANDBOX ACCESS

def getAccess():
    clientId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    redirecturi = "http://localhost:3000"
    pemfile = open('privatekey.pem', 'rb')
    privatekey = pemfile.read()
    header = {
        "alg": "RS384",
        "typ": "JWT"
    }
    payload = {
        "sub": clientId,
        "aud": "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token",
        "jti":  "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "exp": time.time() + 80,
        "iss": clientId,
    }
    Token = jwt.JWT(header=header,
                    claims=payload)
    key = jwk.JWK.from_pem(privatekey, password=None)
    Token.make_signed_token(key)
    SignedToken = Token.serialize()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    fulldata = {'grant_type': 'client_credentials',
                'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
                'client_assertion': SignedToken}
    url = 'https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token'
    response1 = requests.post(url, data=fulldata, headers=headers)
    r1dict = json.loads(response1.text)
    accesstoken = r1dict['access_token']
    authorize = "Bearer " + accesstoken
    return authorize


def requestNote(authorize):
    patient = 'ejJD-7U3OqOcsHTnJnjMrDw3'
    authorizelink = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Binary/" + patient
    headersAccess = {'Authorization': authorize}
    response = requests.get(authorizelink, headers=headersAccess)
    return response.text


@app.route('/getnoteepic', methods=['GET'])
def getnoteepic():
    authorize = getAccess()
    fetchedNote = requestNote(authorize)
    return jsonify({
        "text": fetchedNote
    })


import os
import sys
import uuid
import requests

from flask import make_response, redirect, Flask, request

app = Flask(__name__)

redirect_uri = "http://localhost:8000/auth/"
client_id = os.getenv("GH_CLIENT_ID", "")
if client_id == "":
    print("Cannot get Github ClientID!")
    sys.exit(1)

client_secret = os.getenv("GH_CLIENT_SECRET", "")
if client_secret == "":
    print("Cannot get GitHub Client Secret!")
    sys.exit(2)

state_auth = str(uuid.uuid4()).upper()


@app.route("/login")
def login_with_github():
    """
    Redirection to GitHub OAuth endpoint to authorize the application and start log-in web-flow.
    """
    global client_id, client_secret, redirect_uri, state_auth
    resp = make_response(
        redirect(
            f"https://github.com/login/oauth/authorize?redirect_uri={redirect_uri}&client_id={client_id}&scope=user&state={state_auth}"
        )
    )
    resp.headers["Accept"] = "application/json"
    return resp


@app.route("/auth/")
def authenticated_redirect_target():
    """
    Handle the GitHub web-flow.
    """
    # When code is received, exchange it to an access_token
    global client_id, client_secret, redirect_uri, state_auth
    if (
        isinstance(request.args["code"], str)
        and isinstance(request.args["state"], str)
        and request.args["state"] == state_auth
    ):
        try:
            resp = requests.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "code": str(request.args["code"]),
                    "redirect_uri": "http://localhost:8000/auth",
                },
                headers={"Accept": "application/json"},
                timeout=10,
            )
        except Exception as e:
            return str(e)
        try:
            # Get the user info with the retrieved access_token
            userinfo = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": "token {}".format(resp.json()["access_token"]),
                    "Accept": "application/json",
                },
                timeout=10,
            )
        except Exception as e:
            return str(e)
        return (
            "Welcome " + str(userinfo.json()["name"]) + "!"
        )  # Could be a redirect to the main application page
    return "Login failed!"


if __name__ == "__main__":
    app.run(port=8000)

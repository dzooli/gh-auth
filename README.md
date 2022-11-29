# Description

Example for 'Authentication with Github as identity provider' using Flask framework.

# Installation

- Create a virtualenv
- Activate the virtualenv
- ```bash
  pip install -r requirements.txt
  ```

# Usage

- Create your OAuth application on your github account in [Github Settings](https://github.com/settings/developers)
- ```bash
  export GH_CLIENT_ID=<App client ID>
  export GH_CLIENT_SECRET=<App client secret>
  cd src
  python main.py
  ```
- Go to [the application](http://127.0.0.1:8000/login) login page.

# License

MIT

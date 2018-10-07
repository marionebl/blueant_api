> 🚧 This is an unlicensed Work in Progress

> A partial REST proxy for SOAP services provided by [Proventis Blue Ant](https://www.proventis.net/en/).

# blueant_api

> `blueant_api` is not affiliated with or sanctioned by Proventis in any way

* 🌍 **Web friendly** - Uses JSON and JWT to be easily consumable from web based clients
* 🎈 **Shallow abstraction** - Exposes the same unfiltered datasets as the underlying Blue Ant instance
* 👨‍🎓 **Discoverable** - All resources are easily discoverable and testable via Swagger UI API docs

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/active
pip install --upgrade pip==18.0 pipenv
pipenv sync
pipenv shell

# Configure the proxy to point at your blueant instance
echo "API_URL=\"https://[blueant-host]/blueant/services/\"" > config.py

# Start development server at http://localhost:5000
# API docs available at http://localhost:5000/apidocs
./run.sh 
```

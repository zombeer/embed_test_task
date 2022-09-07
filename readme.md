## embed_xyz
### Technical details.

Task implemented using `fastapi` server + `peewee` ORM.
First one is quite beautiful, the second one is beautiful as well. The only drawdown of this ORM is that it's a sync one.
Nevertheless I suppose it will be more than enough to satisfy task requirements.

Tests implemented with `pytest`.
Small hack has been used to avoid writing multiple levels of fixtures, since app isn't dependent on database object directly.
Therefore you need to set a DB_URI env pointing to test database. Added foolproofing to tests to avoid modifying production database.

### Running.
* Create a virtual environment. (App was crated in Python 3.10.4)
* Run `pip install -r requirements.txt` on order to install dependencies.
* Use command `make test` to run tests.
* Use `make run` to run server locally, usually as port 8000.

### docker/k8s
Repo contains everything needed to run it in _docker/k8s_.
* `docker-compose up` runs dockerized application built from local source. Database used is Sqlite3 mounted at ./database repo folder. You can check it during process if needed.
* Also repo contains k8s manifest: `kubectl apply -f manifest.yml`. You can use it in any environment, DB_URI is stored in _k8s secret_, it's pointing to my own Postgres server.
In task mentioned most secure way to run app. It's obviously not the case. It I was focused on security I would run DB in isolated k8s subnetwork, unreachable from outside.

### Challenging parts
The task was quite interesting. Tough points was:
* Testing. Namely implementing fixtures for endpoint testing. Ended up with setting test database externally. Because it was too much to write multi-level fixtures for endpoints. Models testing weren't complicated though.
* Custom sorting - ended up with a raw SQL, it's a bit tough to transcribe complex SQL with joins and unions into ORM syntax.
* Writing docstrings (: I hope you'll like it. Wording is quite challenging task sometimes as well.

### Extra info.
Currenly instance of this API is running at my node.
You can reach it by address http://51.15.60.207:31600/docs (Yep, I don't have a domain name, and don't really want to set up an ingress in fact (: )
Hopefully, you'll like the result.

Kind regards,
Mikhail.
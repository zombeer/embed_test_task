run:
	cd src && uvicorn server:app
test:
	cd src && pytest -v
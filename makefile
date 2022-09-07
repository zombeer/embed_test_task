test_db := ../database/embed_api_test.db
run:
	cd src && uvicorn server:app
test:
	# Pointing to custom test Database and tearing it down afterwards
	cd src && \
	DB_URI=sqlite:///$(test_db) pytest -v -s; \
	rm $(test_db)
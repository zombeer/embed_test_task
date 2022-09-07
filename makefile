test_db := ../database/embed_api_test.db
run:
	cd src && uvicorn server:app

test:
ifneq (,$(findstring test, $(test_db)))
	echo "All fine! Running tests against test database."
else
	echo "Wrong DB filename. Should contain 'test' substring in it. Exiting."
	exit 1
endif

# Pointing to custom test Database and tearing it down afterwards
	cd src && \
	DB_URI=sqlite:///$(test_db) pytest -v -s; \
	rm $(test_db)
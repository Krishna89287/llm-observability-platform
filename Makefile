.PHONY: install run test
install:
	pip install -r requirements.txt
run:
	uvicorn app.main:app --reload --port 8070
test:
	pytest -q

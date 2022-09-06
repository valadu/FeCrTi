PYTHON = python

.PHONY: main

main:
	$(PYTHON) -m streamlit run app/main.py

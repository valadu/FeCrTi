PYTHON = python

.PHONY: main

main:
	$(PYTHON) -m streamlit run $@.py

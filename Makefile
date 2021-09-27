lint:
	@python3 scripts/lint.py

test_all:
	@python3 -m unittest discover -s tests -t . -v

# test: file
# 	@python3 scripts/lint.py


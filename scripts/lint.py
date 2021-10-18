from pylint import epylint as lint

lint.py_run(
    "src --rcfile pylintrc",
)

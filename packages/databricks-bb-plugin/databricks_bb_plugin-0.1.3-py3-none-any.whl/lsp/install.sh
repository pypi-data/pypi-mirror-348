# wheel packages don't have post install hooks, so need to do this at install time
chmod 777 .venv/lib/python*/site-packages/databricks/labs/remorph/bladerunner/Converter/bin/MacOS/dbxconv
chmod 777 .venv/lib/python*/site-packages/databricks/labs/remorph/bladerunner/Converter/bin/Linux/dbxconv

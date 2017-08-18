if [[ -z "${PA_BUILD}" ]]; then
  RUN_ENV="DEV"
else
  RUN_ENV="${DEPLOY_ENV}"
fi

if [ RUN_ENV="DEV" ]; then
	echo 'Running Standalone'
	python run.py
else
	echo 'Running with Gunicorn'
	gunicorn -w 4 -b 127.0.0.1:5000 app:app
fi

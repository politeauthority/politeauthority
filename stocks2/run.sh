if [ "${PA_BUILD}" == "LIVE" ]; then
  RUN_ENV="LIVE"
else
  RUN_ENV="${PA_BUILD}"
fi

if [ RUN_ENV="DEV" ]; then
	echo 'Running Standalone'
	python run.py
else
	echo 'Running with Gunicorn'
	gunicorn -w 4 -b -D 127.0.0.1:5000 app:app
fi
echo 'Stopped'

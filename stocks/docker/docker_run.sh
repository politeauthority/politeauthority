docker run \
    -v /Users/alix/repos/politeauthority:/opt/politeauthority \
    -e PA_MYSQL_HOST="138.197.194.190" \
    -e PA_MYSQL_USER="devel" \
    -e PA_MYSQL_PASS="78VWc_bKTAap" \
    -e PA_STOCKS_CONFIG='/opt/politeauthority/stocks/flask/configs/config_dev.py' \
    politestocks

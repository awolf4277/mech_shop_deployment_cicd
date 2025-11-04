param([int]$Port = 5000)
$env:FLASK_RUN_PORT = $Port
flask run --host 0.0.0.0 --port $Port

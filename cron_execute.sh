
cd /home/ubuntu/flatfooted/
python3 main.py |& tee "log_$(date +\%Y-\%m-\%d).txt"

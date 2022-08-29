export AWS_ACCESS_KEY_ID=ASIAQ5UOUOL76VIOIA7H
export AWS_SECRET_ACCESS_KEY=f6HxYvBTNhnO/zEKtP/rfT8KdMSRO9U70Js2rIAq
export AWS_SESSION_TOKEN=FwoGZXIvYXdzEGQaDAo09B8ITe22awbiHSKsAdDRMzfvT3kuR3KUxgEHZnbsGraqOZKXNY55Q4H9aOKwBjE90AZykDIHpotgUaQ+gVeyh5F0RqoVUHRQYPHCST53u1lkBLrQNT1BXvL64ZPwUsTwJ26qbyKZlDVleIGIKJdFuIW+WKbO97SLYkrvPskTs1RQFmtHVjOHLmJUbXjc584kRJw2tUO1lTPUys6mh8aURYW+Npvieh/LJNU1RiH2CNB9ox597knGQU0oqfSthQYyLR/LUI06L8+K6LzpM/9xU+Vxws+AUFcONkX4z7cW0p6Tsua+chtCKi/RKLUiCw==
sudo apt-get update
sudo apt-get install awscli
sudo apt-get install tmux
sudo apt-get install unzip
sudo apt install python3-pip
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate
pip install "dask[complete]" --no-cache-dir
pip install "dask-ml[complete]" --no-cache-dir
pip install s3fs
pip install pyarrow
pip install pandas


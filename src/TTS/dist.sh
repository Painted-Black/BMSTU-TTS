sudo apt install python3-pip

sudo apt-get install -y libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev libzstd-dev liblz4-dev
git clone https://github.com/facebook/rocksdb.git
cd rocksdb/
make all

sudo pip3 install -r requirements.txt

# Shannon Home
Shannon Home Automation based on Raspberry pi and Arduino

## Installation
1. make root directory
```bash
sudo mkdir /system
```
2. clone from source
```bash
git clone https://github.com/kkiani/ShannonHome.git
```
3. execute shannon
```bash
cd ShannonHome
sudo chmod +x shannon
./shannon
```
## Setup RabbitMQ Server
installing RabbitMQ
```bash
sudo apt-get install rabbitmq-server
```
adding user for external services
```bash
$ rabbitmqctl add_user YOUR_USERNAME YOUR_PASSWORD
$ rabbitmqctl set_user_tags YOUR_USERNAME administrator
$ rabbitmqctl set_permissions -p / YOUR_USERNAME ".*" ".*" ".*"
```
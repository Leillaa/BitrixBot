import subprocess
import paramiko
from getpass import getpass

docker_hub_username = "leila1313"
docker_hub_password = "13082003Lt"


def deploy(log_serv):
    image_name = f"bot_{log_serv}"
    subprocess.run(["docker", "login", "-u", docker_hub_username, "-p", docker_hub_password])
    subprocess.run(["docker", "build", "-t", f"{docker_hub_username}/{image_name}", "."])
    subprocess.run(["docker", "push", f"{docker_hub_username}/{image_name}"])
    return image_name


# Функция для подключения к серверу через SSH
def ssh_connect(host, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    return ssh


# Функция для загрузки Docker образа с Docker Hub
def pull_docker_image(ssh, image_name):
    stdin, stdout, stderr = ssh.exec_command(f'docker pull {image_name}')
    for line in stdout:
        print(line.strip('\n'))


# Функция для запуска Docker контейнера
def run_docker_container(ssh, container_name, image_name, compose_file):
    stdin, stdout, stderr = ssh.exec_command(f'docker-compose -f {compose_file} up -d')
    for line in stdout:
        print(line.strip('\n'))


# Функция для загрузки и запуска Telegram бота
def deploy_telegram_bot(host, username, password, image_name, compose_file):
    ssh = ssh_connect(host, username, password)
    pull_docker_image(ssh, image_name)
    run_docker_container(ssh, image_name, image_name, compose_file)
    ssh.close()


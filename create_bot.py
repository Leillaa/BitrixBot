import shutil
import os
from deploy import deploy, ssh_connect, pull_docker_image, run_docker_container, deploy_telegram_bot


def create_bot(token, url, log_bit, pass_bit, host_serv, log_serv, pass_serv, log_db, pass_db):
    shutil.copytree('bot_copy', f'bot_{log_serv}')
    env_file_path = os.path.join(f'bot_{url}', '.env')
    env_content = f'BOT_TOKEN="{token}"\n' \
                  f'URL="{url}"\n' \
                  f'LOGIN_BITRIX="{log_bit}"\n' \
                  f'PASSWORD_BITRIX="{pass_bit}"\n' \
                  f'HOST_SERVER={host_serv}\n' \
                  f'LOGIN_SERVER="{log_serv}"\n' \
                  f'PASSWORD_SERVER="{pass_serv}"\n' \
                  f'LOGIN_DB="{log_db}"\n' \
                  f'PASSWORD_DB="{pass_db}"'
    with open(env_file_path, 'w') as env_file:
        env_file.write(env_content)
    docker_path = os.path.join(f'bot_{log_serv}', 'docker-compose.yml')
    docker_context = "version: '3.8'\n" \
                     "services:\n" \
                     "  bot:\n" \
                     "    build:\n" \
                     f"      context: ./\n" \
                     f"      dockerfile: Dockerfile\n"
    with open(docker_path, 'w') as docker_file:
        docker_file.write(docker_context)
    image_name = deploy(log_serv)
    print(f"бот создан. Image name: {image_name}")
    #ssh = ssh_connect(host_serv, log_serv, pass_serv)
    #pull_docker_image(ssh, image_name)
    #run_docker_container(ssh, "container", image_name, docker_path)
    #deploy_telegram_bot(host_serv, log_serv, pass_serv, image_name, docker_path)
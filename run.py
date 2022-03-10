import logging
import os
import shlex
import subprocess
import time

import requests
import urllib3

urllib3.disable_warnings()


def main():
    root = os.environ.get('APP_ROOT', "/var/run")
    host = os.environ.get('GITLAB_HOST', "https://gitlab.com")
    token = os.environ.get('GITLAB_TOKEN')
    group = os.environ.get('GROUP_ID', 1)
    total_pages = 1
    page = 0
    while page < total_pages:
        page += 1
        response = requests.get(
            f"{host}/api/v4/groups/{group}/projects?private_token={token}&include_subgroups=True&per_page=100&page={page}&with_shared=False",
            verify=False)
        for project in response.json():
            path = os.path.join(root, project['path_with_namespace'])
            ssh_url_to_repo = project['ssh_url_to_repo']
            try:
                if project['mirror'] is True:
                    print("Skipping mirrored!")
                elif not os.path.exists(path):
                    command = shlex.split(f"git clone {ssh_url_to_repo} {path}")
                    subprocess.Popen(command)
                    time.sleep(1)
                else:
                    logging.info(f"{path} already exists")
                    os.chdir(path)
                    command = shlex.split(f"git pull")
                    subprocess.Popen(command)
                    os.chdir(root)
                    time.sleep(1)

            except Exception as e:
                logging.error(f"Error on {ssh_url_to_repo}: {e}")

        print("Keeping it alive for a minute to properly sync all repos on your volume...", flush=True)

        total_pages = int(response.headers['X-Total-Pages'])


if __name__ == '__main__':
    main()
    time.sleep(30)
    print('All done!')

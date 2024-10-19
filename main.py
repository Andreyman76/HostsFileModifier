import datetime
import shutil
import os.path
import ctypes

hosts_file = r'C:\Windows\System32\drivers\etc\hosts'
loopback = '127.0.0.1'
create_backup = False

def main():
    if is_run_as_admin() == False:
        print("Please, run as admin")
        return

    user_input = input('Enter hostname or file with hostnames for block: ').replace('"', '')

    lines = create_lines_from_hostnames_file(user_input) \
        if os.path.isfile(user_input) \
        else create_lines_from_hostname(user_input)

    now = datetime.datetime.now()

    if create_backup:
        create_hosts_file_backup(hosts_file, now)

    add_comment_to_hosts_file(hosts_file, f'Updated {get_date_time_string(now)}:')
    add_lines_to_hosts_file(hosts_file, lines)
    return

def create_lines_from_hostname(hostname: str) -> list[str]:
    return [create_hosts_file_line(hostname)]

def create_lines_from_hostnames_file(hostnames_file: str) -> list[str]:
    with open(hostnames_file, 'r', encoding='utf-8') as file:
        hostnames = file.readlines()

    return [create_hosts_file_line(hostname) for hostname in hostnames]

def create_hosts_file_line(hostname: str) -> str:
    return f'{loopback} {hostname.strip()}'

def create_hosts_file_backup(hosts_file_name: str, now: datetime) -> None:
    backup_file = f'{hosts_file_name} backup {get_date_time_string(now)}'
    shutil.copyfile(hosts_file_name, backup_file)
    return

def get_date_time_string(date: datetime) -> str:
    return f'{date.day}-{date.month}-{date.year} {date.hour}.{date.minute}.{date.second}'

def add_lines_to_hosts_file(hosts_file_name: str, lines: list[str]) -> None:
    with open(hosts_file, 'a', encoding='utf-8') as file:
        for line in lines:
            file.write('\n' + line)
    return

def add_comment_to_hosts_file(hosts_file_name: str, comment: str) -> None:
    with open(hosts_file, 'a', encoding='utf-8') as file:
        file.write('\n# ' + comment)

    return

def is_run_as_admin() -> bool:
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin

if __name__ == '__main__':
    try:
        main()
    except Exception as exception:
        print(exception)
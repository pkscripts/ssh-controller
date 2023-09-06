import config
import paramiko
import sys


def connect_ssh(hostname):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the remote host
    try:
        ssh.connect(hostname, config.port, config.username, config.password)
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
        ssh.close()
        exit(1)
    except paramiko.SSHException as e:
        print("Unable to establish SSH connection:", str(e))
        ssh.close()
        exit(1)
    return ssh


def reboot(hostname):
    """
    Resets(removes) configuration file and reboots device
    :param hostname:
    :return:
    """
    ssh = connect_ssh(hostname)
    try:
        remote_file_path = '/run/readwrite/app.cfg'  # Velocity configuration
        reboot_cmd = '/sbin/reboot'  # Reboot command
        # Delete file
        ssh.exec_command(f'rm {remote_file_path}')
        print("Deleted config file")
        # Execute command
        ssh.exec_command(f'{reboot_cmd}')
        print("Reboot command issued")
    except Exception as e:
        print(f"Error: {str(e)}")
    ssh.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        host_address = sys.argv[1]
        print("Host address: {}".format(sys.argv[1]))
        reboot(host_address)
    else:
        print('No host address provided')

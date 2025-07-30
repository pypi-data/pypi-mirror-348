# tests/test_ssh_bruteforce.py

from shield.plugins import ssh_bruteforce

def test_ssh_bruteforce_detection_valid_case():
    line = "May  6 00:22:35 api-monitization sshd[34978]: Failed password for invalid user fakeuser from 127.0.0.1 port 51342 ssh2"
    assert ssh_bruteforce.detect(line) is True

def test_ssh_bruteforce_detection_ignore_case():
    line = "May  6 00:22:35 api-monitization sshd[34978]: Connection closed by 127.0.0.1 port 51342"
    assert ssh_bruteforce.detect(line) is False

# tests/test_sudo_abuse.py

from shield.plugins import sudo_abuse

def test_sudo_session_open_detected():
    line = "May  6 00:22:21 api-monitization sudo: pam_unix(sudo:session): session opened for user root(uid=0) by c80129b(uid=1000)"
    assert sudo_abuse.detect(line) is True

def test_unrelated_log_ignored():
    line = "Some random log line not related to sudo"
    assert sudo_abuse.detect(line) is False

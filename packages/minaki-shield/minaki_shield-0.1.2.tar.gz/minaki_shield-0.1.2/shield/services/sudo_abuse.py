def detect(line):
    suspicious_phrases = [
        "sudo: pam_unix",                          # general sudo session
        "sudo: no tty present",                   # privilege escalation script
        "user NOT in sudoers",                    # privilege escalation attempt
        "sudo: 3 incorrect password attempts",    # brute forcing sudo
        "sudo: authentication failure",           # only match sudo-related auth failures
    ]
    return any(phrase in line for phrase in suspicious_phrases)

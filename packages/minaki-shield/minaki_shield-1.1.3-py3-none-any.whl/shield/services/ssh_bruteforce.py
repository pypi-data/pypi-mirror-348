def detect(line):
    return (
        "sshd" in line and (
            "Failed password" in line or
            "Invalid user" in line or
            "Connection closed by authenticating user" in line
        )
    )

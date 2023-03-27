import datetime


class Logger:
    def __init__(self, filename):
        self.filename = filename

    def log(self, *args, name = None):
        with open(self.filename, "a") as f:
            # datetime name message
            # 2020-01-01 12:00:00 Login: Session ID: 1234567890
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{time} ### {name}: " + " ".join(args) + "\n")

import io
import os


def empty_archive():
    return io.StringIO("")

def archive_with_pedro_and_his_password():
    return io.StringIO("pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b:40\n")

class tempFile:
    def __init__(self,path,content):
        self.path = path
        self.file = open(path)
        self.file.seek(0,2)
        self.file.write(content)

    def read(self):
        pass
        #need to be finished

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        os.unlink(self.path)

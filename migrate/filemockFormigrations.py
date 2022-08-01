import io
import os


def empty_archive():
    return io.StringIO("")

def archive_with_pedro_and_his_password():
    return io.StringIO("pedro:eaf2c12742cb8c161bcbd84b032b9bb98999a23282542672ca01cc6edd268f7dce9987ad6b2bc79305634f89d90b90102bcd59a57e7135b8e3ceb93c0597117b:40\n")

class tempFile:
    def __init__(self,path,content):
        self.path = path
        self.file = open(path, "w+")
        self.file.seek(0,2)
        self.file.write(content)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.file.closed:
            self.file.close()
        os.unlink(self.path)

    def close(self):
        self.file.close()

    def fileno(self):
        return self.file.fileno()

    def flush(self):
        self.file.flush()

    def isatty(self):
        return self.file.isatty()

    def read(self,size=-1):
        return self.file.read(size)

    def readable(self):
        return self.file.readable()

    def readline(self, size=-1):
        return self.file.readline(size)

    def readlines(self, hint=-1):
        return self.file.readlines(hint)

    def seek(self, offset, whence=0):
        return self.file.seek(offset,whence)

    def seekable(self):
        return self.file.seekable()

    def tell(self):
        return self.file.tell()

    def truncate(self,size=None):
        return self.file.truncate(size)

    def writable(self):
        return self.file.writable()

    def write(self,text):
        self.file.write(text)

    def writelines(self,listOfTexts):
        self.file.writelines(listOfTexts)
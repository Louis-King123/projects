import ftplib
import os
import socket

HOST = '121.37.133.196'
USER = 'ftpuser'
PASSWD = 'centent123'


def FtpConnect(host, username, passwd):
    try:
        ftp = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror) as e:
        print('Error, cannot reach ' + HOST)
        return
    else:
        print('Connect To Host Success...')

    try:
        ftp.login(USER, PASSWD)
        ftp.set_pasv(False)
    except ftplib.error_perm:
        print('Username or Passwd Error')
        ftp.quit()
        return
    else:
        print('Login Success...')

    return ftp;


def FtpDownload(ftp, remotePath, localPath):
    try:
        bufsize = 1024  # 设置的缓冲区大小
        f = open(localPath, "wb")
        ftp.retrbinary("RETR %s" % remotePath, f.write, bufsize)  # 上传目标文件
        ftp.quit()
        f.close()
        return True
    except Exception as e:
        print('Error:', e)
        ftp.quit()
        return False


def FtpUpload(ftp, remotepath, localpath):
    try:
        ftp.storbinary('STOR %s' % remotepath, open(localpath, 'rb'))
    except ftplib.error_perm:
        print('File Error')
        os.unlink(localpath)
    else:
        print('Upload Success...')
    ftp.quit()


if __name__ == '__main__':
    ftp = FtpConnect(HOST, USER, PASSWD)
    # FtpUpload(ftp, '/var/ftp/test/test.html', 'test.txt')  # 上传
    FtpDownload(ftp, '/var/ftp/test/test.html', './test.log')  # 下载


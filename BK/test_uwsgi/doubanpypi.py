from urllib import request
from lxml import etree
import os
import logging
import socket
from fake_useragent import UserAgent


logger = logging.getLogger('mylogger') 
logger.setLevel(logging.DEBUG) 
 
fh = logging.FileHandler('douban.log', encoding="utf-8")
fh.setLevel(logging.INFO) 
 
ch = logging.StreamHandler() 
ch.setLevel(logging.DEBUG) 

formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] --*-- %(message)s')
fh.setFormatter(formatter) 
ch.setFormatter(formatter) 
 
logger.addHandler(fh) 
logger.addHandler(ch)



#设置超时时间为30s
socket.setdefaulttimeout(30)

def Schedule(a,b,c):
    '''
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    logger.debug("已下载：%.2f%%"%(per))

def download(begin_str, end_str, target_path):
    ua = UserAgent()
    api_str = "http://pypi.doubanio.com/simple/"
    req = request.Request(url=api_str, method="GET")
    req.add_header("User-Agent", ua.random)
    rep = request.urlopen(req).read()
    html = etree.HTML(rep)
    urls = html.xpath("/html/body/a")
    for i in urls:
        path = i.text
        url = "http://pypi.doubanio.com/simple/" + i.xpath("@href")[0]

        if begin_str <= path[0] < end_str:
            out_flag = 0
            req = request.Request(url=url, method="GET")
            req.add_header("User-Agent", ua.random)
            try:
                out_count = 0
                rep = request.urlopen(req).read()
                html = etree.HTML(rep)
                packet_list = html.xpath("/html/body/a")
                for j in packet_list:
                    flag = 0
                    error_msg = ""
                    packet_name = j.text
                    packet_url = j.xpath("@href")[0].replace("../../", "http://pypi.doubanio.com/")
                    current_dir_list = os.listdir(target_path)
                    if path in current_dir_list and os.path.isdir(os.path.join(target_path, path)):
                        pass
                    else:
                        os.makedirs(os.path.join(target_path,path))
                    try:
                        count = 0
                        logger.debug("开始下载：%s/%s"%(path, packet_name))
                        request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                        logger.info("下载成功：%s/%s"%(path, packet_name))
                    except socket.timeout as e:
                        error_msg = repr(e)
                        count = 1
                        while count <= 5:
                            try:
                                logging.debug("第%d次下载：%s/%s"%(count, path, packet_name))
                                request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                logger.info("下载成功：%s/%s"%(path, packet_name))
                                flag = 1
                                break
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count += 1
                    except Exception as e:
                        error_msg = repr(e)
                        count = 1
                        while count <= 5:
                            try:
                                logging.debug("第%d次下载：%s/%s"%(count, path, packet_name))
                                request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                logger.info("下载成功：%s/%s"%(path, packet_name))
                                flag = 1
                                break
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count += 1
                    if flag == 1:
                        continue
                    if count > 5:
                        logger.warning("下载失败：%s/%s  失败原因：%s"%(path, packet_name, error_msg))
                        continue
            except socket.timeout as e:
                error_msg = repr(e)
                out_count = 1
                while out_count <= 5:
                    try:
                        rep = request.urlopen(req).read()
                        out_flag = 1
                        html = etree.HTML(rep)
                        packet_list = html.xpath("/html/body/a")
                        for j in packet_list:
                            flag = 0
                            error_msg = ""
                            packet_name = j.text
                            packet_url = j.xpath("@href")[0].replace("../../", "http://pypi.doubanio.com/")
                            current_dir_list = os.listdir(target_path)
                            if path in current_dir_list and os.path.isdir(os.path.join(target_path, path)):
                                pass
                            else:
                                os.makedirs(os.path.join(target_path,path))
                            try:
                                count = 0
                                logger.debug("开始下载：%s/%s"%(path, packet_name))
                                request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                logger.info("下载成功：%s/%s"%(path, packet_name))
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s"%(count, path, packet_name))
                                        request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                        logger.info("下载成功：%s/%s"%(path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s"%(count, path, packet_name))
                                        request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                        logger.info("下载成功：%s/%s"%(path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            if flag == 1:
                                continue
                            if count > 5:
                                logger.warning("下载失败：%s/%s  失败原因：%s"%(path, packet_name, error_msg))
                                continue
                        break
                    except socket.timeout as e:
                        error_msg = repr(e)
                        out_count += 1
                    except Exception as e:
                        error_msg = repr(e)
                        out_count += 1
            except Exception as e:
                error_msg = repr(e)
                out_count = 1
                while out_count <= 5:
                    try:
                        rep = request.urlopen(req).read()
                        out_flag = 1
                        html = etree.HTML(rep)
                        packet_list = html.xpath("/html/body/a")
                        for j in packet_list:
                            flag = 0
                            error_msg = ""
                            packet_name = j.text
                            packet_url = j.xpath("@href")[0].replace("../../", "http://pypi.doubanio.com/")
                            current_dir_list = os.listdir(target_path)
                            if path in current_dir_list and os.path.isdir(os.path.join(target_path, path)):
                                pass
                            else:
                                os.makedirs(os.path.join(target_path,path))
                            try:
                                count = 0
                                logger.debug("开始下载：%s/%s"%(path, packet_name))
                                request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                logger.info("下载成功：%s/%s"%(path, packet_name))
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s"%(count, path, packet_name))
                                        request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                        logger.info("下载成功：%s/%s"%(path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s"%(count, path, packet_name))
                                        request.urlretrieve(packet_url, os.path.join(os.path.join(target_path,path), packet_name), Schedule)
                                        logger.info("下载成功：%s/%s"%(path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            if flag == 1:
                                continue
                            if count > 5:
                                logger.warning("下载失败：%s/%s  失败原因：%s"%(path, packet_name, error_msg))
                                continue
                        break
                    except socket.timeout as e:
                        error_msg = repr(e)
                        out_count += 1
                    except Exception as e:
                        error_msg = repr(e)
                        out_count += 1
            if out_flag == 1:
                continue
            if out_count > 5:
                logger.warning("下载失败（文件夹）：%s  失败原因：%s"%(path, error_msg))
                continue

def download_by_package_name(package_name, target_path):
    # ua = UserAgent()
    api_str = "http://pypi.doubanio.com/simple/"
    req = request.Request(url=api_str, method="GET")
    # req.add_header("User-Agent", ua.random)
    rep = request.urlopen(req).read()
    html = etree.HTML(rep)
    urls = html.xpath("/html/body/a")
    for i in urls:
        path = i.text
        url = "http://pypi.doubanio.com/simple/" + i.xpath("@href")[0]
        if package_name == path:
            print("**************************************")
            out_flag = 0
            req = request.Request(url=url, method="GET")
            # req.add_header("User-Agent", ua.random)
            try:
                out_count = 0
                rep = request.urlopen(req).read()
                html = etree.HTML(rep)
                packet_list = html.xpath("/html/body/a")
                for j in packet_list:
                    flag = 0
                    error_msg = ""
                    packet_name = j.text
                    packet_url = j.xpath("@href")[0].replace("../../", "http://pypi.doubanio.com/")
                    logging.debug(packet_url)
                    current_dir_list = os.listdir(target_path)
                    if path in current_dir_list and os.path.isdir(os.path.join(target_path, path)):
                        pass
                    else:
                        os.makedirs(os.path.join(target_path, path))
                    try:
                        count = 0
                        logger.debug("开始下载：%s/%s" % (path, packet_name))
                        request.urlretrieve(packet_url, os.path.join(os.path.join(target_path, path), packet_name),
                                            Schedule)
                        logger.info("下载成功：%s/%s" % (path, packet_name))
                    except socket.timeout as e:
                        error_msg = repr(e)
                        count = 1
                        while count <= 5:
                            try:
                                logging.debug("第%d次下载：%s/%s" % (count, path, packet_name))
                                request.urlretrieve(packet_url,
                                                    os.path.join(os.path.join(target_path, path), packet_name),
                                                    Schedule)
                                logger.info("下载成功：%s/%s" % (path, packet_name))
                                flag = 1
                                break
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count += 1
                    except Exception as e:
                        error_msg = repr(e)
                        count = 1
                        while count <= 5:
                            try:
                                logging.debug("第%d次下载：%s/%s" % (count, path, packet_name))
                                request.urlretrieve(packet_url,
                                                    os.path.join(os.path.join(target_path, path), packet_name),
                                                    Schedule)
                                logger.info("下载成功：%s/%s" % (path, packet_name))
                                flag = 1
                                break
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count += 1
                    if flag == 1:
                        continue
                    if count > 5:
                        logger.warning("下载失败：%s/%s  失败原因：%s" % (path, packet_name, error_msg))
                        continue
            except socket.timeout as e:
                error_msg = repr(e)
                out_count = 1
                while out_count <= 5:
                    try:
                        rep = request.urlopen(req).read()
                        out_flag = 1
                        html = etree.HTML(rep)
                        packet_list = html.xpath("/html/body/a")
                        for j in packet_list:
                            flag = 0
                            error_msg = ""
                            packet_name = j.text
                            packet_url = j.xpath("@href")[0].replace("../../", "http://pypi.doubanio.com/")
                            current_dir_list = os.listdir(target_path)
                            if path in current_dir_list and os.path.isdir(os.path.join(target_path, path)):
                                pass
                            else:
                                os.makedirs(os.path.join(target_path, path))
                            try:
                                count = 0
                                logger.debug("开始下载：%s/%s" % (path, packet_name))
                                request.urlretrieve(packet_url,
                                                    os.path.join(os.path.join(target_path, path), packet_name),
                                                    Schedule)
                                logger.info("下载成功：%s/%s" % (path, packet_name))
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s" % (count, path, packet_name))
                                        request.urlretrieve(packet_url,
                                                            os.path.join(os.path.join(target_path, path), packet_name),
                                                            Schedule)
                                        logger.info("下载成功：%s/%s" % (path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s" % (count, path, packet_name))
                                        request.urlretrieve(packet_url,
                                                            os.path.join(os.path.join(target_path, path), packet_name),
                                                            Schedule)
                                        logger.info("下载成功：%s/%s" % (path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            if flag == 1:
                                continue
                            if count > 5:
                                logger.warning("下载失败：%s/%s  失败原因：%s" % (path, packet_name, error_msg))
                                continue
                        break
                    except socket.timeout as e:
                        error_msg = repr(e)
                        out_count += 1
                    except Exception as e:
                        error_msg = repr(e)
                        out_count += 1
            except Exception as e:
                error_msg = repr(e)
                out_count = 1
                while out_count <= 5:
                    try:
                        rep = request.urlopen(req).read()
                        out_flag = 1
                        html = etree.HTML(rep)
                        packet_list = html.xpath("/html/body/a")
                        for j in packet_list:
                            flag = 0
                            error_msg = ""
                            packet_name = j.text
                            packet_url = j.xpath("@href")[0].replace("../../", "http://pypi.doubanio.com/")
                            current_dir_list = os.listdir(target_path)
                            if path in current_dir_list and os.path.isdir(os.path.join(target_path, path)):
                                pass
                            else:
                                os.makedirs(os.path.join(target_path, path))
                            try:
                                count = 0
                                logger.debug("开始下载：%s/%s" % (path, packet_name))
                                request.urlretrieve(packet_url,
                                                    os.path.join(os.path.join(target_path, path), packet_name),
                                                    Schedule)
                                logger.info("下载成功：%s/%s" % (path, packet_name))
                            except socket.timeout as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s" % (count, path, packet_name))
                                        request.urlretrieve(packet_url,
                                                            os.path.join(os.path.join(target_path, path), packet_name),
                                                            Schedule)
                                        logger.info("下载成功：%s/%s" % (path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            except Exception as e:
                                error_msg = repr(e)
                                count = 1
                                while count <= 5:
                                    try:
                                        logging.debug("第%d次下载：%s/%s" % (count, path, packet_name))
                                        request.urlretrieve(packet_url,
                                                            os.path.join(os.path.join(target_path, path), packet_name),
                                                            Schedule)
                                        logger.info("下载成功：%s/%s" % (path, packet_name))
                                        flag = 1
                                        break
                                    except socket.timeout as e:
                                        error_msg = repr(e)
                                        count += 1
                                    except Exception as e:
                                        error_msg = repr(e)
                                        count += 1
                            if flag == 1:
                                continue
                            if count > 5:
                                logger.warning("下载失败：%s/%s  失败原因：%s" % (path, packet_name, error_msg))
                                continue
                        break
                    except socket.timeout as e:
                        error_msg = repr(e)
                        out_count += 1
                    except Exception as e:
                        error_msg = repr(e)
                        out_count += 1
            if out_flag == 1:
                continue
            if out_count > 5:
                logger.warning("下载失败（文件夹）：%s  失败原因：%s" % (path, error_msg))
                continue
            break


if __name__ == "__main__":
    # download("a", "b", r"E:\pypi")
    
    import threading
    thread_list = []
    package_list = [
        # "ply",
        # "pysmi",
        # "pycryptodomex",
        # "pyasn1",
        # "pysnmp",
        # "uwsgi",
        "django-redis",
    ]
    for package_name in package_list:
        thread_list.append(threading.Thread(target=download_by_package_name, args=(package_name, "/Users/shexiaolong/pypipackage")))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()



from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client,get_tracker_conf
from django.conf import settings





class FastDFSStorage(Storage):
    """自定义文件存储系统类"""

    def __init__(self, client_path=None, base_url=None):
        # fastDFS的客户端配置文件路径
        self.client_path = client_path or settings.FDFS_CLIENT_CONF
        # storage服务器ip:端口
        self.base_url = base_url or settings.FDFS_BASE_URL
        # if client_path:
        #     self.client_path = client_path
        # else:
        #     self.client_path = settings.FDFS_CLIENT_CONF

        # Fdfs_client.upload_by_filename()
        # Fdfs_client.upload_by_buffer()
        # Fdfs_client.upload_by_file()

    def _open(self, name, mode='rb'):
        """
        用来打开文件的,但是我们自定义文件存储系统的目的是为了实现存储到远程的FastDFS服务器,不需要打开文件,所以此方重写后什么也不做pass
        :param name: 要打开的文件名
        :param mode: 打开文件的模式  read bytes
        :return: None
        """
        pass

    def _save(self, name, content):
        """
        文件存储时什么调用此方法,但是此方法默认是向本地存储,在此方法做实现文件存储到远程的FastDFS服务器
        :param name: 要上传的文件名
        :param content: 以rb模式打开的文件对象 将来通过content.read() 就可以读取到文件的二进制数据
        :return: file_id
        """
        # 1.创建FastDFS 客户端
        # client = Fdfs_client('meiduo_mall/utils/fastdfs/client.conf')
        # client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        track_config=get_tracker_conf(self.client_path)
        client = Fdfs_client(track_config)

        # 2.通过客户端调用上传文件的方法上传文件到fastDFS服务器
        # ret=client.upload_by_filename('要写上传文件的绝对路径') 只能通过文件绝对路径进行上传  此方式上传的文件会有后缀
        # upload_by_buffer 可以通过文件二进制数据进行上传  上传后的文件没有后缀

        ret = client.upload_by_buffer(content.read(), file_ext_name='jpg')
        # 3.判断文件是否上传成功
        if ret.get('Status') != 'Upload successed.':
            raise Exception('Upload file failed')

        # 3.1 获取file_id
        file_id = ret.get('Remote file_id')
        # print(type(file_id))
        file_id=file_id.decode()
        # print(type(file_id))

        # 4.返回file_id
        return file_id

    def exists(self, name):
        """
        当要进行上传时都调用此方法判断文件是否已上传,如果没有上传才会调用save方法进行上传
        :param name: 要上传的文件名
        :return: True(表示文件已存在,不需要上传)  False(文件不存在,需要上传)
        """
        return False

    def url(self, name):
        """
        当要访问图片时,就会调用此方法获取图片文件的绝对路径
        :param name: 要访问图片的file_id
        :return: 完整的图片访问路径: storage_server IP:8888 + file_id
        """
        # return 'http://192.168.103.210:8888/' + name
        # return settings.FDFS_BASE_URL + name
        return self.base_url + name
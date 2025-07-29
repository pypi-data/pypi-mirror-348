from requests.auth import HTTPBasicAuth

from ysdb import k2a_requests
from ysdb.ysdbLib import RdbClient, PointRealData
import logging


class RdbWrapper:
    """
    昆仑数据对ysdb sdk的封装类，支持写入遥控命令等部分操作。
    """

    def __init__(self, k2a_host: str, k2a_port: int, k2a_user: str, k2a_basic_token: str, k2a_protocol: str = 'https',
                 k2a_tenant: str = 'root'):
        # self.k2a_user = k2a_user
        # self.k2a_basic_token = k2a_basic_token
        # self.k2a_host = k2a_host
        # self.k2a_port = k2a_port
        self.ysdb_client = RdbClient()
        self.ysdb_token = None

        # 日志配置
        # 注：pytest时日志会不显示
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(self.__class__.__name__)

        # 通过k2a的环境变量接口，获取默认的ysdb信息
        env_url = f"{k2a_protocol}://{k2a_host}:{k2a_port}/api/env/k2box.ysdb"
        auth = HTTPBasicAuth(k2a_user, k2a_basic_token)
        response2 = k2a_requests.get(env_url, auth=auth, tenant=k2a_tenant)
        values = response2.get('body').get('values')
        self.ysdb_host = values.get('k2box.ysdb.host')
        self.ysdb_port = int(values.get('k2box.ysdb.port'))
        self.ysdb_user = values.get('k2box.ysdb.user')
        self.ysdb_password = values.get('k2box.ysdb.password')

        logging.info(f'YSDB info: {self.ysdb_host}:{self.ysdb_port} {self.ysdb_user}/{self.ysdb_password}')

        if self.ysdb_host == '' or self.ysdb_port == '':
            raise Exception(f'YSDB environment not set, please check K2A docker-compose.yml')

        ret = self.ysdb_client.connect(self.ysdb_host, self.ysdb_port)
        if ret != 1:
            raise Exception(f'YSDB connect failed {self.ysdb_host}:{self.ysdb_port}, {ret}')
        self.refresh_token()

    def disconnect(self):
        """
        断开到ysdb的连接，回收资源
        """
        self.ysdb_client.disconnect()

    def write_ctrl_data(self, mode: int, point_id: int, point_value):
        """
       写入遥控数据到YSDB
       :param mode: 0表示状态量，1表示模拟量
       :param point_id: 要遥控的测点id
       :param point_value: 要写入的遥控值。mode为0时，1代表打开，0代表关闭
       :return:
       """
        pointRealData = PointRealData(mode, point_id, 0, 0, point_value, 1, 0, 0)
        ret = self.ysdb_client.writeCtrlDataById(0, 1, 0, self.ysdb_token, pointRealData)
        return ret

    def refresh_token(self):
        """
        重新登录获取token（有效期10分钟）
        :return:
        """
        self.ysdb_token = self.ysdb_client.login(self.ysdb_user, self.ysdb_password)
        # 正常token示例：b'202cb962ac59075b964b07152d234b7000fea074fd7f0000699e03879a170000'
        if self.ysdb_token == 'err' or self.ysdb_token == '' or self.ysdb_token == b'':  # 若用户名错则返回token为b''
            raise Exception(f'YSDB login failed {self.ysdb_user}, {self.ysdb_password}')
        # 将返回的token转为字符串，以便后面调用write_ctrl_data接口
        self.ysdb_token = self.ysdb_token.decode()
        return self.ysdb_token

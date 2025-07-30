class BizException(Exception):
    def __init__(self, code, msg):
        # 调用父类的构造函数
        super().__init__(msg)
        self.code = code
        self.msg = msg

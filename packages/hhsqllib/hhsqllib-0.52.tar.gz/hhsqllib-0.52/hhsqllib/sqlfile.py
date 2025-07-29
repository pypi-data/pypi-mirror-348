import pandas as pd
import yaml
from sqlalchemy import create_engine,text

def testconnection(file = None):
    databasedict = {}
    databaseenginedict = {}
    with open(file) as f:
        databasedata = yaml.load(f, Loader=yaml.FullLoader)

    for databasekey in databasedata.keys():
        print( "测试 %s 连接情况"%databasekey )
        database = databasedata[databasekey]
        try:
            engine = create_engine(database,pool_timeout=10)
            try:
                with engine.connect() as connection:
                    result = connection.execute(text("SELECT 1"))
                    print("连接成功:", result.fetchone())
                    databasedict[databasekey] =  database
                    databaseenginedict['engine_%s'%databasekey] =  engine
            except Exception as e:
                print("连接失败:", e)
        except:
            databasedict[databasekey] = database
    assert len(databasedict)>0, "没有有效数据库连接"
    return databasedict,databaseenginedict


class database(object):
    def __init__(self,file = None):
        self.databasedict,self.databaseenginedict = testconnection(file=file)
        self.__dict__.update(self.databasedict)
        self.__dict__.update(self.databaseenginedict)









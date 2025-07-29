from functools import lru_cache
from sqlalchemy.sql import func
from sqlalchemy.dialects.mssql import NVARCHAR
from sqlalchemy import cast
import time
import datetime
import pandas as pd

# "AIndexHS300FreeWeight".upper()
# db = database(file=r'D:\FACTOR\sqldatabase.yaml')
# sourcedb = get_db(db.sourcedatabase_wind, schem='dbo')
# cf = corefunc(sourcedb = sourcedb )

class corefunc:

    @staticmethod
    def get_stockdt(sourcedb = None, trade_dt_list = None):
        mv_table = sourcedb.ASHAREEODDERIVATIVEINDICATOR
        mv = sourcedb.query(
            mv_table.S_INFO_WINDCODE.label('sid'),
            mv_table.TRADE_DT.label('trade_dt'),
        ).filter(mv_table.TRADE_DT.in_(trade_dt_list)).order_by(
            mv_table.S_INFO_WINDCODE, mv_table.TRADE_DT).to_df()
        return mv

    @staticmethod
    def get_index_eod(indexs = ['000300.SH','000905.SH','000852.SH','932000.CSI','000985.CSI'], sourcedb = None, begin_dt= '20000101' , end_dt = None  ):
        if end_dt is None:
            end_dt = datetime.datetime.today().strftime('%Y%m%d')
        indexeod = sourcedb.AINDEXEODPRICES
        df = sourcedb.query(indexeod.S_INFO_WINDCODE.label('sid'),
                            indexeod.TRADE_DT.label('dt'),
                            (indexeod.S_DQ_CLOSE).label('close'),
                            ).filter(
            indexeod.TRADE_DT >= begin_dt,
            indexeod.TRADE_DT <= end_dt, indexeod.S_INFO_WINDCODE.in_(indexs)).order_by(indexeod.TRADE_DT, indexeod.S_INFO_WINDCODE).to_df()
        return df

    #返回指数成分股权重
    @staticmethod
    def get_index_weight(indexs = ['000300.SH','000905.SH','000852.SH','932000.CSI','000985.CSI'], sourcedb = None):
        subsheet = sourcedb.AINDEXHS300FREEWEIGHT
        df = sourcedb.query(subsheet.S_INFO_WINDCODE.label('indexcode'), subsheet.S_CON_WINDCODE.label('sid'),
                            subsheet.TRADE_DT, subsheet.I_WEIGHT).filter(
            subsheet.S_INFO_WINDCODE.in_(indexs)).to_df()
        return df

    #返回指数成分股
    @staticmethod
    def get_index_members(indexs = ['000300.SH','000905.SH','000852.SH','932000.CSI','000985.CSI'], sourcedb=None):
        '''
        Args:
            indexs: 指数列表
            sourcedb:
        Returns: 返回指数列表构成的
        '''
        subsheet = sourcedb.AINDEXMEMBERS
        df = sourcedb.query(subsheet.S_INFO_WINDCODE.label('indexcode'),subsheet.S_CON_WINDCODE.label('sid'),subsheet.S_CON_INDATE,subsheet.S_CON_OUTDATE ).filter( subsheet.S_INFO_WINDCODE.in_(indexs)).to_df()
        return df

    # 返回交易日序列
    @staticmethod
    def get_trade_dt(dts=None, dte=None, sourcedb=None, offset='first', period='M'):
        '''

        Args:
            dts: 开始日期 默认为 19910101
            dte: 结束日期 默认为 当前日期
            sourcedb: 数据源
            offset: first 取左，last 取右 默认为 取左
            period: 取数周期

        Returns:

        '''
        if dts is None:
            dts = '19910101'
        if dte is None:
            dte = datetime.datetime.now().strftime("%Y%m%d")
        subsheet = sourcedb.ASHARECALENDAR
        df = sourcedb.query(subsheet.TRADE_DAYS).filter(subsheet.TRADE_DAYS >= dts, subsheet.TRADE_DAYS <= dte,
                                                        subsheet.S_INFO_EXCHMARKET == 'SSE').order_by(
            subsheet.TRADE_DAYS).to_df()
        df['dt'] = pd.to_datetime(df.TRADE_DAYS)
        df.set_index('dt', inplace=True)
        dfresample = df.resample(period)
        tddt = dfresample.agg(offset)
        return tddt

    @staticmethod
    def get_industry_all(level=1, sourcedb=None):
        '''
        Args:
            level: 中信行业分类
            sourcedb: 数据源
        Returns:
            中信行业分类情况
        '''
        if level == 1:
            return corefunc.get_citic_indu_levelone(sourcedb=sourcedb)
        elif level == 2:
            return corefunc.get_citic_indu_leveltwo(sourcedb=sourcedb)
        else:
            return corefunc.get_citic_indu_levelthree(sourcedb=sourcedb)

    @staticmethod
    @lru_cache(maxsize=512)
    def get_indu_bydt(trade_dt, sid=None, level=1, sourcedb=None):
        """
        Arguments:
            trade_dt '%Y%m%d' 格式
            sid {[str or iterable]} -- [sids of stocks] (default: {None})
            level {int} -- [level of zx industry] (default: {1})
            adjust {bool} -- [由于中信变更行业分类，是否调整兼容之前的代码] (default: {True})
        Returns:
            [pd.DataFrame] -- [sid: ind]
        """
        df = corefunc.get_industry_all(level=level, sourcedb=sourcedb)
        if sid is not None:
            sid = {sid} if isinstance(sid, str) else set(sid)
            df = df[df['sid'].isin(sid)]
        df = df.loc[(df['S_CON_INDATE'] <= trade_dt) & (
                (df['S_CON_OUTDATE'] >= trade_dt) | (df['S_CON_OUTDATE'].isnull()))].copy()
        return df.set_index('sid')




    @staticmethod
    def get_eodindicator(dts=None, dte=None, stocklist=None, sourcedb=None):
        '''

        Args:
            dts: 开始时间
            dte: 结束时间
            stocklist: 股票池
            sourcedb: 数据源

        Returns:

        '''
        mv_table = sourcedb.ASHAREEODDERIVATIVEINDICATOR

        if dts is None:
            dts = '20030101'
        if dte is None:
            dte = time.strftime('%Y%m%d', time.localtime())

        if stocklist is None:
            df = sourcedb.query(mv_table.S_INFO_WINDCODE.label('sid'), mv_table.TRADE_DT.label('dt'),
                                mv_table.S_VAL_MV.label('val_mv'), mv_table.S_DQ_TURN.label('tvratio'), mv_table.S_DQ_MV.label('dqmv'),
                                mv_table.UP_DOWN_LIMIT_STATUS.label('updownlimit')).filter(
                mv_table.TRADE_DT >= dts, mv_table.TRADE_DT <= dte, mv_table.S_DQ_TURN != None).order_by(
                mv_table.TRADE_DT, mv_table.S_INFO_WINDCODE).to_df()
        else:
            df = sourcedb.query(mv_table.S_INFO_WINDCODE.label('sid'), mv_table.TRADE_DT.label('dt'),
                                mv_table.S_VAL_MV.label('val_mv'), mv_table.S_DQ_TURN.label('tvratio'), mv_table.S_DQ_MV.label('dqmv'),
                                mv_table.UP_DOWN_LIMIT_STATUS.label('updownlimit')).filter(
                mv_table.TRADE_DT >= dts, mv_table.TRADE_DT <= dte, mv_table.S_INFO_WINDCODE.in_(stocklist),
                mv_table.S_DQ_TURN != None).order_by(
                mv_table.TRADE_DT, mv_table.S_INFO_WINDCODE).to_df()

        return df

    @staticmethod
    @lru_cache(maxsize=512)
    def get_mv_bydt(trade_dt, sourcedb=None):
        mv_table = sourcedb.ASHAREEODDERIVATIVEINDICATOR
        df = sourcedb.query(mv_table.S_INFO_WINDCODE.label('sid'),
                            mv_table.S_VAL_MV.label('mv_suffix')).filter(
            mv_table.TRADE_DT == trade_dt).to_df()
        df.set_index('sid', inplace=True)
        return df

    # 返回估值
    @staticmethod
    def get_stockvaluettm(dts=None, dte=None, stocklist=None, sourcedb=None):
        '''

        Args:
            dts: 开始取数时间，默认是20000101
            dte: 取数结束时间，默认是今天
            stocklist: 如果没有股票序列，那么取全部
            sourcedb: 数据源

        Returns:
            S_INFO_WINDCODE,TRADE_DT,S_VAL_MV,S_VAL_PE_TTM,S_VAL_PCF_OCFTTM,S_VAL_PB_NEW
        '''
        subsheet = sourcedb.ASHAREEODDERIVATIVEINDICATOR
        if dts is None:
            dts = '20030101'
        if dte is None:
            dte = time.strftime('%Y%m%d', time.localtime())
        if stocklist is None:
            df = sourcedb.query(subsheet.S_INFO_WINDCODE, subsheet.TRADE_DT, subsheet.S_VAL_MV, subsheet.S_VAL_PE_TTM,
                                subsheet.S_VAL_PCF_OCFTTM, subsheet.S_VAL_PB_NEW).filter(
                subsheet.TRADE_DT >= dts, subsheet.TRADE_DT <= dte).order_by(
                subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()
        else:
            df = sourcedb.query(subsheet.S_INFO_WINDCODE, subsheet.TRADE_DT, subsheet.S_VAL_MV, subsheet.S_VAL_PE_TTM,
                                subsheet.S_VAL_PCF_OCFTTM, subsheet.S_VAL_PB_NEW).filter(
                subsheet.TRADE_DT >= dts, subsheet.TRADE_DT <= dte, subsheet.S_INFO_WINDCODE.in_(stocklist)).order_by(
                subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()
        return df

    # 返回股价
    @staticmethod
    def get_stockeodprice(dts=None, dte=None, stocklist=None, sourcedb=None):
        '''
        Args:
            dts: 开始取数时间，默认是20000101
            dte: 取数结束时间，默认是今天
            stocklist: 如果没有股票序列，那么取全部
            sourcedb: 数据源

        Returns:
            返回股票名，日期，开盘价，收盘价，复权开盘价，复权收盘价，当日均价，涨停价，跌停价，成交量
        '''
        subsheet = sourcedb.ASHAREEODPRICES
        if dts is None:
            dts = '20030101'
        if dte is None:
            dte = time.strftime('%Y%m%d', time.localtime())
        if stocklist is None:
            df = sourcedb.query(subsheet.S_INFO_WINDCODE.label('sid'), subsheet.TRADE_DT.label('dt'),
                                subsheet.S_DQ_OPEN,subsheet.S_DQ_HIGH,subsheet.S_DQ_LOW, subsheet.S_DQ_CLOSE,
                                subsheet.S_DQ_ADJOPEN,subsheet.S_DQ_ADJHIGH, subsheet.S_DQ_ADJLOW,  subsheet.S_DQ_ADJCLOSE,
                                subsheet.S_DQ_AVGPRICE,subsheet.S_DQ_AMOUNT,subsheet.S_DQ_ADJFACTOR,
                                subsheet.S_DQ_LIMIT, subsheet.S_DQ_STOPPING, subsheet.S_DQ_VOLUME, subsheet.S_DQ_PCTCHANGE).filter(
                subsheet.TRADE_DT >= dts, subsheet.TRADE_DT <= dte).order_by(
                subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()
        else:
            df = sourcedb.query(subsheet.S_INFO_WINDCODE.label('sid'), subsheet.TRADE_DT.label('dt'),
                                subsheet.S_DQ_OPEN,subsheet.S_DQ_HIGH,subsheet.S_DQ_LOW, subsheet.S_DQ_CLOSE,
                                subsheet.S_DQ_ADJOPEN,subsheet.S_DQ_ADJHIGH, subsheet.S_DQ_ADJLOW,  subsheet.S_DQ_ADJCLOSE,
                                subsheet.S_DQ_AVGPRICE,subsheet.S_DQ_AMOUNT,subsheet.S_DQ_ADJFACTOR,
                                subsheet.S_DQ_LIMIT, subsheet.S_DQ_STOPPING, subsheet.S_DQ_VOLUME, subsheet.S_DQ_PCTCHANGE).filter(
                subsheet.TRADE_DT >= dts, subsheet.TRADE_DT <= dte, subsheet.S_INFO_WINDCODE.in_(stocklist)).order_by(
                subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()
        return df


    # 返回股价
    @staticmethod
    def get_eodprice(dts=None, dte=None, stocklist=None, sourcedb=None):
        '''
        Args:
            dts: 开始取数时间，默认是20000101
            dte: 取数结束时间，默认是今天
            stocklist: 如果没有股票序列，那么取全部
            sourcedb: 数据源

        Returns:
            返回股票名，日期，开盘价，收盘价，复权开盘价，复权收盘价，当日均价，涨停价，跌停价，成交量
        '''
        subsheet = sourcedb.ASHAREEODPRICES
        if dts is None:
            dts = '20030101'
        if dte is None:
            dte = time.strftime('%Y%m%d', time.localtime())
        if stocklist is None:
            df = sourcedb.query(subsheet.S_INFO_WINDCODE.label('sid'), subsheet.TRADE_DT.label('dt'),
                                subsheet.S_DQ_OPEN, subsheet.S_DQ_HIGH, subsheet.S_DQ_LOW, subsheet.S_DQ_CLOSE,
                                subsheet.S_DQ_ADJOPEN, subsheet.S_DQ_ADJHIGH, subsheet.S_DQ_ADJLOW,
                                subsheet.S_DQ_ADJCLOSE,
                                subsheet.S_DQ_AVGPRICE, subsheet.S_DQ_AMOUNT, subsheet.S_DQ_ADJFACTOR,
                                subsheet.S_DQ_LIMIT, subsheet.S_DQ_STOPPING, subsheet.S_DQ_VOLUME).filter(
                subsheet.TRADE_DT >= dts, subsheet.TRADE_DT <= dte).order_by(
                subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()
        else:
            df = sourcedb.query(subsheet.S_INFO_WINDCODE.label('sid'), subsheet.TRADE_DT.label('dt'),
                                subsheet.S_DQ_OPEN, subsheet.S_DQ_HIGH, subsheet.S_DQ_LOW, subsheet.S_DQ_CLOSE,
                                subsheet.S_DQ_ADJOPEN, subsheet.S_DQ_ADJHIGH, subsheet.S_DQ_ADJLOW,
                                subsheet.S_DQ_ADJCLOSE,
                                subsheet.S_DQ_AVGPRICE, subsheet.S_DQ_AMOUNT, subsheet.S_DQ_ADJFACTOR,
                                subsheet.S_DQ_LIMIT, subsheet.S_DQ_STOPPING, subsheet.S_DQ_VOLUME).filter(
                subsheet.TRADE_DT >= dts, subsheet.TRADE_DT <= dte, subsheet.S_INFO_WINDCODE.in_(stocklist)).order_by(
                subsheet.TRADE_DT, subsheet.S_INFO_WINDCODE).to_df()
        return df


    # 返回中信一级行业
    @staticmethod
    @lru_cache()
    def get_citic_indu_levelone(sourcedb=None):
        AINDEXMEMBERSCITICS = sourcedb.AINDEXMEMBERSCITICS
        B = sourcedb.AINDEXDESCRIPTION
        C = sourcedb.ASHAREDESCRIPTION

        df = sourcedb.query(
            AINDEXMEMBERSCITICS.S_INFO_WINDCODE.label('INDEX_INFO_WINDCODE'),
            AINDEXMEMBERSCITICS.S_CON_WINDCODE.label('sid'),
            AINDEXMEMBERSCITICS.S_CON_INDATE,
            AINDEXMEMBERSCITICS.S_CON_OUTDATE,
            cast(B.S_INFO_NAME, NVARCHAR).label('INDEX_INFO_NAME'),
            cast(C.S_INFO_NAME, NVARCHAR).label('S_INFO_NAME'),
            C.S_INFO_DELISTDATE,
            C.S_INFO_LISTDATE
        ).outerjoin(B, AINDEXMEMBERSCITICS.S_INFO_WINDCODE == B.S_INFO_WINDCODE).outerjoin(C,
                                                                                           AINDEXMEMBERSCITICS.S_CON_WINDCODE == C.S_INFO_WINDCODE).to_df()
        return df

    # 返回中信二级行业
    @staticmethod
    @lru_cache()
    def get_citic_indu_leveltwo(sourcedb=None):
        AINDEXMEMBERSCITICS = sourcedb.AINDEXMEMBERSCITICS2
        B = sourcedb.AINDEXDESCRIPTION
        C = sourcedb.ASHAREDESCRIPTION

        df = sourcedb.query(
            AINDEXMEMBERSCITICS.S_INFO_WINDCODE.label('INDEX_INFO_WINDCODE'),
            AINDEXMEMBERSCITICS.S_CON_WINDCODE.label('sid'),
            AINDEXMEMBERSCITICS.S_CON_INDATE,
            AINDEXMEMBERSCITICS.S_CON_OUTDATE,
            cast(B.S_INFO_NAME, NVARCHAR).label('INDEX_INFO_NAME'),
            cast(C.S_INFO_NAME, NVARCHAR).label('S_INFO_NAME'),
            C.S_INFO_DELISTDATE,
            C.S_INFO_LISTDATE
        ).outerjoin(B, AINDEXMEMBERSCITICS.S_INFO_WINDCODE == B.S_INFO_WINDCODE).outerjoin(C,
                                                                                           AINDEXMEMBERSCITICS.S_CON_WINDCODE == C.S_INFO_WINDCODE).to_df()
        return df

    # 返回中信三级行业
    @staticmethod
    @lru_cache()
    def get_citic_indu_levelthree(sourcedb=None):
        AINDEXMEMBERSCITICS = sourcedb.AINDEXMEMBERSCITICS3
        B = sourcedb.AINDEXDESCRIPTION
        C = sourcedb.ASHAREDESCRIPTION

        df = sourcedb.query(
            AINDEXMEMBERSCITICS.S_INFO_WINDCODE.label('INDEX_INFO_WINDCODE'),
            AINDEXMEMBERSCITICS.S_CON_WINDCODE.label('sid'),
            AINDEXMEMBERSCITICS.S_CON_INDATE,
            AINDEXMEMBERSCITICS.S_CON_OUTDATE,
            cast(B.S_INFO_NAME, NVARCHAR).label('INDEX_INFO_NAME'),
            cast(C.S_INFO_NAME, NVARCHAR).label('S_INFO_NAME'),
            C.S_INFO_DELISTDATE,
            C.S_INFO_LISTDATE
        ).outerjoin(B, AINDEXMEMBERSCITICS.S_INFO_WINDCODE == B.S_INFO_WINDCODE).outerjoin(C,
                                                                                           AINDEXMEMBERSCITICS.S_CON_WINDCODE == C.S_INFO_WINDCODE).to_df()
        return df

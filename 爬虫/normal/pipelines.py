# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from normal import settings
import pymysql


class biliPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBN,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改

        # 插入数据
    def process_item(self, item, spider):
        if spider.name=='bilibili':
            try:
                cursor = self.connect.cursor()
                if item['tag']==0:
                    # sql命令
                    sql1 = "insert into bili_test(b_game_id,b_game_name,b_type) value(%s,%s,%s)"
                    # 执行sql命令
                    cursor.execute(sql1,(item['id'], item['name'], str(item['type'])))
                elif item['tag']==1:
                    sql2 = "insert into biligrade_test(b_gid,b_comment_num,b_grade,b_star_list) value(%s,%s,%s,%s)"
                    cursor.execute(sql2, (item['id'], str(item['comment_number']), str(item['grade']),str(item['star_num_list'])))
                else:
                    pass
            except Exception as e:
                print(e)
            finally:
                # 关闭游标
                cursor.close()
                # 提交
                self.connect.commit()
        return item

class taptapPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBN,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改

        # 插入数据

    def process_item(self, item, spider):
        if spider.name == 'taptap':
            try:
                cursor = self.connect.cursor()
                # sql命令
                sql = "insert into taptap_test(t_game_id,t_game_name,t_fans_count,t_downloads,t_comment_num,t_star_list,t_grade,t_type) " \
                      "value(%s,%s,%s,%s,%s,%s,%s,%s)"
                # 执行sql命令
                cursor.execute(sql, (str(item['id']), item['name'], str(item['fans_count']),
                                     str(item['downloads']),str(item['comment_number']),
                                     str(item['star_num_list']),str(item['grade']),str(item['type'])))

            except Exception as e:
                print(e)

            finally:
                # 关闭游标
                cursor.close()
                # 提交
                self.connect.commit()
        return item
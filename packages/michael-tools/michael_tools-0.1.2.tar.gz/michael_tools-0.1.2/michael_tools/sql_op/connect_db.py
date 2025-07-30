import pymysql


def db_connection_test(connection_params):
    try:
        connection = pymysql.connect(**connection_params)
        connection.close()
        return True
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        return False


def execute_sql_query(db_config, sql):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results, None
    except Exception as e:
        return None, str(e)
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

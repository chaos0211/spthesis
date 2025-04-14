# backend/models/analytics.py
from pyspark.sql import SparkSession
from sqlalchemy.ext.declarative import declarative_base
from ..config import Config
from order import Order
from product import Product


Base = declarative_base()


class Analytics:
    @staticmethod
    def get_sales_report(db_session, seller_id):
        spark = SparkSession.builder \
            .appName("SalesAnalytics") \
            .config("spark.sql.warehouse.dir", Config.SPARK_WAREHOUSE) \
            .getOrCreate()

        # 使用SQLAlchemy加载数据到PySpark
        orders = db_session.query(Order).join(Product).filter(Product.seller_id == seller_id).all()
        orders_data = [(o.product.name, o.total_price) for o in orders]

        # 创建PySpark DataFrame
        orders_df = spark.createDataFrame(orders_data, ["product_name", "total_price"])

        # 统计销售额
        sales = orders_df.groupBy("product_name").sum("total_price").collect()

        spark.stop()
        return [{"product": row['product_name'], "total_sales": row['sum(total_price)']} for row in sales]
# backend/spark/recommender.py
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from ..config import Config


class Recommender:
    @staticmethod
    def train_model():
        spark = SparkSession.builder \
            .appName("Recommendation") \
            .config("spark.sql.warehouse.dir", Config.SPARK_WAREHOUSE) \
            .getOrCreate()

        # 加载用户行为数据
        behavior_df = spark.read.format("jdbc").option("url",
                                                       f"jdbc:mysql://{Config.SQLALCHEMY_DATABASE_URI.split('://')[1].split('/')[0]}/shopping_db") \
            .option("driver", "com.mysql.cj.jdbc.Driver") \
            .option("dbtable", "user_behavior") \
            .option("user", "root") \
            .option("password", "123456").load()

        # 训练ALS模型
        als = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="product_id", ratingCol="rating")
        model = als.fit(behavior_df)

        # 保存模型
        model.write("./models/als_model")

        spark.stop()

    @staticmethod
    def get_recommendations(user_id, num_items=5):
        spark = SparkSession.builder \
            .appName("Recommendation") \
            .config("spark.sql.warehouse.dir", Config.SPARK_WAREHOUSE) \
            .getOrCreate()

        # 加载模型
        model = ALS.load("./models/als_model")

        # 为用户生成推荐
        user_df = spark.createDataFrame([(user_id,)], ["user_id"])
        recommendations = model.recommendForUserSubset(user_df, num_items)

        # 提取推荐结果
        recs = recommendations.collect()[0].recommendations
        product_ids = [r.product_id for r in recs]

        spark.stop()
        return product_ids
import os

os.environ["JAVA_HOME"] = "C:/Program Files/Java/jdk1.8.0_202"
os.environ['HADOOP_HOME'] = "C:/Spark/hadoop-2.10.0"

from pyspark.python.pyspark.shell import sc
import random

NUM_SAMPLES = 100000000


def inside(p):
    x, y = random.random(), random.random()
    return x * x + y * y < 1


count = sc.parallelize(range(0, NUM_SAMPLES)).filter(inside).count()
pi = 4 * count / NUM_SAMPLES
print("pi is roughly", pi)

import pandas as pd
import numpy as np
import random

import dolphindb as ddb
s = ddb.session()
s.connect('192.168.1.8', 18888, "admin", "123456")

script = '''
dbPath = "dfs://valuedb"
        if(existsDatabase(dbPath))
            dropDatabase(dbPath)
        t = table(100:100,`id`time`vol,[SYMBOL,DATE, INT])
        db=database(dbPath,VALUE, `APPL`IBM`AMZN)
        pt = db.createPartitionedTable(t, `pt, `id)
'''
s.run(script)


pool = ddb.DBConnectionPool("localhost", 8848, 20, "admin", "123456")
appender = ddb.PartitionedTableAppender("dfs://valuedb", "pt", "id", pool)
n = 100

date = []
for i in range(n):
    date.append(np.datetime64(
        "201{:d}-0{:1d}-{:2d}".format(random.randint(0, 9), random.randint(1, 9), random.randint(10, 28))))

data = pd.DataFrame({"id": np.random.choice(['AMZN', 'IBM', 'APPL'], n), "time": date,
                     "vol": np.random.randint(100, size=n)})
re = appender.append(data)

print(re)
print(s.run("pt = loadTable('dfs://valuedb', 'pt'); select * from pt;"))
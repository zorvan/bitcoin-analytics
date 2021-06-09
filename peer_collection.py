import subprocess 
import json
import pandas as pd
import time

while True:
    p = subprocess.Popen("bitcoin-cli getpeerinfo", shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    result = json.loads(output)

    df = pd.DataFrame.from_dict(result, orient='columns')
    df2 = pd.read_csv("peers_db")
    df3 = df2.append(df[["addr"]]).drop_duplicates()
    df3.to_csv("peers_db",index=False)

    print(len(df3))
    time.sleep(10)

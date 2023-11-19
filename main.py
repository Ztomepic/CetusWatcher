import requests
import time
from config import my_range
from datetime import datetime
from server_chyan import sc_send

url = "https://api-sui.cetus.zone/v2/sui/swap/count"


def get_current_price(res):
    data = res.json()["data"]["pools"]
    if data[0]["symbol"] == 'USDT-USDC':
        return float(data[0]["price"])
    else:
        for i in data:
            if i["symbol"] == 'USDT-USDC' and i["tvl_in_usd"] != "0":
                return float(i["price"])


if __name__ == "__main__":
    print("Cetus watcher activated...")
    pushed_flag = False
    # 发送GET请求
    while True:
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 打印响应内容
            # print(response.text)
            current_price = get_current_price(response)
            min_price = my_range[0]
            max_price = my_range[1]
            if current_price < min_price or current_price > max_price:
                if not pushed_flag:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    print("!!!price out of range, alert!!!")
                    sc_send("Price out of range", "Current price is %s \n \n while the range is %s - %s" % (str(current_price), str(min_price), str(max_price)))
                    pushed_flag = True  # 一次推送之后，调回range之前不要再推送
            else:
                if pushed_flag:
                    print("Price back in range")
                    sc_send("Price back in range", "Current price is %s" % (str(current_price)))
                    pushed_flag = False
            print("waiting...")
            time.sleep(60)

        else:
            # 如果请求失败，打印错误信息
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(f"Request error: {response.status_code}")
            time.sleep(1)


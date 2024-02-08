import argparse
import os
# 创建ArgumentParser对象
parser = argparse.ArgumentParser(description='Process some external arguments')
parser.add_argument('--url', type=str, default='https://wiki.biligame.com/ys/%E7%A5%9E%E9%87%8C%E7%BB%AB%E5%8D%8E%E8%AF%AD%E9%9F%B3', help="对应语音页的网址")
parser.add_argument('--exp_name', type=str, default='shen_li_ling_hua', help= "实验名称")
args = parser.parse_args()

import requests
from bs4 import BeautifulSoup

url = args.url
dir = os.path.abspath(args.exp_name)

# 使用 requests 库获取网页内容
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
data_src_list = []

tbody_elements = soup.find_all('tbody')
for tbody in tbody_elements:
    entry = {}
    audios = tbody.find_all('div', class_='bikit-audio')
    if audios:
        audios_zn = audios[0]
        if audios_zn and len(audios_zn['data-src']) > 0:
            entry['audio'] = audios_zn['data-src']
        else:
            continue
    else:
        continue

    description = tbody.find('div', class_='voice_text_chs_m')
    if description:
        entry['description'] = description.get_text()
    else:
        continue
    data_src_list.append(entry)
from typing import Dict, Iterable, List, Optional, Tuple, Union
import glob
import os
import numpy as np
def get_latest_run_id(log_path: str = "", log_name: str = "") -> int:
    """
    Returns the latest run number for the given log name and log path,
    by finding the greatest number in the directories.

    :param log_path: Path to the log folder containing several runs.
    :param log_name: Name of the experiment. Each run is stored
        in a folder named ``log_name_1``, ``log_name_2``, ...
    :return: latest run number
    """
    max_run_id = 0
    for path in glob.glob(os.path.join(log_path, f"{glob.escape(log_name)}_[0-9]*")):
        file_name = path.split(os.sep)[-1]
        ext = file_name.split("_")[-1]
        if log_name == "_".join(file_name.split("_")[:-1]) and ext.isdigit() and int(ext) > max_run_id:
            max_run_id = int(ext)
    return max_run_id
opt=[]

opt_name=os.path.basename(dir)
if not os.path.exists(dir):
    os.makedirs(dir)

import requests
from tqdm import tqdm
import os

for item in tqdm(data_src_list):
    url = item['audio']  
    file_name = os.path.join(dir, os.path.basename(url))   # 将要保存的文件名

    if os.path.exists(file_name):
        continue
    response = requests.get(url, stream=True)

    if response.status_code == 200:  # 检查响应状态码，确保请求成功
        with open(file_name, 'wb') as file:
            file.write(response.content)
        with open(file_name+'.txt', 'wb') as file:
            file.write(item['description'].encode('utf-8'))
    else:
        print(f'下载失败{url}，状态码:', response.status_code)

    opt.append("%s|%s|ZH|%s" % (file_name, opt_name, item['description']))

list_file_path = os.path.join(dir, opt_name)+".list"
with open(list_file_path, 'a', encoding='utf-8') as file:
    file.write('\n'.join(opt))

current_folder_path = os.path.dirname(os.path.abspath(__file__))

python_path = os.path.join(os.path.join(current_folder_path, "runtime"), 'python.exe')
web_ui_path = os.path.join(current_folder_path, "webui.py")
os.system(f"{python_path} {web_ui_path} --model_data_path {list_file_path}")
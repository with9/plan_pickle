import os
import datetime
import pickle
def show_task(pickle_file):
    f=open(pickle_file,'rb')
    task_type=pickle_file[0:-7]
    all_list=pickle.load(f)
    study_dict=all_list[0]
    review_dict=all_list[1]
    now=datetime.datetime.now()
    today=datetime.datetime(now.year,now.month,now.day)#获取当日时间
    print('------------------',end='')
    print(task_type,end='')
    print('------------------')
    print('Study:\n')
    if today in study_dict:
        print(study_dict[today])
    print('Review:\n')
    if today in review_dict:
        for task in review_dict[today]:
            if task:
                print(task)
file_dir=os.getcwd()
pickle_files=[]#存取pickle文件列表
for root,dirs,files in os.walk(file_dir):
        for filename in files:
            if '_pickle' in filename:
                pickle_files.append(filename)

for i in pickle_files:
    show_task(i)

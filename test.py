import datetime
import pickle
import sys
#读取文件作为复习任务输入,保存为一个列表
def read_task(task_filename):
    with open(task_filename,'r')as f:
        task_list=f.readlines()
    return task_list
def add_study(task_list,study_dict,today):
    study_day=today
    for task in task_list:
        if task=='\n':
            task=None
        study_dict[study_day]=task
        study_day=study_day+datetime.timedelta(1)
    return study_dict
def add_review(study_dict,review_dict,Ebbinghaus_list):
    for study_date in study_dict.keys():
        for Ebbinghaus_day in Ebbinghaus_list:
            review_date=study_date+datetime.timedelta(Ebbinghaus_day)
            if review_date not in review_dict:
                review_dict[review_date]=[] 
            review_dict[review_date].append(study_dict[study_date])
    return review_dict
def show_task(study_dict,review_dict,plan_filename,today):
    day=today
    with open(plan_filename,'w')as f:
        while len(study_dict)!=0 or len(review_dict)!=0:
            show_day=str(day.year)+'-'+str(day.month)+'-'+str(day.day)+'\n'
            f.write('### ')
            f.write(show_day)
            if day in study_dict:
                f.write('Study:\n')
                if study_dict[day]:
                    f.write('- ')
                    f.write(study_dict[day])
                f.write('\n')
                study_dict.pop(day)
            f.write('Review:\n')
            if day in review_dict:
                review_tasks=review_dict[day]
                for review_task in review_tasks:
                    if review_task:
                        f.write('- ')
                        f.write(review_task)
                review_dict.pop(day)
                f.write('\n')
            day=day+datetime.timedelta(1)
def save_dict(study_dict,review_dict,filename):
    f=open(filename,'wb')
    task_list=[study_dict,review_dict]
    pickle.dump(task_list,f)
    f.close()
if __name__ == "__main__":
    study_dict={}#新学习字典
    review_dict={}#复习字典
    Ebbinghaus_list=[1,3,6,10,14,29]#艾宾浩斯复习点
    now=sys.argv[2]
    now_list=now.split('-')
    today=datetime.datetime(int(now_list[0]),int(now_list[1]),int(now_list[2]))#获取当日时间
    #task_filename=input("请任务所在输入文件名")
    task_filename=sys.argv[1]
    task_list=read_task(task_filename)
    study_dict=add_study(task_list,study_dict,today)
    review_dict=add_review(study_dict,review_dict,Ebbinghaus_list)
    plan_filename=task_filename+'_plan.md'
    pickle_filename=task_filename+'_pickle'
    save_dict(study_dict,review_dict,pickle_filename)
    show_task(study_dict,review_dict,plan_filename,today)
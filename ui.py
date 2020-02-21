from PySide2.QtWidgets import QApplication,QMessageBox,QTableWidget,QTableWidgetItem
from PySide2.QtGui import QColor
from PySide2.QtUiTools import QUiLoader
import os,pickle,sys,datetime
class MainWidget:
    def __init__(self,pickleFiles):
        self.pickleFiles=pickleFiles
        self.ui=QUiLoader().load("ui/mainWidget.ui")#读取qtdesigner文件.
        #self.ui.pushButton.clicked.connect(self.handleCalc)
        self.ui.tableWidget.setColumnCount(len(self.pickleFiles))
        #self.ui.tableWidget.setRowCount(20)
        now=datetime.datetime.now()
        today=datetime.datetime(now.year,now.month,now.day)#获取当日时间
        heades=[]
        for i in self.pickleFiles:
            heades.append(i[0:-7])
        self.ui.tableWidget.setHorizontalHeaderLabels(heades)#设置表头标签
        # for i in range(len(self.pickleFiles)):
        #     self.showOneDay(i,self.pickleFiles[i],today)
        self.theDay=today
        self.show_day()
        
        self.ui.backButton.clicked.connect(self.show_back)
        self.ui.nextButton.clicked.connect(self.show_next)
        self.ui.todayButton.clicked.connect(self.backToToday)
    def showOneDay(self,columnNumber,pickle_file,theDay):
        #在特定列显示特定项目的任务
        f=open(pickle_file,'rb')
        all_list=pickle.load(f)
        review_dict=all_list[1]
        study_dict=all_list[0]
        if theDay in study_dict:
            if 0>=self.ui.tableWidget.rowCount():
                    self.ui.tableWidget.insertRow(0)
            newItem=QTableWidgetItem(study_dict[theDay][0:-1])
            newItem.setTextColor(QColor(200,111,100)) 
            self.ui.tableWidget.setItem(0,columnNumber,newItem)
        if theDay in review_dict:
            rowNumber=1
            for task in review_dict[theDay]:      
                if rowNumber>=self.ui.tableWidget.rowCount():
                    self.ui.tableWidget.insertRow(rowNumber)
                if task:
                    self.ui.tableWidget.setItem(rowNumber,columnNumber,QTableWidgetItem(task[0:-1])) 
                    rowNumber=rowNumber+1
    def show_day(self):
            dayStr=str(self.theDay.year)+'-'+str(self.theDay.month)+'-'+str(self.theDay.day)
            self.ui.label_2.setText(dayStr)
            self.ui.tableWidget.setRowCount(0)
            for i in range(len(self.pickleFiles)):
                self.showOneDay(i,self.pickleFiles[i],self.theDay)
    def show_back(self):
            self.theDay=self.theDay-datetime.timedelta(1)
            self.show_day()
    def show_next(self):
            self.theDay=self.theDay+datetime.timedelta(1)
            self.show_day()
    def backToToday(self):
            now=datetime.datetime.now()
            today=datetime.datetime(now.year,now.month,now.day)#获取当日时间
            self.theDay=today
            self.show_day()
file_dir=os.getcwd()
pickle_files=[]#存取pickle文件列表
for root,dirs,files in os.walk(file_dir):
        for filename in files:
            if '_pickle' in filename:
                pickle_files.append(filename)
app=QApplication([])
mainWidget=MainWidget(pickle_files)
mainWidget.ui.show()





app.exec_()
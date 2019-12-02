import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "milestoneUI.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        #self.loadCatList()
        #self.loadZipList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.currentTextChanged.connect(self.zipChanged)
        self.ui.zipList.currentTextChanged.connect(self.displayTotalBus)
        self.ui.zipList.currentTextChanged.connect(self.displayTotalPop)
        self.ui.zipList.currentTextChanged.connect(self.displayAvgIncome)
        self.ui.catList.currentTextChanged.connect(self.catChanged)
        self.ui.catList.currentTextChanged.connect(self.Overpriced)
        self.ui.catList.currentTextChanged.connect(self.popular)
        self.ui.zipList.currentTextChanged.connect(self.Successful)
        self.ui.user_2.textChanged.connect(self.getUserNames)
        self.ui.userList_2.itemSelectionChanged.connect(self.displayUserInfo)

    def executeQuery(self, sql_str):
        try: 
            conn = psycopg2.connect("dbname='yelpdb3' user ='postgres' host='localhost' password='8114'")
        except:
            print("Unable to connect")
        cur = conn.cursor()
        cur.execute(sql_str)
        result = cur.fetchall()
        conn.close()
        return result
    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT distinct state FROM business ORDER BY state"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
    
    def stateChanged(self):
        self.ui.cityList.clear()
        if (self.ui.stateList.currentIndex()>=0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query Failed!")
            
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
                

            sql_str = "SELECT name, city, state, buspostal, busi_num_of_review, busi_avg_rating, numcheckin, busi_stars FROM business WHERE state ='" + state + "' ORDER BY name;"
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code', '# Reviews', 'Review Rating', 'Checkins', 'Stars'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2, 50)
                
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Query Failed!!")
                
    def cityChanged(self):
        self.ui.zipList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str1 = "SELECT distinct buspostal FROM business WHERE city ='" + city + "' ORDER BY buspostal;"
            try:
                results = self.executeQuery(sql_str1)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query Failed!")
            sql_str = "SELECT name, city, state, buspostal, busi_num_of_review, busi_avg_rating, numcheckin, busi_stars FROM business WHERE city ='" + city + "' AND state= '" + state + "'ORDER BY name;" 
            #print(sql_str)
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code', '# Reviews', 'Review Rating', 'Checkins', 'Stars'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2, 50)
                    
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                    
            except:
                print("Query Failed!!") 
    def zipChanged(self): 
        self.ui.catList.clear()
        if (self.ui.stateList.currentIndex()>=0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipC = self.ui.zipList.currentText()
            sql_str1 = "SELECT distinct cat_name FROM category as c, business where c.busi_id = business.busi_id and business.buspostal = '"+ zipC+ "' AND business.city ='"+city+"' ORDER BY cat_name;"
         
            #print(sql_str1)
            #sql_str2 ="SELECT distinct buspostal FROM business WHERE state ='" + state + "' ORDER BY buspostal;"
            try:
                results = self.executeQuery(sql_str1)
                #print(results)
                for row in results:
                    self.ui.catList.addItem(row[0])
            except:
                print("Query Failed!")
            
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, city, state, buspostal, busi_num_of_review, busi_avg_rating, numcheckin, busi_stars FROM business WHERE state ='" + state + "'AND city = '" + city +"' AND buspostal = '"+ zipC +"' ORDER BY name;"
            #print(sql_str)
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code', '# Reviews', 'Review Rating', 'Checkins', 'Stars'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2, 50)
                
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Query Failed!!")

    def catChanged(self): #for zipcode in page 1 # cant connect to change the business table when zipcode is selected
        if (self.ui.zipList.currentIndex()>=0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            zipC = self.ui.zipList.currentText()
            cat = self.ui.catList.currentText()
            
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT name, city, state, buspostal,busi_num_of_review, busi_avg_rating, numcheckin, busi_stars FROM business, category as c WHERE state ='" + state + "'AND city = '" + city +"' AND buspostal = '"+ zipC +"'AND c.cat_name = '"+cat+ "' AND c.busi_id = business.busi_id ORDER BY name;"
            #print(sql_str)
            try:
                results = self.executeQuery(sql_str)
                #print(results)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code', '# Reviews', 'Review Rating', 'Checkins', 'Stars'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2, 50)
                
                currentRowCount = 0
                for row in results:
                    for colCount in range(0,len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount,colCount,QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                
            except:
                print("Query Failed!!")

    def displayTotalBus(self):
        zipCode = self.ui.zipList.currentText()
        sql_str = "select count(name) from business where buspostal = '" + zipCode +"';"
        
        try:
            #print(sql_str)
            results = self.executeQuery(sql_str)
            #print(results)
            self.ui.numBus.setText(str(results[0][0]))
        except:
            print("Query Failed!!!")
            
    def displayTotalPop(self): #initalize, text on page 1
        zipcode = self.ui.zipList.currentText()
        sql_str = "select population from zipdata where zip = '" +zipcode +"';"
        try:
            results = self.executeQuery(sql_str)
            self.ui.pop.setText(str(results[0][0]))
        except:
            print("Query Failed!!!!")
##                    
    def displayAvgIncome(self): #initalize, text on page 1
        zipcode = self.ui.zipList.currentText()
        sql_str = "select meanincome from zipdata where zip = '" +zipcode +"';"
        try:
            results = self.executeQuery(sql_str)
            #print(results)
            self.ui.avg.setText(str(results[0][0]))
        except:
            print("Query Failed!!!!")
            
 
#user section on page 2        
    def getUserNames(self): # works and displays names 
        self.ui.userList_2.clear()
        userName = self.ui.user_2.text()
        sql_str = "SELECT user_id FROM users WHERE user_name LIKE '%" +userName+ "%' ORDER BY user_name;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.userList_2.addItem(row[0])
        except:
            print("Query Failed!!!")
    def displayUserInfo(self):
        userID = self.ui.userList_2.selectedItems()[0].text()
        sql_str = "SELECT user_name FROM users WHERE user_id ='" +userID + "';"
        sql_str1 = "SELECT user_stars FROM users WHERE user_id ='" +userID + "';"
        sql_str2 = "SELECT user_yelp_since FROM users WHERE user_id ='" +userID + "';"
        sql_str3 = "select user_num_of_fans FROM users WHERE user_id ='" +userID + "';"
        sql_str4 = "select sum(votes_funny) FROM review WHERE review_author ='" +userID + "';"
        sql_str5 = "select sum(votes_cool) FROM review WHERE review_author ='" +userID + "';"
        sql_str6 = "select sum(votes_useful) FROM review WHERE review_author ='" +userID + "';"
        try:
            results = self.executeQuery(sql_str)
            results1 = self.executeQuery(sql_str1)
            results2 = self.executeQuery(sql_str2)
            results3 = self.executeQuery(sql_str3)
            results4 = self.executeQuery(sql_str4)
        
            results5 = self.executeQuery(sql_str5)
            
            results6 = self.executeQuery(sql_str6)
            
            self.ui.userName_2.setText(results[0][0])
            self.ui.userStars_2.setText(str(results1[0][0]))
            self.ui.YelpSince_3.setText(str(results2[0][0]))
            self.ui.numFan.setText(str(results3[0][0]))
            self.ui.funny_2.setText(str(results4[0][0]))
            self.ui.cool_2.setText(str(results5[0][0]))
            self.ui.useful_2.setText(str(results6[0][0]))
        except:
            print("Query Failedinfo")
        

    def Overpriced(self):
        zipcode = self.ui.zipList.currentText()
        cat = self.ui.catList.currentText()
        sql_str = "SELECT name, price_range, review_rating, zip FROM overpriced WHERE zip = '" + zipcode + "' AND category = '" + cat + "';"

        try:
            results = self.executeQuery(sql_str)

            style = ":: section(""background-color: #f3f3f3; )"
            self.ui.overBus.horizontalHeader().setStyleSheet(style)
            self.ui.overBus.setColumnCount(len(results[0]))
            self.ui.overBus.setRowCount(len(results))
            self.ui.overBus.setHorizontalHeaderLabels(['Name', 'Price Range', 'Rating', 'Zip Code'])
            self.ui.overBus.resizeColumnsToContents()
            self.ui.overBus.setColumnWidth(0, 300)
            self.ui.overBus.setColumnWidth(1, 150)
            self.ui.overBus.setColumnWidth(2, 100)
            self.ui.overBus.setColumnWidth(3, 100)

            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.overBus.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1

        except:
            print("Query Failed!!!!")

    def popular(self):
        zipcode = self.ui.zipList.currentText()
        cat = self.ui.catList.currentText()
        sql_str = "SELECT Name, Stars, review_Rating, num_of_review, Zip FROM popular WHERE zip = '" + zipcode + "'AND category = '" + cat + "';"

        try:
            results = self.executeQuery(sql_str)
            style = ":: section(""background-color: #f3f3f3; )"
            self.ui.popBus.horizontalHeader().setStyleSheet(style)
            self.ui.popBus.setColumnCount(len(results[0]))
            self.ui.popBus.setRowCount(len(results))
            self.ui.popBus.setHorizontalHeaderLabels(['Name', 'Stars', 'Rating', '# of review', 'Zip Code'])
            self.ui.popBus.resizeColumnsToContents()
            self.ui.popBus.setColumnWidth(0, 300)
            self.ui.popBus.setColumnWidth(1, 150)
            self.ui.popBus.setColumnWidth(2, 100)
            self.ui.popBus.setColumnWidth(3, 100)

            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.popBus.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            print("Query Failed!!!!")

    def Successful(self):
        zipcode = self.ui.zipList.currentText()
        sql_str = "SELECT * FROM successful WHERE zip = '" + zipcode + "';"

        try:
            results = self.executeQuery(sql_str)
            style = ":: section(""background-color: #f3f3f3; )"
            self.ui.sucBus.horizontalHeader().setStyleSheet(style)
            self.ui.sucBus.setColumnCount(len(results[0]))
            self.ui.sucBus.setRowCount(len(results))
            self.ui.sucBus.setHorizontalHeaderLabels(['Name', '# of checkin', '# of review', 'Zip Code'])
            self.ui.sucBus.resizeColumnsToContents()
            self.ui.sucBus.setColumnWidth(0, 300)
            self.ui.sucBus.setColumnWidth(1, 150)
            self.ui.sucBus.setColumnWidth(2, 150)

            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.sucBus.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except:
            print("Query Failed!!!!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())
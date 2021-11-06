import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog,QMessageBox,QGraphicsDropShadowEffect,QTableWidget,QTableWidgetItem,QHeaderView
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import assets_qrc
# sys.path.append("../")
from model import User,db_close
import hashlib
#get view path file
ui_path =os.path.join(os.path.dirname(os.path.abspath(__file__)),"danh_sach_user.ui")

class NguoiDung(QDialog):
    def __init__(self,userID):
        # super().__init__(*args, **kwargs)
        super().__init__()
        self.userID = userID
        # super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        #load ui file
        uic.loadUi(ui_path, self)

        # #set fix size window
        self.setFixedSize(1008,726)

        header = self.table_danhsach_1.horizontalHeader()  
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)     
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        #diable window title
        # self.setWindowFlags(Qt.FramelessWindowHint)

        #set shadow effect for buttons accent group
        self.btn_update.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=30, xOffset=15, yOffset=15,color=QColor(0,0,0,80)))
        self.btn_them.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=30, xOffset=15, yOffset=15,color=QColor(0,0,0,80)))
        self.btn_xoa.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=30, xOffset=15, yOffset=15,color=QColor(0,0,0,80)))
        self.btn_dong.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=30, xOffset=15, yOffset=15,color=QColor(0,0,0,80)))

        #set event for buttons

        self.btn_xoa.setEnabled(False)
        self.btn_update.setEnabled(False)

        self.btn_dong.clicked.connect(self.closeDialog)
        self.btn_them.clicked.connect(self.addData)
        self.btn_xoa.clicked.connect(self.deleteData)
        self.btn_update.clicked.connect(self.updateData)
        
        # rowdata=['1','1','1','1','1','1']
        # self.insertRow(self.table_danhsach_1,rowdata)

        self.table_danhsach_1.cellClicked.connect(self.on_change)
        self.selectedRow = -1
        self.editMode = False

        #load data to table
        try:
            result = User.select().where(User.id !=1)

            for item in result:
                rowData = [item.id,item.fullname,item.department, item.phoneNum, item.email,item.username,"******"]
                self.insertRow(self.table_danhsach_1,rowData)
        except Exception as ex:
            print(ex)
            pass
        

    #################func handle event of buttons##################################

    #event close
    def closeDialog(self):
        db_close()
        self.close()
    
    #event add
    def addData(self):
        # cell = QTableWidgetItem("1")
        # cell.setFlags( Qt.ItemIsEnabled )
        # self.table_danhsach_1.setItem(self.selectedRow,self.selectedCol,cell)
        self.table_danhsach_1.insertRow(0)
        self.btn_update.setEnabled(True)

        #diabled cell STT
        cell = QTableWidgetItem("")
        cell.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        cell.setFlags( Qt.ItemIsEnabled )
        self.table_danhsach_1.setItem(0,0,cell)

        for i in range(1,6):
            newCell =QTableWidgetItem("")
            newCell.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.table_danhsach_1.setItem(0,i,newCell)
        
        # diabled button
        self.btn_them.setEnabled(False)
        self.btn_xoa.setEnabled(False)
        self.editMode = True


    #event update
    def updateData(self):
        #check valid data:
        ho_ten = self.table_danhsach_1.item(0,1).text()
        phong_khoa = self.table_danhsach_1.item(0,2).text()
        dien_thoai = self.table_danhsach_1.item(0,3).text()
        email = self.table_danhsach_1.item(0,4).text()
        user_name = self.table_danhsach_1.item(0,5).text()
        passwd = self.table_danhsach_1.item(0,6).text()

        valid = len(ho_ten)>0 and len(passwd)>0
        if valid == False:
            mesBox = QMessageBox()
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setText("Vui lòng điền thông tin tên đăng nhập và mật khẩu!")
            mesBox.setWindowTitle("Thông báo")
            mesBox.setStandardButtons(QMessageBox.Ok)
            mesBox.exec()
        
        else:
            try:
                # add data to table User
                user = User()
                user.fullname = ho_ten
                user.department = phong_khoa
                user.phoneNum = dien_thoai
                user.email = email
                user.username = user_name
               
                user.password = hashlib.pbkdf2_hmac('sha256',passwd.encode('utf-8'),b'1402$@&%96',10000).hex()
                user.save()

                # update new row table
                rowData = [user.id,ho_ten,phong_khoa,dien_thoai,email,user_name,"******"]
                self.diableRow(self.table_danhsach_1,rowData)
                self.selectedRow = -1
                self.table_danhsach_1.clearSelection()
                #diable button
                self.btn_update.setEnabled(False)
                self.btn_them.setEnabled(True)

                self.editMode = False

            except Exception as ex:
                print(ex)
                mesBox = QMessageBox()
                mesBox.setIcon(QMessageBox.Warning)
                mesBox.setText("Cập nhật người dùng mới thất bại!\nVui lòng chọn tên tài khoản không trùng với các tài khoản trước!")
                mesBox.setWindowTitle("Thông báo")
                mesBox.setStandardButtons(QMessageBox.Ok)
                mesBox.exec()
         




    #event delete
    def deleteData(self):

        #check quyen
        if self.userID != 1:
            mesBox = QMessageBox()
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setText("Vui lòng đăng nhập tài khoản admin để xóa người dùng!")
            mesBox.setWindowTitle("Thông báo")
            mesBox.setStandardButtons(QMessageBox.Ok)
            mesBox.exec()
            return
        
        #get user id
        # if len(self.table_danhsach_1.item(self.selectedRow,0).text()) ==0:
        #     self.table_danhsach_1.removeRow(self.selectedRow) 
        #     self.selectedRow = -1
        #     self.table_danhsach_1.clearSelection()
        #     self.btn_xoa.setEnabled(False)
        #     self.btn_update.setEnabled(False)
        #     self.btn_them.setEnabled(True)
        #     return

        userDel = int(self.table_danhsach_1.item(self.selectedRow,0).text())
        try:
            User.delete_by_id(userDel)
            self.table_danhsach_1.removeRow(self.selectedRow)
            self.btn_xoa.setEnabled(False)
            self.selectedRow = -1
            self.table_danhsach_1.clearSelection()

            mesBox = QMessageBox()
            mesBox.setIcon(QMessageBox.Information)
            mesBox.setText("Xóa người dùng thành công!")
            mesBox.setWindowTitle("Thông báo")
            mesBox.setStandardButtons(QMessageBox.Ok)
            mesBox.exec()
        except Exception as ex:
            print(ex)
            mesBox = QMessageBox()
            mesBox.setIcon(QMessageBox.Warning)
            mesBox.setText("Xóa người dùng thất bại!")
            mesBox.setWindowTitle("Thông báo")
            mesBox.setStandardButtons(QMessageBox.Ok)
            mesBox.exec()
        
    

    #######################func handle data of table ###############################
    #insert row to table
    def insertRow(self,table,row_data):
        table.insertRow(0)
        col=0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            cell.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            cell.setFlags( Qt.ItemIsEnabled )
            table.setItem(0,col,cell)
            col+=1
    
    #diable a row of table
    def diableRow(self,table,row_data):
        col=0
        for item in row_data:
            cell = QTableWidgetItem(str(item))
            cell.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            cell.setFlags( Qt.ItemIsEnabled )
            table.setItem(0,col,cell)
            col+=1

    #event selected celll 
    def on_change(self,row,col):
        try:
            self.selectedRow = row
            self.selectedCol = col
            if self.editMode == False:
                self.btn_xoa.setEnabled(True)
            # print(row)
        except Exception as ex:
            print(ex)
            pass

# test app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = Home("s")
    # window.show()
    win = NguoiDung(1)
    win.exec()
   


       


       
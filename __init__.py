import sys, os
from PyQt5.QtWidgets import QWidget, QTableWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QAbstractItemView, QTableWidgetItem, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QFile, QIODevice, QTextStream
from PyQt5.QtGui import QFont

class SudokuGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        self.setWindowTitle('SUDOKU')

        self.sudokuGrid = []                                                                      #存放所有9个3*3单元
        for i in range(3):
            self.sudokuGrid.append([])
            for j in range(3):
                smallGrid = QTableWidget(3, 3)                                               #新建3*3单元
                smallGrid.setEditTriggers(QAbstractItemView.NoEditTriggers)
                smallGrid.setSelectionMode(QAbstractItemView.NoSelection)
                smallGrid.verticalHeader().setVisible(False)                                #隐藏表格的表头
                smallGrid.horizontalHeader().setVisible(False)
                smallGrid.setFixedSize(92, 92)
                for r in range(3):
                    smallGrid.setRowHeight(r, 30)
                    smallGrid.setColumnWidth(r, 30)
                self.sudokuGrid[i].append(smallGrid)                                         #将每个单元添加到总单元中

        self.openFileBt = QPushButton('打开文件')                                        #打开文件按钮
        self.fillBt = QPushButton('填充数独')                                                #填充数独按钮
        self.fillBt.setEnabled(False)                                                             #成功打开文件后，才可填充

        sudokuLayout = QGridLayout()
        sudokuLayout.setSpacing(1)
        for i in range(3):
            for j in range(3):
                sudokuLayout.addWidget(self.sudokuGrid[i][j], i, j)                     #在布局中添加所有3*3单元

        controlLayout = QHBoxLayout()
        controlLayout.addStretch()
        controlLayout.addWidget(self.openFileBt)                                         #在控制栏中添加按钮
        controlLayout.addWidget(self.fillBt)
        controlLayout.addStretch()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(sudokuLayout)
        mainLayout.addLayout(controlLayout)

        self.setLayout(mainLayout)
        self.show()
        self.sudokuGridInit()                                                                     #初始化
        self.openFileBt.clicked.connect(self.openTxtFile)
        self.fillBt.clicked.connect(self.fillBtClicked)

    def sudokuGridInit(self):
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        self.setSudokuGrid('', i, j, p, q)
        
        self.newOnlyOne = []
        for i in range(9):
            self.newOnlyOne.append([0, 0, 0, 0, 0, 0, 0, 0, 0])                       #用来判断包含唯一数字的小格是否是首次变为唯一

        self.sudokuNumInit()
        
    def openTxtFile(self):
        filePath = QFileDialog.getOpenFileName(self, "Open Txt File", os.getcwd()+"/sudokuIni/", "Txt Files(*.txt)")
        file = QFile(filePath[0])
        if file.open(QIODevice.ReadOnly):
            fileTxt = QTextStream(file)
            self.insertArray = []
            for i in range(9):
                self.insertArray.append([])
                line = fileTxt.readLine()
                lineParts = line.split(' ')
                for j in range(9):
                    self.insertArray[i].append(int(lineParts[j]))
            self.insertListConfirmed = []
            for i in range(9):
                for j in range(9):
                    if self.insertArray[i][j] != 0:
                        self.insertListConfirmed.append([[i, j, self.insertArray[i][j]]])       #根据txt文件中读取的信息，设置确定的填充序列
            for i in range(len(self.insertListConfirmed)):
                self.setGridItem(self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][0], self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][1], self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][2])
                self.newOnlyOne[self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][0]][self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][1]] = 1
            self.showAllAlone()                                                                          #显示所有已经确定的小格
            self.fillBt.setEnabled(True)

    def setGridItem(self, row, column, number):
        i = row // 3
        j = column // 3
        ii = row % 3
        jj = column % 3
        self.setSudokuGrid(number, i, j, ii, jj)
        self.sudokuNum[row][column] = [number]         #根据确定下来的数字，填充self.sudokuNum
        self.removeOthers(row, column, number)          #根据确定下来的数字，清除相应行、列和3*3单元内的相同数字

    def sudokuNumInit(self):
        self.sudokuNum = []
        for i in range(9):
            self.sudokuNum.append([])
            for j in range(9):
                smallNum = [1, 2, 3, 4, 5, 6, 7, 8, 9]       #将self.sudokuNum的所有9*9个单元格均设置为包含1-9的所有可能数字，完成初始化
                self.sudokuNum[i].append(smallNum)

    def removeOthers(self, row, column, number):
        i = row // 3
        j = column // 3
        for o in range(9):
            self.removeNum(row, o, number)                #去除特定行内的相同数字
            self.removeNum(o, column, number)           #去除特定列内的相同数字
        for p in range(3):
            for q in range(3):
                self.removeNum(i*3+p, j*3+q, number)  #去除特定3*3单元内的相同数字

    def removeNum(self, row, column, number):
        #若self.sudokuNum对应小格中有两个及以上数字，且包含待去除数字，则将其去除
        numLen = len(self.sudokuNum[row][column])
        if numLen == 1:
            return
        if number in self.sudokuNum[row][column]:
            self.sudokuNum[row][column].remove(number)

    def setSudokuGrid(self, number, i, j, ii, jj):
        temp = QTableWidgetItem(str(number))
        temp.setTextAlignment(Qt.AlignCenter)
        temp.setFont(QFont("Microsoft YaHei", 18))
        self.sudokuGrid[i][j].setItem(ii, jj, temp)

    def showAllAlone(self):
        for i in range(9):
            for j in range(9):
                numLen = len(self.sudokuNum[i][j])
                if numLen == 1:
                    temp = QTableWidgetItem(str(self.sudokuNum[i][j][0]))
                    temp.setTextAlignment(Qt.AlignCenter)
                    temp.setFont(QFont("Microsoft YaHei", 18))
                    self.sudokuGrid[i//3][j//3].setItem(i%3, j%3, temp)

    def fillBtClicked(self):
        self.insertListDoubt = []                                                        #待验证的填充序列
        while True:
            self.reloadSudokuNum()                                                    #重新加载self.sudokuNum
            falseHappen = self.checkCorrect()                                     #确认待验证的填充序列的正确性
            if falseHappen == 1:
                while len(self.insertListDoubt[len(self.insertListDoubt)-1]) == 1:
                    self.insertListDoubt.pop()                                         #若待验证的填充序列的最后一项只有一种可能，则将其去除，直到包含两种以上可能性的分叉点
                self.insertListDoubt[len(self.insertListDoubt)-1].pop()       #在包含两种以上可能的分叉点，去除后一项
                continue                                                                  #跳过本次循环，进入下一次循环，用更新过的待验证填充序列继续进行
            findNewOne = self.findOnlyOne()                                       #寻找有没有新出现的可以确定的位置
            if findNewOne == 1:
                self.insertListDoubt.append(self.currentInsert)                 #若有新出现的确定位置，则将其填充到待验证序列中
            else:
                allSettle = self.findOnlyTwo()                                       #查找新出现的分叉点
                if allSettle == 1:
                    falseHappen = self.checkCorrect()                            #确认是否完全填充
                    if falseHappen == 0:
                        break                                                              #若完全填充，则跳出填充循环
                self.insertListDoubt.append(self.currentInsert)                #若未完全填充，则将其加入到待验证的填充序列中
        for i in range(9):
            for j in range(9):
                self.setSudokuGrid(self.sudokuNum[i][j][0], i//3, j//3, i%3, j%3)
        self.fillBt.setEnabled(False)
        
    def checkCorrect(self):
        #确认每一行、每一列和每一个3*3单元内是否存在重复错误
        for i in range(9):
            once = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for j in range(9):
                if len(self.sudokuNum[i][j]) == 1:
                    once[self.sudokuNum[i][j][0]-1] += 1
            if 2 in once:
                return 1
        
        for j in range(9):
            once = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(9):
                if len(self.sudokuNum[i][j]) == 1:
                    once[self.sudokuNum[i][j][0]-1] += 1
            if 2 in once:
                return 1
                
        for i in range(3):
            for j in range(3):
                once = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for p in range(3):
                    for q in range(3):
                        if len(self.sudokuNum[i*3+p][j*3+q]) == 1:
                            once[self.sudokuNum[i*3+p][j*3+q][0]-1] += 1
                if 2 in once:
                    return 1
        return 0
        
    def reloadSudokuNum(self):
        #重新加载self.sudokuNum
        for i in range(9):
            for j in range(9):
                self.sudokuNum[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in self.insertListConfirmed:
            self.sudokuNum[i[0][0]][i[0][1]] = [i[0][2]]
            self.removeOthers(i[0][0], i[0][1], i[0][2])
            self.newOnlyOne[i[0][0]][i[0][1]] = 1
        for i in self.insertListDoubt:
            k = len(i) - 1
            self.sudokuNum[i[k][0]][i[k][1]] = [i[k][2]]
            self.removeOthers(i[k][0], i[k][1], i[k][2])
            self.newOnlyOne[i[k][0]][i[k][1]] = 1
            
    def findOnlyTwo(self):
        #若没有新的唯一点，则查找分叉点
        self.currentInsert = []
        short = 9
        minX = 9
        minY = 9
        for i in range(9):
            for j in range(9):
                length = len(self.sudokuNum[i][j])
                if length < short:
                    if length > 1:
                        short = length
                        minX = i
                        minY = j
        if minX != 9 and minY != 9:
            for i in self.sudokuNum[minX][minY]:
                self.currentInsert.append([minX, minY, i])
        else:
            return 1
            
    def findOnlyOne(self):
        #查找隐藏或显式的新唯一点
        self.currentInsert = []
        
        #查找每行中是否存在新唯一点
        for i in range(9):
            appearTimes = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for j in range(9):
                for length in range(len(self.sudokuNum[i][j])):
                    appearTimes[self.sudokuNum[i][j][length]-1] += 1
            for p in range(9):
                if appearTimes[p] == 1:
                    for j in range(9):
                        if p+1 in self.sudokuNum[i][j]:
                            if self.newOnlyOne[i][j] == 0:
                                self.currentInsert.append([i, j, p+1])
                                return 1
                                
        #查找每列中是否存在新唯一点
        for j in range(9):
            appearTimes = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(9):
                for length in range(len(self.sudokuNum[i][j])):
                    appearTimes[self.sudokuNum[i][j][length]-1] += 1
            for p in range(9):
                if appearTimes[p] == 1:
                    for i in range(9):
                        if p+1 in self.sudokuNum[i][j]:
                            if self.newOnlyOne[i][j] == 0:
                                self.currentInsert.append([i, j, p+1])
                                return 1
                                
        #查找每个3*3单元中是否存在新唯一点
        for i in range(3):
            for j in range(3):
                appearTimes = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for p in range(3):
                    for q in range(3):
                        for length in range(len(self.sudokuNum[i*3+p][j*3+q])):
                            appearTimes[self.sudokuNum[i*3+p][j*3+q][length]-1] += 1
                for o in range(9):
                    if appearTimes[o] == 1:
                        for p in range(3):
                            for q in range(3):
                                if o+1 in self.sudokuNum[i*3+p][j*3+q]:
                                    if self.newOnlyOne[i*3+p][j*3+q] == 0:
                                        self.currentInsert.append([i*3+p, j*3+q, o+1])
                                        return 1
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Su = SudokuGrid()
    app.exit(app.exec_())

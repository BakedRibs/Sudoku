import sys
from PyQt5.QtWidgets import QWidget, QTableWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QAbstractItemView, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SudokuGrid(QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()
        
    def Init_UI(self):
        self.setWindowTitle('SUDOKU')
        
        self.sudokuGrid = []
        for i in range(3):
            self.sudokuGrid.append([])
            for j in range(3):
                smallGrid = QTableWidget(3, 3)
                smallGrid.setEditTriggers(QAbstractItemView.NoEditTriggers)
                smallGrid.setSelectionMode(QAbstractItemView.NoSelection)
                smallGrid.verticalHeader().setVisible(False)
                smallGrid.horizontalHeader().setVisible(False)
                smallGrid.setFixedSize(92, 92)
                for r in range(3):
                    smallGrid.setRowHeight(r, 30)
                    smallGrid.setColumnWidth(r, 30)
                self.sudokuGrid[i].append(smallGrid)
                
        self.fillBt = QPushButton('NextMove')
                
        sudokuLayout = QGridLayout()
        sudokuLayout.setSpacing(1)
        for i in range(3):
            for j in range(3):
                sudokuLayout.addWidget(self.sudokuGrid[i][j], i, j)
        
        controlLayout = QHBoxLayout()
        controlLayout.addStretch()
        controlLayout.addWidget(self.fillBt)
        controlLayout.addStretch()
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(sudokuLayout)
        mainLayout.addLayout(controlLayout)
        
        self.setLayout(mainLayout)
        self.show()
        self.sudokuGridInit()
        self.fillBt.clicked.connect(self.fillBtClicked)
        
    def sudokuGridInit(self):
        for i in range(3):
            for j in range(3):
                for p in range(3):
                    for q in range(3):
                        self.setSudokuGrid('', i, j, p, q)
                        
        self.newOne = []
        for i in range(9):
            self.newOne.append([])
            for j in range(9):
                self.newOne[i].append(0)
                
        self.sudokuNumInit()
                
        self.insertList = []
        self.insertList.append([1, 2, 2])
        self.insertList.append([1, 4, 5])
        self.insertList.append([0, 6, 1])
        self.insertList.append([0, 8, 3])
        self.insertList.append([3, 0, 1])
        self.insertList.append([3, 5, 7])
        self.insertList.append([4, 3, 9])
        self.insertList.append([4, 5, 3])
        self.insertList.append([4, 7, 5])
        self.insertList.append([5, 2, 4])
        self.insertList.append([5, 7, 2])
        self.insertList.append([6, 0, 7])
        self.insertList.append([7, 0, 3])
        self.insertList.append([7, 4, 6])
        self.insertList.append([8, 4, 4])
        self.insertList.append([8, 6, 2])
        self.insertList.append([8, 7, 6])
        
        for i in range(len(self.insertList)):
            self.setGridItem(self.insertList[i][0], self.insertList[i][1], self.insertList[i][2])
        
        self.showAllAlone()
        
    def setGridItem(self, row, column, number):
        i = row // 3
        j = column // 3
        ii = row % 3
        jj = column % 3
        self.setSudokuGrid(number, i, j, ii, jj)
        self.sudokuNum[row][column] = [number]
        self.removeOthers(row, column, number)
        
    def sudokuNumInit(self):
        self.sudokuNum = []
        for i in range(9):
            self.sudokuNum.append([])
            for j in range(9):
                smallNum = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.sudokuNum[i].append(smallNum)
        
    def removeOthers(self, row, column, number):
        i = row // 3
        j = column // 3
        for o in range(9):
            self.removeNum(row, o, number)
            self.removeNum(o, column, number)
        for p in range(3):
            for q in range(3):
                self.removeNum(i*3+p, j*3+q, number)
            
    def removeNum(self, row, column, number):
        numLen = len(self.sudokuNum[row][column])
        if numLen == 1:
            return
        if number in self.sudokuNum[row][column]:
            self.sudokuNum[row][column].remove(number)
            if len(self.sudokuNum[row][column]) == 1:
                self.newOne[row][column] = 1
            
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
        lenTotal = 0
        for i in range(9):
            for j in range(9):
                lenTotal += len(self.sudokuNum[i][j])
        while lenTotal > 81:
            lenMinButOne = 9
            minI = 0
            minJ = 0
            for i in range(9):
                for j in range(9):
                    self.newOne[i][j] = 0
                    if len(self.sudokuNum[i][j]) <= lenMinButOne:
                        if len(self.sudokuNum[i][j]) != 1:
                            lenMinButOne = len(self.sudokuNum[i][j])
                            minI = i
                            minJ = j

            currentInsert = []
            for cur in range(lenMinButOne):
                currentInsert.append([minI, minJ, self.sudokuNum[minI][minJ][cur]])
            self.insertList.append(currentInsert)
            self.removeOthers(minI, minJ, currentInsert[len(currentInsert)-1][2])
            checkRe = self.checkOne()
            if checkRe == 1:
                checkRe = 0
            pass
            
    def checkOne(self):
        for i in range(9):
            for j in range(9):
                if self.newOne[i][j] == 1:
                    for p in range(9):
                        if len(self.sudokuNum[i][p]) == 1:
                            if p != j:
                                if self.sudokuNum[i][j] == self.sudokuNum[i][p]:
                                    return 1
                        if len(self.sudokuNum[p][j]) == 1:
                            if p != i:
                                if self.sudokuNum[i][j] == self.sudokuNum[p][j]:
                                    return 1
                    for p in range(3):
                        for q in range(3):
                            iD = i // 3
                            jD = j // 3
                            iY = i % 3
                            jY = j % 3
                            if len(self.sudokuNum[iD*3+p][jD*3+q]) == 1:
                                if (p != iY) or (q != jY):
                                   if self.sudokuNum[i][j] == self.sudokuNum[iD*3+p][jD*3+q]:
                                       return 1
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Su = SudokuGrid()
    app.exit(app.exec_())

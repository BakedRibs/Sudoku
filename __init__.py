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
        self.sudokuNew = []
        for i in range(3):
            self.sudokuGrid.append([])
            self.sudokuNew.append([])
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
                self.sudokuNew[i].append([])
        
        self.sudokuNum = []
        self.sudokuCheck = []
        for i in range(9):
            self.sudokuNum.append([])
            self.sudokuCheck.append([])
            for j in range(9):
                smallNum = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.sudokuNum[i].append(smallNum)
                self.sudokuCheck[i].append(0)
                
        self.sudokuGridInit()
                
        sudokuLayout = QGridLayout()
        sudokuLayout.setSpacing(1)
        for i in range(3):
            for j in range(3):
                sudokuLayout.addWidget(self.sudokuGrid[i][j], i, j)
                
        self.nextMoveBt = QPushButton('NextMove')
        
        controlLayout = QHBoxLayout()
        controlLayout.addStretch()
        controlLayout.addWidget(self.nextMoveBt)
        controlLayout.addStretch()
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(sudokuLayout)
        mainLayout.addLayout(controlLayout)
        
        self.setLayout(mainLayout)
        self.show()
        
        self.nextMoveBt.clicked.connect(self.nextMoveBtClicked)
        
    def sudokuGridInit(self):
        self.setGridItem(1, 2, 2)
        self.setGridItem(1, 4, 5)
        self.setGridItem(0, 6, 1)
        self.setGridItem(0, 8, 3)
        self.setGridItem(3, 0, 1)
        self.setGridItem(3, 5, 7)
        self.setGridItem(4, 3, 9)
        self.setGridItem(4, 5, 3)
        self.setGridItem(4, 7, 5)
        self.setGridItem(5, 2, 4)
        self.setGridItem(5, 7, 2)
        self.setGridItem(6, 0, 7)
        self.setGridItem(7, 0, 3)
        self.setGridItem(7, 4, 6)
        self.setGridItem(8, 4, 4)
        self.setGridItem(8, 6, 2)
        self.setGridItem(8, 7, 6)
        self.showAllAlone()
        
    def setGridItem(self, row, column, number):
        i = row // 3
        j = column // 3
        ii = row % 3
        jj = column % 3
        self.setSudokuGrid(number, i, j, ii, jj)
        self.sudokuNum[row][column] = [number]
        self.removeOthers(row, column, number)
        
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
            
    def setSudokuGrid(self, number, i, j, ii, jj):
        temp = QTableWidgetItem(str(number))
        temp.setTextAlignment(Qt.AlignCenter)
        temp.setFont(QFont("Microsoft YaHei", 18))
        self.sudokuGrid[i][j].setItem(ii, jj, temp)
        
    def nextMoveBtClicked(self):
        for i in range(3):
            for j in range(3):
                numCount = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for p in range(3):
                    for q in range(3):
                        for n in self.sudokuNum[i*3+p][j*3+q]:
                            numCount[n-1] = numCount[n-1] + 1
                for b in range(9):
                    if numCount[b] == 1:
                        if b+1 in self.sudokuNew[i][j]:
                            pass
                        else:
                            for p in range(3):
                                for q in range(3):
                                    if b+1 in self.sudokuNum[i*3+p][j*3+q]:
                                        self.setSudokuGrid(b+1, i, j, p, q)
        
    def showAllAlone(self):
        for i in range(9):
            for j in range(9):
                numLen = len(self.sudokuNum[i][j])
                if numLen == 1:
                    temp = QTableWidgetItem(str(self.sudokuNum[i][j][0]))
                    temp.setTextAlignment(Qt.AlignCenter)
                    temp.setFont(QFont("Microsoft YaHei", 18))
                    self.sudokuGrid[i//3][j//3].setItem(i%3, j%3, temp)
                    self.sudokuCheck[i][j] = 1
                    self.sudokuNew[i//3][j//3].append(self.sudokuNum[i][j][0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Su = SudokuGrid()
    app.exit(app.exec_())

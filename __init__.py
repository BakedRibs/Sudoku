import sys
from PyQt5.QtWidgets import QWidget, QTableWidget, QGridLayout, QVBoxLayout, QApplication, QAbstractItemView, QTableWidgetItem
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
        
        self.sudokuNum = []        
        for i in range(9):
            self.sudokuNum.append([])
            for j in range(9):
                smallNum = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.sudokuNum[i].append(smallNum)
                
        self.sudokuGridInit()
                
        sudokuLayout = QGridLayout()
        sudokuLayout.setSpacing(1)
        for i in range(3):
            for j in range(3):
                sudokuLayout.addWidget(self.sudokuGrid[i][j], i, j)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(sudokuLayout)
        
        self.setLayout(mainLayout)
        #self.setMinimumSize(300, 300)
        self.show()
        
    def sudokuGridInit(self):
        self.setGridItem(1, 2, 2)
        pass
        
    def setGridItem(self, row, column, number):
        i = row // 3
        j = column // 3
        ii = row % 3
        jj = column % 3
        temp = QTableWidgetItem(str(number))
        temp.setTextAlignment(Qt.AlignCenter)
        temp.setFont(QFont("Microsoft YaHei", 18))
        self.sudokuGrid[i][j].setItem(ii, jj, temp)
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
                self.removeNum(i+p, j+q, number)
            
    def removeNum(self, row, column, number):
        numLen = len(self.sudokuNum[row][column])
        if numLen == 1:
            return
        if number in self.sudokuNum[row][column]:
            self.sudokuNum[row][column].remove(number)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Su = SudokuGrid()
    app.exit(app.exec_())

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

        self.openFileBt = QPushButton('打开文件')
        self.fillBt = QPushButton('填充数独')
        self.fillBt.setEnabled(False)

        sudokuLayout = QGridLayout()
        sudokuLayout.setSpacing(1)
        for i in range(3):
            for j in range(3):
                sudokuLayout.addWidget(self.sudokuGrid[i][j], i, j)

        controlLayout = QHBoxLayout()
        controlLayout.addStretch()
        controlLayout.addWidget(self.openFileBt)
        controlLayout.addWidget(self.fillBt)
        controlLayout.addStretch()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(sudokuLayout)
        mainLayout.addLayout(controlLayout)

        self.setLayout(mainLayout)
        self.show()
        self.sudokuGridInit()
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
            self.newOnlyOne.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

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
                        self.insertListConfirmed.append([[i, j, self.insertArray[i][j]]])
            for i in range(len(self.insertListConfirmed)):
                self.setGridItem(self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][0], self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][1], self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][2])
                self.newOnlyOne[self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][0]][self.insertListConfirmed[i][len(self.insertListConfirmed[i])-1][1]] = 1
            self.showAllAlone()
            self.fillBt.setEnabled(True)

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
        self.insertListDoubt = []
        while True:
            self.reloadSudokuNum()
            falseHappen = self.checkCorrect()
            if falseHappen == 1:
                while len(self.insertListDoubt[len(self.insertListDoubt)-1]) == 1:
                    self.insertListDoubt.pop()
                self.insertListDoubt[len(self.insertListDoubt)-1].pop()
                continue
            findNewOne = self.findOnlyOne()
            if findNewOne == 1:
                self.insertListDoubt.append(self.currentInsert)
            else:
                allSettle = self.findOnlyTwo()
                if allSettle == 1:
                    falseHappen = self.checkCorrect()
                    if falseHappen == 0:
                        break
                self.insertListDoubt.append(self.currentInsert)
            asd = 0
        for i in range(9):
            for j in range(9):
                self.setSudokuGrid(self.sudokuNum[i][j][0], i//3, j//3, i%3, j%3)
        self.fillBt.setEnabled(False)
        
    def checkCorrect(self):
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
        self.currentInsert = []
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

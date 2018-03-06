import sys
from PyQt5.QtWidgets import QWidget, QTableWidget, QGridLayout, QVBoxLayout, QApplication, QAbstractItemView

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Su = SudokuGrid()
    app.exit(app.exec_())

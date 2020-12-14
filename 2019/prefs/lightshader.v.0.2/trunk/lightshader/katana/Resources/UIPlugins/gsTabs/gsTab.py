try:
    from Katana import QtGui, QtCore, QtWidgets
except:
    from Katana import QtCore, QtGui as QtWidgets
from Katana import UI4, NodegraphAPI
import math

STYLES = {
          'regular': "background-color:#262626;",
          'orange': "background-color:#2e2e2e;"
                    "color: orange;"
                    "font: bold 13px;"
                    "padding: 6px;",
          'red': "background-color: #b31c19; font: 13px",
          'lineEndit': "background-color: #2e2e2e;"
                       "font: bold 13px;"
                       "selection-background-color: orange;"
                       "selection-color: black;",
}

class pbNewGSV(QtWidgets.QDialog):
    def __init__(self):
        super(pbNewGSV, self).__init__()
        self.__masterLayout = QtWidgets.QVBoxLayout(self)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.returnPressed.connect(self.addGSV)
        self.lineEdit.setStyleSheet(STYLES['lineEndit'])
        self.__masterLayout.addWidget(self.lineEdit)

        self.windowProperties()

    def windowProperties(self):
        self.move(QtGui.QCursor.pos()-QtCore.QPoint(self.width()/6, 20))
        self.setWindowOpacity(0.5)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.installEventFilter(self)

    def addGSV(self):
        gsvName = self.lineEdit.text()
        if gsvName=='':
            return
        else:
            newGSV = NodegraphAPI.GetRootNode().getParameter("variables").createChildGroup(str(gsvName))
            newGSV.createChildNumber('enable', 1)
            newGSV.createChildStringArray('options', 0)
            newGSV.createChildString('value', '')

        self.close()

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate, QtCore.QEvent.FocusOut]:
            self.close()
            return True
        return False

class GS_button(QtWidgets.QPushButton):
    """Custom QPushButton"""
    def __init__(self, name, button_width, parent=None):
        super(GS_button, self).__init__(parent)
        self.setMouseTracking(True)
        self.setText(name)
        self.setMinimumWidth(button_width / 2)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Preferred)
        self.setStyleSheet(STYLES['regular'])

    def enterEvent(self, event):
        if not self.styleSheet() == STYLES['red']:
            self.setStyleSheet(STYLES['orange'])

    def leaveEvent(self, event):
        if not self.styleSheet() == STYLES['red']:
            self.setStyleSheet(STYLES['regular'])

class LineEdit(QtWidgets.QLineEdit):
    """Custom QLineEdit"""
    def __init__(self, parent, layer_list):
        super(LineEdit, self).__init__(parent)
        self.parent = parent
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Preferred)
        self.completer = QtWidgets.QCompleter(layer_list, self)
        # self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)  # pylint: disable=line-too-long
        self.setCompleter(self.completer)
        self.completer.activated.connect(self.returnPressed)
        self.setStyleSheet(STYLES['lineEndit'])

class pbGSManager(QtWidgets.QDialog):
    def __init__(self):
        super(pbGSManager, self).__init__()
        self.removeList = []
        root = NodegraphAPI.GetRootNode()
        self.currentVar = root.getParameter('gsVal').getValue(0)
        self.currentVal = root.getParameter('variables.{}.value'.format(self.currentVar))

        self.__masterLayout = QtWidgets.QVBoxLayout(self)
        self.buildUI()
        self.windowProperties()
        self.hideInputWidget()

    def buildUI(self):
        variables = self.getGSvalues()
        length = math.ceil(math.sqrt(len(variables) + 1))
        width, height = length * 200, length * 50
        self.setFixedSize(width, height)
        self.offset = QtCore.QPoint(width * 0.5, height * 0.5)

        columnCNTR, rowCNTR = 0, 0
        button_width = width / length

        self.grid = QtWidgets.QGridLayout()
        self.controlRow = QtWidgets.QHBoxLayout()

        for var in variables:
            button = GS_button(var, button_width)
            button.clicked.connect(self.varClicked)
            self.grid.addWidget(button, rowCNTR, columnCNTR)

            if columnCNTR > int(length):
                rowCNTR += 1
                columnCNTR = 0

            else:
                columnCNTR += 1

        self.input = LineEdit(self, variables)
        self.grid.addWidget(self.input, rowCNTR, columnCNTR)
        self.input.returnPressed.connect(self.line_enter)

        addBtn = QtWidgets.QPushButton('vs')
        addBtn.setStyleSheet(STYLES['orange'])
        addBtn.clicked.connect(self.createVSnode)

        self.newGSname = QtWidgets.QLineEdit()
        self.newGSname.setMinimumWidth(250)
        self.newGSname.setPlaceholderText("add new options")
        self.newGSname.setStyleSheet(STYLES['lineEndit'])
        self.newGSname.setFixedHeight(30)
        self.newGSname.returnPressed.connect(self.addNewVar)

        removeGSVBtn = QtWidgets.QPushButton('X')
        removeGSVBtn.setStyleSheet(STYLES['orange'])
        removeGSVBtn.clicked.connect(self.deleteGSV)

        self.controlRow.addWidget(addBtn)
        self.controlRow.addWidget(self.newGSname)
        self.controlRow.addWidget(removeGSVBtn)

        self.__masterLayout.addLayout(self.controlRow)
        self.__masterLayout.addLayout(self.grid)

    def deleteGSV(self):
        variables = NodegraphAPI.GetRootNode().getParameter('variables')
        variables.deleteChild(variables.getChild(self.currentVar))
        self.close()

    def getGSvalues(self):
        variables = []
        for i in NodegraphAPI.GetRootNode().getParameter('variables.{}.options'.format(self.currentVar))\
                .getChildren():
            variables.append(i.getValue(0))
        variables.sort()
        return variables

    def windowProperties(self):
        self.move(QtGui.QCursor.pos() - self.offset)
        self.setWindowOpacity(0.9)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #make sure the widgets closes when it loses focus
        self.installEventFilter(self)
        self.input.setFocus()

    def varClicked(self):
        gsValue = self.sender().text()
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            channel = self.sender().text()
            if channel in self.removeList:
                self.removeList.remove(channel)
                self.sender().setStyleSheet(STYLES['regular'])
            else:
                self.sender().setStyleSheet(STYLES['red'])
                self.removeList.append(channel)

        elif modifiers == QtCore.Qt.ControlModifier:
            vsNode = NodegraphAPI.CreateNode('VariableSet', parent=NodegraphAPI.GetRootNode())
            vsNode.setName('vSet_{}_{}'.format(self.currentVar.upper(), str(self.sender().text())))
            vsNode.getParameter('variableName').setValue(self.currentVar, 0)
            vsNode.getParameter('variableValue').setValue(str(self.sender().text()), 0)
            nodegraphTab = UI4.App.Tabs.FindTopTab('Node Graph')
            if nodegraphTab:
                nodegraphTab.floatNodes([vsNode])
            self.close()
        else:
            self.currentVal.setValue(str(gsValue), 0)

    def line_enter(self):
        self.currentVal.setValue(str(self.input.text()), 0)
        self.close()

    def addNewVar(self):
        varName = self.newGSname.text()
        if varName=="":
            return
        currentVar = NodegraphAPI.GetRootNode().getParameter('variables.{}'.format(self.currentVar))
        # Get an array of options
        child = currentVar.getChild('options')
        # Get number of values
        array_length = child.getNumChildren()
        # Resize array to fit more
        child.resizeArray(array_length + 1)
        # Set the value

        child.getChildByIndex(array_length).setValue(str(varName), 0)

        currentVar.getChild('value').setValue(child.getChildByIndex(array_length).getValue(0), 0)

        self.reDrawUI()
        self.newGSname.setText('')
        self.newGSname.setFocus()

    def removeVars(self):
        currentVar = NodegraphAPI.GetRootNode().getParameter('variables.{}'.format(self.currentVar))
        child = currentVar.getChild('options')
        for var in self.removeList:
            if currentVar.getChild('value').getValue(0) == str(var):
                currentVar.getChild('value').setValue('', 0)
            array_length = child.getNumChildren()
            for i in child.getChildren():
                if i.getValue(0) == str(var):
                    child.reorderChild(i, array_length - 1)
                    child.resizeArray(array_length - 1)

        self.reDrawUI()
        self.hideInputWidget()

    def reDrawUI(self):
        self.removeList = []
        self.grid.setParent(None)
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setVisible(False)
        self.grid.deleteLater()

        self.controlRow.setParent(None)
        self.controlRow.deleteLater()
        self.buildUI()

    def hideInputWidget(self):
        if len(self.getGSvalues())== 0:
            self.input.setHidden(True)

    def createVSnode(self):
        vsNode = NodegraphAPI.CreateNode('VariableSwitch', parent=NodegraphAPI.GetRootNode())
        vsNode.setName('vs_{}'.format(self.currentVar))
        vsNode.getParameter('variableName').setValue(self.currentVar, 0)
        variables = NodegraphAPI.GetRootNode().getParameter('variables.{}.options'.format(self.currentVar))\
                .getChildren()
        for i in variables:
            if len(self.removeList) == 0:
                vsNode.addInputPort(i.getValue(0))
            else:
                if i.getValue(0) in self.removeList:
                    vsNode.addInputPort(i.getValue(0))
        nodegraphTab = UI4.App.Tabs.FindTopTab('Node Graph')
        if nodegraphTab:
            nodegraphTab.floatNodes([vsNode])
        self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_Delete:
            self.removeVars()

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate, QtCore.QEvent.FocusOut]:
            self.close()
            return True
        return False

def start():
    start.panel = pbGSManager()
    start.panel.show()

def newGSV():
    start.panel = pbNewGSV()
    start.panel.show()

try:
    from Katana import QtGui, QtCore, QtWidgets
except:
    from Katana import QtCore, QtGui as QtWidgets

from Katana import UI4, QT4Widgets, QT4FormWidgets
from Katana import NodegraphAPI, Utils
from Katana import UniqueName, FormMaster
import re
import os


aovList = [
    "RGBA",
    "N",
    "P",
    "Z",
    "background",
    "albedo",
    "direct",
    "indirect",
    "opacity",
    "coat",
    "coat_albedo",
    "coat_direct",
    "coat_indirect",
    "diffuse",
    "diffuse_albedo",
    "diffuse_direct",
    "diffuse_indirect",
    "emission",
    "specular",
    "specular_albedo",
    "specular_direct",
    "specular_indirect",
    "sss",
    "sss_albedo",
    "sss_direct",
    "sss_indirect",
    "transmission",
    "transmission_albedo",
    "transmission_direct",
    "transmission_indirect",
    "volume",
    "volume_albedo",
    "volume_direct",
    "volume_indirect",
    "crypto_asset",
    "crypto_material",
    "crypto_object",
]

class ArnoldAOVsEditor(QtWidgets.QWidget):
    def __init__(self, parent, node):
        node.upgrade()

        self.__node = node

        QtWidgets.QWidget.__init__(self, parent)

        self.__frozen = True
        self.__updateTreeOnIdle = False
        self.__selectedPonyPolicy = None
        self.__preselectName = None

        self.__buildUI()

        self.__populate()

    def __buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        fileLayout = QtWidgets.QHBoxLayout()

        formatLayout = QtWidgets.QHBoxLayout()

        filenamePolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.__node.getParameter('Filename'))
        factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory
        filenameLine = factory.buildWidget(self, filenamePolicy)
        fileLayout.addWidget(filenameLine)

        formatPolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.__node.getParameter('Format'))
        formatParam = factory.buildWidget(self, formatPolicy)

        BitDepthPolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.__node.getParameter('BitDepth'))
        BitDepthParam = factory.buildWidget(self, BitDepthPolicy)

        tiledPolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.__node.getParameter('Tiled'))
        tiledParam = factory.buildWidget(self, tiledPolicy)

        mergePolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.__node.getParameter('MergeAOVs'))
        mergeParam = factory.buildWidget(self, mergePolicy)

        formatLayout.addWidget(formatParam)
        formatLayout.addWidget(BitDepthParam)
        formatLayout.addWidget(tiledParam)

        overallListLayout = QtWidgets.QHBoxLayout()

        globalListLayout = QtWidgets.QVBoxLayout()
        sceneListLayout = QtWidgets.QVBoxLayout()

        __labelAOV1 = QtWidgets.QLabel('AOV List')
        __labelAOV2 = QtWidgets.QLabel('Scene AOVs')
        globalListLayout.addWidget(__labelAOV1)
        sceneListLayout.addWidget(__labelAOV2)

        self.globalAovsList = QtWidgets.QListWidget()
        self.globalAovsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.globalAovsList.itemDoubleClicked.connect(self.__addButtonClicked)
        globalListLayout.addWidget(self.globalAovsList)

        self.scenAovsList = QtWidgets.QListWidget()
        self.scenAovsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.scenAovsList.itemDoubleClicked.connect(self.__removeButtonClicked)
        self.scenAovsList.itemClicked.connect(self.showNodeParams)
        sceneListLayout.addWidget(self.scenAovsList)

        btnLayout = QtWidgets.QHBoxLayout()
        __addAovBtn = QtWidgets.QPushButton('>>')
        __addAovBtn.clicked.connect(self.__addButtonClicked)
        globalListLayout.addWidget(__addAovBtn)

        customBtn = QtWidgets.QPushButton('Custom')
        customBtn.clicked.connect(self.__customClicket)
        btnLayout.addWidget(customBtn)

        __removeAovBtn = QtWidgets.QPushButton('<<')
        __removeAovBtn.clicked.connect(self.__removeButtonClicked)
        btnLayout.addWidget(__removeAovBtn)

        __scrollWidget = QtWidgets.QWidget()
        # __scrollWidget.setMinimumHeight(350)
        __scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.scrollLayout = QtWidgets.QVBoxLayout(__scrollWidget)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        scrollArea.setMinimumHeight(200)
        scrollArea.setWidget(__scrollWidget)

        sceneListLayout.addLayout(btnLayout)
        overallListLayout.addLayout(globalListLayout)
        overallListLayout.addLayout(sceneListLayout)

        layout.addLayout(fileLayout)
        layout.addLayout(formatLayout)
        layout.addWidget(mergeParam)
        layout.addWidget(QHLine())
        layout.addLayout(overallListLayout)
        # layout.addLayout(btnLayout)
        layout.addWidget(scrollArea)
        # layout.addStretch()

    def showNodeParams(self):
        self.__clearCmd()

        vertSpacer = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        vertSpacer1 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)

        factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory
        name = self.scenAovsList.currentItem().text()
        for node in self.__node.getChildren():
            if node.getParameter('aov'):
                if node.getParameter('aov').getValue(0) == name:
                    self.aov=node

        self.aocd = self.aov.getChildByIndex(0)
        self.rod = self.aov.getChildByIndex(1)

        typePolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.aocd.getParameter('type'))
        typeParam = factory.buildWidget(self, typePolicy)

        filterPolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.aocd.getParameter('filter'))
        filterParam = factory.buildWidget(self, filterPolicy)

        lpePolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.aocd.getParameter('lightPathExpression'))
        lpeParam = factory.buildWidget(self, lpePolicy)

        lGrpPolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.aocd.getParameter('lightGroups'))
        lGrpParam = factory.buildWidget(self, lGrpPolicy)

        cust_lGrpPolicy = UI4.FormMaster.CreateParameterPolicy(
            None, self.aocd.getParameter('customLightGroup'))
        cust_lGrpParam = factory.buildWidget(self, cust_lGrpPolicy)

        self.__nameLine = QtWidgets.QLineEdit('')
        self.__nameLine.setText(str(self.aocd.getParameter('name').getValue(0)))
        self.__nameLine.returnPressed.connect(self.__nameReturnPressed)

        nameLayout = QtWidgets.QHBoxLayout()
        self.__label = QtWidgets.QLabel('AOV Name')
        nameLayout.addWidget(self.__label)
        nameLayout.addWidget(self.__nameLine)

        self.scrollLayout.addItem(vertSpacer1)
        self.scrollLayout.addLayout(nameLayout)
        self.scrollLayout.addWidget(QHLine())
        self.scrollLayout.addWidget(typeParam)
        self.scrollLayout.addWidget(filterParam)
        self.scrollLayout.addWidget(QHLine())

        self.scrollLayout.addWidget(lpeParam)
        self.scrollLayout.addWidget(lGrpParam)
        self.scrollLayout.addWidget(cust_lGrpParam)

        self.scrollLayout.addItem(vertSpacer)

    def __nameReturnPressed(self):
        name = self.__nameLine.text()
        self.aov.setName('_AOV_'+str(name))
        self.aov.getParameter('aov').setValue(str(name), 0)
        self.aocd.setName('AOCD_'+str(name))
        self.aocd.getParameter('name').setValue(str(name), 0)
        self.aocd.getParameter('channel').setValue(str(name), 0)
        self.rod.setName('ROD_'+str(name))
        self.rod.getParameter('outputName').setValue(str(name), 0)
        self.rod.getParameter('args.renderSettings.outputs.outputName.'
                              'rendererSettings.channel.value').setValue(str(name), 0)

        self.__populate()

    def __clearCmd(self):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                widget.setVisible(False)
                widget.deleteLater()
                self.__nameLine.setVisible(False)
                self.__nameLine.deleteLater()
                self.__label.setVisible(False)
                self.__label.deleteLater()

    def __openDialog(self):
        filenameParam = self.__node.getParameter('Filename')
        filename = UI4.Util.AssetId.BrowseForAsset('', 'Textures Path', True,
                                                   {'fileTypes': 'none', 'acceptDir': True, 'acceptFile': False})

        if filename:
            if os.path.splitext(os.path.split(filename)[-1])[-1]:
                filename = filename
            else:
                filename = filename+str(os.path.split(filenameParam.getValue(0))[-1])
            filenameParam.setValue(filename, 0)

    def __countAovs(self):
        aovs=[]
        for i in range(self.globalAovsList.count()):
            aovs.append(self.globalAovsList.item(i).text())

    def __getSceneAovs(self):
        sceneAovs = []
        for i in self.__node.getChildren():
            if i.getParameter('aov'):
                sceneAovs.append(i.getParameter('aov').getValue(0))
        # for node in self.__node.getChildren():
        #     if node.getType() == 'Group' and '_MERGE_SETUP_' not in node.getName():
        #         # cleaned = re.sub(r'\d+$', '', str(node.getName()).replace('_AOV_', ''))
        #         sceneAovs.append(str(node.getName()).replace('_AOV_', ''))
        return sceneAovs

    def __populate(self):
        self.globalAovsList.clear()
        self.scenAovsList.clear()

        sceneAovs = self.__getSceneAovs()
        # globalAovs = list(set(aovList)-set(sceneAovs))
        pip = []
        for i in sceneAovs:
            pip.append(re.sub(r'\d+$', '', i))
        globalAovs = [x for x in aovList if x not in pip]

        for aov in sorted(globalAovs):
            item = QtWidgets.QListWidgetItem(aov)
            self.globalAovsList.addItem(item)

        for aov in sorted(sceneAovs):
            item = QtWidgets.QListWidgetItem(aov)
            self.scenAovsList.addItem(item)

    def __customClicket(self):
        self.__node.addLayer('custom')
        self.__populate()

    def __addButtonClicked(self):
        for aov in self.globalAovsList.selectedItems():
            name = aov.text()
            if name == 'Z' or name == 'P' or name == 'N':
                self.__node.addLayer(str(name), 'closest_filter')
            else:
                self.__node.addLayer(str(name))

        self.__populate()

    def __removeButtonClicked(self):
        for aov in self.scenAovsList.selectedItems():
            for node in self.__node.getChildren():
                if node.getParameter('aov'):
                    if node.getParameter('aov').getValue(0) == aov.text():
                        aovNode = node
                        NodegraphAPI.Util.IsolateNode(aovNode)
                        aovNode.delete()
        self.__populate()
        self.__clearCmd()

    # We thaw/freeze the UI when it is shown/hidden.  This means that we aren't
    # wasting CPU cycles by listening and responding to events when the editor
    # is not active.
    def showEvent(self, event):
        QtWidgets.QWidget.showEvent(self, event)
        if self.__frozen:
            self.__frozen = False
        self.__populate()
            # self._thaw()

    def hideEvent(self, event):
        QtWidgets.QWidget.hideEvent(self, event)
        if not self.__frozen:
            self.__frozen = True
            # self._freeze()

    # def _thaw(self):
    #     self.__setupEventHandlers(True)
    #
    # def _freeze(self):
    #     self.__setupEventHandlers(False)


class QHLine(QtWidgets.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
# The following code shows how to register a custom NodeActionDelegate for
# the ArnoldAOVs node.
# NodeActionDelegates are subclasses of BaseNodeActionDelegate and allow to
# add QActions to the node's context menu and wrench menu



from UI4.FormMaster.NodeActionDelegate import BaseNodeActionDelegate

class ArnoldAOVsActionDelegate(BaseNodeActionDelegate.BaseNodeActionDelegate):
    class _AddPony(QtWidgets.QAction):
        def __init__(self, parent, node):
            QtWidgets.QAction.__init__(self, "Add Pony", parent)
            self.__node = node
            if node:
                self.triggered.connect(self.__triggered)
        def __triggered(self, checked):
            self.__node.addPony('pony')

    def addToWrenchMenu(self, menu, node, hints=None):
        menu.addAction(self._AddPony(menu, node))

    def addToContextMenu(self, menu, node):
        menu.addAction(self._AddPony(menu, node))


UI4.FormMaster.NodeActionDelegate.RegisterActionDelegate("ArnoldAOVs_LS", ArnoldAOVsActionDelegate())

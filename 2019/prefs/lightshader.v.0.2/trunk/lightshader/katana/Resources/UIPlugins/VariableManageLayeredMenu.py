from Katana import NodegraphAPI, LayeredMenuAPI
import gsTabs.gsTab as graphTab


def PopulateCallback(layeredMenu):
    variableNames = []
    for i in NodegraphAPI.GetRootNode().getParameter("variables").getChildren():
        variableNames.append(i.getName())
    variableNames.insert(0, "_gsvCreate_")

    for variable in variableNames:
        if variable == "_gsvCreate_":
            layeredMenu.addEntry(variable, text=" NEW GSV",
                                 color=(1, 1, 1), size=(130, 15))
        else:
            layeredMenu.addEntry(variable, text=variable,
                                 color=(0.95, 0.46, 0))
def ActionCallback(value):
    if value == "_gsvCreate_":
        ui = graphTab.newGSV()
    else:
        gsVal = NodegraphAPI.GetRootNode().getParameters().createChildString('gsVal', value)
        gsVal.setHintString(repr({'hide': 'True'}))
        ui = graphTab.start()
        a = NodegraphAPI.GetRootNode().getParameters()
        a.deleteChild(a.getChild('gsVal'))

layeredMenu=LayeredMenuAPI.LayeredMenu(PopulateCallback, ActionCallback,
                                       'Alt+X', alwaysPopulate=True,
                                       onlyMatchWordStart=False)
LayeredMenuAPI.RegisterLayeredMenu(layeredMenu, 'VariableManage')

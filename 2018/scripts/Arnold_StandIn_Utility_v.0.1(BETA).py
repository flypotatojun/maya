###Arnold_StandIn_utility - 2020- MrLixm
#FOR PERSONAL USE ONLY
#for commercial use contact me: monsieurlixm@gmail.com
#pro email: lcollod@gmail.com

import maya.cmds as mc
import pymel.core as pm
import os,glob
import functools as func
from mtoa.core import createStandIn


##############
VERSION= "v0.1(BETA)"
WINDN= 'Ai_StandIn'


bgcai= [0.314,0.677,0.717]
bgcgrey= [0.2,0.2,0.2]
bgcgreyl= [0.25,0.25,0.25]
bgcgreenM= [0,0.96,0.54]
bgcwhite= [0.95,0.95,0.95]
bgcgreyd= [0.18,0.18,0.18]
bgcblackl = [0.05,0.05,0.05]


##UI CHECKUP
###DELETE UI
if mc.window('%s' %WINDN, query=True, exists=True):
    mc.deleteUI('%s' %WINDN, window=True)
if mc.windowPref('%s' %WINDN, query=True, exists=True):
    mc.windowPref('%s' %WINDN, remove=True )
##DELETE INFO UI
if mc.windowPref('infoAiAssWind', query=True, exists=True):
    mc.windowPref('infoAiAssWind', remove=True )
if mc.window('infoAiAssWind', query=True, exists=True):
    mc.deleteUI('infoAiAssWind', window=True)



class AiFuncClass:

    def __init__(self):
        print 'init'
        self.projectPath = self.def_projectPath()
        self.export_sf =5

    def export_ass(self,*args):
        '''Function to export the standIn'''
        opTxtField = mc.textField("textFieldOptions", q=True,tx=True)
        file_path = mc.textField("textFieldFile", q=True,tx=True)
        meshList =  mc.ls(sl=True)
        selType = mc.iconTextButton('itbChkEsf',q=True,label=True)
        if selType=='On':
            assFileName = mc.textField("textFieldName", q=True,tx=True)
            file_pathName = os.path.join(file_path,assFileName+'.ass')
            mc.file(file_pathName,typ= r"ASS Export",pr=True,es=True,force=True,op=opTxtField)
        else:
            for meshs in meshList:
                mc.select(cl=True)
                mc.select(meshs)
                file_pathName = os.path.join(file_path,meshs.replace("|","")+'.ass')
                mc.file(file_pathName,typ= r"ASS Export",pr=True,es=True,force=True,op=opTxtField)
                #mc.arnoldExportAss(s=True, bb= True, f= "L:/PROJECTS/Enviro_motorbike_margot/Maya/enviro_bike_project/data/test.ass", mask=maskv, sl= 1, ll= 1,fp=True,cam = 'perspShape')

    def import_ass(self,*args):
        file_path = mc.textField("textFieldFile", q=True,tx=True)
        assFiles_list = glob.glob(os.path.join(file_path,"*.ass") )
        for assFile in assFiles_list:
            assName = os.path.basename(assFile).replace(".ass","")
            if mc.objExists(assName+'_aiStndn'):
                continue
            else:
                standin_node = createStandIn(path=assFile)
                mc.rename(mc.listRelatives(standin_node,p=True),assName+'_aiStndn')

    def resetField(self,*args):
        opTx = "-shadowLinks 1; -mask 6399; -lightLinks 1; -boundingBox; -fullPath"
        mc.textField("textFieldOptions", e=True,tx=opTx)

    def def_projectPath(self,*args):
        print"path"
        project_path = mc.workspace(q=True,rd=True)
        assets_project_path = os.path.join(project_path,"assets")
        ai_assets_path = os.path.join(assets_project_path,"StandIn_arnold")
        if not os.path.exists(ai_assets_path):
          os.makedirs(ai_assets_path)
        return ai_assets_path

    def fileDialog(self,*args):
        self.filePath=mc.fileDialog2(fm=2,dir=self.projectPath)
        mc.textField("textFieldFile",e=True,tx=self.filePath[0])
        return self.filePath

    def chkChange_esf(self,*args):
        itbState = mc.iconTextButton('itbChkEsf',q=True,label=True)
        if itbState == 'On':
            mc.rowColumnLayout("rclFielName", e=True,en=False)
            bgcItb = bgcgreyd
            labelItb = 'Off'
        else:
            mc.rowColumnLayout("rclFielName", e=True,en=True)
            bgcItb=bgcai
            labelItb = 'On'

        mc.iconTextButton('itbChkEsf',e=True,bgc=bgcItb,label=labelItb)


    def closeWind(*args):
        mc.deleteUI('%s' %WINDN, window=True)

    def infoWind(*args):
        winshow=InfoUIClass()
        winshow.showWindInfo()

    def hyperLink(self,value):
        if value==0:
            os.startfile('https://gumroad.com/liam_collod')
        if value==1:
            os.startfile('https://twitter.com/MrLixm')
        if value==2:
            os.startfile('https://www.artstation.com/monsieur_lixm')
        if value==3:
            os.startfile('https://answers.arnoldrenderer.com/questions/3652/flags-for-mayacmdsarnoldexportass.html')


### UI FUNCTION
class AiStandInUIClass:

    def __init__(self):

        ####UI STYLE#####
        bgcwind=[0.2,0.2,0.2]
        opTxt = "-shadowLinks 1; -mask 6399; -lightLinks 1; -boundingBox; -fullPath"

        aif = AiFuncClass()

        self.windowv = mc.window('%s' %WINDN, title=" ", widthHeight=(320, 130), backgroundColor=bgcwind, nde=True, ds=True, le=650,tbm=False,s=True)


        mc.rowColumnLayout("uiTopRowGlobal", adj=True)

        mc.rowColumnLayout("uiTopRowName", nr=1,adj=True,cat=[1,"left",1])
        mc.rowColumnLayout( nr=1)
        mc.iconTextButton(st='iconOnly', h = 25,w=25,image=":/ExportStandinShelf.png")
        mc.text(label=' Arnold StandIn Utility '+VERSION, h = 20,w = 285, bgc=[0.2, 0.2, 0.2], al='left', fn='tinyBoldLabelFont' , rs=False)
        mc.setParent('..')
        mc.iconTextButton(st='iconOnly', h = 25,w=25,image=":/info.png",c=aif.infoWind)
        mc.iconTextButton(st='iconOnly',label= "   ", h = 15,w=25 ,command=aif.closeWind ,image=":/closeTabButton.png"  )
        mc.setParent('..')

        mc.separator( height=4, style='none' )
        mc.iconTextButton(st='textOnly',label= "   ", h = 2,w=150 , backgroundColor=bgcai  )
        mc.setParent('..')

        mc.rowColumnLayout("rclytUiFuncGlobal", adj=True)

        mc.rowLayout("rowlytField",nc=2,cl2=["left","center"],ct2=["left","left"],co2=[1,0],ad2=True)
        mc.iconTextButton('itbFolder',st='iconOnly', h = 25,w=25 ,command=aif.fileDialog, backgroundColor=(bgcgrey),image=":/folder-open.png",ebg=True )
        mc.textField("textFieldFile", ann="export path",sbm="export path" , font = "obliqueLabelFont", h= 20,w= 350,bgc=(bgcgreyd),tx=aif.projectPath)
        mc.setParent( '..' )

        mc.separator(style='none',h=10)

        '''Export options'''
        mc.rowColumnLayout('rclExOp',nr=1,ral=[1,'center'],bgc=bgcai,adj=True)
        mc.separator(style='none',w=3)
        mc.iconTextButton('itbHelp',st='iconOnly', h = 25,w=25 ,command=func.partial(aif.hyperLink,3),image=":/help.png")
        mc.text(l='<font style="color:rgb(50,50,50)">ExportOptions:</font>',fn= "smallBoldLabelFont")
        mc.separator(style='none',w=3)
        mc.textField("textFieldOptions", ann="export ass options" , h= 20,w=280,bgc=bgcgreyl,tx=opTxt,p='rclExOp')
        mc.iconTextButton('itbFolder',st='iconOnly',l="r",ann="Reset field", h = 20,w=15 ,command=aif.resetField,bgc=bgcgreyd,image=":/cycle.png",mh=6)
        mc.setParent( '..' )


        '''OPTIONS PART'''
        mc.separator(style='none',h=10)

        mc.rowColumnLayout("rclOpGlobal", nc=3)

        chkS = 15
        txtOp = ['Cameras','Lights','Shapes','Shaders']
        mc.rowColumnLayout("rcl1", nc=4,rs=[1,5])
        mc.columnLayout(bgc=bgcgreyl)
        mc.columnLayout(bgc=bgcgreyl)
        mc.iconTextButton('itbChkEsf',l='Off',st='iconOnly',bgc=bgcgreyd,w=chkS,h=chkS,mh=0,c=aif.chkChange_esf)
        mc.setParent('..')
        mc.setParent('..')
        mc.separator( w=4, style='none' )
        mc.iconTextButton(st='textOnly',l='Export selection as a single file',h=chkS,fn="smallBoldLabelFont")
        mc.separator( w=8, style='none' )

        #
        # mc.iconTextButton(st='iconOnly',bgc=bgcgreenM,w=chkS,h=chkS,mh=0)
        # mc.separator( w=4, style='none' )
        # mc.iconTextButton(st='textOnly',l=txtOp[2],h=chkS)
        # mc.separator( w=8, style='none' )
        mc.setParent('..')

        mc.rowColumnLayout("rclFielName", nc=4,rs=[1,5],en=False)
        mc.iconTextButton(st='textOnly',bgc=bgcwhite,w=2,h=20)
        mc.separator( w=15, style='none' )
        mc.text(l='Name:')
        mc.textField("textFieldName", ann="Name of the single exported file" , h= 20,w=150,bgc=bgcgreyl,tx="asset_msh")
        mc.setParent('..')

        #
        # mc.rowColumnLayout("rcl2", nc=4,rs=[1,5])
        # mc.iconTextButton(st='iconOnly',bgc=bgcgreenM,w=chkS,h=chkS,mh=0)
        # mc.separator( w=4, style='none' )
        # mc.iconTextButton(st='textOnly',l=txtOp[1],h=chkS)
        # mc.separator( w=8, style='none' )
        #
        # mc.iconTextButton(st='iconOnly',bgc=bgcgreenM,w=chkS,h=chkS,mh=0)
        # mc.separator( w=4, style='none' )
        # mc.iconTextButton(st='textOnly',l=txtOp[3],h=chkS)
        # mc.separator( w=8, style='none' )
        # mc.setParent('..')
        #
        mc.setParent('..')
        '''END'''

        mc.separator(style='none',h=10)

        mc.columnLayout("cLytBtn1",adj=True)
        mc.iconTextButton(label="",style="textOnly",bgc=bgcgreyl,h=4)
        mc.iconTextButton(label="EXPORT to Path",style="textOnly",bgc=bgcgreyd,command=aif.export_ass,fn="smallBoldLabelFont")
        mc.separator(style='none',h=5)
        mc.iconTextButton(label="",style="textOnly",bgc=bgcgreyl,h=4)
        mc.iconTextButton(label="CREATE from Path",style="textOnly",bgc=bgcgreyd,command=aif.import_ass,fn="smallBoldLabelFont")
        mc.setParent('..')


        mc.setParent( '..' )#rclUiFuncGlobal


    def showWind(self):
        mc.showWindow(self.windowv)

class InfoUIClass:
    def __init__(self):

        if mc.windowPref('infoAiAssWind', query=True, exists=True):
            mc.windowPref('infoAiAssWind', remove=True )
        if mc.window('infoAiAssWind', query=True, exists=True):
            mc.deleteUI('infoAiAssWind', window=True)

        aif = AiFuncClass()

        windbgc=0.2,0.2,0.2 #color of the background of the window

        self.windInfo = mc.window('infoAiAssWind', title="Info", widthHeight=(315, 200), backgroundColor=windbgc, tlc=[250,450],te=25,s=True,mnb=False,mxb=False,i=False)


        mc.rowColumnLayout("rclInfoGlobal", adj=True)

        mc.iconTextButton(st='textOnly',label= "   ", h = 2, backgroundColor=bgcgreenM  )
        mc.separator( h=15, style='none' )
        mc.text(l='<font color=#00f58a><h3>This tool was made by LiamCollod<h3></font>',h=15)
        mc.text(l='<font <h5>mail pro: <i>lcollod@gmail.com<i><h5></font>',h=35)


        mc.rowColumnLayout("rclInfoSep", nc=3)
        mc.separator( w=10, style='none' )
        mc.iconTextButton(st='iconOnly',bgc=bgcwhite,w=3)

        mc.rowColumnLayout("rclInfo2ndCol", nc=1,cal=[1,'left'])
        mc.text(label=' > A StandIn will be exported for each selection',fn='smallBoldLabelFont',h=16)
        mc.text(label=" > Remove this value from mask to remove corresponding",fn='smallBoldLabelFont',h=16)
        mc.text(label='       Options=1 ; Camera=2 ; Light=4 ; Shape=8 ; Shader=16',fn='smallBoldLabelFont',h=16)
        mc.setParent('..')
        mc.setParent('..')

        mc.separator( h=5, style='none' )

        mc.rowColumnLayout("rclInfoSep2", nc=3)
        mc.separator( w=10, style='none' )
        mc.iconTextButton(st='iconOnly',bgc=bgcwhite,w=3)

        mc.rowColumnLayout("rclInfo2ndCol2", adj=True)
        stItbLink="iconAndTextHorizontal"
        imgItbLink=":/out_genericConstraint.png"
        mc.iconTextButton(st=stItbLink,label='GUMROAD LINK',fn='smallBoldLabelFont',i=imgItbLink,c=func.partial(aif.hyperLink,0))
        mc.iconTextButton(st=stItbLink,label='TWITTER LINK',fn='smallBoldLabelFont',i=imgItbLink,c=func.partial(aif.hyperLink,1))
        mc.iconTextButton(st=stItbLink,label='ARTSTATION LINK',fn='smallBoldLabelFont',i=imgItbLink,c=func.partial(aif.hyperLink,2))
        mc.setParent('..')


        mc.setParent('..')
        mc.text(l='<font <h5>You find a bug ? Submit it to <i>monsieurlixm@gmail.com<i><h5></font>',h=35)
        mc.iconTextButton(st='textOnly',label= "   ", h = 2, backgroundColor=bgcwhite  )

        mc.setParent('..')

    def showWindInfo(self,*args):
        mc.showWindow(self.windInfo)

winshow= AiStandInUIClass()
winshow.showWind()


###ACES_Colorspace_utility - 2020- MrLixm
#FOR PERSONAL USE ONLY
#for commercial use, please buy a commercial license.
#Contact: lcollod@gmail.com



###<ChangeLog>#####

##v1.2.1
#add: A message is now displayed if ACES is not enabled
#fix: All tex to Acescg didn't work.
#fix: The button to convert all the texture could result in errors if you had non-file nodes as textures in the hypershade.
#

##v1.2.2
#change: Interface redesign
#

##v2.0
#change: code rewrited for optimization
#change: Interface redesigned
#add: Option to Enable or disabled use of Ocio file.
#add: Option to find & load the .ocio file
#add: Option to Enable or disable the Ocio Input space Rule option
#add: promptmenu when converting all textures to avoid mistakes.
#add: x3 IDT options with default colorManagement
#add: list of x4 usefull links to use ACES + YoutubePlaylist
#add: Quick Guide to work with Aces in maya

##v2.0.1
#add/fix: When loading the config.ocio, the colorManagement in general is force enabled

##v2.0.2
#fix: folder icon doesn't exist on some machine

##v2.1.0
#add:twitter icon replace by info icon. Open an Info Window
#change: 'Aces Links' is now named 'Aces Help' and can be minimised.(minimised by default)
#change: Link updated for ACES v1.2
#change: some UI updates

VERSION= "v2.1.0"
WINDAN= 'liamaceswind'

import maya.cmds as mc
import functools as func
import os


#colorGlobalVARIABLES
bgcwhited=[0.9,0.9,0.9]
bgcwhite= [0.95,0.95,0.95]
bgcgreylight1=[0.5,0.5,0.5]
bgcgreyll= [0.35,0.35,0.35]
bgcgreyl=[0.25,0.25,0.25]
bgcgrey= [0.2,0.2,0.2]
bgcgreyd= [0.18,0.18,0.18]
bgcdarkl= [0.15,0.15,0.15]
bgcgreenUVo=[0.33,0.6,0.46]
bgcgreenUV= [0.2,0.49,0.2]
bgcgreenUVl= [0.25,0.5,0.25]
bgcgreenUVll= [0.3,0.5,0.3]
bgcgreenM= [0,0.96,0.54]
bgcgreen2= [0.08, 0.76, 0.3]
bgcred1=[1,0.38,0.38]
bgcred2=[0.8, 0.2, 0.25]
bgcblue=[0.235,0.62,0.945]
bgcblueSea=[0.1,0.4,0.5]
bgcyellow=[1,0.83,0.44]
bgcpurple=[0.4,0.28,0.5]
bgcpurple2=[0.45,0.35,0.5]
bgcpurpleR=[0.45,0.28,0.5]
bgcpurpleF=[0.65,0.35,0.6]




### DELETE window prefs Aces Window
if mc.windowPref('%s' %WINDAN, query=True, exists=True):
    mc.windowPref( '%s' %WINDAN, remove=True )
if mc.window('%s' %WINDAN, query=True, exists=True):
    mc.deleteUI('%s' %WINDAN, window=True)

### DELETE window prefs Help Window
if mc.windowPref('AcesQuickHelp', query=True, exists=True):
    mc.windowPref('AcesQuickHelp', remove=True )
if mc.window('AcesQuickHelp', query=True, exists=True):
    mc.deleteUI('AcesQuickHelp', window=True)

### DELETE window prefs Info Window
if mc.windowPref('infoUdimWind', query=True, exists=True):
    mc.windowPref('infoUdimWind', remove=True )
if mc.window('infoUdimWind', query=True, exists=True):
    mc.deleteUI('infoUdimWind', window=True)



### Colorspacefunctions

class AcesFunctions:

    def __init__(self):

        ## ICON PATH
        self.mayaVersion = mc.about(v=True)
        self.userDir = mc.internalVar(userAppDir=True)
        self.iconsPath = os.path.join(self.userDir, self.mayaVersion+'/prefs/icons/AcesUtility')

        self.item_list = mc.ls( selection=True )
        self.ocioResult= self.ocioCheck()
        self.ocioPath= self.getOcioPath()

        self.acesresult= self.acesCheck()
        self.mAcesOn= self.acesresult
        self.mAcesOff= not self.acesresult

        self.imgTitlev=self.iconsCheck('Titlev2.0','caution')
        self.stTitleState=self.stTitlev
        self.imgTitleLeft=self.iconsCheck('Twitter','Bookmark')
        self.imgYtb=self.iconsCheck('Youtube','playblast')

    def iconsCheck(self,iconNameCt,iconNameNm):

        iconLoc= self.iconsPath+'/Script_AcesUtility_%s.png'%iconNameCt
        if os.path.isfile(iconLoc):
            self.iconExist=True
            self.imgIcon="%s"%iconLoc
            self.stTitlev='iconOnly'
        else:
            self.iconExist=False
            self.imgIcon=":/%s.png"%iconNameNm
            self.stTitlev='textOnly'

        return self.imgIcon


    def ocioCheck(self):
        self.value= mc.colorManagementPrefs(q=True,cfe=False)
        return self.value

    def acesCheck(self):
        wsname= mc.getAttr('defaultColorMgtGlobals.workingSpaceName')
        for value in [wsname]:
            if value=='ACES - ACEScg':
               self.acesresult = True
            else :
                self.acesresult = False
        return self.acesresult

    def ocioChange(self,value):

        ccOcio=not mc.colorManagementPrefs(q=True,cfe=True)
        if value:
            ccOcio=value
        mc.colorManagementPrefs(e=True,cfe=ccOcio)
        mAcesOn=ccOcio
        mAcesOff=not ccOcio
        if ccOcio:
            iconCbOcio=":/checkboxOn.png"
            bgcIcbOcio=bgcgreen2
        else:
            iconCbOcio=":/checkboxOff.png"
            bgcIcbOcio=bgcred1

        mc.iconTextButton("iconTextButtonUseOcio",e=True,image=iconCbOcio,bgc=bgcIcbOcio)
        self.updateAcesUi()

    def ocioRule(self,ccv):
        mc.colorManagementPrefs(e=True,ore=ccv)

    def ocioRuleWind(*args):
        mc.confirmDialog(title='OCIO Rule',message='If enabled ,a imported texture will be set automatically to the default colorspace set.   (You can set it to Utility-Raw by clicking on the right button)',defaultButton='OK',cancelButton='Cancel',dismissString='Cancel',icn="help")

    def ocioRuleChange(self):
        if self.ocioCheck():
            mc.colorManagementFileRules('Default',e=True,cs='Utility - Raw')
            mc.colorManagementFileRules(save=True)
            mc.colorManagementFileRules(load=True)
        else:
            print"Ocio disabled, can't change Default Rule"

    def updateAcesUi(self):
        mAcesOn=self.acesCheck()
        mAcesOff=not self.acesCheck()
        mc.flowLayout("lytFlowAcesOn",e=True,m=mAcesOn)
        mc.separator("separatorAcesOn",e=True,m=mAcesOn)
        mc.text("textColorAcesOn",e=True,m=mAcesOn )
        mc.text('textAcesOn',e=True,m=mAcesOn)

        mc.flowLayout("lytFlowAcesOff",e=True,m=mAcesOff)
        mc.separator("separatorAcesOff",e=True,m=mAcesOff)
        mc.text("textColorAcesOff",e=True,m=mAcesOff )
        mc.text('textAcesOff',e=True,m=mAcesOff )
        mc.iconTextButton('itbAcesOff',e=True,m=mAcesOff )

    def idtUiUpdate(self):
        valeur=mc.iconTextButton('itbIconTitle',q=True,image=True)
        leWind=mc.window('%s' %WINDAN, q=True,le=True )
        hWindO=mc.window('%s' %WINDAN, q=True,h=True )
        if valeur==":/nodeGrapherArrowDown.png":
            mV=False
            iV=":/moveUVRight.png"
            hLyt=33
            hWind=hWindO-280
        else:
            mV=True
            iV=":/nodeGrapherArrowDown.png"
            hLyt=309
            hWind=hWindO+280

        mc.iconTextButton('itbIconTitle',e=True,image=iV)
        mc.separator('idtSeparator1', e=True,m=mV )
        mc.iconTextButton('idtItbIcon',e=True,m=mV )
        mc.text('idtTextBttns',e=True,m=mV )
        mc.separator('idtSeparator2',e=True,m=mV )
        mc.flowLayout("flowLayoutBttns",e=True,m=mV )
        mc.separator('idtSeparator3',e=True,m=mV )
        mc.text("textColorBttns0",e=True,m=mV )
        mc.iconTextButton('itbBttns0',e=True,m=mV )
        mc.separator('idtSeparator4',e=True,m=mV )
        mc.text("textColorBttns1",e=True,m=mV )
        mc.iconTextButton('itbBttns1',e=True,m=mV )
        mc.separator('idtSeparator5',e=True,m=mV )
        mc.flowLayout("flowLayoutTxtBttns2",e=True,m=mV )
        mc.iconTextButton('itbIcon2',e=True,m=mV )
        mc.text('textBttns2',e=True,m=mV )
        mc.separator('idtSeparator6',e=True,m=mV )
        mc.flowLayout("flowLayoutBttns2",e=True,m=mV )
        mc.separator('idtSeparator7',e=True,m=mV )
        mc.text("textColorBttns2",e=True,m=mV )
        mc.iconTextButton('itbBttns2',e=True,m=mV )
        mc.separator('idtSeparator8',e=True,m=mV )
        mc.text("textColorBttns3",e=True,m=mV )
        mc.iconTextButton('itbBttns3',e=True,m=mV )
        mc.flowLayout("flowLayoutBttns3",e=True,m=mV )
        mc.separator('idtSeparator9',e=True,m=mV )
        mc.text("textColorBttns3",e=True,m=mV )
        mc.iconTextButton('itbBttns3',e=True,m=mV )
        mc.separator('idtSeparator10',e=True,m=mV )
        mc.text("textColorBttns4",e=True,m=mV )
        mc.iconTextButton('itbBttns4',e=True,m=mV )
        mc.separator('idtSeparator11',e=True,m=mV )
        mc.flowLayout("flowLayoutTxtBttns32",e=True,m=mV )
        mc.iconTextButton('itbIcon32',e=True,m=mV )
        mc.text('textBttns32',e=True,m=mV )
        mc.separator('idtSeparator12',e=True,m=mV )
        mc.flowLayout("flowLayoutBttns33",e=True,m=mV )
        mc.separator('idtSeparator13',e=True,m=mV )
        mc.text("textColorBttns30",e=True,m=mV )
        mc.iconTextButton('itbBttns30',e=True,m=mV )
        mc.separator('idtSeparator14',e=True,m=mV )
        mc.text("textColorBttns31",e=True,m=mV )
        mc.iconTextButton('itbBttns31',e=True,m=mV )
        mc.separator('idtSeparator15',e=True,m=mV )
        mc.text("textColorBttns32",e=True,m=mV )
        mc.iconTextButton('itbBttns32',e=True,m=mV )
        mc.rowColumnLayout("uiRowColLytSide2", e=True,h=hLyt)
        mc.window('%s' %WINDAN, e=True, h=hWind )
        mc.window('%s' %WINDAN, e=True,le=leWind )

    def helpUiUpdate(self,*args):
        visState = mc.iconTextButton('itbBkmrkLinks', q=True,i=True)
        hWindhelpO=mc.window('%s' %WINDAN, q=True,h=True )

        if visState==':/nodeGrapherArrowDown.png':
            itbImg=':/moveUVRight.png'
            itbVis=False
            hWindHelpN=hWindhelpO-100

        elif visState==':/moveUVRight.png':
            itbImg=':/nodeGrapherArrowDown.png'
            itbVis=True
            hWindHelpN=hWindhelpO+100
            hLyt = 150

        mc.rowColumnLayout("rclUiGlobalHelps", e=True, vis=itbVis,m=itbVis )
        mc.iconTextButton('itbBkmrkLinks', e=True,i=itbImg)
        mc.window('%s' %WINDAN, e=True,h=hWindHelpN )


    def getOcioPath(self):
        self.ocioPath=mc.colorManagementPrefs(q=True,cfp=True)
        return self.ocioPath

    def fileDialogOcio(self):
        self.ocioFile=mc.fileDialog2(fm=1)
        mc.textField("textFieldOcio",e=True,tx=self.ocioFile[0])

        return self.ocioFile

    def validateOcio(self,*args):
        ocioPath=mc.textField("textFieldOcio",q=True,tx=True)
        mc.colorManagementPrefs(e=True,cme=True)
        mc.colorManagementPrefs(e=True,cfp=ocioPath)
        self.ocioChange(True)


    def allTexCs(self,value):
        tex_list= mc.ls(type='file')
        if value==0:
            text='ACEScg'
        if value==1:
            text='Utility-Raw'
        if value==2:
            text='Raw'
        promptResult = mc.confirmDialog(title='Convert ALL textures',message='You are about to convert ALL the texture of your maya file to %s'%text,button=['OK', 'Cancel'],defaultButton='OK',cancelButton='Cancel',dismissString='Cancel',icn="warning")
        if promptResult=='OK':
            for textures in tex_list:
                if value==0:
                    mc.setAttr('%s.colorSpace' %textures, "ACES - ACEScg", type="string")
                if value==1:
                    mc.setAttr('%s.colorSpace' %textures, "Utility - Raw", type="string")
                if value==2:
                    mc.setAttr('%s.colorSpace' %textures, "Raw", type="string")
        else :
            print "Conversion aborted by user"

    def csTex(self,value):
        item_list = mc.ls( selection=True )
        for things in item_list:
            if value==0:
                mc.setAttr('%s.colorSpace' %things, "ACES - ACEScg", type="string")
            if value==1:
                mc.setAttr('%s.colorSpace' %things, "Utility - Raw", type="string")
            if value==2:
                mc.setAttr('%s.colorSpace' %things, "Utility - Linear - sRGB", type="string")
            if value==3:
                mc.setAttr('%s.colorSpace' %things, "Utility - sRGB - Texture", type="string")
            if value==4:
                mc.setAttr('%s.colorSpace' %things, "sRGB", type="string")
            if value==5:
                mc.setAttr('%s.colorSpace' %things, "Raw", type="string")
            if value==6:
                mc.setAttr('%s.colorSpace' %things, "Output - sRGB", type="string")
            if value==7:
                mc.setAttr('%s.colorSpace' %things, "Raw", type="string")


    def hyperLink(self,value):
        if value==0:
            os.startfile('https://github.com/colour-science/OpenColorIO-Configs/archive/feature/aces-1.2-config.zip')
        if value==1:
            os.startfile('https://acescentral.com/faq')
        if value==2:
            os.startfile('https://chrisbrejon.com/cg-cinematography/chapter-1-5-academy-color-encoding-system-aces/')
        if value==3:
            os.startfile('https://z-fx.nl/ColorspACES.pdf')
        if value==4:
            os.startfile('https://gumroad.com/liam_collod')
        if value==5:
            os.startfile('https://www.youtube.com/watch?v=ctCL0OhCGjk&list=PLK1rYEsZB6pu138crJeB4X3m94UCbtjuX')
        if value==6:
            os.startfile('https://twitter.com/MrLixm')
        if value==7:
            os.startfile('https://www.artstation.com/monsieur_lixm')

    def helpWind(*args):
        winshow=HelpUI()
        winshow.showWindHelp()

    def infoWind(*args):
        winshow=InfoUI()
        winshow.showWindInfo()


    ###Close window function
    def closeWind(*args):
        mc.deleteUI('%s' %WINDAN, window=True)
        if mc.window('infoUdimWind', query=True, exists=True):
            mc.deleteUI('infoUdimWind', window=True)




### UI FUNCTION


class AcesUI:

    def __init__(self):

        af=AcesFunctions()

        cbRv=mc.colorManagementPrefs(q=True,ore=True)

        if af.ocioResult==True:
            cbv=True
            iconCbOcio=":/checkboxOn.png"
            bgcIcbOcio=bgcgreen2
        else:
            cbv=False
            iconCbOcio=":/checkboxOff.png"
            bgcIcbOcio=bgcred1

        ####UI STYLE#####
        windbgcR,windbgcG,windbgcB=0.2,0.2,0.2 #color of the background of the window
        wGlobal=353
        #BUTTON HEIGHT weight
        hv=15
        wv=30
        #icontextbutton
        hiv=25
        wiv=25
        ##--------------

        self.windowv = mc.window('%s' %WINDAN, title=" ", widthHeight=(wGlobal, 725), backgroundColor=(windbgcR,windbgcG,windbgcB), le=650,te=150,tbm=False,s=False)

        mc.columnLayout( columnAttach=('both', 0), rowSpacing=10, columnWidth=wGlobal )
        mc.text(label= "   ", h = 3 , rs=True, backgroundColor=bgcblue  )
        mc.setParent( '..' )

        mc.rowColumnLayout("uiRowColLytSide1", nc=4)
        mc.separator( w=5, style='none' )
        mc.iconTextButton(label= "   ", w = 3 , bgc=bgcgreyl )
        mc.separator( w=4, style='none' )

        #fourth column
        mc.rowColumnLayout("uiTopRowGlobal", adj=True )


        mc.rowLayout("rowlytName",bgc=bgcblue,nc=4,cl4=["left","left","left","left"],h=29 )
        mc.separator( w=2, style='none' )
        mc.iconTextButton(st='iconOnly',label= "   ", h = 20,w=20 ,i=':/info.png',command=af.infoWind )
        mc.iconTextButton(st=af.stTitleState,label=' ACES Colorspace Utility %s' %VERSION, h = 22,w = 276, bgc=[0.204, 0.204, 0.21], al='left', fn='boldLabelFont' ,ebg=False,hlc=bgcgreen2,command=func.partial(af.hyperLink,4),i=af.imgTitlev,mw=5)
        mc.iconTextButton(st='iconOnly',label= "   ", h = 25,w=25 ,command=af.closeWind, backgroundColor=(bgcwhited),image=":/error.png",ebg=False  )
        mc.setParent('..')

        mc.iconTextButton(st='textOnly',label= "   ", h = 2,w=170 , backgroundColor=(bgcwhited)  )
        mc.separator( height=15, style='none' )


    	## Is aces enabled ? ##
        # ACES ON UI #
        self.uiAcesOn1=mc.flowLayout("lytFlowAcesOn",m=af.mAcesOn)
        self.uiAcesOn2=mc.separator("separatorAcesOn", w=4,h=15, style='none' ,m=af.mAcesOn)
        self.uiAcesOn3=mc.text("textColorAcesOn",label= "   ", w = 5 , rs=False, backgroundColor=(0.08, 0.76, 0.3) ,m=af.mAcesOn )
        self.uiAcesOn4=mc.text('textAcesOn',label= '  ACES is enabled', al='left', fn='obliqueLabelFont' , rs=False ,m=af.mAcesOn)
        mc.setParent( '..' )

        # ACES OFF UI #
        htxtAcesOff=15
        self.uiAcesOff1=mc.flowLayout("lytFlowAcesOff",m=af.mAcesOff)
        self.uiAcesOff2=mc.separator("separatorAcesOff", w=4, style='none' ,m=af.mAcesOff)
        self.uiAcesOff3=mc.text("textColorAcesOff",label= "   ", w = 5,h=htxtAcesOff , rs=False, backgroundColor=(bgcred2) ,m=af.mAcesOff)
        self.uiAcesOff4=mc.text('textAcesOff',label= "   ACES is not enabled ",h=htxtAcesOff,fn='obliqueLabelFont', al='left' , rs=False, backgroundColor=(0.3, 0.3, 0.3) ,m=af.mAcesOff,ebg=False )
        self.uiAcesOff5=mc.iconTextButton('itbAcesOff',st='iconOnly', h = 13,w=13 , backgroundColor=(bgcgrey),image=":/caution.png",ebg=True,m=af.mAcesOff  )
        mc.setParent( '..' )



        mc.separator( height=20, style='none' )

        #########################
        # CheckBox OCIO #
        mc.rowLayout("rowlytOcio",bgc=(bgcgreyl),nc=3,cl3=["center","center","left"])
        mc.separator( w=2,h=25, style='none' )
        mc.iconTextButton("iconTextButtonUseOcio",st='iconOnly',label= "   ", h = 20,w=20 ,command=func.partial(af.ocioChange,False), backgroundColor=(bgcIcbOcio),image=iconCbOcio,ebg=True  )
        mc.text('textUseOcio',label= " USE OCIO",h=15,fn='smallBoldLabelFont', al='left' ,rs=False, bgc=(0.3, 0.3, 0.3) ,ebg=False )
        mc.setParent( '..' )

        mc.separator( height=8, style='none' )
        #################################


        ## OCIO LOADING UI ##
        mc.rowColumnLayout("rowCLOcio", nc=3)
        mc.separator( w=2, style='none' )
        mc.text(label= "   ", w = 2 , rs=False, backgroundColor=(bgcwhited)  )
        # Third column
        mc.rowColumnLayout("uiTopRowGlobal", adj=True )

        mc.rowLayout("rowlytField",nc=2,cl2=["center","center"],ct2=["both","left"],co2=[5,0])
        mc.iconTextButton('itbFolder',st='iconOnly', h = 20,w=20 ,command=af.fileDialogOcio, backgroundColor=(bgcgrey),image=":/folder-open.png",ebg=True )
        ocioPathField = mc.textField("textFieldOcio", ann="path of the .ocio" , font = "obliqueLabelFont", h= 20,w= 280,bgc=(bgcgreyd),tx=af.ocioPath)
        mc.setParent( '..' )

        mc.rowLayout("rowlytOcio",bgc=(bgcgreyl),nc=2,cl2=["left","right"],cw2=[229,50],ebg=False)

        mc.rowColumnLayout("uiTopRowGlobal", adj=True )
        mc.text('textOcioPath',label= "   1.Set the path to config.ocio",h=15,fn='smallBoldLabelFont', al='left' ,rs=False, bgc=(0.3, 0.3, 0.3) ,ebg=False )
        mc.text('textOcioPathVal',label= "   2.Load after selecting the config.ocio",h=15,fn='smallBoldLabelFont', al='left' ,rs=False, bgc=(0.3, 0.3, 0.3) ,ebg=False )
        mc.setParent( '..' )

        mc.button(label='LOAD', h =25,w = 80, bgc=(bgcgreyd),command=af.validateOcio)
        mc.setParent( '..' )

        mc.setParent( '..' )
        mc.setParent( '..' )



        ######################
        # CheckBox OCIO RULE #
        mc.separator( height=12, style='none' )
        mc.rowLayout("rowlytOcioRule",bgc=(bgcgreyl),nc=5,cl5=["center","center","right","center","center"],ct5=["both","both","both","right","right"],co5=[0,0,12,0,0])
        mc.separator( w=2,h=25, style='none' )
        mc.checkBox("checkBoxOcioRule", label='OCIO Rule',v=cbRv,cc=af.ocioRule )
        mc.iconTextButton('itbHelp',st='iconOnly', h = 20,w=20 ,ann='If enabled , a texture will be set to the default colorspace you choose', backgroundColor=(bgcgrey),image=":/help.png",ebg=False,command=af.ocioRuleWind )
        mc.iconTextButton('itbOrtxt',st='textOnly', h = 20,w=110 ,label='Set Default OcioRule to:', backgroundColor=(bgcgrey),ebg=False,fn="tinyBoldLabelFont" )
        mc.iconTextButton('itbOrtxtCs',st='textOnly', h = 18,w=80 ,label='Utility - Raw',command=af.ocioRuleChange, backgroundColor=(bgcgreyd),ebg=True,fn="tinyBoldLabelFont" )

        mc.setParent( '..' )

        mc.iconTextButton(st='textOnly',label= "   ", h = 2,w=150 , backgroundColor=(bgcblue)  )
        mc.setParent( '..' )
        mc.setParent( '..' )

        mc.separator( w=8, style='none' )








############################################################################################################
        ## SEPARATOR WHITE ##

        mc.rowColumnLayout("uiRowColLytSide2", nc=3,h=308)
        mc.separator( w=2, style='none' )
        mc.text("idtTxtLineSide",label= "   ", w = 2 , rs=False, backgroundColor=(bgcgreyl)  )
        ##################
        ## BUTTONS ##
        ##################
        mc.rowColumnLayout("uiTopRowGlobalButtons", adj=True )



        mc.rowColumnLayout("uiRowColLytTitle", nc=2)
        mc.text(label= "   ",h=30, w = 4 , rs=False, backgroundColor=(bgcblue)  )
        mc.rowLayout("rowlytTitle",bgc=(bgcdarkl),nc=2,cl2=["left","left"],h=30)
        mc.iconTextButton('itbIconTitle',st='iconOnly', h = 18,w=18 , backgroundColor=(bgcgrey),image=":/nodeGrapherArrowDown.png",ebg=False,command=af.idtUiUpdate,ann="Open/Close Menu")
        mc.text('textTitleFile',label="CHANGE FILES NODE COLORSPACE (IDT)",fn='boldLabelFont',w=wGlobal-43,al="left")
        mc.setParent( '..' )
        mc.setParent( '..' )


        mc.separator('idtSeparator1', h=15, style='none' )


        # UI STYLE #
        wSepLnk=2
        hBttnsCs=40
        stItbCs="iconAndTextCentered" #iconAndTextCentered
        alItbCs="left"
        imgItbCs=":/"#":/teUnexpandableRowBackground.png"
        loItbCs=5
        ebgItbCs=False
        bgcTxtCs=bgcpurple

        #################
        # BUTTONS ROW 1 #
        #################
        mc.flowLayout("idtFlowLayoutTxtBttns",h=20)
        mc.iconTextButton('idtItbIcon',st='iconOnly', h = 18,w=18 , backgroundColor=(bgcgrey),image=":/out_displayLayer.png",ebg=True)
        mc.text('idtTextBttns',label= "Convert ALL the files nodes:",h=15,fn='smallBoldLabelFont', al='left' ,rs=False, bgc=(0.3, 0.3, 0.3) ,ebg=False )
        mc.setParent( '..' )

        mc.separator('idtSeparator2', h=3, style='none' )

        mc.flowLayout("flowLayoutBttns")
        mc.separator('idtSeparator3', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns0",label= " ", w = 3,h=hBttnsCs-5, rs=False, backgroundColor=(bgcred1))
        mc.iconTextButton('itbBttns0',st=stItbCs,label='  ALL ACEScg',fn='smallBoldLabelFont', h = hBttnsCs-5,w=150 ,command=func.partial(af.allTexCs,0), backgroundColor=(bgcpurpleR),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.separator('idtSeparator4', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns1",label= " ", w = 3,h=hBttnsCs-5, rs=False, backgroundColor=(bgcred1))
        mc.iconTextButton('itbBttns1',st=stItbCs,label='  ALL Utility-Raw',fn='smallBoldLabelFont', h = hBttnsCs-5,w=150 ,command=func.partial(af.allTexCs,1), backgroundColor=(bgcpurpleR),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.setParent( '..' )

        mc.separator('idtSeparator5', h=5, style='none' )



        ###################
        # BUTTONS ROW 2.1 #
        ###################
        mc.flowLayout("flowLayoutTxtBttns2",h=20)
        mc.iconTextButton('itbIcon2',st='iconOnly', h = 18,w=18 , backgroundColor=(bgcgrey),image=":/imageDisplay.png",ebg=True)
        mc.text('textBttns2',label= "Convert the selected files nodes:",h=15,fn='smallBoldLabelFont', al='left' ,rs=False, bgc=(0.3, 0.3, 0.3) ,ebg=False )
        mc.setParent( '..' )

        mc.separator('idtSeparator6', h=3, style='none' )

        mc.flowLayout("flowLayoutBttns2")
        mc.separator('idtSeparator7', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns2",label= " ", w = 3,h=hBttnsCs, rs=False, backgroundColor=(bgcpurpleF))
        mc.iconTextButton('itbBttns2',st=stItbCs,label='  ACEScg',fn='smallBoldLabelFont', h = hBttnsCs,w=120 ,command=func.partial(af.csTex,0), backgroundColor=(bgcpurple),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.separator('idtSeparator8', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns3",label= " ", w = 3,h=hBttnsCs, rs=False, backgroundColor=(bgcyellow))
        mc.iconTextButton('itbBttns3',st=stItbCs,label='  Utility-Raw',fn='smallBoldLabelFont', h = hBttnsCs,w=100 ,command=func.partial(af.csTex,1), backgroundColor=(bgcpurple),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.separator('idtSeparator9v2', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns3v2",label= " ", w = 3,h=hBttnsCs, rs=False, backgroundColor=(bgcgreenUVo))
        mc.iconTextButton('itbBttns3v2',st=stItbCs,label='  Output sRGB',fn='smallBoldLabelFont', h = hBttnsCs,w=100 ,command=func.partial(af.csTex,6), backgroundColor=(bgcpurple2),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)

        mc.setParent( '..' )

        mc.separator('idtSeparatortest',h=2, style='none' )#TEST SEPRATOR

        # BUTTONS ROW 2.2 #
        mc.flowLayout("flowLayoutBttns3")
        mc.separator('idtSeparator9', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns3",label= " ", w = 3,h=hBttnsCs, rs=False, backgroundColor=(bgcgreenUVo))
        mc.iconTextButton('itbBttns3',st=stItbCs,label='  Utility-Linear-sRGB',fn='smallBoldLabelFont', h = hBttnsCs,w=120 ,command=func.partial(af.csTex,2), backgroundColor=(bgcpurple2),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.separator('idtSeparator10', w=wSepLnk,h=hBttnsCs, style='none' )
        mc.text("textColorBttns4",label= " ", w = 3,h=hBttnsCs, rs=False, backgroundColor=(bgcgreenUVo))
        mc.iconTextButton('itbBttns4',st=stItbCs,label='  Utility-sRGB-Texture',fn='smallBoldLabelFont', h = hBttnsCs,w=150 ,command=func.partial(af.csTex,3), backgroundColor=(bgcpurple2),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.setParent( '..' )

        mc.separator('idtSeparator11', h=20, style='none' )

        #################
        # BUTTONS ROW 3 #
        #################
        mc.flowLayout("flowLayoutTxtBttns32")
        mc.iconTextButton('itbIcon32',st='iconOnly', h = 18,w=18 , backgroundColor=(bgcgrey),image=":/out_file.png",ebg=True)
        mc.text('textBttns32',label= "Default colorManagement Options",h=15,fn='smallBoldLabelFont', al='left' ,rs=False, bgc=(0.3, 0.3, 0.3) ,ebg=False )
        mc.setParent( '..' )

        mc.separator('idtSeparator12', h=5, style='none' )

        mc.flowLayout("flowLayoutBttns33")
        mc.separator('idtSeparator13', w=wSepLnk,h=hBttnsCs-20, style='none' )
        mc.text("textColorBttns30",label= " ", w = 3,h=hBttnsCs-20, rs=False, backgroundColor=(bgcblueSea))
        mc.iconTextButton('itbBttns30',st=stItbCs,label='  ALL to Raw',fn='smallBoldLabelFont', h = hBttnsCs-20,w=100 ,command=func.partial(af.allTexCs,2), backgroundColor=(bgcpurpleR),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.separator('idtSeparator14', w=wSepLnk, style='none' )
        mc.text("textColorBttns31",label= " ", w = 3,h=hBttnsCs-20, rs=False, backgroundColor=(bgcblueSea))
        mc.iconTextButton('itbBttns31',st=stItbCs,label='  sRGB',fn='smallBoldLabelFont', h = hBttnsCs-20,w=100 ,command=func.partial(af.csTex,4), backgroundColor=(bgcpurpleR),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.separator('idtSeparator15', w=wSepLnk,h=hBttnsCs-20, style='none' )
        mc.text("textColorBttns32",label= " ", w = 3,h=hBttnsCs-20, rs=False, backgroundColor=(bgcblueSea))
        mc.iconTextButton('itbBttns32',st=stItbCs,label='  Raw',fn='smallBoldLabelFont', h = hBttnsCs-20,w=80 ,command=func.partial(af.csTex,5), backgroundColor=(bgcpurpleR),al=alItbCs,lo=loItbCs,ebg=ebgItbCs)
        mc.setParent( '..' )


        mc.setParent( '..' )
        mc.setParent( '..' )
        mc.setParent( '..' )




##########################################################################################
        ##################
        ## USEFUL LINKS ##
        ##################

        stItbLink="iconAndTextHorizontal"
        imgItbLink=":/out_genericConstraint.png"

        mc.rowColumnLayout("uiTopRowGlobalLinks", adj=True )
        mc.separator( h=15, style='none' )

        mc.flowLayout("flowLayoutTxtLinks",h=25,bgc=bgcgreyl)
        mc.text("textColorLinks0",label= " ", w = 3,h=25, rs=False, bgc=bgcblue)
        mc.iconTextButton('itbBkmrkLinks',st='iconOnly', h = 25,w=20 ,image=":/nodeGrapherArrowDown.png",c=af.helpUiUpdate)
        mc.iconTextButton('textUsflLinks',st='textOnly',label= "ACES HELP",h=25,fn='smallBoldLabelFont',c=af.helpUiUpdate)
        mc.setParent( '..' )

        wSepLnk=2
        mc.separator( h=5, style='none' )
        mc.rowColumnLayout("rclUiGlobalHelps", adj=True )

        # LINKS ROW 1 #


        mc.flowLayout("flowLayoutLinks")
        mc.separator( w=wSepLnk,h=25, style='none' )
        mc.text("textColorLinks0",label= " ", w = 3,h=25, rs=False, backgroundColor=(bgcgreen2))
        mc.iconTextButton('itbAcesLink',st=stItbLink,label='DOWNLOAD ACESv1.2 ',fn='smallBoldLabelFont', h = 25,w=150 ,command=func.partial(af.hyperLink,0), backgroundColor=(bgcpurpleR),ebg=False,image=imgItbLink )
        mc.separator( w=wSepLnk,h=25, style='none' )
        mc.text("textColorLinks1",label= " ", w = 3,h=25, rs=False, backgroundColor=(bgcgreyl))
        mc.iconTextButton('itbAcesLink2',st=stItbLink,label='ACES CENTRAL FAQ',fn='smallBoldLabelFont', h = 25,w=150 ,command=func.partial(af.hyperLink,1), backgroundColor=(bgcpurple),ebg=False,image=imgItbLink)
        mc.setParent( '..' )

        mc.separator(h=3,style='none')


        # LINKS ROW 2 #
        mc.flowLayout("flowLayoutLinks2")
        mc.separator( w=wSepLnk,h=25, style='none' )
        mc.text("textColorLinks2",label= " ", w = 3,h=25, rs=False, backgroundColor=(bgcgreyl))
        mc.iconTextButton('itbAcesLink2.1',st=stItbLink,label='Chris Brejon Book',fn='smallBoldLabelFont', h = 25,w=150 ,command=func.partial(af.hyperLink,2), backgroundColor=(bgcpurple2),ebg=False,image=imgItbLink)
        mc.separator( w=wSepLnk,h=25, style='none' )
        mc.text("textColorLinks3",label= " ", w = 3,h=25, rs=False, backgroundColor=(bgcgreyl))
        mc.iconTextButton('itbAcesLink2.2',st=stItbLink,label='W.Zwarthoed ACES PDF',fn='smallBoldLabelFont', h = 25,w=150 ,command=func.partial(af.hyperLink,3), backgroundColor=(bgcpurple2),ebg=False,image=imgItbLink)
        mc.setParent( '..' )

        mc.separator( h=5, style='none' )

        #LINKS ROW 3 #
        mc.rowLayout("flowLayoutLinks3",nc=6,bgc=bgcgreyl)
        mc.separator( w=1,h=25, style='none' )
        mc.text("textColorLinks3",label= " ", w = 3,h=25, rs=False, backgroundColor=(bgcred2))
        mc.iconTextButton('itbAcesLink3',st=stItbLink,label='Quick ACES Help',fn='smallBoldLabelFont', h = 25,w=150 ,command=af.helpWind, backgroundColor=(bgcpurple2),ebg=False,image=":/help.png")
        mc.separator( w=1,h=25, style='none' )
        mc.text("textColorLinks4",label= " ", w = 3,h=25, rs=False, backgroundColor=(bgcred2))
        mc.iconTextButton('itbAcesLink4',st=stItbLink,label='Youtube ACES Tuto',fn='smallBoldLabelFont', h = 30,w=150 ,command=func.partial(af.hyperLink,5), backgroundColor=(bgcpurple2),ebg=False,image=af.imgYtb)
        mc.setParent( '..' )
        mc.iconTextButton(st='textOnly',label= "   ", h = 4,w=150 , backgroundColor=(bgcblue)  )


        mc.setParent( '..' )#END rclUiGlobalLinks
        mc.setParent('..')

        mc.setParent('..')


        af.idtUiUpdate()
        # af.helpUiUpdate()


    def showWind(self):
        mc.showWindow(self.windowv)

class HelpUI:
    def __init__(self):

        if mc.windowPref('AcesQuickHelp', query=True, exists=True):
            mc.windowPref('AcesQuickHelp', remove=True )
        if mc.window('AcesQuickHelp', query=True, exists=True):
            mc.deleteUI('AcesQuickHelp', window=True)


        windbgcR,windbgcG,windbgcB=0.2,0.2,0.2 #color of the background of the window

        self.windHelp = mc.window('AcesQuickHelp', title=" ", widthHeight=(500, 760), backgroundColor=(windbgcR,windbgcG,windbgcB), le=750,te=25,s=True)

        mc.rowColumnLayout("uiHelpRclGlobal", adj=True )
        mc.separator( h=5, style='none' )

        mc.rowColumnLayout("uiHelpRclSide1", nc=4)
        mc.separator( w=5, style='none' )
        mc.text(label= "   ", w = 2 , rs=False, backgroundColor=(bgcblue)  )
        mc.separator( w=5, style='none' )

        mc.rowColumnLayout("uiHelpRclInside", adj=True ) #third column

        hTitle=30
        mc.flowLayout("uiHelpFlowLayoutTop")
        mc.text("textColorAcesOff",label= "   ", w = 5,h=hTitle, bgc=(bgcblue))
        mc.iconTextButton(label=" QUICK ACES HELP GUIDE   ",fn="boldLabelFont",al="left",h=hTitle,bgc=bgcgreyl,st="iconAndTextHorizontal",i=":/info.png")
        mc.setParent('..')

        hSepTxt=5 #hauteur interligne
        mc.separator( h=10, style='none' )
        mc.text(label="Which Colorspace to Choose ?",fn="boldLabelFont",al="left")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(label="Is your texture a 'Color'Map ? (Albedo/BaseColor/Translucency/SubsurfaceColor/...)",st="iconAndTextHorizontal",fn="plainLabelFont",al="left",i=":/help.png")
        mc.separator( h=hSepTxt, style='none' )

        mc.rowLayout(nc=2)
        mc.separator( w=15, style='none' )
        mc.rowColumnLayout("uiHelpRclColor", adj=True )
        mc.iconTextButton(st="iconAndTextHorizontal",label="Is your texture in a linear format (.exr,...)?",fn="plainLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      Set it to Utility - Linear - sRGB",fn="obliqueLabelFont",al="left",i=":/imageDisplay.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="Is your texture in a 8/16bit format (.jpg,.png,.tiff,...)?",fn="plainLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      Set it to Utility - sRGB - Texture",fn="obliqueLabelFont",al="left",i=":/imageDisplay.png")
        mc.setParent('..') #End
        mc.setParent('..') #End



        ################### DATA

        mc.separator( h=hSepTxt+10, style='none' )
        mc.iconTextButton(label="Is your texture a 'Data'Map ? (Roughness,Normal,Bump,Displacement,Specular,...)",st="iconAndTextHorizontal",fn="plainLabelFont",al="left",i=":/help.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.rowLayout(nc=2)
        mc.separator( w=15, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      Set it to Utility - Raw",fn="obliqueLabelFont",al="left",i=":/imageDisplay.png")
        mc.setParent('..') #End

        ################### HDRI

        mc.separator( h=hSepTxt+10, style='none' )
        mc.iconTextButton(label="Is your texture a HDRI (.hdr,.exr)",st="iconAndTextHorizontal",fn="plainLabelFont",al="left",i=":/help.png")
        mc.separator( h=hSepTxt, style='none' )

        mc.rowLayout(nc=2)
        mc.separator( w=15, style='none' )
        mc.rowColumnLayout("uiHelpRclHdri", adj=True )
        mc.iconTextButton(st="iconAndTextHorizontal",label="Your HDRI has to be converted to ACEScg if you want it displayed correctly",fn="plainLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      Use Nuke,Natron,Houdini,... to convert it then set it to ACEScg",fn="obliqueLabelFont",al="left",i=":/saveGeneric.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="You can't convert it ?:",fn="plainLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      Then set it to Utility - Raw",fn="obliqueLabelFont",al="left",i=":/out_envBall.png")
        mc.setParent('..') #End
        mc.setParent('..') #End


        ################### ACES

        mc.separator( h=hSepTxt+10, style='none' )
        mc.iconTextButton(label="Has your texture already been converted to ACEScg ?",st="iconAndTextHorizontal",fn="plainLabelFont",al="left",i=":/help.png")
        mc.iconTextButton(label="     (or you worked in ACEScg when creating them(ex:Mari))",st="iconAndTextHorizontal",fn="plainLabelFont",al="left")
        mc.separator( h=hSepTxt, style='none' )
        mc.rowLayout(nc=2)
        mc.separator( w=15, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      Set it to ACEScg",fn="obliqueLabelFont",al="left",i=":/imageDisplay.png")
        mc.setParent('..') #End

        ################### oUTPU Srgb


        mc.separator( h=hSepTxt+10, style='none' )
        mc.iconTextButton(label="What is Output - sRGB for ?",st="iconAndTextHorizontal",fn="plainLabelFont",al="left",i=":/help.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.separator( w=15, style='none' )
        mc.rowColumnLayout(nr=2)
        mc.iconTextButton(st="iconAndTextHorizontal",label="Using Utility-sRGB-Texture as an IDT will darken your texture (this is a normal behavior)",fn="obliqueLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.iconTextButton(st="iconAndTextHorizontal",label="      If you really want to preserve the color of your original of your file you can use this IDT",fn="obliqueLabelFont",al="left")

        mc.setParent('..') #End

        ################### REDSHIFT

        mc.separator( h=20, style='none' )
        mc.iconTextButton(st='iconAndTextHorizontal',label="Are you using Redshift to render ?",fn="boldLabelFont",al="left",i=":/rvRedChannel")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(label="Redshift doesn't fully support Ocio, changing colorspace on nodes will not work",st="iconAndTextHorizontal",fn="plainLabelFont",al="left",i=":/info.png")
        mc.separator( h=hSepTxt, style='none' )

        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="      So you have to convert your textures to ACEScg before in Nuke,Natron,...",fn="obliqueLabelFont",al="left",i=":/clip_norgie_close.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="     Albedo/BaseColor/Translucency/SubsurfaceColor/... to ACEScg",fn="obliqueLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="     NormalMap don't have to be converted if you use the RS NormalMap node ",fn="obliqueLabelFont",al="left",i=":/clip_poseoffset.png")
        mc.separator( h=hSepTxt, style='none' )
        mc.iconTextButton(st="iconAndTextHorizontal",label="     Greyscale/Data maps (roughness,metalness,...) can be converted whether or not to ACEScg",fn="obliqueLabelFont",al="left",i=":/clip_poseoffset.png")








        mc.setParent('..') #End rowColumnLayout"uiHelpRclInside" adj=True

        mc.setParent('..') #End rowColumnLayout"uiHelpRclSide1" nc=3
        mc.setParent('..')

    def showWindHelp(self):
        mc.showWindow(self.windHelp)

class InfoUI:
    def __init__(self):

        if mc.windowPref('infoUdimWind', query=True, exists=True):
            mc.windowPref('infoUdimWind', remove=True )
        if mc.window('infoUdimWind', query=True, exists=True):
            mc.deleteUI('infoUdimWind', window=True)

        af = AcesFunctions()

        windbgc=0.2,0.2,0.2 #color of the background of the window

        self.windInfo = mc.window('infoUdimWind', title="Info", widthHeight=(290, 200), backgroundColor=windbgc, tlc=[250,450],te=25,s=True,mnb=False,mxb=False,i=False)


        mc.rowColumnLayout("rclInfoGlobal", adj=True)

        mc.iconTextButton(st='textOnly',label= "   ", h = 2, backgroundColor=bgcgreenM  )
        mc.separator( h=15, style='none' )
        mc.text(l='<font color=#00f58a><h3>This tool was made by LiamCollod<h3></font>',h=15)
        mc.text(l='<font <h5>mail pro: <i>lcollod@gmail.com<i><h5></font>',h=35)


        mc.rowColumnLayout("rclInfoSep", nc=3)
        mc.separator( w=10, style='none' )
        mc.iconTextButton(st='iconOnly',bgc=bgcwhite,w=3)

        mc.rowColumnLayout("rclInfo2ndCol", nc=1,cal=[1,'left'])
        mc.text(label=' > The IDT functions were mainly made for Arnold',fn='smallBoldLabelFont',h=16)
        mc.text(label="    as REDSHIFT doesn't support file nodes IDT",fn='smallBoldLabelFont',h=16)
        # mc.text(label=' > The script can take some time if your scene is big',fn='smallBoldLabelFont',h=16)
        mc.setParent('..')
        mc.setParent('..')

        mc.separator( h=5, style='none' )

        mc.rowColumnLayout("rclInfoSep2", nc=3)
        mc.separator( w=10, style='none' )
        mc.iconTextButton(st='iconOnly',bgc=bgcwhite,w=3)

        mc.rowColumnLayout("rclInfo2ndCol2", adj=True)
        stItbLink="iconAndTextHorizontal"
        imgItbLink=":/out_genericConstraint.png"
        mc.iconTextButton(st=stItbLink,label='GUMROAD LINK',fn='smallBoldLabelFont',i=imgItbLink,c=func.partial(af.hyperLink,4))
        mc.iconTextButton(st=stItbLink,label='TWITTER LINK',fn='smallBoldLabelFont',i=imgItbLink,c=func.partial(af.hyperLink,6))
        mc.iconTextButton(st=stItbLink,label='ARTSTATION LINK',fn='smallBoldLabelFont',i=imgItbLink,c=func.partial(af.hyperLink,7))
        mc.setParent('..')


        mc.setParent('..')
        mc.text(l='<font <h5>You find a bug ? Submit it to <i>monsieurlixm@gmail.com<i><h5></font>',h=35)
        mc.iconTextButton(st='textOnly',label= "   ", h = 2, backgroundColor=bgcwhite  )

        mc.setParent('..')

    def showWindInfo(self,*args):
        mc.showWindow(self.windInfo)




winshow= AcesUI()
winshow.showWind()

aftmp=AcesFunctions()
aftmp.helpUiUpdate()


########END CODE

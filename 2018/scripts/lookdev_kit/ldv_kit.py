# Lookdev kit 2.3 by Dusan Kovic - www.dusankovic.com
# Special thanks to Aleksandar Kocic - www.aleksandarkocic.com - for being great advisor on this project
# Also, thanks to Arvid Schneider - arvidschneider.com - for reporting a lot of stuff and making Lookdev Kit a better tool

# So you wanted to check my code! Before you go on, let me quote my TD friend Aleksandar:
# "Your code is crap, but it works... more or less"
# Remmeber those words while you read the rest of the code...

import maya.cmds as cmds
import maya.mel as mel
import mtoa.utils as mutils
import mtoa.core as core
import os
import subprocess
import sys
import math
import time
import glob
import webbrowser
import dk_shd

LOOKDEV_KIT_FOLDER = os.path.dirname(os.path.abspath(__file__))
MINI_HDR_FOLDER = os.path.join(LOOKDEV_KIT_FOLDER, "sourceimages", "mini").replace("\\", "/")
TEX_FOLDER = os.path.join(LOOKDEV_KIT_FOLDER, "sourceimages").replace("\\", "/")
HDR_FOLDER = os.path.join(TEX_FOLDER, "hdr").replace("\\", "/")
OIIO_FOLDER = os.path.join(LOOKDEV_KIT_FOLDER, "oiio", "bin").replace("\\", "/")
LDV_VER = "2.3"

# COMMANDS

def web(*args):
    webbrowser.open("https://dusankovic.artstation.com/pages/lookdev-kit")


def LDVbutton(*args):
    hdrs = hdr_list()[0]
    if len(hdrs) == 0:
        cmds.warning("Please run Refresh HDRs command")
        return
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.warning("Lookdev kit is already loaded")
        return
    if cmds.namespace(exists='mac') == True:
        createLDV()
        cmds.parent("mac:macbeth_spheres_grp", "dk_Ldv:lookdev_ctrl_grp")
        cmds.select(clear=True)
    if cmds.namespace(exists='dk_turn') == True:
        createLDV()
        cmds.parent("dk_turn:turntable_grp", "dk_Ldv:lookdevkit_grp")
        cmds.select(clear=True)
    else:
        createLDV()


def check_cm_config(*args):
    config_check = cmds.colorManagementPrefs(query = True,cmConfigFileEnabled = True)
    return config_check


def createLDV(*args):
    try:
        bounding_out = bounding()
        scale_factor = bounding_out[0]
        asset_center = bounding_out[1]
        asset = bounding_out[2]
        box = bounding_out[3]
        y_neg = bounding_out[4]
    except:
        box = 0
        scale_factor = 1
        asset_center = [0,90.175,0]
        y_neg = 0

    cmds.namespace(add='dk_Ldv')
    cmds.namespace(set=':dk_Ldv')

    distTool = cmds.distanceDimension(startPoint=[0, 0, 550], endPoint=[0, 0, 0])

    LDVgroup = cmds.group(name='lookdevkit_grp', empty=True)
    cmds.setAttr(LDVgroup + ".useOutlinerColor", 1)
    cmds.setAttr(LDVgroup + ".outlinerColor", 1, 1, 0)
    LDVctrlgroup = cmds.group(name='lookdev_ctrl_grp', empty=True)
    cmds.setAttr(LDVctrlgroup + ".useOutlinerColor", 1)
    cmds.setAttr(LDVctrlgroup + ".outlinerColor", 0, 1, 1)
    cmds.parent(LDVctrlgroup, LDVgroup)
    skydome = mutils.createLocator('aiSkyDomeLight', asLight=True)
    sky_name = cmds.rename(skydome[1], 'aiSkydome')
    skydome_shape = cmds.listRelatives(sky_name, shapes=True)

    # read camera visibility slider
    cmds.undoInfo(swf=False)
    skyVis = cmds.floatSliderGrp("sky_vis", query=True, value=True)
    cmds.setAttr(skydome_shape[0] + ".camera", skyVis)

    cmds.addAttr(skydome_shape[0], longName="rotOffset", min=0,max=360, defaultValue=0, attributeType="double")

    cmds.addAttr(skydome_shape[0], longName="start", dataType="string")
    start_val = cmds.optionMenu("chck_1001", query=True, select=True)
    cmds.setAttr(skydome_shape[0] + ".start", start_val, type="string")

    cmds.addAttr(skydome_shape[0], longName="ldv_ver", dataType="string")
    cmds.setAttr(skydome_shape[0] + ".ldv_ver", LDV_VER, type="string")

    cmds.addAttr(skydome_shape[0], longName="scale_factor", dataType="string")
    cmds.setAttr(skydome_shape[0] + ".scale_factor", scale_factor, type="string")

    cmds.addAttr(skydome_shape[0], longName="asset_center", dataType="string")
    cmds.setAttr(skydome_shape[0] + ".asset_center", asset_center, type="string")

    cmds.addAttr(skydome_shape[0], longName="y_neg", dataType="string")
    cmds.setAttr(skydome_shape[0] + ".y_neg", y_neg, type="string")

    cmds.addAttr(skydome_shape[0], longName="turntable_fr", dataType="string")
    tr_fr = cmds.optionMenu('autott', value=True, query=True)
    cmds.setAttr(skydome_shape[0] + ".turntable_fr", tr_fr, type="string")

    cmds.addAttr(skydome_shape[0], longName="turntable_ass", dataType="string")
    turn_ass = ""
    cmds.setAttr(skydome_shape[0] + ".turntable_ass", turn_ass, type="string")

    # read rotation offset slider
    rotOff = cmds.floatSliderGrp("rotOff", query=True, value=True)
    cmds.setAttr(sky_name + ".rotateY", rotOff)
    cmds.setAttr(skydome_shape[0] + ".rotOffset", rotOff)
    cmds.undoInfo(swf=True)

    hdrtx = hdr_list()[0]
    hdrskynum = len(hdrtx)
    cmds.addAttr(skydome_shape[0], longName="hdrsl", min=1,max=hdrskynum, defaultValue=1, attributeType="long")
    cmds.setAttr('dk_Ldv:aiSkydomeShape.aiSamples', 3)
    # read exposure slider
    value = cmds.floatSliderGrp('exp', query=True, value=True)
    cmds.setAttr('dk_Ldv:aiSkydomeShape.exposure', value)
    cmds.undoInfo(swf=True)

    if scale_factor <= 1:
        obj_factor = 1 
    if scale_factor > 1:
        obj_factor = scale_factor

    cmds.setAttr('dk_Ldv:aiSkydomeShape.skyRadius', 5000 * obj_factor)
    cmds.setAttr('dk_Ldv:aiSkydomeShape.resolution', 2048)
    cmds.setAttr('dk_Ldv:aiSkydome.overrideEnabled', 1)
    cmds.setAttr('dk_Ldv:aiSkydome.overrideDisplayType', 2)

    cmds.parent(sky_name, LDVctrlgroup)
    imageNode = cmds.shadingNode("file", asTexture=True, n="hdrTextures")
    hdr_num = cmds.intSliderGrp('hdrSw', query=True, value=True)
    file = hdr_list()[0]
    hdr_file = hdr_list()[2]

    if len(file) == 0:
        new_hdr = os.path.join(TEX_FOLDER, "no_prev.tx").replace("\\", "/")
    else:
        new_hdr = os.path.join(HDR_FOLDER, hdr_file[hdr_num-1]).replace("\\", "/")

    cmds.setAttr("dk_Ldv:hdrTextures.fileTextureName", new_hdr, type="string")
    cmds.setAttr(imageNode + '.aiAutoTx', 0)

    if check_cm_config() == True:
        cmds.setAttr(imageNode + '.colorSpace', 'Utility - Linear - sRGB', type='string')
    if check_cm_config() == False:
        cmds.setAttr(imageNode + '.colorSpace', 'scene-linear Rec 709/sRGB', type='string')

    cmds.connectAttr(imageNode + '.outColor', skydome_shape[0] + '.color', force=True)

    shCatchMain = cmds.polyPlane(n='shadowCatcher', w=4000 * obj_factor, h=4000 * obj_factor, sx=1, sy=1, cuv=2, ax=[0, 1, 0], ch=False)
    shCatch = shCatchMain[0]
    cmds.addAttr(shCatchMain, longName="shadowChckVis", attributeType="bool")
    shadowStr = cmds.shadingNode('aiShadowMatte', asShader=True)
    shadowMatte = cmds.rename(shadowStr, 'aiShadow')
    cmds.select(shCatch)
    cmds.hyperShade(assign=shadowMatte)
    cmds.parent(shCatch, LDVctrlgroup)
    cmds.setAttr(shCatch + ".overrideEnabled", 1)
    cmds.setAttr(shCatch + ".overrideDisplayType", 2)
    cmds.setAttr(shCatch + ".translateY", y_neg)

    # read shadow matte checkbox
    shCatchBox = cmds.checkBox("shMatte", query=True, value=True)
    cmds.setAttr(shCatch + ".shadowChckVis", shCatchBox)
    cmds.setAttr(shCatch + ".visibility", shCatchBox)

    # camera
    cam = cmds.camera(
        focalLength=50,
        centerOfInterest=5,
        lensSqueezeRatio=1,
        cameraScale=1,
        horizontalFilmAperture=1.41732,
        horizontalFilmOffset=0,
        verticalFilmAperture=0.94488,
        verticalFilmOffset=0,
        filmFit="Fill",
        overscan=1.2,
        motionBlur=0,
        shutterAngle=144,
        nearClipPlane=1,
        farClipPlane=1000000,
        orthographic=0,
        orthographicWidth=30,
        panZoomEnabled=0,
        horizontalPan=0,
        verticalPan=0,
        zoom=1,
        displayGateMask=1,
        displayResolution=1,
    )

    cmds.lookThru(cam)
    cmds.setAttr(cam[0] + ".renderable", 1)

    cmds.setAttr(cam[0] + ".displayGateMaskColor", 0.1, 0.1, 0.1, type="double3")
    cmds.setAttr(cam[0] + ".translateZ", 550)
    cmds.setAttr(cam[0] + ".locatorScale", 15)
    cmds.setAttr(cam[0] + ".displayCameraFrustum", 1)

    # add additional attributes
    cmds.addAttr(cam[0], longName="DoF", attributeType="bool")

    senCount = cmds.optionMenu('sensor', numberOfItems=True, query=True)
    cmds.addAttr(cam[0], longName="SensorCam", attributeType="long", min=1, max=senCount)

    focCount = cmds.optionMenu('focal', numberOfItems=True, query=True)
    cmds.addAttr(cam[0], longName="FocalCam", attributeType="long", min=1, max=focCount)

    fstopCount = cmds.optionMenu('fstop', numberOfItems=True, query=True)
    cmds.addAttr(cam[0], longName="FstopCam", attributeType="long", min=1, max=fstopCount)

    # focus plane
    focus_text_import = os.path.join(TEX_FOLDER, "ldv_fcs_font.fbx").replace("\\", "/")
    fcsPlane = cmds.curve(name="focusPlane_ctrl", degree=1, point=[(-198, -111.5, 0), (-198, 111.5, 0), (198, 111.5, 0), (198, -111.5, 0), (-198, -111.5, 0)])
    fcsText = cmds.file( focus_text_import, i=True )
    fcsGrp = cmds.ls("dk_Ldv:focusPlane_txtShape", long=True)

    # text position
    cmds.setAttr(fcsGrp[0] + ".scaleX", 12)
    cmds.setAttr(fcsGrp[0] + ".scaleY", 12)
    cmds.setAttr(fcsGrp[0] + ".scaleZ", 12)
    cmds.setAttr(fcsGrp[0] + ".translateX", 120)
    cmds.setAttr(fcsGrp[0] + ".translateY", 112)
    cmds.makeIdentity(fcsGrp, translate=True, scale=True, apply=True)

    fcsSel = cmds.listRelatives(fcsGrp, allDescendents=True, fullPath=True)
    fcsSel2 = cmds.listRelatives(fcsSel, shapes=True, fullPath=True)
    fcsSelPlane = cmds.listRelatives(fcsPlane, allDescendents=True)
    fcsSelPlane2 = cmds.ls(fcsSelPlane, shapes=True, long=True)
    fcsSelMain = fcsSel2 + fcsSelPlane2

    for each in fcsSel2:
        cmds.setAttr(each + ".overrideEnabled", 1)
        cmds.setAttr(each + ".overrideDisplayType", 1)

    crvGrp = cmds.group(name="fcsCrv", empty=True)
    crvGrpa = cmds.listRelatives(crvGrp, shapes=True)

    cmds.parent(fcsSelMain, crvGrp, shape=True, relative=True)
    cmds.delete("dk_Ldv:focusPlane_txtShape")
    cmds.delete(fcsPlane)

    distSel = cmds.ls(distTool)
    distShape = distSel[0]
    camShape = cam[0]
    cmds.setAttr(distSel[0] + ".visibility", 0)
    distLoc = cmds.listConnections(distSel, source=True)
    for each in distLoc:
        cmds.setAttr(each + ".visibility", 0)

    cmds.parent("dk_Ldv:locator2", crvGrp)
    cmds.parent("dk_Ldv:locator1", cam[0])

    cmds.connectAttr(distShape + ".distance", camShape + ".aiFocusDistance", force=True)

    cmds.parent(distTool, "dk_Ldv:lookdev_ctrl_grp", shape=True)
    cmds.delete("dk_Ldv:distanceDimension1")
    cmds.parent(crvGrp, cam[0])
    cmds.parent(cam[0], "dk_Ldv:lookdev_ctrl_grp")
    cmds.setAttr(cam[0] + ".translateY", 200)
    cmds.setAttr(cam[0] + ".translateZ", 565)
    cmds.setAttr(cam[0] + ".rotateX", -11)

    # camera DoF checkbox read
    camBox = cmds.checkBox("camDoF", query=True, value=True)
    cmds.setAttr(cam[0] + ".DoF", camBox)
    cmds.setAttr("dk_Ldv:fcsCrv.visibility", camBox)

    cmds.makeIdentity(crvGrp, translate=True, apply=True)
    cmds.setAttr(crvGrp + ".translateZ", -25.563)
    cmds.makeIdentity(crvGrp, translate=True, apply=True)

    cmds.setAttr(crvGrp + ".translateX", keyable=False, lock=True)
    cmds.setAttr(crvGrp + ".translateY", keyable=False, lock=True)
    cmds.setAttr(crvGrp + ".rotateX", keyable=False, lock=True)
    cmds.setAttr(crvGrp + ".rotateY", keyable=False, lock=True)
    cmds.setAttr(crvGrp + ".rotateZ", keyable=False, lock=True)
    cmds.setAttr(crvGrp + ".scaleX", keyable=False)
    cmds.setAttr(crvGrp + ".scaleY", keyable=False)
    cmds.setAttr(crvGrp + ".scaleZ", keyable=False)

    # create global ctrl
    ctrl_num = 2050 * obj_factor
    ldvCtrl = cmds.curve(name="ldvGlobal_ctrl", degree=1, point=[(-ctrl_num, 0, ctrl_num), (-ctrl_num, 0, -ctrl_num), (ctrl_num, 0, -ctrl_num), (ctrl_num, 0, ctrl_num), (-ctrl_num, 0, ctrl_num)])
    cmds.setAttr(ldvCtrl + ".translateY", y_neg)

    cmds.parent(ldvCtrl, LDVgroup)
    cmds.scaleConstraint(ldvCtrl, LDVctrlgroup, maintainOffset=True, weight=1)

    focal()
    fstop()

    # remove and lock attributes
    cmds.setAttr(sky_name + ".translateX", keyable=False)
    cmds.setAttr(sky_name + ".translateY", keyable=False)
    cmds.setAttr(sky_name + ".translateZ", keyable=False)
    cmds.setAttr(sky_name + ".rotateX", keyable=False)
    cmds.setAttr(sky_name + ".rotateY", keyable=False)
    cmds.setAttr(sky_name + ".rotateZ", keyable=False)
    LDVgrplist = [LDVgroup, LDVctrlgroup, shCatch, ldvCtrl]
    for each in LDVgrplist:
        cmds.setAttr(each + ".translateX", keyable=False, lock=True)
        cmds.setAttr(each + ".translateY", keyable=False, lock=True)
        cmds.setAttr(each + ".translateZ", keyable=False, lock=True)
        cmds.setAttr(each + ".rotateX", keyable=False, lock=True)
        cmds.setAttr(each + ".rotateY", keyable=False, lock=True)
        cmds.setAttr(each + ".rotateZ", keyable=False, lock=True)

    #camera autoframe move
    auto_frame(cam, scale_factor, crvGrp, box, asset_center, y_neg)

    cmds.namespace(set=':')

    try:
        cmds.select(asset)
        turntableButton()
    except:
        pass

    cmds.select(clear=True)


def auto_frame(camera, scale, curves, bbox, asset_center,y_neg):
    cam = camera
    scale_factor = scale
    crv = curves
    crv_pos_bef = cmds.pointPosition(crv, world = True)

    world_loc = cmds.spaceLocator(name="world_loc", position=[0, 0, 0])
    cam_loc = cmds.spaceLocator(name="cam_loc", position=[0, 200, 565])
    cmds.parent(cam_loc, world_loc)
    cmds.setAttr(world_loc[0] + ".scaleX", scale_factor)
    cmds.setAttr(world_loc[0] + ".scaleY", scale_factor)
    cmds.setAttr(world_loc[0] + ".scaleZ", scale_factor)
    cmds.setAttr(world_loc[0] + ".translateY", y_neg)
    cam_pos = cmds.pointPosition(cam_loc, world = True)
    cmds.setAttr(cam[0] + ".translateX", cam_pos[0])
    cmds.setAttr(cam[0] + ".translateY", cam_pos[1])
    cmds.setAttr(cam[0] + ".translateZ", cam_pos[2])
    try:
        cmds.setAttr(cam[0] + ".translateX", cam_pos[0] + asset_center[0])
    except:
        pass
    cmds.delete(world_loc)

    crv_pos_aft = cmds.pointPosition(crv, world = True)

    try:
        if zmax >= 0:
            zmax = asset_center[2] + bbox * 0.5
        if zmax < 0:
            zmax = -asset_center[2] + bbox * 0.5
    except:
        zmax = 0

    try:
        cam_ass_dist = math.sqrt((cam_pos[2] - asset_center[2])**2 + (cam_pos[1] - asset_center[1])**2)
        focus_diff = 575.563 - cam_ass_dist
    except:
        focus_diff = 0

    if focus_diff <= 575.563:
        cmds.setAttr(crv + ".translateZ", focus_diff + zmax)
    else:
        cmds.setAttr(crv + ".translateZ", -focus_diff + zmax)

    try:
        cmds.viewLookAt(cam[1], pos=asset_center)
    except:
        pass


def removeLDV(*args):
    cmds.namespace(set=':')
    if cmds.namespace(exists='dk_Ldv') == False:
        cmds.warning("Nothing to remove")
        return
    if cmds.namespace(exists='mac') == True:
        cmds.namespace(removeNamespace='mac', deleteNamespaceContent=True)
    if cmds.namespace(exists='dk_turn') == True:
        cmds.namespace(removeNamespace='dk_turn', deleteNamespaceContent=True)
    if cmds.namespace(exists='dk_bake') == True:
        cmds.namespace(removeNamespace='dk_bake', deleteNamespaceContent=True)
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.namespace(removeNamespace='dk_Ldv', deleteNamespaceContent=True)

    cmds.lookThru("persp")


def Macbutton(*args):
    hdrs = hdr_list()[0]
    if len(hdrs) == 0:
        cmds.warning("Please run Refresh HDRs command")
        return
    if cmds.namespace(exists=':mac') == True:
        cmds.warning("Macbeth chart and spheres are already loaded")
        return
    if cmds.namespace(exists='dk_Ldv') == True:
        createMAC()
        cmds.parent("mac:macbeth_spheres_grp", "dk_Ldv:lookdev_ctrl_grp")
        cmds.select(clear=True)
    if cmds.namespace(exists='dk_Ldv') == False:
        createMAC()


def createMAC(*args):
    cmds.namespace(add='mac')
    cmds.namespace(set=':mac')
    
    macbeth_data = [
        {
            "row": 1,
            "column": 1,
            "name": "Patch_01_Dark_Skin",
            "base_color": (0.13574, 0.08508, 0.05844),
        },
        {
            "row": 1,
            "column": 2,
            "name": "Patch_02_Light_Skin",
            "base_color": (0.44727, 0.29639, 0.22607),
        },
        {
            "row": 1,
            "column": 3,
            "name": "Patch_03_Blue_Sky",
            "base_color": (0.14404, 0.18530, 0.30762),
        },
        {
            "row": 1,
            "column": 4,
            "name": "Patch_04_Foliage",
            "base_color": (0.11804, 0.14587, 0.06372),
        },
        {
            "row": 1,
            "column": 5,
            "name": "Patch_05_Blue_Flower",
            "base_color": (0.23254, 0.21704, 0.39697),
        },
        {
            "row": 1,
            "column": 6,
            "name": "Patch_06_Bluish_Green",
            "base_color": (0.26196, 0.47803, 0.41626),
        },
        {
            "row": 2,
            "column": 1,
            "name": "Patch_07_Orange",
            "base_color": (0.52686, 0.23767, 0.06519),
        },
        {
            "row": 2,
            "column": 2,
            "name": "Patch_08_Purplish_Blue",
            "base_color": (0.08972, 0.10303, 0.34717),
        },
        {
            "row": 2,
            "column": 3,
            "name": "Patch_09_Moderate_Red",
            "base_color": (0.37646, 0.11469, 0.11987),
        },
        {
            "row": 2,
            "column": 4,
            "name": "Patch_10_Purple",
            "base_color": (0.08813, 0.04837, 0.12622),
        },
        {
            "row": 2,
            "column": 5,
            "name": "Patch_11_Yellow_Green",
            "base_color": (0.37329, 0.47803, 0.10223),
        },
        {
            "row": 2,
            "column": 6,
            "name": "Patch_12_Orange_Yellow",
            "base_color": (0.59424, 0.38135, 0.07593),
        },
        {
            "row": 3,
            "column": 1,
            "name": "Patch_13_Blue",
            "base_color": (0.04327, 0.04965, 0.25073),
        },
        {
            "row": 3,
            "column": 2,
            "name": "Patch_14_Green",
            "base_color": (0.12939, 0.27075, 0.08832),
        },
        {
            "row": 3,
            "column": 3,
            "name": "Patch_15_Red",
            "base_color": (0.28809, 0.06543, 0.04855),
        },
        {
            "row": 3,
            "column": 4,
            "name": "Patch_16_Yellow",
            "base_color": (0.70947, 0.58350, 0.08929),
        },
        {
            "row": 3,
            "column": 5,
            "name": "Patch_17_Magenta",
            "base_color": (0.36133, 0.11279, 0.26929),
        },
        {
            "row": 3,
            "column": 6,
            "name": "Patch_18_Cyan",
            "base_color": (0.07062, 0.21643, 0.35132),
        },
        {
            "row": 4,
            "column": 1,
            "name": "Patch_19_White_9_5_005D",
            "base_color": (0.87891, 0.88379, 0.84131),
        },
        {
            "row": 4,
            "column": 2,
            "name": "Patch_20_Neutral_8_023D",
            "base_color": (0.58691, 0.59131, 0.58545),
        },
        {
            "row": 4,
            "column": 3,
            "name": "Patch_21_Neutral_6_5_044D",
            "base_color": (0.36133, 0.36646, 0.36523),
        },
        {
            "row": 4,
            "column": 4,
            "name": "Patch_22_Neutral_5_070D",
            "base_color": (0.19031, 0.19080, 0.18994),
        },
        {
            "row": 4,
            "column": 5,
            "name": "Patch_23_Neutral_3_5_1_05D",
            "base_color": (0.08710, 0.08856, 0.08960),
        },
        {
            "row": 4,
            "column": 6,
            "name": "Patch_24_Black_2_1_5D",
            "base_color": (0.03146, 0.03149, 0.03220),
        },
    ]

    cmds.scriptEditorInfo(suppressWarnings=1,si=1,sr=1, ssw=1)
    MACgroup = cmds.group(name='macbeth_spheres_grp', empty=True)
    patchGroupFlat = cmds.group(name='macbethPatchesFlat_grp', empty=True)
    MACflat = cmds.group(name='macbethFlat_grp', empty=True)
    MACctrlGrp = cmds.group(name='macbeth_ctrl_grp', empty=True)
    cmds.parent(MACctrlGrp, MACgroup)
    cmds.parent(MACflat, MACctrlGrp)
    cmds.parent(patchGroupFlat, MACflat)
    MACshaded = cmds.group(name='macbethShaded_grp', empty=True)
    patchGroupShaded = cmds.group(name='macbethPatchesShaded_grp', empty=True)
    cmds.parent(MACshaded, MACctrlGrp)
    cmds.parent(patchGroupShaded, MACshaded)
    Sphgroup = cmds.group(name='spheres_grp', empty=True)
    cmds.parent(Sphgroup, MACctrlGrp)
    mtp = 4.5

    # checker body flat
    chckBodyFlat = cmds.polyCube(name="checkerBodyFlat", width=28,
                                 height=19, depth=0.5, createUVs=4, ch=False)
    cmds.setAttr(chckBodyFlat[0] + ".translateZ", -0.25)
    cmds.setAttr(chckBodyFlat[0] + ".translateY", 12)
    cmds.makeIdentity(chckBodyFlat[0], translate=True, apply=True)
    cmds.move(0, 0, 0, chckBodyFlat[0] + ".scalePivot",
              chckBodyFlat[0] + ".rotatePivot", absolute=True)
    cmds.parent(chckBodyFlat[0], MACflat)
    # checker body shader Flat
    chckShdFlat = cmds.shadingNode('aiFlat', asShader=True, name="aiMacbethBodyFlat")
    cmds.setAttr(chckShdFlat + ".color", 0, 0, 0, type='double3')
    cmds.select(chckBodyFlat[0])
    cmds.hyperShade(assign=chckShdFlat)

    # checker body shaded
    chckBodyShaded = cmds.polyCube(name="checkerBodyShaded", width=28,
                                   height=19, depth=0.5, createUVs=4, ch=False)
    cmds.setAttr(chckBodyShaded[0] + ".translateZ", -0.25)
    cmds.setAttr(chckBodyShaded[0] + ".translateY", 32)
    cmds.makeIdentity(chckBodyShaded[0], translate=True, apply=True)
    cmds.move(0, 0, 0, chckBodyShaded[0] + ".scalePivot",
              chckBodyShaded[0] + ".rotatePivot", absolute=True)
    cmds.parent(chckBodyShaded[0], MACshaded)
    # checker body shader shaded
    chckShdShaded = cmds.shadingNode('aiStandardSurface', asShader=True, name="aiMacbethBodyShaded")
    cmds.setAttr(chckShdShaded + ".base", 1)
    cmds.setAttr(chckShdShaded + ".baseColor", 0, 0, 0, type='double3')
    cmds.setAttr(chckShdShaded + ".specular", 0.0)
    cmds.setAttr(chckShdShaded + ".specularRoughness", 0.5)
    cmds.select(chckBodyShaded[0])
    cmds.hyperShade(assign=chckShdShaded)

    # spheres
    # chrome
    chrome = cmds.polySphere(name="chromeSphere", radius=6.6, createUVs=2, ch=False)
    cmds.setAttr(chrome[0] + ".translateX", -7.5)
    cmds.setAttr(chrome[0] + ".translateY", 49)
    cmds.setAttr(chrome[0] + '.aiSubdivType', 1)
    cmds.setAttr(chrome[0] + '.aiSubdivIterations', 3)
    cmds.makeIdentity(chrome[0], translate=True, apply=True)
    cmds.move(0, 0, 0, chrome[0] + ".scalePivot", chrome[0] + ".rotatePivot", absolute=True)
    cmds.parent(chrome[0], Sphgroup)
    chromeShd = cmds.shadingNode('aiStandardSurface', asShader=True, name="aiChrome")
    cmds.setAttr(chromeShd + ".base", 1)
    cmds.setAttr(chromeShd + ".baseColor", 0.75, 0.75, 0.75, type='double3')
    cmds.setAttr(chromeShd + ".metalness", 1)
    cmds.setAttr(chromeShd + ".specular", 1)
    cmds.setAttr(chromeShd + ".specularRoughness", 0)
    cmds.select(chrome[0])
    cmds.hyperShade(assign=chromeShd)
    # gray
    gray = cmds.polySphere(name="graySphere", radius=6.6, createUVs=2, ch=False)
    cmds.setAttr(gray[0] + ".translateX", 7.5)
    cmds.setAttr(gray[0] + ".translateY", 49)
    cmds.setAttr(gray[0] + '.aiSubdivType', 1)
    cmds.setAttr(gray[0] + '.aiSubdivIterations', 3)
    cmds.makeIdentity(gray[0], translate=True, apply=True)
    cmds.move(0, 0, 0, gray[0] + ".scalePivot", gray[0] + ".rotatePivot", absolute=True)
    cmds.parent(gray[0], Sphgroup)
    grayShd = cmds.shadingNode('aiStandardSurface', asShader=True, name="aiGray")
    cmds.setAttr(grayShd + ".base", 1)
    cmds.setAttr(grayShd + ".baseColor", 0.18, 0.18, 0.18, type='double3')
    cmds.setAttr(grayShd + ".specular", 1)
    cmds.setAttr(grayShd + ".specularRoughness", 0.65)
    cmds.select(gray[0])
    cmds.hyperShade(assign=grayShd)

    dispOver = [gray, chrome, chckBodyShaded, chckBodyFlat]
    for each in dispOver:
        doSel = cmds.ls(each)
        cmds.setAttr(each[0] + ".overrideEnabled", 1)
        cmds.setAttr(each[0] + ".overrideDisplayType", 2)

    # PATCHES FLAT
    
    for each in macbeth_data:
        # geo
        patch = cmds.polyCube(name=(each["name"] + "Flat"), width=4.2,height=4.2, depth=0.3, createUVs=4, axis=[0, 1, 0], ch=False)
        patchDOsel = cmds.ls(patch)
        cmds.setAttr(patch[0] + ".translateX", (each["column"])*mtp)
        cmds.setAttr(patch[0] + ".translateY", (each["row"])*-mtp)
        xpos = cmds.getAttr(patch[0] + ".translateX")
        ypos = cmds.getAttr(patch[0] + ".translateY")
        cmds.setAttr(patch[0] + ".translateX", xpos-15.75)
        cmds.setAttr(patch[0] + ".translateY", ypos+23.25)
        cmds.makeIdentity(patch[0], translate=True, apply=True)
        cmds.move(0, 0, 0, patch[0] + ".scalePivot", patch[0] + ".rotatePivot", absolute=True)
        cmds.setAttr(patch[0] + ".receiveShadows", 0)
        cmds.setAttr(patch[0] + ".motionBlur", 0)
        cmds.setAttr(patch[0] + ".castsShadows", 0)
        cmds.setAttr(patch[0] + ".visibleInRefractions", 0)
        cmds.setAttr(patch[0] + ".visibleInReflections", 0)
        cmds.setAttr(patch[0] + ".aiVisibleInDiffuseReflection", 0)
        cmds.setAttr(patch[0] + ".aiVisibleInSpecularReflection", 0)
        cmds.setAttr(patch[0] + ".aiVisibleInDiffuseTransmission", 0)
        cmds.setAttr(patch[0] + ".aiVisibleInSpecularTransmission", 0)
        cmds.setAttr(patch[0] + ".aiVisibleInVolume", 0)
        cmds.setAttr(patch[0] + ".aiSelfShadows", 0)
        cmds.setAttr(patchDOsel[0] + ".overrideEnabled", 1)
        cmds.setAttr(patchDOsel[0] + ".overrideDisplayType", 2)
        cmds.setAttr(patch[0] + ".translateX", keyable=False, lock=True)
        cmds.setAttr(patch[0] + ".translateY", keyable=False, lock=True)
        cmds.setAttr(patch[0] + ".translateZ", keyable=False, lock=True)
        cmds.setAttr(patch[0] + ".rotateX", keyable=False, lock=True)
        cmds.setAttr(patch[0] + ".rotateY", keyable=False, lock=True)
        cmds.setAttr(patch[0] + ".rotateZ", keyable=False, lock=True)
        cmds.parent(patch[0], patchGroupFlat)

        # shader
        mat_name = each["name"] + "Flat"
        sg_name = mat_name + "SG"
        patchBscShd = cmds.shadingNode('aiFlat', asShader=True, name=mat_name)
        SG = cmds.sets(name= sg_name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr(patchBscShd + ".outColor", SG + ".surfaceShader")
        cmds.setAttr(patchBscShd + ".color", each["base_color"][0],each["base_color"][1], each["base_color"][2], type='double3')
        cmds.select(patch[0])
        cmds.hyperShade(assign=patchBscShd)

        # PATCHES SHADED
    for each in macbeth_data:
        # geo
        patchShaded = cmds.polyCube(name=(each["name"] + "Shaded"), width=4.2, height=4.2, depth=0.3, createUVs=4, axis=[0, 1, 0], ch=False)
        patchShadedDOsel = cmds.ls(patchShaded)
        cmds.setAttr(patchShaded[0] + ".translateX", (each["column"])*mtp)
        cmds.setAttr(patchShaded[0] + ".translateY", (each["row"])*-mtp)
        xpos = cmds.getAttr(patchShaded[0] + ".translateX")
        ypos = cmds.getAttr(patchShaded[0] + ".translateY")
        cmds.setAttr(patchShaded[0] + ".translateX", xpos-15.75)
        cmds.setAttr(patchShaded[0] + ".translateY", ypos+43.25)
        cmds.makeIdentity(patchShaded[0], translate=True, apply=True)
        cmds.move(0, 0, 0, patchShaded[0] + ".scalePivot",patchShaded[0] + ".rotatePivot", absolute=True)
        cmds.setAttr(patchShaded[0] + ".receiveShadows", 0)
        cmds.setAttr(patchShaded[0] + ".motionBlur", 0)
        cmds.setAttr(patchShaded[0] + ".castsShadows", 0)
        cmds.setAttr(patchShaded[0] + ".visibleInRefractions", 0)
        cmds.setAttr(patchShaded[0] + ".visibleInReflections", 0)
        cmds.setAttr(patchShaded[0] + ".aiVisibleInDiffuseReflection", 0)
        cmds.setAttr(patchShaded[0] + ".aiVisibleInSpecularReflection", 0)
        cmds.setAttr(patchShaded[0] + ".aiVisibleInDiffuseTransmission", 0)
        cmds.setAttr(patchShaded[0] + ".aiVisibleInSpecularTransmission", 0)
        cmds.setAttr(patchShaded[0] + ".aiVisibleInVolume", 0)
        cmds.setAttr(patchShaded[0] + ".aiSelfShadows", 0)
        cmds.setAttr(patchShadedDOsel[0] + ".overrideEnabled", 1)
        cmds.setAttr(patchShadedDOsel[0] + ".overrideDisplayType", 2)
        cmds.setAttr(patchShaded[0] + ".translateX", keyable=False, lock=True)
        cmds.setAttr(patchShaded[0] + ".translateY", keyable=False, lock=True)
        cmds.setAttr(patchShaded[0] + ".translateZ", keyable=False, lock=True)
        cmds.setAttr(patchShaded[0] + ".rotateX", keyable=False, lock=True)
        cmds.setAttr(patchShaded[0] + ".rotateY", keyable=False, lock=True)
        cmds.setAttr(patchShaded[0] + ".rotateZ", keyable=False, lock=True)
        cmds.parent(patchShaded[0], patchGroupShaded)

        # shader
        mat_name = each["name"] + "Shaded"
        patchBscShdShaded = cmds.shadingNode('aiStandardSurface', asShader=True, name=mat_name)
        cmds.setAttr(patchBscShdShaded + ".base", 1)
        cmds.setAttr(patchBscShdShaded + ".baseColor",each["base_color"][0], each["base_color"][1], each["base_color"][2], type='double3')
        cmds.setAttr(patchBscShdShaded + ".specular", 0)
        cmds.setAttr(patchBscShdShaded + ".specularRoughness", 0.7)
        sg_name = mat_name + "SG"
        SG = cmds.sets(name= sg_name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr(patchBscShdShaded + ".outColor", SG + ".surfaceShader")
        cmds.select(patchShaded[0])
        cmds.hyperShade(assign=patchBscShdShaded)
    

    # macbeth control curve and constraints
    macCtrl = cmds.curve(name="Macbeth_ctrl", degree=1, point=[(-17, -2, 0), (-17, 57, 0), (17, 57, 0), (17, -2, 0), (-17, -2, 0)])
    macLoc = cmds.spaceLocator(name="mac_loc", position=[0, 0, 0])

    cmds.parent(macCtrl, MACgroup)
    cmds.parent(macLoc, MACgroup)
    cmds.setAttr(macCtrl + ".translateY", 2)
    cmds.makeIdentity(macCtrl, translate=True, apply=True)
    cmds.move(0, 0, 0, macCtrl + ".scalePivot", macCtrl + ".rotatePivot", absolute=True)

    cmds.parentConstraint(macCtrl, MACctrlGrp, maintainOffset=True, weight=1)
    cmds.scaleConstraint(macCtrl, MACctrlGrp, maintainOffset=True, weight=1)
    cmds.setAttr(macCtrl + ".translateX", -170)

    # CREATE A MAC SCALING
    if cmds.namespace(exists=":dk_Ldv") == True:
        scale = cmds.getAttr("dk_Ldv:ldvGlobal_ctrl.scaleX")
        cmds.parentConstraint(macLoc[0], macCtrl, maintainOffset=True, weight=1)
        cmds.setAttr(macLoc[0] + ".scaleX", scale)
    try:
        scale_factor = float(cmds.getAttr("dk_Ldv:aiSkydomeShape.scale_factor"))
    except:
        scale_factor = 1
    try:
        get_cent = cmds.getAttr("dk_Ldv:aiSkydomeShape.asset_center")
        aset_data = list(get_cent.split(","))
        asset_center = [aset_data[0][1:],aset_data[1],aset_data[2]]
    except:
        asset_center = [0,0,0]
    try:
        y_min = cmds.getAttr("dk_Ldv:aiSkydomeShape.y_neg")
    except:
        y_min = 0

    cmds.setAttr(macLoc[0] + ".scaleX", scale_factor)
    cmds.setAttr(macLoc[0] + ".scaleY", scale_factor)
    cmds.setAttr(macLoc[0] + ".scaleZ", scale_factor)
    cmds.setAttr("mac:Macbeth_ctrl.scaleX", scale_factor)
    cmds.setAttr("mac:Macbeth_ctrl.scaleY", scale_factor)
    cmds.setAttr("mac:Macbeth_ctrl.scaleZ", scale_factor)
    cmds.setAttr("mac:mac_loc.translateX", float(asset_center[0]))
    cmds.setAttr("mac:mac_loc.translateY", float(y_min))
    cmds.setAttr("mac:mac_loc.visibility", 0)

    # lock attr
    MACgrplist = [MACgroup, patchGroupFlat, MACflat, MACctrlGrp, MACshaded,
                  patchGroupShaded, Sphgroup, chckBodyFlat[0], chckBodyShaded[0], chrome[0], gray[0]]
    for each in MACgrplist:
        cmds.setAttr(each + ".translateX", keyable=False, lock=True)
        cmds.setAttr(each + ".translateY", keyable=False, lock=True)
        cmds.setAttr(each + ".translateZ", keyable=False, lock=True)
        cmds.setAttr(each + ".rotateX", keyable=False, lock=True)
        cmds.setAttr(each + ".rotateY", keyable=False, lock=True)
        cmds.setAttr(each + ".rotateZ", keyable=False, lock=True)

    # Arnold attributes
    attrList = [chckBodyFlat[0], chckBodyShaded[0], chrome[0], gray[0]]
    for each in attrList:
        cmds.setAttr(each + ".receiveShadows", 0)
        cmds.setAttr(each + ".motionBlur", 0)
        cmds.setAttr(each + ".castsShadows", 0)
        cmds.setAttr(each + ".visibleInRefractions", 0)
        cmds.setAttr(each + ".visibleInReflections", 0)
        cmds.setAttr(each + ".aiVisibleInDiffuseReflection", 0)
        cmds.setAttr(each + ".aiVisibleInSpecularReflection", 0)
        cmds.setAttr(each + ".aiVisibleInDiffuseTransmission", 0)
        cmds.setAttr(each + ".aiVisibleInSpecularTransmission", 0)
        cmds.setAttr(each + ".aiVisibleInVolume", 0)
        cmds.setAttr(each + ".aiSelfShadows", 0)

    cmds.scriptEditorInfo(suppressWarnings=0, si=0,sr=0,ssw=0)

    cmds.namespace(set=':')
    cmds.select(clear=True)


def removeMAC(*args):
    cmds.namespace(set=':')
    if cmds.namespace(exists='mac') == False:
        cmds.warning('Nothing to remove')
    if cmds.namespace(exists='mac') == True:
        cmds.namespace(removeNamespace=':mac', deleteNamespaceContent=True)


def hdrSw(*args):
    hdr_num = cmds.intSliderGrp("hdrSw", query=True, value=True)
    tx_file = hdr_list()[0]
    hdr_file = hdr_list()[2]
    mini_file = hdr_list()[1]

    if cmds.namespace(exists="dk_Ldv") == True and len(tx_file) != 0:
        new_hdr = os.path.join(HDR_FOLDER, hdr_file[hdr_num-1]).replace("\\", "/")
        mini_int_file = os.path.join(MINI_HDR_FOLDER, mini_file[hdr_num-1]).replace("\\", "/")
        cmds.image("hdrSym", edit=True, image=mini_int_file)
        cmds.setAttr("dk_Ldv:hdrTextures.fileTextureName", new_hdr, type="string")
        cmds.setAttr("dk_Ldv:aiSkydomeShape.hdrsl", hdr_num)
        cmds.setAttr("dk_Ldv:hdrTextures.colorSpace", "Raw", type="string")
    if len(tx_file) != 0:
        mini_int_file = os.path.join(MINI_HDR_FOLDER, mini_file[hdr_num-1]).replace("\\", "/")
        cmds.image("hdrSym", edit=True, image=mini_int_file)
        try:
            if check_cm_config() == True:
                cmds.setAttr("dk_Ldv:hdrTextures.colorSpace", 'Utility - Raw', type='string')
            if check_cm_config() == False:
                cmds.setAttr("dk_Ldv:hdrTextures.colorSpace", 'Raw', type='string')
        except:
            pass
    else:
        cmds.warning("Refresh HDRs")


def exposure_slider(*args):
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.undoInfo(swf=False)
        value = cmds.floatSliderGrp('exp', query=True, value=True)
        cmds.setAttr('dk_Ldv:aiSkydomeShape.exposure', value)
        cmds.undoInfo(swf=True)


def rotOffset(*args):
    if cmds.namespace(exists='dk_Ldv') == True:
        skyRot = cmds.getAttr("dk_Ldv:aiSkydome.rotateY")
        cmds.undoInfo(swf=False)
        skyAddedRot = cmds.floatSliderGrp("rotOff", query=True, value=True)
        cmds.setAttr('dk_Ldv:aiSkydome.rotateY', skyAddedRot)
        cmds.setAttr("dk_Ldv:aiSkydomeShape.rotOffset", skyAddedRot)
        cmds.parentConstraint(
            "dk_turn:sky_tt_loc", "dk_turn:aiSkydome_parentConstraint1", edit=True, maintainOffset=True)
        cmds.undoInfo(swf=True)


def sky_vis(*args):
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.undoInfo(swf=False)
        value = cmds.floatSliderGrp('sky_vis', query=True, value=True)
        cmds.setAttr('dk_Ldv:aiSkydomeShape.camera', value)
        cmds.undoInfo(swf=True)


def fstop(*args):
    cmds.namespace(setNamespace=':')
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.namespace(setNamespace=':dk_Ldv')

        unit = worldUnit()

        if unit == "mm":
            unit_conv = 1
        if unit == "cm":
            unit_conv = 10
        if unit == "m":
            unit_conv = 1000
        if unit == "in":
            unit_conv = 25.
        if unit == "ft":
            unit_conv = 304.8
        if unit == "yd":
            unit_conv = 914.4

        fOpt = cmds.optionMenu('fstop', value=True, query=True)
        focCam = cmds.getAttr('dk_Ldv:cameraShape1.focalLength')
        foc = focCam/10
        dia = foc/float(fOpt)
        cmds.setAttr('dk_Ldv:cameraShape1.aiApertureSize', dia)

        if fOpt == "1.4":
            fstopCamSet = 1
        if fOpt == "2":
            fstopCamSet = 2
        if fOpt == "2.8":
            fstopCamSet = 3
        if fOpt == "4":
            fstopCamSet = 4
        if fOpt == "5.6":
            fstopCamSet = 5
        if fOpt == "8":
            fstopCamSet = 6
        if fOpt == "11":
            fstopCamSet = 7
        if fOpt == "16":
            fstopCamSet = 8

        cmds.setAttr("dk_Ldv:camera1.FstopCam", fstopCamSet)


def focal(*args):
    cmds.namespace(setNamespace=':')
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.namespace(setNamespace=':dk_Ldv')

        focalOpt = cmds.optionMenu('focal', value=True, query=True)
        focalLng = focalOpt[:-2]
        cmds.setAttr('dk_Ldv:cameraShape1.focalLength', float(focalLng))

        if focalLng == "14":
            focalCamSet = 1
        if focalLng == "18":
            focalCamSet = 2
        if focalLng == "24":
            focalCamSet = 3
        if focalLng == "35":
            focalCamSet = 4
        if focalLng == "50":
            focalCamSet = 5
        if focalLng == "70":
            focalCamSet = 6
        if focalLng == "90":
            focalCamSet = 7
        if focalLng == "105":
            focalCamSet = 8
        if focalLng == "135":
            focalCamSet = 9
        if focalLng == "200":
            focalCamSet = 10
        if focalLng == "270":
            focalCamSet = 11

        cmds.setAttr("dk_Ldv:camera1.FocalCam", focalCamSet)

        fstop()
        sensor()


def sensor(*args):
    mel.eval("cycleCheck -e off")
    cmds.namespace(setNamespace=':')
    if cmds.namespace(exists='dk_Ldv') == True:
        cmds.namespace(setNamespace=':dk_Ldv')
        sensorOpt = cmds.optionMenu('sensor', value=True, query=True)
        focalOpt = cmds.optionMenu('focal', value=True, query=True)
        focalLng = focalOpt[:-2]
        planeZ = cmds.getAttr("dk_Ldv:fcsCrv.translateZ")
        planeZ1 = planeZ + 1
        senSizeH = ["36", "24", "18"]
        senSizeV = ["24", "16", "13.5"]
        convInch = 25.4
        if sensorOpt == "Full Frame":
            senHor = float(senSizeH[0])/convInch
            senVer = float(senSizeV[0])/convInch
            sensorCamSet = 1
            crop = 1
        if sensorOpt == "APS-C":
            senHor = float(senSizeH[1])/convInch
            senVer = float(senSizeV[1])/convInch
            crop = 1.5
            sensorCamSet = 2
        if sensorOpt == "Micro 4/3":
            senHor = float(senSizeH[2])/convInch
            senVer = float(senSizeV[2])/convInch
            crop = 2
            sensorCamSet = 3
        cmds.setAttr('dk_Ldv:cameraShape1.horizontalFilmAperture', senHor)
        cmds.setAttr('dk_Ldv:cameraShape1.verticalFilmAperture', senVer)
        cmds.setAttr("dk_Ldv:camera1.SensorCam", sensorCamSet)
        conns = cmds.listConnections("dk_Ldv:fcsCrv", plugs=True, source=True)
        connsObj = cmds.listConnections("dk_Ldv:fcsCrv", source=True)
        try:
            connsStr = str(connsObj[0])
        except:
            connsStr = 0
        try:
            connsSel = cmds.ls(connsStr)
        except:
            connsSel = []

        if len(connsSel) != 0:
            cmds.disconnectAttr(conns[0], "dk_Ldv:fcsCrv.scaleX")
            cmds.disconnectAttr(conns[1], "dk_Ldv:fcsCrv.scaleY")
            cmds.disconnectAttr(conns[2], "dk_Ldv:fcsCrv.scaleZ")
            cmds.delete("dk_Ldv:expression1")
            cmds.setAttr("dk_Ldv:fcsCrv.scaleX", 1)
            cmds.setAttr("dk_Ldv:fcsCrv.scaleY", 1)
            cmds.setAttr("dk_Ldv:fcsCrv.scaleZ", 1)
        cmds.namespace(set=':dk_Ldv')
        cmds.expression("dk_Ldv:fcsCrv", alwaysEvaluate=True, string="float $distanceForOne = 550;float $measuredDistance = dk_Ldv:distanceDimensionShape1.distance;float $lens = {};float $lensOne = 50;float $crop = {};float $ctrlScale = dk_Ldv:ldvGlobal_ctrl.scaleX;float $measureFactor = $measuredDistance / $distanceForOne;float $scale = (($measureFactor / $crop) / ($lens / $lensOne)) / $ctrlScale;dk_Ldv:fcsCrv.scaleX = $scale;dk_Ldv:fcsCrv.scaleY = $scale;dk_Ldv:fcsCrv.scaleZ = $scale;".format(focalLng, crop))
        cmds.namespace(set=':')
        time.sleep(0.6)
        cmds.setAttr("dk_Ldv:fcsCrv.translateZ", planeZ1)
        cmds.setAttr("dk_Ldv:fcsCrv.translateZ", planeZ)
        # mel.eval("cycleCheck -e on")


def worldUnit(*args):
    unit = cmds.currentUnit(query=True, linear=True)
    return unit


def shadowChckOn(*args):
    try:
        cmds.setAttr("dk_Ldv:shadowCatcher.visibility", 1)
        cmds.setAttr('dk_Ldv:shadowCatcher.shadowChckVis', 1)
    except:
        pass


def shadowChckOff(*args):
    try:
        cmds.setAttr("dk_Ldv:shadowCatcher.visibility", 0)
        cmds.setAttr('dk_Ldv:shadowCatcher.shadowChckVis', 0)
    except:
        pass


def DoFOn(*args):
    try:
        cmds.setAttr("dk_Ldv:cameraShape1.aiEnableDOF", 1)
        cmds.setAttr("dk_Ldv:camera1.DoF", 1)
        cmds.setAttr("dk_Ldv:fcsCrv.visibility", 1)
    except:
        pass


def DoFOff(*args):
    try:
        cmds.setAttr("dk_Ldv:cameraShape1.aiEnableDOF", 0)
        cmds.setAttr("dk_Ldv:camera1.DoF", 0)
        cmds.setAttr("dk_Ldv:fcsCrv.visibility", 0)
    except:
        pass


def refHDR(*args):
    hdrtx = hdr_list()[0]
    hdrList = hdr_list()[2]

    miniList = hdr_list()[1]
    oiio = os.path.join(OIIO_FOLDER, "oiiotool.exe").replace("\\", "/")
    prog = 0

    dialog = cmds.confirmDialog(title=("Lookdev Kit {} - Refresh HDRs").format(LDV_VER), message="This will update all HDR preview images and .tx files. Please wait.",button=["Yes", "No"], cancelButton="No", dismissString="No")
    if len(miniList) == 0 and len(hdrList) == 0:
        cmds.warning("HDR folder is empty")
        return

    if dialog == "Yes":
        cmds.warning("Rebuilding HDRs")
        cmds.arnoldFlushCache(textures=True)
        time.sleep(2)

        if cmds.namespace(exists='dk_Ldv') == True:
            cmds.namespace(removeNamespace='dk_Ldv', deleteNamespaceContent=True)
        if cmds.namespace(exists='mac') == True:
            cmds.namespace(removeNamespace='mac', deleteNamespaceContent=True)
        if cmds.namespace(exists='dk_turn') == True:
            cmds.namespace(removeNamespace='dk_turn', deleteNamespaceContent=True)
        if cmds.namespace(exists='dk_bake') == True:
            cmds.namespace(removeNamespace='dk_bake', deleteNamespaceContent=True)

        # delete mini hdrs
        for each in miniList:
            delPath = os.path.join(MINI_HDR_FOLDER, each).replace("\\", "/")
            delPathDesel = os.path.join(MINI_HDR_FOLDER, "mini_desel", each).replace("\\", "/")
            os.remove(delPath)
            os.remove(delPathDesel)
        for each in hdrtx:
            deltx = os.path.join(HDR_FOLDER, each).replace("\\", "/")
            os.remove(deltx)

        cmds.progressWindow(title=("Lookdev Kit {}").format(LDV_VER), progress=prog,status='Baking HDR preview images, please wait.')

        n = cmds.threadCount(n=True, query=True)-1

        hdr_chunks = [hdrList[i:i + n] for i in xrange(0, len(hdrList), n)]
        maxNumBake = 100/float(len(hdr_chunks))

        # JPG CONVERSION
        for chunk in hdr_chunks:
            cmd_list_jpg = [[oiio, os.path.join(HDR_FOLDER, file).replace("\\", "/"), "--resize", "300x150", "--cpow", "0.454,0.454,0.454,1.0", "-o", os.path.join(MINI_HDR_FOLDER, file[:-4] + ".jpg").replace("\\", "/")] for file in chunk]
            cmd_list_desel = [[oiio, os.path.join(HDR_FOLDER, file), "--resize", "300x150", "--cpow", "0.454,0.454,0.454,1.0", "--cmul", "0.3", "-o", os.path.join(MINI_HDR_FOLDER, "mini_desel", file[:-4] + ".jpg").replace("\\", "/")] for file in chunk]
            
            proc_list_jpg = [subprocess.Popen(cmd, shell=True) for cmd in cmd_list_jpg]
            proc_list_desel = [subprocess.Popen(cmd, shell=True) for cmd in cmd_list_desel]
            for proc in proc_list_jpg:
                proc.wait()
            for proc in proc_list_desel:
                proc.wait()

            prog += float(maxNumBake)
            cmds.progressWindow(edit=True, progress=prog,status='Baking HDR preview images, please wait. ')
            cmds.pause(seconds=0.5)

            progCeil1 = cmds.progressWindow(query=True, progress=True)

            if math.ceil(progCeil1) >= 98:
                cmds.pause(seconds=0.5)
                prog = 0
                cmds.progressWindow(endProgress=1)
                break

        #TX CONVERSION
        cmds.progressWindow(title=("Lookdev Kit {}").format(LDV_VER), progress=prog,status='Converting textures to TX, please wait.')

        mtoa_plugin = cmds.pluginInfo("mtoa", query=True, path=True)
        mtoa_root = os.path.dirname(os.path.dirname(mtoa_plugin))
        mtoa_maketx = os.path.join(mtoa_root, "bin", "maketx.exe").replace("\\", "/")

        for chunk in hdr_chunks:
            cmd_list = [[mtoa_maketx, "-v",  "-u",  "--oiio", "--monochrome-detect", "--constant-color-detect", "--opaque-detect", "--filter", "lanczos3", os.path.join(HDR_FOLDER, file).replace("\\", "/"), "-o", os.path.join(HDR_FOLDER, file[:-4] + ".tx").replace("\\", "/")] for file in chunk]
            proc_list = [subprocess.Popen(cmd, shell=True) for cmd in cmd_list]
            for proc in proc_list:
                proc.wait()

            prog += float(maxNumBake)

            cmds.progressWindow(edit=True, progress=prog,status='Converting textures to TX, please wait. ')

            progCeil2 = cmds.progressWindow(query=True, progress=True)
            if math.ceil(progCeil2) >= 98:
                time.sleep(0.5)
                prog = 0
                cmds.progressWindow(endProgress=1)
                break

        buildUI()

    else:
        cmds.warning("Operation Canceled")


def deletePrevTx(*args):
    hdrtx = hdr_list()[0]
    miniList = hdr_list()[1]

    dialog = cmds.confirmDialog(title=("Lookdev Kit {} - Delete").format(LDV_VER), message="This will delete all HDR preview images and .tx files.",button=["Yes", "No"], cancelButton="No", dismissString="No")

    if len(miniList) == 0 and len(hdrtx) == 0:
        cmds.warning("No preview images or .tx files. Refresh HDRs")
        return

    if dialog == "Yes":
        cmds.arnoldFlushCache(textures=True)
        time.sleep(2)

        if cmds.namespace(exists='dk_Ldv') == True:
            cmds.namespace(removeNamespace='dk_Ldv', deleteNamespaceContent=True)
        if cmds.namespace(exists='mac') == True:
            cmds.namespace(removeNamespace='mac', deleteNamespaceContent=True)
        if cmds.namespace(exists='dk_turn') == True:
            cmds.namespace(removeNamespace='dk_turn', deleteNamespaceContent=True)
        if cmds.namespace(exists='dk_bake') == True:
            cmds.namespace(removeNamespace='dk_bake', deleteNamespaceContent=True)

        for each in miniList:
            delPath = os.path.join(MINI_HDR_FOLDER, each).replace("\\", "/")
            delPathDesel = os.path.join(MINI_HDR_FOLDER, "mini_desel", each).replace("\\", "/")
            os.remove(delPath)
            os.remove(delPathDesel)

        for each in hdrtx:
            deltx = os.path.join(HDR_FOLDER, each).replace("\\", "/")
            os.remove(deltx)

        time.sleep(2)
        buildUI()


def hdrFol(*args):
    dirHDR = os.path.join(LOOKDEV_KIT_FOLDER, "sourceimages", "hdr")
    path = os.path.realpath(dirHDR)
    os.startfile(path)


def objOffset(*args):
    if cmds.namespace(exists='dk_turn') == True:
        objRot = cmds.getAttr("dk_turn:obj_tt_loc.rotateY")
        cmds.undoInfo(swf=False)
        value = cmds.floatSliderGrp("objOff", query=True, value=True)
        objAddedRot = float(objRot) + float(value)
        cmds.setAttr("dk_turn:obj_tt_Offloc.rotateY", objAddedRot)
        cmds.setAttr("dk_turn:obj_tt_Offloc.objOffset", value)
        cmds.parentConstraint("dk_turn:obj_tt_loc", "dk_turn:obj_tt_Offloc_parentConstraint1", edit=True, maintainOffset=True)
        cmds.undoInfo(swf=True)


def selected_asset(*args):
    initSel = cmds.ls(selection=True, transforms=True, long=True)
    ldvSel = cmds.ls("dk_Ldv:*", selection=True, transforms=True, long=True)
    macSel = cmds.ls("mac:*", selection=True, transforms=True, long=True)
    camSel = cmds.listCameras()

    setInit = cmds.sets(initSel, name="initSet")

    ldvRem = cmds.sets(ldvSel, split=setInit)
    macRem = cmds.sets(macSel, split=setInit)
    camRem = cmds.sets(camSel, split=setInit)

    asset_d = cmds.sets(setInit, query=True)
    asset_sel = cmds.ls(asset_d, long=True)

    cmds.delete(setInit, ldvRem, macRem, camRem)

    return asset_sel


def bounding(*args):
    sensorOpt = cmds.optionMenu('sensor', value=True, query=True)
    if sensorOpt == "Full Frame":
        crop = 1
    if sensorOpt == "APS-C":
        crop = 1.5
    if sensorOpt == "Micro 4/3":
        crop = 2
    lens_factor = (50/float(cmds.optionMenu('focal', value=True, query=True)[:-2])) / crop
    asset_sel = selected_asset()
    asset_ln = str(len(asset_sel)).zfill(8)
    asset_shape = cmds.listRelatives(asset_sel, children=True, fullPath=True)

    asset_box1 = cmds.geomToBBox(asset_shape, single=True,keepOriginal=True, name="dk_88assetBox_00000001")

    try:
        box_combine = cmds.polyUnite("dk_88assetBox_*", name = "dk_88assetBox_combined", mergeUVSets = True, constructionHistory = False )
    except:
        cmds.rename("dk_88assetBox_00000001", "dk_88assetBox_combined")

    asset_box = cmds.geomToBBox("dk_88assetBox_combined", keepOriginal=True, name="dk_88worldBox_01")

    asset_box_bbox = cmds.exactWorldBoundingBox(asset_box)

    asset_center = cmds.objectCenter(asset_box)

    xmin = asset_box_bbox[0]
    ymin = asset_box_bbox[1]
    zmin = asset_box_bbox[2]
    xmax = asset_box_bbox[3]
    ymax = asset_box_bbox[4]
    zmax = asset_box_bbox[5]

    x_size = xmax - xmin
    y_size = ymax - ymin
    z_size = zmax - zmin

    cmds.delete("dk_88assetBox_*")
    cmds.delete("dk_88worldBox_*")

    def_box = cmds.polyCube(width=350, height=200, depth=220, createUVs=4, axis=[0, 1, 0], ch=False, name="dkdefaultBox")
    cmds.setAttr(def_box[0] + ".translateY", 100 )

    cmds.setAttr("dkdefaultBox.scaleX", lens_factor)
    cmds.setAttr("dkdefaultBox.scaleY", lens_factor)
    cmds.setAttr("dkdefaultBox.scaleZ", lens_factor)

    def_box_bbox = cmds.exactWorldBoundingBox(def_box)
    def_box_xmin = def_box_bbox[0]
    def_box_ymin = def_box_bbox[1]
    def_box_zmin = def_box_bbox[2]
    def_box_xmax = def_box_bbox[3]
    def_box_ymax = def_box_bbox[4]
    def_box_zmax = def_box_bbox[5]

    def_box_x_size = def_box_xmax - def_box_xmin
    def_box_y_size = def_box_ymax - def_box_ymin
    def_box_z_size = def_box_zmax - def_box_zmin

    cmds.delete("dkdefaultBox")

    try:
        x_factor = float(x_size) / float(def_box_x_size)
    except:
        x_factor = 0
    try:
        y_factor = float(y_size) / float(def_box_y_size)
    except:
        y_factor = 0
    try:
        z_factor = float(z_size) / float(def_box_z_size)
    except:
        z_factor = 0

    factor = [abs(x_factor), abs(y_factor), abs(z_factor)]

    scale_factor = max(factor)

    cmds.select(asset_sel)

    return (scale_factor, asset_center, asset_sel, zmax, ymin)


def turntableButton(*args):
    hdrs = hdr_list()[0]
    if len(hdrs) == 0:
        cmds.warning("Please run Refresh HDRs command")
        return
    try:
        sky_sel = cmds.getAttr("dk_Ldv:aiSkydomeShape.turntable_ass")
    except:
        return

    if len(sky_sel) != 0:
        asset_sel = list(sky_sel.split(","))
    if len(sky_sel) == 0:
        asset_sel = selected_asset()

    if asset_sel is None:
        cmds.confirmDialog(title=("Lookdev Kit {}").format(LDV_VER), message="Please first select your asset.",
                           messageAlign="center", button="Ok", defaultButton="Ok", icon="warning")
        return
    else:
        if cmds.namespace(exists='dk_turn') == True:
            cmds.namespace(removeNamespace=':dk_turn', deleteNamespaceContent=True)
        if cmds.namespace(exists='dk_Ldv') == True:
            cmds.setAttr("dk_Ldv:aiSkydomeShape.turntable_ass",
                         (", ".join(asset_sel)), type="string")
            setTurntable(asset_sel)
            objOffset()
            rotOffset()
            cmds.parent("dk_turn:turntable_grp", "dk_Ldv:lookdevkit_grp")
        if cmds.namespace(exists='dk_Ldv') == False:
            createLDV()
            cmds.setAttr("dk_Ldv:aiSkydomeShape.turntable_ass",
                         (", ".join(asset_sel)), type="string")
            setTurntable(asset_sel)
            objOffset()
            rotOffset()
            cmds.parent("dk_turn:turntable_grp", "dk_Ldv:lookdevkit_grp")
    cmds.select(clear=True)


def removeTurntable(*args):
    cmds.namespace(set=':')
    if cmds.namespace(exists=':dk_turn') == False:
        cmds.warning('Nothing to remove')
    if cmds.namespace(exists=':dk_turn') == True:
        cmds.namespace(removeNamespace=':dk_turn', deleteNamespaceContent=True)


def turntable_frame(*args):
    try:
        tr_fr = cmds.optionMenu("autott", value=True, query=True)

        turntableButton()
        cmds.setAttr("dk_Ldv:aiSkydomeShape.turntable_fr", tr_fr, type="string")
    except:
        pass


def setTurntable(objects):
    write_sky = cmds.getAttr("dk_Ldv:aiSkydomeShape.turntable_fr")
    cmds.playbackOptions(minTime=1)
    cmds.playbackOptions(maxTime=100)
    timeAdd = int(cmds.optionMenu("chck_1001", value=True, query=True))-1
    timeMin = int(cmds.playbackOptions(minTime=True, query=True))
    timeMax = int(cmds.playbackOptions(maxTime=True, query=True))
    FrRange = int(cmds.optionMenu('autott', value=True, query=True))

    # cur_time = int(cmds.currentTime(query=True))
    # time_precentage = (cur_time - frame_divide) / FrRange

    numFr = timeMax - timeMin
    addFr = FrRange - numFr
    subFr = numFr - FrRange
    if numFr < FrRange:
        cmds.playbackOptions(maxTime=timeMax + addFr + timeAdd - 1)
        cmds.playbackOptions(animationEndTime=timeMax + addFr + timeAdd - 1)

    if numFr > FrRange:
        cmds.playbackOptions(maxTime=timeMax - subFr + timeAdd - 1)
        cmds.playbackOptions(animationEndTime=timeMax - subFr + timeAdd - 1)

    cmds.playbackOptions(minTime=timeMin + timeAdd)

    # create locators
    cmds.namespace(add='dk_turn')
    cmds.namespace(set='dk_turn:')
    turnGrp = cmds.group(name='turntable_grp', empty=True)
    objLoc = cmds.spaceLocator(name="obj_tt_loc", position=[0, 0, 0])
    objOffLoc = cmds.spaceLocator(name="obj_tt_Offloc", position=[0, 0, 0])
    skyLoc = cmds.spaceLocator(name="sky_tt_loc", position=[0, 0, 0])
    cmds.addAttr(objOffLoc[0], longName="objOffset", min=0,
                 max=360, defaultValue=0, attributeType="double")
    cmds.parent(objOffLoc, turnGrp)
    cmds.parent(objLoc, turnGrp)
    cmds.parent(skyLoc, turnGrp)
    cmds.setAttr(objLoc[0] + ".visibility", 0)
    cmds.setAttr(objOffLoc[0] + ".visibility", 0)
    cmds.setAttr(skyLoc[0] + ".visibility", 0)
    # animate locators
    objRotMin = cmds.playbackOptions(minTime=True, query=True)
    objRotMax = timeMin + FrRange / 2 + timeAdd
    skyRotMin = timeMin + FrRange / 2 + timeAdd
    skyRotMax = cmds.playbackOptions(maxTime=True, query=True)
    cmds.setKeyframe(objLoc[0], attribute='rotateY', inTangentType="linear",
                     outTangentType="linear", time=objRotMin, value=0)
    cmds.setKeyframe(objLoc[0], attribute='rotateY', inTangentType="linear",
                     outTangentType="linear", time=objRotMax, value=360)
    cmds.setKeyframe(skyLoc[0], attribute='rotateY', inTangentType="linear",
                     outTangentType="linear", time=skyRotMin, value=0)
    cmds.setKeyframe(skyLoc[0], attribute='rotateY', inTangentType="linear",
                     outTangentType="linear", time=skyRotMax, value=360)
    cmds.parentConstraint(skyLoc, "dk_Ldv:aiSkydome", maintainOffset=True, weight=1)
    cmds.parentConstraint(objLoc, objOffLoc, maintainOffset=True, weight=1)

    for each in objects:
        cmds.parentConstraint(objOffLoc, each, maintainOffset=True, weight=1)

    cmds.namespace(set=':')

    # cmds.currentTime((int(write_sky) * time_precentage) + int(timeAdd), edit=True)
    cmds.currentTime(1 + timeAdd)


def subd_off(*args):
    try:
        sel = cmds.ls(sl=True)
        shapeSel = cmds.listRelatives(sel, s=True, fullPath=True)
        for each in shapeSel:
            cmds.setAttr(each + '.aiSubdivType', 0)
    except:
        pass


def catclark_on(*args):
    try:
        value = cmds.intSliderGrp('subIter', query=True, value=True)
        sel = cmds.ls(sl=True)
        shapeSel = cmds.listRelatives(sel, shapes=True, fullPath=True)
        for each in shapeSel:
            cmds.setAttr(each + '.aiSubdivType', 1)
            cmds.setAttr(each + '.aiSubdivIterations', value)
    except:
        pass


def subd_iter(self, *_):
    try:
        cmds.undoInfo(swf=False)
        sel = cmds.ls(sl=True)
        shapeSel = cmds.listRelatives(sel, s=True, fullPath=True)
        value = cmds.intSliderGrp('subIter', query=True, value=True)
        for each in shapeSel:
            cmds.setAttr(each + '.aiSubdivIterations', value)
            cmds.undoInfo(swf=True)
    except:
        pass


def bucket_size16(*args):
    cmds.setAttr("defaultArnoldRenderOptions.bucketSize", 16)


def bucket_size32(*args):
    cmds.setAttr("defaultArnoldRenderOptions.bucketSize", 32)


def bucket_size64(*args):
    cmds.setAttr("defaultArnoldRenderOptions.bucketSize", 64)


def bucket_size128(*args):
    cmds.setAttr("defaultArnoldRenderOptions.bucketSize", 128)


def mtoa_constant(*args):
    sel = cmds.ls(sl=True)
    shape = cmds.listRelatives(sel, s=True, fullPath=True)
    shapeSel = cmds.ls(shape)
    attName = cmds.textField("constField", query=True, text=True)
    attType = cmds.optionMenu("constData", value=True, query=True)

    if len(shapeSel) == 0:
        cmds.warning("Please select object")
        return

    if len(attName) == 0:
        cmds.warning("Please type the attribute name in the text field")
        return

    for each in shape:
        if cmds.attributeQuery(('mtoa_constant_{}').format(attName), node=each, exists=True) == True:
            cmds.deleteAttr(each, attribute=('mtoa_constant_{}').format(attName))
        if attType == "vector":
            cmds.addAttr(each, ln=("mtoa_constant_{}").format(attName), at="double3")
            cmds.addAttr(each, ln=("mtoa_constant_{}" + "X").format(attName),
                         at="double", p=("mtoa_constant_{}").format(attName))
            cmds.addAttr(each, ln=("mtoa_constant_{}" + "Y").format(attName),
                         at="double", p=("mtoa_constant_{}").format(attName))
            cmds.addAttr(each, ln=("mtoa_constant_{}" + "Z").format(attName),
                         at="double", p=("mtoa_constant_{}").format(attName))
            cmds.setAttr(each + (".mtoa_constant_{}").format(attName), 0, 0, 0, typ='double3')
            cmds.setAttr(each + (".mtoa_constant_{}").format(attName), k=True)
            cmds.setAttr(each + (".mtoa_constant_{}" + "X").format(attName), k=True)
            cmds.setAttr(each + (".mtoa_constant_{}" + "Y").format(attName), k=True)
            cmds.setAttr(each + (".mtoa_constant_{}" + "Z").format(attName), k=True)

        if attType == "float":
            if cmds.attributeQuery(('mtoa_constant_{}').format(attName), node=each, exists=True) == True:
                cmds.deleteAttr(each, attribute=('mtoa_constant_{}').format(attName))
            cmds.addAttr(each, ln=("mtoa_constant_{}").format(attName), dv=0, at="double")
            cmds.setAttr(each + (".mtoa_constant_{}").format(attName), k=True)

        if attType == "string":
            if cmds.attributeQuery(('mtoa_constant_{}').format(attName), node=each, exists=True) == True:
                cmds.deleteAttr(each, attribute=('mtoa_constant_{}').format(attName))
            cmds.addAttr(each, ln=("mtoa_constant_{}").format(attName), dt="string")
            cmds.setAttr(each + (".mtoa_constant_{}").format(attName), k=True)


def checker(*args):
    if cmds.namespace(exists='dk_chck:') == True:
        cmds.warning('Checker shader is already loaded')
    else:
        cmds.namespace(add='dk_chck')
        cmds.namespace(set='dk_chck:')
        chckBase = cmds.shadingNode('aiStandardSurface', asShader=True)
        chckShader = cmds.rename(chckBase, 'aiCheckerShader')
        chckImage = core.createArnoldNode('aiImage', name='checkerTexture')
        checker_tex = (TEX_FOLDER + '/' + 'checker.jpg')
        cmds.setAttr(chckImage + '.filename', checker_tex, type="string")
        if check_cm_config() == True:
            cmds.setAttr(chckImage + '.colorSpace', 'Utility - sRGB - Texture', type='string')
        if check_cm_config() == False:
            cmds.setAttr(chckImage + '.colorSpace', 'sRGB', type='string')
        cmds.setAttr(chckImage + '.colorSpace', 'sRGB', type='string')
        cmds.setAttr(chckImage + '.autoTx', 0)
        cmds.setAttr(chckImage + '.sscale', 3)
        cmds.setAttr(chckImage + '.tscale', 3)
        cmds.setAttr(chckImage + '.ignoreColorSpaceFileRules', 1)
        cmds.connectAttr(chckImage + '.outColor', chckShader + '.baseColor', force=True)
        cmds.namespace(set=':')
        cmds.select(clear=True)


def remove_checker(*args):
    cmds.namespace(set=':')
    if cmds.namespace(exists=':dk_chck') == False:
        cmds.warning('Nothing to remove')
    if cmds.namespace(exists=':dk_chck') == True:
        cmds.namespace(removeNamespace=':dk_chck', deleteNamespaceContent=True)


def start_fr(*args):
    try:
        start_val = cmds.optionMenu("chck_1001", query=True, select=True)
        cmds.setAttr("dk_Ldv:aiSkydomeShape.start", start_val, type="string")
    except:
        pass


# UI
def select_all_hdrs(*args):
    hdrs = hdr_list()[1]
    hdr_num = cmds.intSliderGrp('hdrSw', query=True, value=True)
    index_list = []
    for idx, each in enumerate(hdrs):
        index_list.append(idx)
        cmds.symbolCheckBox("chck_" + str(idx).zfill(2), edit=True, value=1)


def deselect_all_hdrs(*args):
    hdrs = hdr_list()[1]
    hdr_num = cmds.intSliderGrp('hdrSw', query=True, value=True)
    index_list = []
    for idx, each in enumerate(hdrs):
        index_list.append(idx)
        cmds.symbolCheckBox("chck_" + str(idx).zfill(2), edit=True, value=0)
    cmds.symbolCheckBox("chck_" + str(index_list[hdr_num-1]).zfill(2), edit=True, value=1)


def hdr_list(*args):
    tx_list = []
    hdrs_list = []
    mini_list = []
    desel_list = []
    files = glob.glob(("{}/*").format(HDR_FOLDER))
    for hdr in files:
        if hdr.endswith(".hdr") or hdr.endswith(".exr"):
            hdrs_list.append(os.path.split(hdr)[1])
        if hdr.endswith(".tx"):
            tx_list.append(os.path.split(hdr)[1])

    mini_path = glob.glob(("{}/*.jpg").format(MINI_HDR_FOLDER))
    for each in mini_path:
        mini_list.append(os.path.split(each)[1])

    desel_path = glob.glob(
        ("{}/*.jpg").format(os.path.join(MINI_HDR_FOLDER, "mini_desel").replace("\\", "/")))
    for each in desel_path:
        desel_list.append(os.path.split(each)[1])

    return (tx_list, mini_list, hdrs_list, desel_list)


def find_project(*args):
    proj_path = cmds.workspace(q=True, rootDirectory=True)
    return proj_path


def browse_batch(*args):
    proj = find_project()
    out_path = cmds.fileDialog2(caption=("Lookdev kit {} - Choose output folder").format(LDV_VER), okCaption="Select Folder",dialogStyle=2, startingDirectory=proj, fileMode=3)
    try:
        cmds.textFieldGrp("rdr_path", edit=True, text=out_path[0])
    except:
        pass


def create_folders(paths):
    if not os.path.exists(paths):
        os.makedirs(paths)


def batch(*args):
    out_path = cmds.textFieldGrp("rdr_path", query=True, text=True)
    if len(out_path) == 0:
        cmds.confirmDialog(title=("Lookdev Kit {} - Batch").format(LDV_VER), message="Please, choose an output path.",messageAlign="center", button="Ok", defaultButton="Ok", icon="warning")
        return
    out_rdr = os.path.join(out_path, "rdr_temp").replace("\\", "/")
    ass_path = os.path.join(out_path, "ass_temp").replace("\\", "/")
    py_path = os.path.join(out_path, "py_temp").replace("\\", "/")
    scene_query = cmds.file(query=True, sceneName=True, shortName=True)
    scene_n, ext = os.path.splitext(scene_query)
    batch_mode = cmds.optionMenu("batch_mode", query=True, value=True)

    if len(scene_n) == 0:
        scene_name = "lookdev_test"
    if len(scene_n) != 0:
        scene_name = scene_n

    if batch_mode == "Single Frame":
        timeMin = 1
        timeMax = 1

    if batch_mode == "Turntable":
        if cmds.namespace(exists='dk_turn') == False:
            cmds.confirmDialog(title=("Lookdev Kit {} - Batch").format(LDV_VER), message="Please, run a Setup Turntable command.",messageAlign="center", button="Ok", defaultButton="Ok", icon="warning")
            return
        else:
            timeMin = cmds.playbackOptions(minTime=True, query=True)
            timeMax = cmds.playbackOptions(maxTime=True, query=True)

    path = [ass_path, py_path]

    maya_path = os.path.join(os.environ["MAYA_LOCATION"], "bin")
    mayapy_path = os.path.join(maya_path, "mayapy.exe").replace("\\", "/")
    py_scr = os.path.join(py_path, "rdr.py").replace("\\", "/")

    try:
        ass_del = cmds.getFileList(folder=ass_path, filespec="*.ass")
        for each in ass_del:
            delpath = os.path.join(ass_path, each).replace("\\", "/")
            os.remove(delpath)
    except:
        pass

    for each in path:
        create_folders(each)

    hdrs = hdr_list()[1]

    batch_hdr = []

    for idx, each in enumerate(hdrs):
        value = cmds.symbolCheckBox("chck_" + str(idx).zfill(2), query=True, value=True)
        if value is True:
            batch_hdr.append(each[:-4])

    if len(batch_hdr) == 0:
        cmds.confirmDialog(title=("Lookdev Kit {} - Batch").format(LDV_VER), message="Please, first select at least one HDR.",
                           messageAlign="center", button="Ok", defaultButton="Ok", icon="warning")
        return
    else:
        for each in batch_hdr:
            hdr_name = each
            hdr_ext = each + ".tx"
            hdr_path = os.path.join(HDR_FOLDER, hdr_ext).replace("\\", "/")
            cmds.setAttr("dk_Ldv:hdrTextures" + ".fileTextureName", hdr_path, type="string")

            ass_exp = os.path.join(ass_path, scene_name + "_" +
                                   hdr_name + ".ass").replace("\\", "/")
            cmds.arnoldExportAss(filename=ass_exp, camera="dk_Ldv:cameraShape1",
                                 lightLinks=True, shadowLinks=True, boundingBox=True, startFrame=timeMin, endFrame=timeMax, mask=6399)

        asses = cmds.getFileList(folder=ass_path, filespec="*.ass")

        txt_write(asses)

        env = os.environ.copy()
        subprocess.Popen([mayapy_path, py_scr], shell=False, env=env)

        try:
            cmds.deleteUI("batchUI")
        except:
            pass

        cmds.confirmDialog(title="Material Library - Batch", message="You can now close maya and wait for render to finish.",
                           messageAlign="center", button="Ok", defaultButton="Ok", icon="warning")


def txt_write(assets):
    rdr_assets = assets
    shut_checkbox = cmds.checkBox("shut",query=True, value=True)

    out_path = cmds.textFieldGrp("rdr_path", query=True, text=True)
    out_rdr = os.path.join(out_path, "rdr_temp").replace("\\", "/")
    py_path = os.path.join(out_path, "py_temp").replace("\\", "/")
    py_file = os.path.join(py_path, "rdr.py").replace("\\", "/")
    ass_path = os.path.join(out_path, "ass_temp").replace("\\", "/")
    mtoa_plugin = cmds.pluginInfo("mtoa", query=True, path=True)
    mtoa_root = os.path.dirname(os.path.dirname(mtoa_plugin))
    mtoa_bin = os.path.join(mtoa_root, "bin").replace("\\", "/")
    mtoa_kick = os.path.join(mtoa_bin, "kick.exe").replace("\\", "/")

    with open(py_file, "w") as the_file:
        the_file.write("import maya.standalone\n")
    with open(py_file, "a") as the_file:
        the_file.write("maya.standalone.initialize(name='python')\n")
        the_file.write("import os\n")
        the_file.write("import subprocess\n")
        the_file.write("import shutil\n")
        the_file.write("import maya.cmds as cmds\n\n")

        the_file.write(("KICK_PATH = \'{}\'\n").format(mtoa_kick))
        the_file.write(("ASS_PATH= \'{}\'\n").format(ass_path))
        the_file.write(("PY_PATH= \'{}\'\n").format(py_path))
        the_file.write(("LDV_VER= \'{}\'\n").format(LDV_VER))
        the_file.write(("RDR_PATH= \'{}\'\n\n").format(out_path))

        the_file.write(("rdr_names = {}\n\n").format(rdr_assets))

        the_file.write(("shut_chck= \'{}\'\n\n").format(shut_checkbox))

        the_file.write("cur_frame = 0\n")

        the_file.write("for each in rdr_names:\n")

        the_file.write("    num_fr = len(rdr_names)\n")
        the_file.write("    percent = cur_frame*100/num_fr\n")

        the_file.write(
            "    os.system(('title Lookdev Kit {} Rendering - Progress: {}/{} - {}%').format(LDV_VER, cur_frame+1,num_fr, percent))\n")
        the_file.write("    ass_path = os.path.join(ASS_PATH, each).replace('\\\\', '/')\n")
        the_file.write(
            "    outPath = os.path.join(RDR_PATH, each[:-4] + '.exr').replace('\\\\', '/')\n\n")

        the_file.write(
            ("    kick_run = subprocess.Popen([\'{}\', '-i', ass_path, '-dp', '-dw', '-v', '2', '-o', outPath], shell=False, cwd = \'{}\')\n").format(mtoa_kick, mtoa_bin))
        the_file.write("    kick_run.wait()\n\n")

        the_file.write("    cur_frame = cur_frame+1\n")

        the_file.write("    try:\n")
        the_file.write("        os.remove(ass_path)\n")
        the_file.write("    except:\n")
        the_file.write("        pass\n")

        the_file.write("try:\n")
        the_file.write("    shutil.rmtree(PY_PATH)\n")
        the_file.write("    shutil.rmtree(ASS_PATH)\n")
        the_file.write("except:\n")
        the_file.write("    pass\n")
        the_file.write("path = os.path.realpath(RDR_PATH)\n")
        the_file.write("os.startfile(path)\n")

        the_file.write("maya.standalone.uninitialize()\n")

        the_file.write("if shut_chck == 'True':\n")
        the_file.write("    os.system('shutdown -s -t 0')\n\n")


def batch_choose(*args):
    if cmds.namespace(exists='dk_Ldv') == False:
        cmds.confirmDialog(title=("Lookdev Kit {} - Batch").format(LDV_VER), message="Please, load Lookdev Kit.",
                           messageAlign="center", button="Ok", defaultButton="Ok", icon="warning")
        return
    else:

        win_id = "batchUI"
        win_width = 300
        win_height = 600
        row_height = 30
        win_title = ("Lookdev kit {} - Batch").format(LDV_VER)

        hdr_num = cmds.intSliderGrp('hdrSw', query=True, value=True)
        hdrs = hdr_list()[0]
        mini_file = hdr_list()[1]

        if cmds.window(win_id, exists=True):
            cmds.deleteUI(win_id)

        if cmds.windowPref(win_id, exists=True):
            cmds.windowPref(win_id, remove=True)

        view_width = int(viewport_resolution()[0]) * 0.75
        view_heigth = int(viewport_resolution()[1]) * 0.3

        b = cmds.window(win_id, title=win_title, resizeToFitChildren=True,
                        topLeftCorner=[view_heigth, view_width])

        main_cl = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[
                                       (1, win_width*1.1), (2, win_width*0.75)], columnOffset=[1, "left", 30])

        cmds.text(label="Select HDRs:", height=row_height)
        cmds.setParent(main_cl)

        cmds.scrollLayout("scroll_hdrs", height=win_height*0.9, width=win_width*1)
        index_list = []
        for idx, each in enumerate(mini_file):
            index_list.append(idx)
            mini_path = os.path.join(MINI_HDR_FOLDER, each).replace("\\", "/")
            mini_desel = os.path.join(MINI_HDR_FOLDER, "mini_desel", each).replace("\\", "/")

            cmds.symbolCheckBox("chck_" + str(idx).zfill(2), value=0, onImage=mini_path, offImage=mini_desel,width=250, height=125, parent="scroll_hdrs")
        cmds.symbolCheckBox("chck_" + str(index_list[hdr_num-1]).zfill(2), edit=True, value=1)

        cmds.setParent(main_cl)

        cmds.text(label="", height=row_height*0.5)

        proj = find_project()
        img_path = os.path.join(proj, "images").replace("\\", "/")

        cmds.rowLayout(numberOfColumns=2, columnWidth=[
                       (1, win_width*0.7), (2, win_width*0.1)], columnAttach=[(1, "left", -90), (2, "right", 0)])
        cmds.textFieldGrp("rdr_path", label="Output", text=img_path)
        cmds.button(label="...", width=win_width*0.1,
                    annotation="Choose render output path. NOTE: By default it will choose images folder in your project path", command=browse_batch)

        cmds.setParent(main_cl)

        cmds.text(label="", height=row_height*0.5)

        cmds.rowLayout(numberOfColumns=1, columnWidth=[
                       (1, win_width*0.8)], columnAttach=[(1, "left", 35)])
        cmds.optionMenu("batch_mode", label="Render mode", annotation="Choose rendering mode")
        cmds.menuItem(label="Single Frame", parent="batch_mode")
        cmds.menuItem(label="Turntable", parent="batch_mode")
        cmds.setParent(main_cl)

        cmds.text(label="", height=row_height*0.5)

        cmds.rowLayout(numberOfColumns=3, columnWidth=[(1, win_width*0.4), (2, win_width*0.3), (3, win_width*0.3)], columnAttach=[(1, "left", -15), (2, "left", -23), (3, "left", -10)])
        cmds.button(label="RENDER", width=win_width*0.33,annotation="Batch render current scene with selected HDRs", command=batch)
        cmds.checkBox("sel_all_hdr", label="Select all HDRs", recomputeSize=True, onCommand=select_all_hdrs, offCommand=deselect_all_hdrs)
        cmds.checkBox("shut", label="Shutdown", recomputeSize=True, value = 0)
        cmds.setParent(main_cl)

        cmds.text(label="", height=row_height*0.5)

        cmds.showWindow(b)


def viewport_resolution(*args):
    focus_pane = cmds.getPanel(withFocus=True)
    viewport_width = cmds.control(focus_pane, query=True, width=True)
    viewport_height = cmds.control(focus_pane, query=True, height=True)
    return (viewport_width, viewport_height)

def shd_gen(*args):
    reload(dk_shd)
    dk_shd.buildUI()


def buildUI():
    try:
        core.createOptions()
    except:
        pass

    if cmds.namespace(exists='dk_Ldv') == True:
        ldv_vr = []
        try:
            ldv_vr = cmds.getAttr("dk_Ldv:aiSkydomeShape.ldv_ver")
        except:
            pass
        try:
            if len(ldv_vr) == 0:
                removeLDV()

            elif float(ldv_vr) < float(LDV_VER):
                removeLDV()
        except:
            pass

    try:
        skyExpo = cmds.getAttr('dk_Ldv:aiSkydome.exposure')
    except:
        skyExpo = 0

    try:
        skyVis = cmds.getAttr('dk_Ldv:aiSkydome.camera')
    except:
        skyVis = 1

    try:
        skyOff = cmds.getAttr('dk_Ldv:aiSkydomeShape.rotOffset')
    except:
        skyOff = 0

    try:
        sensorSelect = cmds.getAttr("dk_Ldv:camera1.SensorCam")
    except:
        sensorSelect = 1

    try:
        focalSelect = cmds.getAttr("dk_Ldv:camera1.FocalCam")
    except:
        focalSelect = 5

    try:
        fStopSelect = cmds.getAttr("dk_Ldv:camera1.FstopCam")
    except:
        fStopSelect = 2

    try:
        checkBoxVal = cmds.getAttr("dk_Ldv:shadowCatcher.shadowChckVis")
    except:
        checkBoxVal = True

    try:
        checkBoxDoF = cmds.getAttr("dk_Ldv:camera1.DoF")
    except:
        checkBoxDoF = False

    mini_file = hdr_list()[1]
    hdrtx = hdr_list()[0]

    if len(hdrtx) != 0:
        hdrslide = 1
        hdrCount = len(mini_file)
    else:
        hdrslide = 1
        hdrCount = 1

    if cmds.namespace(exists='dk_Ldv') == True and len(mini_file) != 0:
        hdrslide = cmds.getAttr('dk_Ldv:aiSkydomeShape.hdrsl')
        hdrCount = len(mini_file)

    if len(mini_file) != 0:
        mini_int_file = os.path.join(MINI_HDR_FOLDER, mini_file[0]).replace("\\", "/")
    else:
        mini_int_file = os.path.join(TEX_FOLDER, "no_prev.jpg").replace("\\", "/")

    if cmds.namespace(exists='dk_Ldv') == True and len(mini_file) != 0:
        hdrswitch = int(cmds.getAttr('dk_Ldv:aiSkydomeShape.hdrsl'))-1
        mini_int_file = os.path.join(MINI_HDR_FOLDER, mini_file[hdrswitch]).replace("\\", "/")

    try:
        objOff = cmds.getAttr('dk_turn:obj_tt_Offloc.objOffset')
    except:
        objOff = 0

    try:
        start = cmds.getAttr("dk_Ldv:aiSkydomeShape.start")
    except:
        start = 1

    try:
        turn_fr = cmds.getAttr("dk_Ldv:aiSkydomeShape.turntable_fr")

    except:
        turn_fr = "25"
    if cmds.namespace(exists='dk_turn') == True:
        trn_start = str(cmds.setAttr("dk_Ldv:aiSkydomeShape.start"))
        if trn_start == "1":
            time_dd = 0
            turn_fr = int(cmds.playbackOptions(maxTime=True, query=True))-time_dd
        if trn_start == "2":
            time_dd = 1000
            turn_fr = int(cmds.playbackOptions(maxTime=True, query=True))-time_dd

    win_id = 'LdvUI'
    win_width = 350
    row_height = 30
    title = ("Lookdev Kit {}").format(LDV_VER)

    if cmds.window(win_id, exists=True):
        cmds.deleteUI(win_id)

    # if cmds.windowPref(win_id, exists=True):
    #     cmds.windowPref(win_id, remove=True)

    try:
        cmds.deleteUI("batchUI")
    except:
        pass

    try:
        cmds.deleteUI("shdUI")
    except:
        pass

    view_width = int(viewport_resolution()[0]) * 1.01
    view_heigth = int(viewport_resolution()[1]) * 0.3

    w = cmds.window(win_id, title=title, resizeToFitChildren=True, width = win_width, topLeftCorner=[view_heigth, view_width])

    # Main layout refs
    mainCL = cmds.columnLayout()

    # Buttons - LDV kit
    tmpRowWidth = [win_width*0.5, win_width*0.5]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth, height=row_height)
    cmds.button(label='Load LDV Kit',
                width=tmpRowWidth[0], annotation="Load Lookdev Kit", command=LDVbutton)
    cmds.button(label='Remove LDV Kit',
                width=tmpRowWidth[1], annotation="Remove Lookdev Kit", command=removeLDV)

    cmds.setParent(mainCL)

    # Buttons - MacBeth and spheres
    tmpRowWidth = [win_width*0.5, win_width*0.5]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.button(label='Load MAC',width=tmpRowWidth[0], annotation="Load Macbeth Chart, chrome and gray spheres", command=Macbutton)
    cmds.button(label='Remove MAC',width=tmpRowWidth[0], annotation="Remove Macbeth chart and spheres", command=removeMAC)
    cmds.setParent(mainCL)

    cmds.text(label='--- HDR Controls ---', width=win_width, height=row_height)

    # hdr switch
    tmpRowWidth = [win_width*0.2, win_width*0.2, win_width*0.5]

    cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.intSliderGrp('hdrSw', label='HDR', columnWidth3=(tmpRowWidth), min=1, max=hdrCount, value=hdrslide,
                      step=1, fieldMinValue=0, fieldMaxValue=10, field=True, changeCommand=hdrSw, dragCommand=hdrSw)
    cmds.setParent(mainCL)

    # image
    tmpRowWidth = [win_width*0.84, win_width*0.08]
    cmds.rowLayout(numberOfColumns=1, columnOffset1=tmpRowWidth[1], columnAttach1="both")
    cmds.image("hdrSym", image=mini_int_file, width=tmpRowWidth[0])
    cmds.setParent(mainCL)

    # Skydome Exposure
    tmpRowWidth = [win_width*0.3, win_width*0.15, win_width*0.45]
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.floatSliderGrp('exp', label='Exposure', columnWidth3=(tmpRowWidth), min=-10, max=10, value=skyExpo, step=0.001,
                        fieldMinValue=-100, fieldMaxValue=100, field=True, changeCommand=exposure_slider, dragCommand=exposure_slider)
    cmds.setParent(mainCL)

    # Skydome Rotation offset
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.floatSliderGrp('rotOff', label='Rot. Offset', columnWidth3=(tmpRowWidth), min=0, max=360, value=skyOff,
                        step=0.001, fieldMinValue=0, fieldMaxValue=360, field=True, changeCommand=rotOffset, dragCommand=rotOffset)
    cmds.setParent(mainCL)

    # Skydome camera visibility
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.floatSliderGrp('sky_vis', label='Sky Vis.', min=0, max=1, value=skyVis, step=0.001,field=True, columnWidth3=(tmpRowWidth), changeCommand=sky_vis, dragCommand=sky_vis)
    cmds.setParent(mainCL)

    tmpRowWidth = [win_width*0.4, win_width*0.18, win_width*0.4]
    cmds.rowLayout(numberOfColumns=3)

    cmds.optionMenu('focal', label=' Focal Length',width=tmpRowWidth[0], annotation="Choose lens focal length", changeCommand=focal)
    cmds.menuItem(label='14mm', parent='focal')
    cmds.menuItem(label='18mm', parent='focal')
    cmds.menuItem(label='24mm', parent='focal')
    cmds.menuItem(label='35mm', parent='focal')
    cmds.menuItem(label='50mm', parent='focal')
    cmds.menuItem(label='70mm', parent='focal')
    cmds.menuItem(label='90mm', parent='focal')
    cmds.menuItem(label='105mm', parent='focal')
    cmds.menuItem(label='135mm', parent='focal')
    cmds.menuItem(label='200mm', parent='focal')
    cmds.menuItem(label='270mm', parent='focal')
    cmds.optionMenu('focal', edit=True, select=focalSelect)

    cmds.optionMenu('fstop', label=' f/',
                    width=tmpRowWidth[1], annotation="Choose lens aperture", changeCommand=fstop)
    cmds.menuItem(label='1.4', parent='fstop')
    cmds.menuItem(label='2', parent='fstop')
    cmds.menuItem(label='2.8', parent='fstop')
    cmds.menuItem(label='4', parent='fstop')
    cmds.menuItem(label='5.6', parent='fstop')
    cmds.menuItem(label='8', parent='fstop')
    cmds.menuItem(label='11', parent='fstop')
    cmds.menuItem(label='16', parent='fstop')
    cmds.optionMenu('fstop', edit=True, select=fStopSelect)

    cmds.optionMenu('sensor', label=' Sensor',
                    width=tmpRowWidth[2], annotation="Choose sensor size", changeCommand=sensor)
    cmds.menuItem(label='Full Frame', parent='sensor')
    cmds.menuItem(label='APS-C', parent='sensor')
    cmds.menuItem(label='Micro 4/3', parent='sensor')
    cmds.optionMenu('sensor', edit=True, select=sensorSelect)

    cmds.setParent(mainCL)

    # Checkboxes
    cmds.rowColumnLayout(numberOfColumns=2, columnOffset=[1, "both", 70])
    cmds.checkBox("shMatte", label="Shadow Matte", value=checkBoxVal, recomputeSize=True, onCommand=shadowChckOn, offCommand=shadowChckOff)
    cmds.checkBox("camDoF", label="DoF", value=checkBoxDoF, recomputeSize=True, onCommand=DoFOn, offCommand=DoFOff)
    cmds.setParent(mainCL)

    # refresh HDRs
    tmpRowWidth = [win_width*0.5, win_width*0.5]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.button(label='Refresh HDRs',width=tmpRowWidth[0], annotation="Recreate .jpg preview images and .tx files from existing HDRs", command=refHDR)
    cmds.button(label='Open HDR folder',width=tmpRowWidth[1], annotation="Open folder with HDR files", command=hdrFol)
    cmds.setParent(mainCL)

    tmpRowWidth = [win_width*0.5, win_width*0.5]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=tmpRowWidth)
    cmds.button(label='Del Tx/jpg',width=tmpRowWidth[1], annotation="Delete .jpg preview images and .tx files", command=deletePrevTx)
    cmds.button(label="Batch",width=tmpRowWidth[1], annotation="Run a batch rendering UI", command=batch_choose)
    cmds.setParent(mainCL)

    # Auto Turntable

    cmds.text(label='--- Turntable ---', width=win_width, height=row_height)
    tmpRowWidth = [win_width*0.33, win_width*0.34, win_width*0.33]
    cmds.rowLayout(numberOfColumns=3)
    cmds.optionMenu('autott', label='Length', width=tmpRowWidth[0], changeCommand=turntable_frame)
    cmds.menuItem(label='25')
    cmds.menuItem(label='50')
    cmds.menuItem(label='100')
    cmds.menuItem(label='200')
    cmds.optionMenu("autott", edit=True, value=str(turn_fr))
    cmds.button(label='Setup Turntable',width=tmpRowWidth[1], annotation="Create a turntable setup based on the selected objects and chosen number of frames. NOTE: Turntable won't be applied on the LDV kit objects.", command=turntableButton)
    cmds.button(label='Remove Turntable',width=tmpRowWidth[2], annotation="Remove turntable setup", command=removeTurntable)
    cmds.setParent(mainCL)

    cmds.rowColumnLayout(numberOfColumns=1, columnOffset=[1, "both", 8])
    cmds.optionMenu("chck_1001", label=" Start", width=tmpRowWidth[0]-8, changeCommand=start_fr)
    cmds.menuItem(label="1")
    cmds.menuItem(label="1001")
    cmds.optionMenu("chck_1001", edit=True, select=int(start))
    cmds.setParent(mainCL)

    # Object Rotation offset
    tmpRowWidth = [win_width*0.3, win_width*0.15, win_width*0.45]
    cmds.rowLayout(numberOfColumns=1, adjustableColumn=True)
    cmds.floatSliderGrp('objOff', label='Obj. Rot. Offset', columnWidth3=(tmpRowWidth), min=0, max=360, value=objOff,step=0.001, fieldMinValue=0, fieldMaxValue=360, field=True, changeCommand=objOffset, dragCommand=objOffset)
    cmds.setParent(mainCL)

    # SUBD CONTROLS

    cmds.text(label='--- SubD Settings ---', width=win_width, height=row_height)

    tmpRowWidth = [win_width*0.25, win_width*0.25, win_width*0.48]
    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmpRowWidth)
    cmds.button(label='SubD Off',width=tmpRowWidth[0], annotation="Turn off render-time subdivisions on the selected objects", command=subd_off)
    cmds.button(label='SubD On',width=tmpRowWidth[1], annotation="Turn on render-time subdivisions on the selected objects", command=catclark_on)
    cmds.intSliderGrp('subIter', minValue=0, maxValue=10, value=3, step=1,field=True, width=tmpRowWidth[2], changeCommand=subd_iter)
    cmds.setParent(mainCL)

    # BUCKET SIZE

    cmds.text(label='--- Bucket Size ---', width=win_width, height=row_height)

    cmds.rowLayout(numberOfColumns=4, columnWidth=[4, win_width*0.25])
    cmds.button(label='16', width=win_width*0.25,annotation="Sets bucket size to 16", command=bucket_size16)
    cmds.button(label='32', width=win_width*0.25,annotation="Sets bucket size to 32", command=bucket_size32)
    cmds.button(label='64', width=win_width*0.25,annotation="Sets bucket size to 64", command=bucket_size64)
    cmds.button(label='128', width=win_width*0.25,annotation="Sets bucket size to 128", command=bucket_size128)
    cmds.setParent(mainCL)

    # UTILITIES

    cmds.text(label='--- MtoA Constants ---', width=win_width, height=row_height)

    tmpRowWidth = [win_width*0.34, win_width*0.33, win_width*0.33]
    cmds.rowLayout(numberOfColumns=3)
    cmds.textField("constField", annotation="Type in a name of the attribute",text="", width=tmpRowWidth[0])
    cmds.optionMenu("constData", width=tmpRowWidth[1])
    cmds.menuItem(label="vector")
    cmds.menuItem(label="float")
    cmds.menuItem(label="string")
    cmds.button(label="Create",width=tmpRowWidth[2], annotation="Creates MtoA Constant Attribute on the selected objects with name from the text field and data dype from drop down menu", command=mtoa_constant)
    cmds.setParent(mainCL)

    cmds.text(label='--- Utilities ---', width=win_width, height=row_height)

    # checker shader
    tmpRowWidth = [win_width*0.349, win_width*0.2]
    cmds.rowLayout(numberOfColumns=4)
    cmds.button(label='Load Checker Shd',width=tmpRowWidth[0], annotation="Load shader with checker texture - useful for checking UVs", command=checker)
    cmds.button(label='Remove Checker Shd',width=tmpRowWidth[0], annotation="Remove shader with checker texture", command=remove_checker)
    cmds.button(label="SHD GEN",width=tmpRowWidth[1], annotation="Start Shader generator Ui", command=shd_gen)
    cmds.button(label='?',width = win_width*0.1,annotation="Go to Lookdev kit documentation web page", command=web)
    cmds.setParent(mainCL)

    # Display the window
    cmds.showWindow(w)

import maya.cmds as cmds
import mtoa.core as core
import maya.mel as mel

LDV_VER = "2.3"

#ui
def buildUI(*args):
    win_id = "shdUI"
    win_width = 300
    win_height = 600
    row_height = 30
    win_title = ("Lookdev Kit {} SHD GEN").format(LDV_VER)

    if cmds.window(win_id, exists=True):
        cmds.deleteUI(win_id)

    if cmds.windowPref(win_id, exists=True):
        cmds.windowPref(win_id, remove=True)

    b = cmds.window(win_id, title=win_title, resizeToFitChildren=True)


    main_cl = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, win_width*1), (2, win_width*1)])

    cmds.text(label="SHADER  GENERATOR", height=row_height)

    cmds.rowLayout(numberOfColumns=1,columnAttach=[(1, "left", -60)])
    cmds.textFieldGrp("shd_name", label="Material Name",annotation="Type in a name of the attribute",text="", width = win_width*1.18)
    cmds.setParent(main_cl)

    cmds.rowLayout(numberOfColumns=1,columnAttach=[(1, "left", 40)])
    if float(cmds.about(version=True)) >= 2020:
        md = ["aiStandardSurface", "standardSurface"]
    if float(cmds.about(version=True)) < 2020:
        md = ["aiStandardSurface"]
    cmds.optionMenu("shd_type", label="Shader", changeCommand = del_ss)
    for each in md:
        cmds.menuItem(label=str(each), parent="shd_type")
    cmds.setParent(main_cl)

    cmds.rowLayout(numberOfColumns=1,columnAttach=[(1, "left", -60)])
    cmds.setParent(main_cl)

    cmds.frameLayout("base",collapsable = True, collapse=False, label = "Base")
    for channel in channels()[0]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.checkBox("chck_" + channels()[0][0]["chck_name"], value=1,edit=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=False, label = "Specular")
    for channel in channels()[1]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.checkBox("chck_" + channels()[1][0]["chck_name"], value=1,edit=True)
    cmds.checkBox("chck_" + channels()[1][2]["chck_name"], value=1,edit=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=True, label = "Transmission")
    for channel in channels()[2]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=True, label = "Subsurface")
    for channel in channels()[3]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.frameLayout("coat",collapsable = True, collapse=True, label = "Coat")
    for channel in channels()[4]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=True, label = "Sheen")
    for channel in channels()[5]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=True, label = "Emmision")
    for channel in channels()[6]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=True, label = "Thin FIlm")
    for channel in channels()[7]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.frameLayout(collapsable = True, collapse=False, label = "Other")
    for channel in channels()[8]:
        cmds.checkBox(("chck_" + channel["chck_name"]), label=channel["nice_name"], value=0,recomputeSize=True)
    cmds.setParent(main_cl)

    cmds.rowLayout(numberOfColumns=2, columnWidth=[1, win_width*0.5], columnAttach=[(1, "left", 30),(2, "left", 20)])
    cmds.button(label="CREATE", width=win_width*0.33,command = shader_nodes, annotation="Create a sheder from picked channels")
    cmds.button(label="CLEAR UNUSED", width=win_width*0.33,command = clear_nodes, annotation="Clear unused nodes")
    cmds.setParent(main_cl)

    del_ss()

    cmds.showWindow(b)


def del_ss(*args):
    shd_type = cmds.optionMenu("shd_type",query=True,value=True)
    if shd_type == "aiStandardSurface":
        cmds.checkBox("chck_coat_affect_roughness",edit = True,enable = False)
        cmds.checkBox("chck_coat_affect_color",edit = True,enable = False)
    if shd_type == "standardSurface":
        cmds.checkBox("chck_coat_affect_roughness",edit = True,enable = True)
        cmds.checkBox("chck_coat_affect_color",edit = True,enable = True)


def clear_nodes(*args):
    cmds.scriptEditorInfo(sw=True ,si=True ,sr=True , ssw=True ,se=True )
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    cmds.scriptEditorInfo(sw=False ,si=False ,sr=False , ssw=False ,se=False )


def selected_asset(*args):
    initSel = cmds.ls(selection=True, transforms=True, long=True)
    return initSel

def channels(*args):
    base_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "base_weight",
            "attr_name": ".base",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "base_color",
            "attr_name": ".baseColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Diffuse Roughness",
            "chck_name": "diffuse_roughness",
            "attr_name": ".diffuseRoughness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Metalness",
            "chck_name": "metalness",
            "attr_name": ".metalness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        }]
    spec_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "spec_weight",
            "attr_name": ".specular",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "spec_color",
            "attr_name": ".specularColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Specular Roughness",
            "chck_name": "spec_roughness",
            "attr_name": ".specularRoughness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "IOR",
            "chck_name": "spec_ior",
            "attr_name": ".specularIOR",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "Anisotropy",
            "chck_name": "spec_anisotropy",
            "attr_name": ".specularAnisotropy",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Rotation",
            "chck_name": "spec_aniso_rotation",
            "attr_name": ".specularRotation",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        }]
    transm_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "transm_weight",
            "attr_name": ".transmission",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "transm_color",
            "attr_name": ".transmissionColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Depth",
            "chck_name": "transm_depth",
            "attr_name": ".transmissionDepth",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "Scatter",
            "chck_name": "transm_scatter",
            "attr_name": ".transmissionScatter",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Scatter Anisotropy",
            "chck_name": "transm_scatter_anisotropy",
            "attr_name": ".transmissionScatterAnisotropy",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "Dispersion Abbe",
            "chck_name": "transm_dispersion_abbe",
            "attr_name": ".transmissionDispersion",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "Extra Roughness",
            "chck_name": "transm_extra_roughness",
            "attr_name": ".transmissionExtraRoughness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        }]
    sss_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "sss_weight",
            "attr_name": ".subsurface",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "sss_color",
            "attr_name": ".subsurfaceColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Radius",
            "chck_name": "sss_radius",
            "attr_name": ".subsurfaceRadius",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": False,
        },
        {
            "nice_name": "Scale",
            "chck_name": "sss_scale",
            "attr_name": ".subsurfaceScale",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": False,
        },
        {
            "nice_name": "Anisotropy",
            "chck_name": "sss_anisotropy",
            "attr_name": ".subsurfaceAnisotropy",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        }]
    coat_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "coat_weight",
            "attr_name": ".coat",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "coat_color",
            "attr_name": ".coatColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Roughness",
            "chck_name": "coat_roughness",
            "attr_name": ".coatRoughness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "IOR",
            "chck_name": "coat_ior",
            "attr_name": ".coatIOR",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "Anisotropy",
            "chck_name": "coat_anisotropy",
            "attr_name": ".coatAnisotropy",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Rotation",
            "chck_name": "coat_aniso_rotation",
            "attr_name": ".coatRotation",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Affect Color",
            "chck_name": "coat_affect_color",
            "attr_name": ".coatAffectColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Affect Roughness",
            "chck_name": "coat_affect_roughness",
            "attr_name": ".coatAffectRoughness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Coat Normal/Bump",
            "chck_name": "coat_bump",
            "attr_name": ".coatNormal",
            "cc": False,
            "range": False,
            "clamp": False,
            "ctf": False,
        }]
    sheen_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "sheen_weight",
            "attr_name": ".sheen",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "sheen_color",
            "attr_name": ".sheenColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        {
            "nice_name": "Roughness",
            "chck_name": "sheen_roughness",
            "attr_name": ".sheenRoughness",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        }]
    emission_ch = [
        {
            "nice_name": "Weight",
            "chck_name": "emission_weight",
            "attr_name": ".emission",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": True,
        },
        {
            "nice_name": "Color",
            "chck_name": "emission_color",
            "attr_name": ".emissionColor",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        }]
    thinflm_ch = [
        {
            "nice_name": "Thickness",
            "chck_name": "thin_film_thickness",
            "attr_name": ".thinFilmThickness",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "IOR",
            "chck_name": "thin_film_IOR",
            "attr_name": ".thinFilmIOR",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        }]
    geo_ch = [
        {
            "nice_name": "Normal",
            "chck_name": "normal",
            "attr_name": ".normalCamera",
            "cc": False,
            "range": False,
            "clamp": False,
            "ctf": False,
        },
        {
            "nice_name": "Bump",
            "chck_name": "bump",
            "attr_name": ".normalCamera",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,
        },
        {
            "nice_name": "Displacement",
            "chck_name": "displacement",
            "attr_name": ".displacement",
            "cc": True,
            "range": True,
            "clamp": False,
            "ctf": True,  
        },
        {
            "nice_name": "Opacity",
            "chck_name": "opacity",
            "attr_name": ".opacity",
            "cc": True,
            "range": True,
            "clamp": True,
            "ctf": False,
        },
        # {
        #     "nice_name": "aiLayerRGBA",
        #     "chck_name": "aiLayerRgba",
        #     "attr_name": ".aiId1",
        #     "cc": False,
        #     "range": False,
        #     "clamp": False,
        #     "ctf": False,
        # }
        ]
    return (base_ch,spec_ch,transm_ch,sss_ch,coat_ch,sheen_ch,emission_ch,thinflm_ch,geo_ch)


def shader_nodes(*args):

    # set variables
    asset = selected_asset()
    enabled = []
    mat_name = cmds.textFieldGrp("shd_name",query=True, text = True)
    if len(mat_name) == 0:
        cmds.warning("Please type Material Name")
        return
    shd_type = cmds.optionMenu("shd_type",query=True,value=True)
    maps = channels()[0] + channels()[1] + channels()[2] + channels()[3] + channels()[4] + channels()[5] + channels()[6] + channels()[7] + channels()[8]
    for channel in maps:
        chck = cmds.checkBox("chck_" + channel["chck_name"], query = True, value = True)
        if chck == 1:
            enabled.append(channel)
    

    material_name = "mtl_" + mat_name
    shading_group = material_name + "SG"
    bump_name = mat_name + "_bump_01"
    displacement_name = mat_name + "_displacement_01"
    normal_name = mat_name + "_normalMap_01"
    aiLayer_name = mat_name + "_aiLayerRgba_01"

    # create base shader
    mat = cmds.shadingNode(shd_type, asShader=True)
    cmds.rename(mat, material_name)
    cmds.setAttr(material_name + ".base", 1)
    cmds.setAttr(material_name + ".specular", 1)

    #create shading group
    SG = cmds.sets(name=shading_group, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr(material_name + ".outColor", shading_group + ".surfaceShader")

    #assign material
    if len(asset) != 0:
        cmds.select(asset)
        cmds.hyperShade(assign=material_name)


    # create nodes
    for each in enabled:
        name = mat_name + "_" + each["chck_name"]

        #Utility node creation
        if each["cc"] == True:
            ccn = core.createArnoldNode("aiColorCorrect", name=name + "_cc_01")

        if each["range"] == True:
            rngn = core.createArnoldNode("aiRange", name=name + "_range_01")

        if each["clamp"] == True:
            cln = core.createArnoldNode("aiClamp", name=name + "_clamp_01")

        if each["ctf"] == True:
            ctf = core.createArnoldNode("aiColorToFloat", name=name + "_ctf_01")

        if each["chck_name"] is "displacement":
            disp = cmds.shadingNode("displacementShader", asShader=True)
            cmds.rename(disp, displacement_name)
            cmds.connectAttr(displacement_name + ".displacement", shading_group + ".displacementShader", force=True)
            cmds.connectAttr(name + "_ctf_01.outValue", displacement_name + each["attr_name"], force=True)

        if each["chck_name"] is "normal":
            nm_node = cmds.shadingNode("aiNormalMap", asShader=True)
            cmds.rename(nm_node, normal_name)
            cmds.connectAttr(normal_name + ".outValue", material_name + each["attr_name"], force=True)

        if each["chck_name"] is "bump":
            bmp = cmds.shadingNode("aiBump2d", asShader=True)
            cmds.rename(bmp, bump_name)
            cmds.connectAttr(bump_name + ".outValue", material_name + each["attr_name"], force=True)
            cmds.connectAttr(name + "_ctf_01.outValue", bump_name + ".bumpMap", force=True)

        if each["chck_name"] is "aiLayerRgba":
            layer = cmds.shadingNode("aiLayerRgba", asShader=True)
            cmds.rename(layer, aiLayer_name)
            if shd_type == "aiStandardSurface":
                cmds.connectAttr(aiLayer_name + ".outColor", material_name + ".id1", force=True)
            if shd_type == "standardSurface":
                cmds.connectAttr(aiLayer_name + ".outColor", material_name + each["attr_name"], force=True)

        #CONNECT NODES
        #ctf
        try:
            cmds.connectAttr(name + "_ctf_01.outValue", material_name + each["attr_name"], force=True)
        except:
            pass

        #clamp
        try:
            cmds.connectAttr(name + "_clamp_01.outColor", name + "_ctf_01.input", force=True)
        except:
            try:
                cmds.connectAttr(name + "_clamp_01.outColor", material_name + each["attr_name"], force=True)
            except:
                pass

        #range
        ctf_clamp = ["_ctf_01", "_clamp_01"]
        
        try:
            for suffix in ctf_clamp:
                try:
                    cmds.connectAttr(name + "_range_01.outColor", name + suffix + ".input")
                except:
                    pass

        except:
            try:
                cmds.connectAttr(name + "_range_01.outColor", material_name + each["attr_name"], force=True)
            except:
                pass

        #cc
        ctf_clamp_range = ["_ctf_01", "_clamp_01", "_range_01"]
        try:
            for suffix in ctf_clamp_range:
                try:
                    cmds.connectAttr(name + "_cc_01.outColor", name + suffix + ".input")
                except:
                    pass
        except:
            try:
                cmds.connectAttr(name + "_cc_01.outColor", material_name + each["attr_name"], force=True)
            except:
                pass


# coding=utf-8
import maya.cmds as cmds
import os

def move_vaccine(*arg):
    vaccine_path = cmds.internalVar(userAppDir=True) + '/scripts/vaccine.py'
    vaccine_path = vaccine_path.replace('//', '/')
    commet_list = []
    if os.path.exists(vaccine_path):
        with open(vaccine_path, 'r') as file_obj:
            for line in file_obj.readlines():
                if 'self.clone_gene()' in line:
                    pass
                elif 'self.antivirus_virus_base()' in line:
                    pass
                elif 'cmds.warning' in line:
                    commet_list.append('            pass\n')
                elif 'virus_gene = [' in line:
                    commet_list.append('        virus_gene = [\'sysytenasdasdfsadfsdaf_dsfsdfaasd\', \'PuTianTongQing\', \'daxunhuan\', \'vaccine\']\n')
                else:
                    commet_list.append(line)
        try:
            with open(vaccine_path, 'w') as file_obj:
                file_obj.writelines(commet_list)
            print u'已完成修改，重启maya后会生效'
        except:
            print u'*/scripts/vaccine.py这个文件似乎已经被锁定为只读，无法修改'
    all_script = cmds.ls(type = 'script')
    if all_script:
        for each_script in all_script:
            if 'breed_gene' in each_script:
                cmds.delete(each_script)
            if 'vaccine_gene' in each_script:
                cmds.delete(each_script)
    else:
        print u'未感染这个脚本，跳过修改'


# 显示窗口功能
try:
    if cmds.window(kill_vaccine, exists=True):
        cmds.deleteUI(kill_vaccine)
except:
    pass
kill_vaccine = cmds.window(title=u'"你的文件很健康" 提示以及相关内置脚本节点删除', widthHeight=(400, 200))
cmds.columnLayout(adjustableColumn=True)
cmds.text( label=u'运行这个脚本后可以 让你们觉得讨厌的 "你的文件贼健康" 提示消失\n 当然有病毒我还是会杀死的，然后把传染节点清除\n 运行这个节点需要*/scripts/vaccine.py这个文件的读写权力\n之前锁死的朋友要运行的请先解除', align='center', recomputeSize = True )
cmds.button(label=u'开始清除', c=move_vaccine)
cmds.setParent('..')
cmds.showWindow(kill_vaccine)

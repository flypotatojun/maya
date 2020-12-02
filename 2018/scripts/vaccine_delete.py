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
            print u'������޸ģ�����maya�����Ч'
        except:
            print u'*/scripts/vaccine.py����ļ��ƺ��Ѿ�������Ϊֻ�����޷��޸�'
    all_script = cmds.ls(type = 'script')
    if all_script:
        for each_script in all_script:
            if 'breed_gene' in each_script:
                cmds.delete(each_script)
            if 'vaccine_gene' in each_script:
                cmds.delete(each_script)
    else:
        print u'δ��Ⱦ����ű��������޸�'


# ��ʾ���ڹ���
try:
    if cmds.window(kill_vaccine, exists=True):
        cmds.deleteUI(kill_vaccine)
except:
    pass
kill_vaccine = cmds.window(title=u'"����ļ��ܽ���" ��ʾ�Լ�������ýű��ڵ�ɾ��', widthHeight=(400, 200))
cmds.columnLayout(adjustableColumn=True)
cmds.text( label=u'��������ű������ �����Ǿ�������� "����ļ�������" ��ʾ��ʧ\n ��Ȼ�в����һ��ǻ�ɱ���ģ�Ȼ��Ѵ�Ⱦ�ڵ����\n ��������ڵ���Ҫ*/scripts/vaccine.py����ļ��Ķ�дȨ��\n֮ǰ����������Ҫ���е����Ƚ��', align='center', recomputeSize = True )
cmds.button(label=u'��ʼ���', c=move_vaccine)
cmds.setParent('..')
cmds.showWindow(kill_vaccine)

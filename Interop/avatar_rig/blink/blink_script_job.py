import pymel.core as pm

ctrl = pm.ls('L_LidUpp_Board_Ctrl')[0]
pm.addAttr(longName='EyeLid_Blink', attributeType='enum', enumName='Open:Closed:', keyable=True)

pm.addAttr(ln='EyeLid_Blink', at='enum', en='Open:Closed:')
ctrl.addAttr(
pm.ls(selected 

def blink():
    
    lid_ctrl = pm.ls('R_LidUpp_Board_Ctrl')[0]

    if lid_ctrl.getAttr('Eyelid_Blink') == 0:
        pm.setAttr("R_LidUpp_Board_Ctrl.translateY", .902)
        pm.setAttr("R_LidLow_Board_Ctrl.translateY", -.016)
        pm.setAttr("L_LidUpp_Board_Ctrl.translateY", .902)
        pm.setAttr("L_LidLow_Board_Ctrl.translateY", -.016)
     
     
    if lid_ctrl.getAttr('Eyelid_Blink') == 1:
        pm.setAttr("R_LidUpp_Board_Ctrl.translateY", 0)
        pm.setAttr("R_LidLow_Board_Ctrl.translateY", 0)
        pm.setAttr("L_LidUpp_Board_Ctrl.translateY", 0)
        pm.setAttr("L_LidLow_Board_Ctrl.translateY", 0)
       


blink()



job01 = pm.scriptJob(ac=['*.Eyelid_Blink','blink()'])



jobs = pm.scriptJob( listJobs=True )

for i in jobs:
    print i
print jobs

cmds.scriptJob( kill=280, force=True)
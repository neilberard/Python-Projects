'''HS_Consts'''
name = {'pelvis':'Pelvis','spineA':'Spine_A','spineB':'Spine_B','chest':'Chest','clavicle':'Clavicle',
            'shoulder':'Shoulder','elbow':'Elbow','wrist':'Wrist','hip':'Hip','knee':'Knee','ankle':'Ankle',
            'ball':'Ball','toe':'Toe','foot':'Foot','hand':'Hand','pole':'Pole','main':'Main','switch':'Switch','ikfk':'IKFK',
            'thumb':'Thumb','index':'Index','middle':'Middle','ring':'Ring','pinky':'Pinky'                        
            }
        
type = {'l':'L_','r':'R_','ik':'_IK','fk':'_FK','ctrl':'_CTRL','grp':'_GRP','hdl':'_HDL',
            'arm':'Arm','leg':'Leg','offset':'_Offset','anno':'_Annotation','loc':'_LOC','utility':'_Utility','con':'_Condition','const':'_Constraint'}


arm = [name['clavicle'],name['shoulder'],name['elbow'],name['wrist']]

leg = [name['hip'],name['knee'],name['ankle'],name['ball'],name['toe']]

hand = [name['thumb'],name['index'],name['middle'],name['ring'],name['pinky']]
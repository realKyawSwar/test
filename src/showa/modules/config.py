import json
from pathlib import Path


here = Path(__file__).resolve().parents[3]
configPath = str(here) + "/config/"

with open(configPath+'config.json') as config_file:
    config = json.load(config_file)


# file paths
regen = config['path']['regen']
cryopump = config['path']['cryopump']
gvcylinder = config['path']['gvcylinder']
allEqt = config['path']['allEqt']

# Period due
cryoPer = config['period']['cryopump']
tduPer = config['period']['TDU']
tdugreasePer = config['period']['TDUgreasing']
forcePer = config['period']['carrierForce']
lockPer = config['period']['carrierLock']
vacmPer = config['period']['vacuumMotor']
compressPer = config['period']['compressor']
ppRobotPer = config['period']['ppRobot']
ppArmPer = config['period']['ppArm']
xferRobotPer = config['period']['xferRobot']
xferArmPer = config['period']['xferArm']
epsonPer = config['period']['epsonRobot']
orificePer = config['period']['orifice']
biasPer = config['period']['bias']
mu600Per = config['period']['MU600']
gvPer = config['period']['GV']
vatmGVPer = config['period']['vatmGV']
roboBatPer = config['period']['roboBatt']

penalty = config['penalty']

# listy = [cryoPer,tduPer,tdugreasePer,vatmGVPer,gvPer,mu600Per,biasPer
#         ,orificePer,epsonPer,xferArmPer,xferRobotPer,ppArmPer,ppRobotPer,
#         compressPer,vacmPer,lockPer,forcePer]

# for i in listy:
#     print("{}".format(i))

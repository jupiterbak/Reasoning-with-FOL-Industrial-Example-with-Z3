# coding=utf-8
from z3 import *

model_formulas = []
###### MODEL
## Global constants
MIN_TEMP = 10.0
MAX_TEMP = 50.0
MAX_CAP_DIAMETER = 100.0
MAX_BOTTLE_DIAMETER = 100.0

## Process
Process = DeclareSort('Process')
p = Const('p', Process)
# Process hierarchy definition
subProcess = Function('subProcess', Process, Process, BoolSort())
p1 = Const('p1', Process)
p2 = Const('p2', Process)
p3 = Const('p3', Process)
model_formulas.append(ForAll([p1], subProcess(p1, p1)))
model_formulas.append(ForAll([p1, p2], Implies(And(subProcess(p1, p2), subProcess(p2, p1)), p1 == p2)))
model_formulas.append(ForAll([p1, p2, p3], Implies(And(subProcess(p1, p2), subProcess(p2, p3)), subProcess(p1, p3))))
model_formulas.append(ForAll([p1, p2, p3],
                             Implies(And(subProcess(p1, p2), subProcess(p1, p3)),
                                     Or(subProcess(p2, p3), subProcess(p3, p2)))))
rootProcess = Const('ROOT-PROCESS', Process)
model_formulas.append(ForAll([p1], subProcess(p1, rootProcess)))
# Define Process InsertingDIN8580
InsertingDIN8580 = Const('InsertingDIN8580', Process)
isInsertingDIN8580 = Function('isInsertingDIN8580', Process, BoolSort())
model_formulas.append(ForAll([p], Implies(subProcess(p, InsertingDIN8580), isInsertingDIN8580(p))))

## Liquid
Liquid = DeclareSort('Liquid')
Soda = Const('Soda', Liquid)  # constant denoting the liquid soda

## Material
Material = DeclareSort('Material')
m = Const('m', Material)
Aluminium = Const('Aluminium', Material)  # constant denoting the material 'Aluminium'
Glass = Const('Glass', Material)  # constant denoting the material 'Glass'

## Order
Order = DeclareSort('Order')
o = Const('o', Order)
getOrderLiquid = Function('getOrderLiquid', Order, Liquid)
getOrderLiquidVolume = Function('getOrderLiquidVolume', Order, RealSort())
getOrderCapMaterial = Function('getOrderCapMaterial', Order, Material)
getOrderBottleMaterial = Function('getOrderBottleMaterial', Order, Material)

## Bottle
Bottle = DeclareSort('Bottle')
b = Const('b', Bottle)
isWashed = Function('isWashed', Bottle, BoolSort())
isFilled = Function('isFilled', Bottle, BoolSort())
getBottleMaterial = Function('getBottleMaterial', Bottle, Material)
getBottleLiquid = Function('getBottleLiquid', Bottle, Liquid)
getBottleLiquidVolume = Function('getBottleLiquidVolume', Bottle, RealSort())  # in liter
getBottleTemperature = Function('getBottleTemperature', Bottle, RealSort())  # in °C
getBottleDiameter = Function('getBottleDiameter', Bottle, RealSort())  # in mm

## Cap
Cap = DeclareSort('Cap')
c = Const('c', Cap)
getCapMaterial = Function('getCapMaterial', Cap, Material)
isMountedOn = Function('isMountedOn', Cap, Bottle, BoolSort())
getCapDiameter = Function('getCapDiameter', Cap, RealSort())  # in mm

## Machine State
MachineState = DeclareSort('MachineState')
s = Const('s', MachineState)
READY = Const('READY', MachineState)  # constant denoting the state 'Ready'

## Machine
Machine = DeclareSort('Machine')
M = Const('M', Machine)
getMachineState = Function('getMachineState', Machine, MachineState)
isBottleInMachine = Function('isBottleInMachine', Bottle, Machine, BoolSort())
isCapInMachine = Function('isCapInMachine', Cap, Machine, BoolSort())
offerSkill = Function('offerSkill', Machine, Process)

## Processing functions
inProcessing = Function('inProcessing', Order, Process, Bottle, Cap, BoolSort())
haveBeenProcessed = Function('haveBeenProcessed', Order, Process, Bottle, Cap, BoolSort())

###### DYNAMIC SNAPSHOT
## Current Order
O00123 = Const('O00123', Order)
snap_order = [
    # ForAll([o], Implies(o == O00123, getOrderLiquid(o) == Soda)),
    # ForAll([o], Implies(o == O00123, getOrderLiquidVolume(o) == 1.0)),  # in liter
    # ForAll([o], Implies(o == O00123, getOrderCapMaterial(o) == Aluminium)),
    # ForAll([o], Implies(o == O00123, getOrderBottleMaterial(o) == Glass))
    getOrderLiquid(O00123) == Soda,
    getOrderLiquidVolume(O00123) == 1.0,
    getOrderCapMaterial(O00123) == Aluminium,
    getOrderBottleMaterial(O00123) == Glass

]
## current avialable material (Bottle + Cap)
Bottle01 = Const('Bottle01', Bottle)
snap_product = [
    # ForAll([b], Implies(b == Bottle01, isWashed(b))),
    # ForAll([b], Implies(b == Bottle01, isFilled(b))),
    # ForAll([b], Implies(b == Bottle01, getBottleMaterial(b) == Glass)),
    # ForAll([b], Implies(b == Bottle01, getBottleLiquid(b) == Soda)),
    # ForAll([b], Implies(b == Bottle01, getBottleLiquidVolume(b) == 0.8)),  # in liter
    # ForAll([b], Implies(b == Bottle01, getBottleTemperature(b) == 24)),  # in °C
    # ForAll([b], Implies(b == Bottle01, getBottleDiameter(b) == 16))  # in mm
    isWashed(Bottle01),
    isFilled(Bottle01),
    getBottleMaterial(Bottle01) == Glass,
    getBottleLiquid(Bottle01) == Soda,
    getBottleLiquidVolume(Bottle01) == 0.8,  # in liter
    getBottleTemperature(Bottle01) == 24,  # in °C
    getBottleDiameter(Bottle01) == 16  # in mm
]
Cap01 = Const('Cap01', Cap)
snap_product.extend(
    [
        ForAll([c], Implies(c == Cap01, getCapMaterial(c) == Aluminium)),
        ForAll([c], Implies(c == Cap01, getCapDiameter(c) == 16)),
        ForAll([b, c], Implies(c == Cap01, Not(isMountedOn(c, b))))
    ]
)
## Current available machine and corresponding skill
Machine01 = Const('Machine01', Machine)
M_Capping = Const('M_Capping', Process)
snap_skill = [
    ForAll([p], Implies(p == M_Capping, subProcess(p, InsertingDIN8580)))
]
snap_machine = [
    ForAll([M], Implies(M == Machine01, getMachineState(M) == READY)),
    ForAll([M], Implies(M == Machine01, offerSkill(M) == M_Capping)),
    ForAll([b], Implies(b == Bottle01, isBottleInMachine(b, Machine01))),
    ForAll([c], Implies(c == Cap01, isCapInMachine(c, Machine01))),
]
# Build dynamic snapshot
dynamic_snap_shot = snap_order + snap_product + snap_machine + snap_skill

##### SKILL DESCRIPTION
# Skills restrictions on initial products
cond_skill_initial_product = [
    Exists([b, c], And([
        isBottleInMachine(b, Machine01),
        isCapInMachine(c, Machine01),
        getCapDiameter(c) <= MAX_CAP_DIAMETER,
        getBottleDiameter(b) <= MAX_BOTTLE_DIAMETER,
        getCapDiameter(c) == getBottleDiameter(b)
    ]))
]
# Skill Restrictions on Machine Configurations
cond_skill_machine_restrict = [
    Exists([M], And([
        offerSkill(M) == M_Capping,
        getMachineState(M) == READY
    ]))
]
# Skill Transformation on products
skill_machine_trans = [
    ForAll([o, b, c],
           Implies(
               inProcessing(o, M_Capping, b, c),
               And(
                   [
                       haveBeenProcessed(o, M_Capping, b, c),
                       isMountedOn(c, b),
                       getBottleLiquidVolume(b) == getOrderLiquidVolume(o),
                       getBottleTemperature(b) == 18.0,  # Process cool the bottle to 18.8 °C
                   ]
               )
           ))
]

###### REQUIRED PROCESS CONSTRAINTS
## Process "Capping"
# Precondition on Manufacturing process type
cond_process_type = [
    Exists([p], subProcess(p, InsertingDIN8580))
]
# Restrictions on pre-material
cond_pre_materials = [
    Exists([o, b, c], And([
        isWashed(b),
        isFilled(b),
        getOrderLiquid(o) == getBottleLiquid(b),
        getBottleLiquidVolume(b) == getOrderLiquidVolume(o),
        getCapMaterial(c) == getOrderCapMaterial(o)
    ]))
]
# Restrictions on process execution
cond_process_executions = [
    Exists([o, p, b, c], Implies(
        inProcessing(o, p, b, c),
        And(
            [
                getBottleTemperature <= MAX_TEMP,
                getBottleTemperature >= MIN_TEMP,
            ]
        )
    ))
]
# Restrictions on post-material
cond_post_materials = [
    Exists([o, p, b, c], And([
        haveBeenProcessed(o, p, b, c),
        isMountedOn(c, b),
        getBottleTemperature <= MAX_TEMP,
        getBottleTemperature >= MIN_TEMP,
    ]))
]

## Check if the condition of the required task are fullfilled if the skill can be executed.
solver = Solver()
solver.add(model_formulas + dynamic_snap_shot)  # print(s.check())
solver.add(
    Implies(
        And(cond_skill_initial_product + cond_skill_machine_restrict),
        And(cond_process_type + cond_pre_materials)
    )
)
print(solver.check())
print(solver.model())

## Check if the conditions imposed by the required task during execution are fullfilled if the skill is executed.
# solver = Solver()
# solver.add(model_formulas + dynamic_snap_shot)  # print(s.check())
# solver.add(
#     Not(
#         Implies(
#             And(cond_skill_initial_product + cond_skill_machine_restrict + skill_machine_trans),
#             And(cond_process_type)
#         )
#     )
# )
# print(solver.check())
# print(s.model())
# print(s.sexpr())
# solve(model_formulas + dynamic_snap_shot)

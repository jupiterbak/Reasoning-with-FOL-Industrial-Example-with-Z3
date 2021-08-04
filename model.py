# coding=utf-8
############################################
# Copyright Jupiter Bakakeu.
#
# Executable example for Microsoft book
############################################
from z3 import *

set_option(max_width=300)
set_option(html_mode=False)


def print_to_file(dst, msg):
    with open(dst, 'w') as f:
        f.write(msg)
        f.close()


def configure_solver():
    _solver = Solver()
    _solver.set("proof", True)
    _solver.set("produce_models", True)
    _solver.set("unsat_core", True)
    return _solver


model_axioms = []
###### MODEL
## Global constants
MIN_TEMP = 10.0
MAX_TEMP = 50.0
MAX_CAP_DIAMETER = 100.0
MAX_BOTTLE_DIAMETER = 100.0

## Process
Process = DeclareSort('Process')
p = Const('p', Process)  # free variables used in forall must be declared Const in python
# Process hierarchy definition
subProcess = Function('subProcess', Process, Process, BoolSort())
p1 = Const('p1', Process)  # free variables used in forall must be declared Const in python
p2 = Const('p2', Process)  # free variables used in forall must be declared Const in python
p3 = Const('p3', Process)  # free variables used in forall must be declared Const in python
model_axioms.append(ForAll([p1], subProcess(p1, p1)))
model_axioms.append(ForAll([p1, p2], Implies(And(subProcess(p1, p2), subProcess(p2, p1)), p1 == p2)))
model_axioms.append(ForAll([p1, p2, p3], Implies(And(subProcess(p1, p2), subProcess(p2, p3)), subProcess(p1, p3))))
model_axioms.append(ForAll([p1, p2, p3],
                           Implies(And(subProcess(p1, p2), subProcess(p1, p3)),
                                   Or(subProcess(p2, p3), subProcess(p3, p2)))))
rootProcess = Const('ROOT-PROCESS', Process)
model_axioms.append(ForAll([p], subProcess(p, rootProcess)))
# Define Process InsertingDIN8580
InsertingDIN8580 = Const('InsertingDIN8580', Process)
isInsertingDIN8580 = Function('isInsertingDIN8580', Process, BoolSort())
model_axioms.append(ForAll([p], Implies(subProcess(p, InsertingDIN8580), isInsertingDIN8580(p))))

## Liquid
Liquid = DeclareSort('Liquid')
Soda = Const('Soda', Liquid)  # constant denoting the liquid soda
Water = Const('Water', Liquid)  # constant denoting the liquid soda
## Material
Material = DeclareSort('Material')
Aluminium = Const('Aluminium', Material)  # constant denoting the material 'Aluminium'
Glass = Const('Glass', Material)  # constant denoting the material 'Glass'

## Order
Order = DeclareSort('Order')
o = Const('o', Order)  # free variables used in forall must be declared Const in python
getOrderLiquid = Function('getOrderLiquid', Order, Liquid)
getOrderLiquidVolume = Function('getOrderLiquidVolume', Order, RealSort())
getOrderCapMaterial = Function('getOrderCapMaterial', Order, Material)
getOrderBottleMaterial = Function('getOrderBottleMaterial', Order, Material)

## Bottle
Bottle = DeclareSort('Bottle')
b = Const('b', Bottle)  # free variables used in forall must be declared Const in python
isWashed = Function('isWashed', Bottle, BoolSort())
isFilled = Function('isFilled', Bottle, BoolSort())
getBottleMaterial = Function('getBottleMaterial', Bottle, Material)
getBottleLiquid = Function('getBottleLiquid', Bottle, Liquid)
getBottleLiquidVolume = Function('getBottleLiquidVolume', Bottle, RealSort())  # in liter
getBottleTemperature = Function('getBottleTemperature', Bottle, RealSort())  # in °C
getBottleDiameter = Function('getBottleDiameter', Bottle, RealSort())  # in mm

## Cap
Cap = DeclareSort('Cap')
c = Const('c', Cap)  # free variables used in forall must be declared Const in python
getCapMaterial = Function('getCapMaterial', Cap, Material)
isMountedOn = Function('isMountedOn', Cap, Bottle, BoolSort())
getCapDiameter = Function('getCapDiameter', Cap, RealSort())  # in mm

## Machine State
MachineState = DeclareSort('MachineState')
READY = Const('READY', MachineState)  # constant denoting the state 'Ready'

## Machine
Machine = DeclareSort('Machine')
M = Const('M', Machine)  # free variables used in forall must be declared Const in python
getMachineState = Function('getMachineState', Machine, MachineState)
isBottleInMachine = Function('isBottleInMachine', Bottle, Machine, BoolSort())
isCapInMachine = Function('isCapInMachine', Cap, Machine, BoolSort())
offerSkill = Function('offerSkill', Machine, Process)

## Processing functions
inProcessing = Function('inProcessing', Order, Process, Bottle, Cap, BoolSort())
haveBeenProcessed = Function('haveBeenProcessed', Order, Process, Bottle, Cap, BoolSort())

###### DYNAMIC SNAPSHOT
## Current Order
Order01 = Const('Order01', Order)
snap_order = [
    getOrderLiquid(Order01) == Soda,
    getOrderLiquidVolume(Order01) == 0.8,
    getOrderCapMaterial(Order01) == Aluminium,
    getOrderBottleMaterial(Order01) == Glass
]
## current available material (Bottle + Cap)
Bottle01 = Const('Bottle01', Bottle)
snap_product = [
    isWashed(Bottle01),
    isFilled(Bottle01),
    getBottleMaterial(Bottle01) == Glass,
    getBottleLiquid(Bottle01) == Soda,
    getBottleLiquidVolume(Bottle01) == 0.8,  # in liter
    getBottleTemperature(Bottle01) == 24,  # in °C
    getBottleDiameter(Bottle01) == 16.0  # in mm
]
Cap01 = Const('Cap01', Cap)
snap_product.extend(
    [
        getCapMaterial(Cap01) == Aluminium,
        getCapDiameter(Cap01) == 16.0,
        ForAll([b], Not(isMountedOn(Cap01, b)))
    ]
)
## Current available machine and corresponding skill
Machine01 = Const('Machine01', Machine)
M_Capping = Const('M_Capping', Process)
snap_skill = [
    ForAll([p], Implies(p == M_Capping, subProcess(p, InsertingDIN8580)))
]
snap_machine = [
    getMachineState(Machine01) == READY,
    offerSkill(Machine01) == M_Capping,
    isBottleInMachine(Bottle01, Machine01),
    isCapInMachine(Cap01, Machine01),
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
        getCapDiameter(c) >= getBottleDiameter(b)
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
    ForAll(
        [o, b, c],
        Implies(
            inProcessing(o, M_Capping, b, c),
            And(
                [
                    haveBeenProcessed(o, M_Capping, b, c),
                    isMountedOn(c, b),
                    getBottleLiquidVolume(b) == getOrderLiquidVolume(o),
                    getBottleTemperature(b) == 18.8,  # Process cool the bottle to 18.8 °C
                ]
            )
        )
    )
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
        getCapMaterial(c) == getOrderCapMaterial(o),
        getCapDiameter(c) == getBottleDiameter(b)
    ]))
]
# Restrictions on process execution
cond_process_executions = [
    ForAll([o, p, b, c], Implies(
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
    ForAll([o, p, b, c], And([
        haveBeenProcessed(o, p, b, c),
        isMountedOn(c, b),
        getBottleTemperature <= MAX_TEMP,
        getBottleTemperature >= MIN_TEMP,
    ]))
]

## Check if the pre conditions of the required task are fulfilled if the skill can be executed.
print "STEP 1: Check if the pre conditions of the required task are fulfilled by the available skill 'M_Capping'.\n" \
      "I.e. if the skill 'M_Capping' can be executed, are all the preconditions " \
      "of the required production task fulfilled?\n",
solver = configure_solver()
solver.add(model_axioms + dynamic_snap_shot)
solver.add(
    Not(
        Implies(
            And(cond_skill_initial_product + cond_skill_machine_restrict),
            And(cond_process_type + cond_pre_materials)
        )
    )
)
print("  %s" % solver.check())
file_name = "model_pre_conditions.smt2"
print("  saving model to %s ..." % file_name)
print_to_file(file_name, solver.to_smt2())
print("  Done.\n")

# Check if the conditions imposed by the required task during execution are fulfilled if the skill is executed.
print "STEP 2: Check if the restrictions on process execution are fulfilled if the skill 'M_Capping' is executed.\n" \
      "If the skill 'M_capping' is executed, are all restriction on process execution fulfilled?"
solver_exec = configure_solver()
solver_exec.add(model_axioms + dynamic_snap_shot)
solver_exec.add(
    Not(
        Implies(
            And(
                cond_skill_initial_product
                + cond_skill_machine_restrict
                + skill_machine_trans
                + [inProcessing(Order01, M_Capping, Bottle01, Cap01)]
            ),
            And(cond_process_executions)
        )
    )
)
print("  %s" % solver_exec.check())
file_name = "model_conditions_exec.smt2"
print("  saving model to %s ..." % file_name)
print_to_file(file_name, solver_exec.to_smt2())
print("  Done.\n")

# Check if the post conditions imposed by the required task during execution are fulfilled after the skill is executed.
print "STEP 3: Check if the restrictions on post-material are fulfilled if the skill 'M_Capping' is executed.\n" \
      "If the skill 'M_capping' is executed, are all restrictions on post-material fulfilled?"
solver_post = configure_solver()
solver_post.add(model_axioms + dynamic_snap_shot)
solver_post.add(
    Not(
        Implies(
            And(
                cond_skill_initial_product
                + cond_skill_machine_restrict
                + skill_machine_trans
                + [inProcessing(Order01, M_Capping, Bottle01, Cap01)]
            ),
            And(cond_post_materials)
        )
    )
)
print("  %s" % solver_post.check())
file_name = "model_post_conditions.smt2"
print("  saving model to %s ..." % file_name)
print_to_file(file_name, solver_post.to_smt2())
print("  Done.\n")

; benchmark generated from python API
(set-info :status unknown)
(declare-sort Process)
(declare-sort Liquid)
(declare-sort Order)
(declare-sort Material)
(declare-sort Bottle)
(declare-sort Cap)
(declare-sort MachineState)
(declare-sort Machine)
(declare-fun ROOT-PROCESS () Process)
(declare-fun InsertingDIN8580 () Process)
(declare-fun Soda () Liquid)
(declare-fun getOrderLiquid (Order) Liquid)
(declare-fun Order01 () Order)
(declare-fun getOrderLiquidVolume (Order) Real)
(declare-fun Aluminium () Material)
(declare-fun getOrderCapMaterial (Order) Material)
(declare-fun Glass () Material)
(declare-fun getOrderBottleMaterial (Order) Material)
(declare-fun Bottle01 () Bottle)
(declare-fun getBottleMaterial (Bottle) Material)
(declare-fun getBottleLiquid (Bottle) Liquid)
(declare-fun getBottleLiquidVolume (Bottle) Real)
(declare-fun getBottleTemperature (Bottle) Real)
(declare-fun getBottleDiameter (Bottle) Real)
(declare-fun getCapMaterial (Cap) Material)
(declare-fun Cap01 () Cap)
(declare-fun getCapDiameter (Cap) Real)
(declare-fun READY () MachineState)
(declare-fun getMachineState (Machine) MachineState)
(declare-fun Machine01 () Machine)
(declare-fun M_Capping () Process)
(declare-fun offerSkill (Machine) Process)
(declare-fun subProcess (Process Process) Bool)
(declare-fun isInsertingDIN8580 (Process) Bool)
(declare-fun isWashed (Bottle) Bool)
(declare-fun isFilled (Bottle) Bool)
(declare-fun isMountedOn (Cap Bottle) Bool)
(declare-fun isBottleInMachine (Bottle Machine) Bool)
(declare-fun isCapInMachine (Cap Machine) Bool)
(declare-fun inProcessing (Order Process Bottle Cap) Bool)
(declare-fun haveBeenProcessed (Order Process Bottle Cap) Bool)
(assert
(forall ((p1 Process) )(subProcess p1 p1))
)
(assert
(forall ((p1 Process) (p2 Process) )(=> (and (subProcess p1 p2) (subProcess p2 p1)) (= p1 p2)))
)
(assert
(forall ((p1 Process) (p2 Process) (p3 Process) )(=> (and (subProcess p1 p2) (subProcess p2 p3)) (subProcess p1 p3)))
)
(assert
(forall ((p1 Process) (p2 Process) (p3 Process) )(=> (and (subProcess p1 p2) (subProcess p1 p3)) (or (subProcess p2 p3) (subProcess p3 p2))))
)
(assert
(forall ((p Process) )(subProcess p ROOT-PROCESS))
)
(assert
(forall ((p Process) )(let (($x39 (subProcess p InsertingDIN8580)))
(=> $x39 (isInsertingDIN8580 p))))
)
(assert
(= (getOrderLiquid Order01) Soda))
(assert
(= (getOrderLiquidVolume Order01) (/ 4.0 5.0)))
(assert
(= (getOrderCapMaterial Order01) Aluminium))
(assert
(= (getOrderBottleMaterial Order01) Glass))
(assert
(isWashed Bottle01))
(assert
(isFilled Bottle01))
(assert
(= (getBottleMaterial Bottle01) Glass))
(assert
(= (getBottleLiquid Bottle01) Soda))
(assert
(= (getBottleLiquidVolume Bottle01) (/ 4.0 5.0)))
(assert
(= (getBottleTemperature Bottle01) 24.0))
(assert
(= (getBottleDiameter Bottle01) 16.0))
(assert
(= (getCapMaterial Cap01) Aluminium))
(assert
(= (getCapDiameter Cap01) 16.0))
(assert
(forall ((b Bottle) )(not (isMountedOn Cap01 b)))
)
(assert
(= (getMachineState Machine01) READY))
(assert
(= (offerSkill Machine01) M_Capping))
(assert
(isBottleInMachine Bottle01 Machine01))
(assert
(isCapInMachine Cap01 Machine01))
(assert
(forall ((p Process) )(let (($x39 (subProcess p InsertingDIN8580)))
(=> (= p M_Capping) $x39)))
)
(assert
(let (($x120 (forall ((o Order) (p Process) (b Bottle) (c Cap) )(=> (inProcessing o p b c) (and false true)))
))
(let (($x134 (forall ((o Order) (b Bottle) (c Cap) )(let (($x131 (and (haveBeenProcessed o M_Capping b c) (isMountedOn c b) (= (getBottleLiquidVolume b) (getOrderLiquidVolume o)) (= (getBottleTemperature b) (/ 94.0 5.0)))))
(=> (inProcessing o M_Capping b c) $x131)))
))
(let (($x116 (exists ((M Machine) )(and (= (offerSkill M) M_Capping) (= (getMachineState M) READY)))
))
(let (($x112 (exists ((b Bottle) (c Cap) )(and (isBottleInMachine b Machine01) (isCapInMachine c Machine01) (<= (getCapDiameter c) 100.0) (<= (getBottleDiameter b) 100.0) (>= (getCapDiameter c) (getBottleDiameter b))))
))
(let (($x317 (and $x112 $x116 $x134 (inProcessing Order01 M_Capping Bottle01 Cap01))))
(not (=> $x317 (and $x120)))))))))
(check-sat)

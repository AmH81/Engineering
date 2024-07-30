from main import Equipment, materials, Din

Rho = materials["Lube oil"]["rho"]
Miu = materials["Lube oil"]["miu"]
Cp = materials["Lube oil"]["cp"]
Rough = 1.5E-4  # ft


def test_equipment():
    pump1 = Equipment(P=4 * 14.7, T=68, Q=560).pump(Efficiency=0.75, Power=12)
    assert pump1 == 73
    '''pipe1 = Equipment(P=pump1["P2"], T=pump1["T2"], Q=pump1["Q2"]).pipe(Lentgh=10, Diameter=Din, Roughness=Rough,
                                                                        rho=Rho, miu=Miu)
    cv1 = Equipment(P=pipe1["P2"], T=pipe1["T2"], Q=pipe1["Q2"]).cv(Diameter=Din, Roughness=Rough, rho=Rho, miu=Miu,
                                                                    opening=80)
    pipe2 = Equipment(P=cv1["P2"], T=cv1["T2"], Q=cv1["Q2"]).pipe(Lentgh=5, Diameter=Din, Roughness=Rough, rho=Rho,
                                                                  miu=Miu)'''



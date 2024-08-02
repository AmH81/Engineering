"""
Testing equipment functions with Aspen hysys resulted data
    - T, P and Q are same for input, but may differ in outputs
    of each equipment which might be the input of next equipment.

    - A default tolerance error has been set for this equipment
    test. The test will be paased with following condition for each
    equipment:

    Python function output - Aspen hysys result / (Aspen hysys result)
    * 100 < tolerance error (%)
"""

from main import Equipment, materials, Din

Rho = materials["Lube oil"]["rho"]
Miu = materials["Lube oil"]["miu"]
Cp = materials["Lube oil"]["cp"]
Rough = 1.5E-4  # ft

def test_equipment(Pin=58.7837778275171, Tin=68, Qin=560, tolerance_error = 1.5E-2):

    pump1 = Equipment(P=Pin, T=Tin, Q=Qin).pump(Efficiency=0.75, Power=12)
    assert (pump1["T2"] - 68.2553105305809) / 68.2553105305809 * 100 < tolerance_error
    assert (pump1["P2"] - 86.3335085848319) / 86.3335085848319 * 100 < tolerance_error

    pipe1 = Equipment(P=pump1["P2"], T=pump1["T2"], Q=pump1["Q2"]).pipe(Lentgh=10, Diameter=Din, Roughness=Rough,
                                                                  rho=Rho, miu=Miu)
    assert (pipe1["T2"] - 68.2553104798749) / 68.2553104798749 * 100 < tolerance_error
    assert (pipe1["P2"] - 86.3291810126926) / 86.3291810126926 * 100 < tolerance_error

    cv1 = Equipment(P=pipe1["P2"], T=pipe1["T2"], Q=pipe1["Q2"]).cv(Diameter=Din, Roughness=Rough, rho=Rho, miu=Miu,
                                                                    opening=80)
    assert (cv1["T2"] - 68.2553104798749) / 68.2553104798749 * 100 < tolerance_error
    assert (cv1["P2"] - 86.3291810126926) / 86.3291810126926 * 100 < tolerance_error

    pipe2 = Equipment(P=cv1["P2"], T=cv1["T2"], Q=cv1["Q2"]).pipe(Lentgh=5, Diameter=Din, Roughness=Rough, rho=Rho,
                                                                  miu=Miu)
    assert (pipe2["T2"] - 68.2553104545306) / 68.2553104545306 * 100 < tolerance_error
    assert (pipe2["P2"] - 86.3270172455115) / 86.3270172455115 * 100 < tolerance_error

# Import csv, xls
# Export multi answers in (pdf)
from math import pi, log10, exp

'''
Default SCH
SCH 40, ND 12" 
'''
Din = 11.938  # inches
Dout = 12.750  # inches
Thickness = 0.406  # inches

"""
Unit set
rho --> lbm/ft^3
miu --> lbm/ft/h
"""
materials = {
    "Water":  # Extra fluid for further tests
        {
            "rho": 62.3042,
            "miu": 2.46065,
        },

    "Lube oil":  # 4bar  58.02psia   104F
        {
            "rho": 49.1298217410589,
            "miu": 139.332371090859,
            "cp": 307.412257535115,
        },

    "Fuel gas":  # Methane
        {
            "rho": 1.16960935749085,
            "miu": 2.96603447758313e-002,
        }
}


class Properties:
    def __init__(self, T, P, Q):
        self.T = T
        self.P = P
        self.Q = Q
# return the whole dict as the output to give the straight results to next equipment
    def __str__(self) -> dict:
        return {
            "T2": self.T,
            "P2": self.P,
            "Q2": self.Q,
        }


class Equipment(Properties):
    # Optional
    def __init__(self, T, P, Q):
        super().__init__(T, P, Q)

    def pump(self, Diameter=Din, Efficiency=0.75, Power=12.15007585, rho=materials["Lube oil"]["rho"], cp=materials["Lube oil"]["cp"],
             On=True):
        T = self.T
        P = self.P
        Q = self.Q

        Q2 = Q / 448.8325  # GPM to ft^3/s
        Diameter = Diameter / 12  # INCH TO FT
        A = pi * (Diameter / 2) ** 2  # ft^2
        V = Q2 / A  # ft/s
        P2 = P
        T2 = T
        Q2 = Q
        g = 32.174

        if On == True:
            delta_p = Power * 1715 * Efficiency / Q  # psia
            head = delta_p * 144 / (rho * g)  # ft
            P2 = delta_p + P  # psia

            m = rho * V * A
            H2 = delta_p / (rho * m) + cp * T
            T2 = H2 / cp

        return Properties(T2, P2, Q2).__str__()

    def fan(self, Diameter, cp=materials["Lube oil"]["cp"], rho=materials["Lube oil"]["rho"], Efficiency=0.75, Power=12.15007585, On=True):
        T = self.T
        P = self.P
        Q = self.Q

        Q2 = Q / 448.8325  # GPM to ft^3/s
        P = P * 144  # PSI to PSF
        Diameter = Diameter / 12  # INCH TO FT
        A = pi * (Diameter / 2) ** 2  # ft^2
        V = Q2 / A  # ft/s

        P2 = P
        Q2 = Q
        if On == True:
            delta_p = 550 * Efficiency / Q
            P2 = P - delta_p
            m = rho * V * A
            H2 = delta_p / (rho * m) + cp * T
            T2 = H2 / cp

        return Properties(T2, P2, Q2).__str__()

    def cv(self, Diameter, Roughness, rho, miu, cp=materials["Lube oil"]["cp"], opening=50):
        '''
        Based on a flanged gate valve
        '''
        T = self.T
        P = self.P
        Q = self.Q

        kd = 14.00 * Diameter ** (-0.36)
        ko = 123.48 * exp(-0.066 * opening)
        k = kd + ko

        g = 32.174

        miu = miu / 3600  # lbm/ft/h to lbm/ft/s
        Q2 = Q / 448.8325  # GPM to ft^3/s
        P = P * 144  # PSI to PSF
        Diameter = Diameter / 12  # INCH TO FT
        A = pi * (Diameter / 2) ** 2  # ft^2
        V = Q2 / A  # ft/s

        h_loss = (V ** 2 / (2 * g)) * k
        delta_p = h_loss * rho * g
        P2 = P - delta_p
        P2 = P2 / 144

        m = rho * V * A
        H2 = delta_p / (rho * m) + cp * T
        T2 = H2 / cp

        return Properties(T2, P2, Q).__str__()

    ## well Tested
    def pipe(self, Lentgh, Diameter, Roughness, rho, miu, cp=materials["Lube oil"]["cp"], angel=0):
        T = self.T
        P = self.P
        Q = self.Q

        ks = {
            0: [0, 0],
            5: [0.016, 0.024],
            10: [0.034, 0.044],
            15: [0.042, 0.062],
            22.5: [0.066, 0.154],
            30: [0.130, 0.165],
            45: [0.236, 0.320],
            60: [0.471, 0.684],
            90: [1.129, 1.265]
        }

        g = 32.174
        Roughness = Roughness * 12  # ft to inch
        rel_roughness = Roughness / Diameter  # inch / inch

        if rel_roughness < 0.0022:
            k = ks[angel][0]
        else:
            k = ks[angel][1]

        miu = miu / 3600  # lbm/ft/h to lbm/ft/s
        Q2 = Q / 448.8325  # GPM to ft^3/s
        P = P * 144  # PSI to PSF
        Diameter = Diameter / 12  # INCH TO FT
        A = pi * (Diameter / 2) ** 2  # ft^2
        V = Q2 / A  # ft/s

        Re = rho * V * Diameter / miu

        if Re < 2300:
            f = 64 / Re
        else:  # Holland equation
            f = (1 / (-1.8 * log10(6.9 / Re + (rel_roughness / 3.7) ** 1.11))) ** 2

        h_loss = (V ** 2 / (2 * g)) * (f * Lentgh / Diameter + k)
        delta_p = h_loss * rho * g
        P2 = P - delta_p
        P2 = P2 / 144

        m = rho * V * A
        H2 = delta_p / (rho * m) + cp * T
        T2 = H2 / cp

        return Properties(T2, P2, Q).__str__()


def main():
    Rho = materials["Lube oil"]["rho"]
    Miu = materials["Lube oil"]["miu"]
    Rough = 1.5E-4

    pump1 = Equipment(P=4 * 14.7, T=68, Q=560).pump(Efficiency=0.75, Power=1200000)

    pipe1 = Equipment(P=pump1["P2"], T=pump1["T2"], Q=pump1["Q2"]).pipe(Lentgh=10, Diameter=Din, Roughness=Rough,
                                                                        rho=Rho, miu=Miu)
    cv1 = Equipment(P=pipe1["P2"], T=pipe1["T2"], Q=pipe1["Q2"]).cv(Diameter=Din, Roughness=Rough, rho=Rho, miu=Miu,
                                                                    opening=80)
    pipe2 = Equipment(P=cv1["P2"], T=cv1["T2"], Q=cv1["Q2"]).pipe(Lentgh=5, Diameter=Din, Roughness=Rough, rho=Rho,
                                                                  miu=Miu)

    print("Pump 1 output:\n", pump1)
    print("Pipe 1 output:\n", pipe1)
    print("CV 1 output:\n", cv1)
    print("Pipe 2 output:\n", pipe2)


if __name__ == '__main__':
    main()

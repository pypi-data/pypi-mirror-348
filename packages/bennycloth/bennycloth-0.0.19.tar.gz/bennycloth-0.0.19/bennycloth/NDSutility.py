def MyRound(x, base=10):
        x = int(base*round(float(x)/base))
        return float(x)

def S4SWidth(bnom):
        """
        Return width based on nominal dimension of S4S lumber

        bnom - nominal width (inch)
        """
        
        if bnom == 1:
                return 0.75
        else:
                return bnom-0.5

def S4SDepth(dnom):
        """
        Return depth based on nominal dimension of S4S lumber

        dnom - nominal depth (inch)
        """
        
        if dnom < 8:
                return dnom-0.5
        else:
                return dnom-0.75

def S4SArea(bnom, dnom):
        """
        Return section area based on nominal dimensions of S4S lumber

        bnom - nominal width (inch)
        dnom - nominal depth (inch)
        """
        
        b = S4SWidth(bnom)
        d = S4SDepth(dnom)

        return b*d

def S4SModulus(bnom, dnom):
        """
        Return section modulus, S, based on nominal dimensions of S4S lumber

        bnom - nominal width (inch)
        dnom - nominal depth (inch)
        """
        
        b = S4SWidth(bnom)
        d = S4SDepth(dnom)
        
        return b*d**2/6

def TimberWidth(bnom):
        """
        Return width based on nominal dimension of timber

        bnom - nominal width (inch)
        """
        
        return bnom-0.5

def TimberDepth(dnom):
        """
        Return depth based on nominal dimension of timber

        dnom - nominal width (inch)
        """
        
        return dnom-0.5

def TimberArea(bnom, dnom):
        """
        Return section area based on nominal dimensions of timber

        bnom - nominal width (inch)
        dnom - nominal depth (inch)
        """
        
        b = TimberWidth(bnom)
        d = TimberDepth(dnom)
        
        return b*d

def TimberModulus(bnom, dnom):
        """
        Return section modulus, S, based on nominal dimensions of timber

        bnom - nominal width (inch)
        dnom - nominal depth (inch)
        """
        
        b = TimberWidth(bnom)
        d = TimberDepth(dnom)
        
        return b*d**2/6

def StabilityFactor(FcE, Fcstar, c=0.8):
        """
        Return stability factor, C_P, based on Euler and crushing stresses

        FcE - Euler buckling stress
        Fcstar - Crushing stress
        c - member factor (optional, default = 0.8)
            Note: use c = 0.9 for glulam
        """
        
        a = FcE/Fcstar
        b = (1+a)/(2*c)

        return b - (b**2-a/c)**0.5

def IncisingFactor(type):
        if type == 'Fb' or type == 'Ft' or type == 'Fc' or type == 'Fv':
                return 0.8
        if type == 'Fcp':
                return 1.0
        if type == 'E' or type == 'Emin':
                return 0.95
        return 1.0

def WetServiceFactor(type, b=2, d=2):
        if b > 4 and d > 4:
                # Timbers
                if type == 'Fcp':
                        return 0.67
                if type == 'Fc':
                        return 0.91
                return 1.0

        if type == 'Fb':
                return 0.85
        if type == 'Ft':
                return 1.0
        if type == 'Fv':
                return 0.97
        if type == 'Fcp':
                return 0.67
        if type == 'Fc':
                return 0.8
        if type == 'E' or type == 'Emin':
                return 0.9
        if type == 'Z':
                return 0.7
        return 1.0

def TemperatureFactor(type,T,WetOrDry='Dry'):
	if T <= 100:
		return 1.0

	if type == 'Fb' or type == 'Fv' or type == 'Fc' or type == 'Fcp':
		if T > 100 and T <= 125:
			if WetOrDry == 'Wet':
				return 0.7
			else:
				return 0.8
		if T > 125 and T <= 150:
			if WetOrDry == 'Wet':
				return 0.5
			else:
				return 0.7

	if type == 'Ft' or type == 'E' or type == 'Emin':
		if T > 100:
			return 0.9

def VolumeFactor(L, d, b, x=0.1):
        """
        Return volume factor, C_V, for glulam members

        L - member length (ft)
        d - member depth (inch)
        b - member width (inch)
        x - factor for glulam species (optional, default = 0.1)
            Note: use x = 0.05 for Southern Pines
        """
        
        CV = (21/L)**x * (12/d)**x * (5.125/b)**x

        return min(1.0,CV)

def SizeFactor(type, b, d):
        if type == 'Fb':
		# Timbers
                if b > 4 and d <= 12:
                        return 1.0
                if b > 4 and d > 12:
                        return (12.0/d)**(1./9)
                        
                if d <= 4:
                        return 1.5
                if d == 5:
                        return 1.4
                if d == 6:
                        return 1.3   
                        
                if d == 8 and b == 4:
                        return 1.3
                if d == 8 and b < 4:
                        return 1.2
        
                if d == 10 and b == 4:
                        return 1.2
                if d == 10 and b < 4:
                        return 1.1

                if d == 12 and b == 4:
                        return 1.1
                if d == 12 and b < 4:
                        return 1.0   
                        
                if d >= 14 and b == 4:
                        return 1.0
                if d >= 14 and b < 4:
                        return 0.9   
                        
                return 1.0

        if type == 'Ft':
		# Timbers
                if b > 4:
                        return 1.0

                if d <= 4:
                        return 1.5
                if d == 5:
                        return 1.4
                if d == 6:
                        return 1.3
                if d == 8:
                        return 1.2
                if d == 10:
                        return 1.1
                if d == 12:
                        return 1.0
                if d >= 14:
                        return 0.9

        if type == 'Fc':
                # Timbers
                if b > 4:
                        return 1.0

                if d <= 4:
                        return 1.15
                if d == 5:
                        return 1.1
                if d == 6:
                        return 1.1
                if d == 8:
                        return 1.05
                if d == 10:
                        return 1.0
                if d == 12:
                        return 1.0
                if d >= 14:
                        return 0.9
                        
        return 1.0      


 
def FormatConversionFactor(type):    
        if type == 'Fb':
                return 2.54
        if type == 'Ft':  
                return 2.70
        if type == 'Fv':  
                return 2.88
        if type == 'Fc':  
                return 2.40
        if type == 'Fcp': 
                return 1.67
        if type == 'Emin': 
                return 1.76
        if type == 'Z' or type == 'W':
                return 3.32
        return 1.0
                        
def phiFactor(type):
        if type == 'Fb':
                return 0.85
        if type == 'Ft':
                return 0.80
        if type == 'Fv':   
                return 0.75
        if type == 'Fc':   
                return 0.90
        if type == 'Fcp':  
                return 0.90
        if type == 'Emin': 
                return 0.85
        if type == 'Z' or type == 'W':
                return 0.65
        return 1.0

def GroupActionFactor(Am,As,n,D=1.0,s=4,Em=1.4e6,Es=1.4e6):
        """
        Return group action factor for a bolt group

        Am - area of main member (inch^2)
        As - area of side member (inch^2)
        n - number of rows
        D - bolt diameter (inch, optional, default = 1.0)
        s - bolt spacing (inch, optional, default = 4.0)
        Em - elastic modulus of main member (psi, optional, default = 1.4e6)
        Es - elastic modulus of side member (psi, optional, default = 1.4e6)
        """
        
        if D < 0.25:
                return 1.0

        REA = min(Es*As/(Em*Am),Em*Am/(Es*As))
        gamma = 180000*D**1.5
        u = 1 + gamma*s/2*(1/(Em*Am)+1/(Es*As))
        m = u - (u**2-1)**0.5
        num = m*(1-m**(2*n))
        den = n*((1+REA*m**n)*(1+m)-1+m**(2*n))
        Cg = (num/den)*(1+REA)/(1-m)
        
        return Cg

def BoltSingleShear(tm,ts,D,G):
        """
        Return bolt strength in single shear
        
        tm - thickness of main member (inch)
        ts - thinkness of side member (inch)
        D - bolt diameter (inch)
        G - specific gravity of members

        Returns list of four values
        [Z||,Zpside,Zpmain,Zperp]
          loading parallel to grain of both members
          loading perpendicular to grain side member
          loading perpendicular to grain main member
          loading perpendicular to grain of both members
        """
        
        lm = tm
        ls = ts
        Rt = lm/ls

        Zref = [0,0,0,0]

        Fyb = 45000.0
        if D < 0.25:
                Fyb = 100000.0

	# Z parallel
        theta = 0
        Fem = MyRound(11200.0*G,50)
        Fes = MyRound(11200.0*G,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = D*ls*Fes/Rd
        Z = min(Z,ZIs)
        k1 = (math.sqrt(Re+2*Re**2*(1+Rt+Rt**2)+Rt**2*Re**3)-Re*(1+Rt))/(1+Re)
        Rd = 3.6*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZII = k1*D*ls*Fes/Rd
        Z = min(Z,ZII)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k2 = -1+math.sqrt(2*(1+Re)+(2*Fyb*(1+2*Re)*D**2)/(3*Fem*lm**2))
        ZIIIm = k2*D*lm*Fem/((1+2*Re)*Rd)
        Z = min(Z,ZIIIm)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[0] = MyRound(Z,1)

        # Z perpendicular
        theta = 90
        Fem = MyRound(6100.0*G**1.45/D**0.5,50)
        Fes = MyRound(6100.0*G**1.45/D**0.5,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = D*ls*Fes/Rd
        Z = min(Z,ZIs)
        k1 = (math.sqrt(Re+2*Re**2*(1+Rt+Rt**2)+Rt**2*Re**3)-Re*(1+Rt))/(1+Re)
        Rd = 3.6*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZII = k1*D*ls*Fes/Rd
        Z = min(Z,ZII)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k2 = -1+math.sqrt(2*(1+Re)+(2*Fyb*(1+2*Re)*D**2)/(3*Fem*lm**2))
        ZIIIm = k2*D*lm*Fem/((1+2*Re)*Rd)
        Z = min(Z,ZIIIm)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[3] = MyRound(Z,1)

        # Z perpendicular to main
        theta = 90
        Fem = MyRound(6100.0*G**1.45/D**0.5,50)
        Fes = MyRound(11200.0*G,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = D*ls*Fes/Rd
        Z = min(Z,ZIs)
        k1 = (math.sqrt(Re+2*Re**2*(1+Rt+Rt**2)+Rt**2*Re**3)-Re*(1+Rt))/(1+Re)
        Rd = 3.6*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZII = k1*D*ls*Fes/Rd
        Z = min(Z,ZII)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k2 = -1+math.sqrt(2*(1+Re)+(2*Fyb*(1+2*Re)*D**2)/(3*Fem*lm**2))
        ZIIIm = k2*D*lm*Fem/((1+2*Re)*Rd)
        Z = min(Z,ZIIIm)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[2] = MyRound(Z,1)

        # Z perpendicular to side member
        theta = 90
        Fem = MyRound(11200.0*G,50)
        Fes = MyRound(6100.0*G**1.45/D**0.5,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = D*ls*Fes/Rd
        Z = min(Z,ZIs)
        k1 = (math.sqrt(Re+2*Re**2*(1+Rt+Rt**2)+Rt**2*Re**3)-Re*(1+Rt))/(1+Re)
        Rd = 3.6*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZII = k1*D*ls*Fes/Rd
        Z = min(Z,ZII)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k2 = -1+math.sqrt(2*(1+Re)+(2*Fyb*(1+2*Re)*D**2)/(3*Fem*lm**2))
        ZIIIm = k2*D*lm*Fem/((1+2*Re)*Rd)
        Z = min(Z,ZIIIm)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[1] = MyRound(Z,1)

        return Zref


def BoltDoubleShear(tm,ts,D,G):
        """
        Return bolt strength in double shear
        
        tm - thickness of main member (inch)
        ts - thinkness of side member (inch)
        D - bolt diameter (inch)
        G - specific gravity of members

        Returns list of four values
        [Z||,Zpside,Zpmain,Zperp]
          loading parallel to grain of both members
          loading perpendicular to grain side member
          loading perpendicular to grain main member
          loading perpendicular to grain of both members
        """
        
        lm = tm
        ls = ts
        Rt = lm/ls

        Fyb = 45000.0
        if D < 0.25:
                Fyb = 100000.0

        Zref = [0,0,0]

        # Z parallel
        theta = 0
        Fem = MyRound(11200.0*G,50)
        Fes = MyRound(11200.0*G,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = 2.0*D*ls*Fes/Rd
        Z = min(Z,ZIs)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = 2.0*k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = 2.0*D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[0] = MyRound(Z,10)

        # Z perpendicular to main
        theta = 90
        Fem = MyRound(6100.0*G**1.45/D**0.5,50)
        Fes = MyRound(11200.0*G,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = 2.0*D*ls*Fes/Rd
        Z = min(Z,ZIs)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = 2.0*k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = 2.0*D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[2] = MyRound(Z,10)

        # Z perpendicular to side member
        theta = 90
        Fem = MyRound(11200.0*G,50)
        Fes = MyRound(6100.0*G**1.45/D**0.5,50)

        Re = Fem/Fes

        Ktheta = 1 + 0.25*(theta/90.0)
        Rd = 4*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        ZIm = D*lm*Fem/Rd
        Z = ZIm
        ZIs = 2.0*D*ls*Fes/Rd
        Z = min(Z,ZIs)
        Rd = 3.2*Ktheta
        if D < 0.25:
                Rd = max(2.2,10*D + 0.5)
        k3 = -1+math.sqrt(2*(1+Re)/Re+(2*Fyb*(2+Re)*D**2)/(3*Fem*ls**2))
        ZIIIs = 2.0*k3*D*ls*Fem/((2+Re)*Rd)
        Z = min(Z,ZIIIs)
        ZIV = 2.0*D**2/Rd*math.sqrt(2*Fem*Fyb/(3*(1+Re)))
        Z = min(Z,ZIV)
        Zref[1] = MyRound(Z,10)

        return Zref


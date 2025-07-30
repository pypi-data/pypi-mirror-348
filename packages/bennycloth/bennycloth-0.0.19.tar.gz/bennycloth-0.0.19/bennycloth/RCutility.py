import numpy as np
import math

def barSizes():
    """
    Returns a list of US bar designations 3--18
    """
    return [3,4,5,6,7,8,9,10,11,14,18]


def barNums():
    """
    Returns a list of US bar designations 3--18
    """
    return barSizes()


def barArea(designation):
    """
    Cross-sectional area (in^2) of round bars
    US designations 3,4,5,6,7,8,9,10,11,14,18

    designation (integer, 3--18)
    """
    
    if designation not in barSizes():
        return None
    
    return {
        3: 0.11,
        4: 0.20,
        5: 0.31,
        6: 0.44,
        7: 0.60,
        8: 0.79,
        9: 1.00,
        10: 1.27,
        11: 1.56,
        14: 2.25,
        18: 4.00
    }[designation]


def barDiam(designation):
    """
    Diameter (in) of round bars
    US designations 3,4,5,6,7,8,9,10,11,14,18

    designation (integer, 3--18)
    """
    
    if designation not in barSizes():
        return None
    
    return {
        3: 0.375,
        4: 0.50,
        5: 0.625,
        6: 0.75,
        7: 0.875,
        8: 1.00,
        9: 1.128,
        10: 1.27,
        11: 1.41,
        14: 1.693,
        18: 2.257
    }[designation]


def selectBar(Abreq):
    """
    Returns the smallest round bar with required area
    US designations 3--18

    Abreq - required bar area (in^2)
    """
    
    for bar in barSizes():
        if Abreq <= barArea(bar):
            return bar

    return None

def straightAnchorage(fc, fy, bar, psit=1.0, psie=1.0, lam=1.0):
    """
    Returns required development length (in) for straight anchorage

    fc - concrete compressive strength (psi)
    fy - bar strength (psi)
    bar - bar size, US designation 3--18
    psit - top steel factor (optional, default = 1)
    psie - epoxy factor (optional, default = 1)
    lam - lightweight concrete factor (optional, default = 1)
    """

    if bar not in barSizes():
        return None
    
    db = barDiam(bar)

    if bar <= 6:
        ld = db*(fy*psit*psie)/(25*lam*fc**0.5)
    else:
        ld = db*(fy*psit*psie)/(20*lam*fc**0.5)        

    return ld

def hookedAnchorage(fc, fy, bar, psie=1.0, psic=1.0, psir=1.0, lam=1.0):
    """
    Returns required development length (in) for hooked anchorage

    fc - concrete compressive strength (psi)
    fy - bar strength (psi)
    bar - bar size, US designation 3--18
    psie - epoxy factor (optional, default = 1)
    psic - (optional, default = 1)
    psir - (optional, default = 1)
    lam - lightweight concrete factor (optional, default = 1)
    """
    
    db = barDiam(bar)

    ldh = db*(fy*psie*psic*psir)/(50*lam*fc**0.5)

    return ldh

def beta1(fc):
    """
    Returns WSB parameter, $\beta_1$

    fc - concrete compressive strength (psi)
    """
    
    if fc < 4000:
        return 0.85
    if fc > 8000:
        return 0.65
    return 0.85-0.05*(fc-4000)/1000.0

def beamPhi(et):
    """
    Returns strength reduction factor, $\phi$, for flexural members
    with non-conforming transverse reinforcement

    et - strain in tension steel at ultimate strength
    """
    
    if et < 0.002:
        return 0.65
    if et > 0.005:
        return 0.90
    return 0.65 + 250.0/3*(et-0.002)

def beamPhiRound(et):
    """
    Returns strength reduction factor, $\phi$, for flexural members
    with conforming spiral transverse reinforcement

    et - strain in tension steel at ultimate strength
    """    
    if et < 0.002:
        return 0.75
    if et > 0.005:
        return 0.90
    return 0.75 + 150.0/3*(et-0.002)

def flexuralStrength(fc, fy, E, b, As, d, Asp=0, dp=0):
    """
    Calculate the flexural strength (nominal and avaialble)
    for a rectangular RC section with compression steel
    
    OUTPUTS [Mn,phi,c]
    Mn - nominal flexural strength (lb-in)
    phi - strength reduction factor
    c - depth from compression face to neutral axis (in)

    INPUTS
    fc - concrete compressive strength (psi)
    fy - steel strength (psi)
    E - steel modulus of elasticity (psi)
    b - section width (in)
    As - total area of tension steel (in^2)
    d - depth from compression face to centroid of tension steel (in)
    Asp - total area of comrpession steel (in^2) (optional, default=0)
    dp - depth from compression face to centroid of compression steel (in) (optional, default=0)
    """

    # Initial guess for NA
    c = d/4.0

    b1 = beta1(fc)

    T = As*fy
    a = b1*c
    Cc = 0.85*fc*a*b
    Cs = 0.0

    i = 0
    iMax = int(d/0.001)
    while i < iMax and abs(T-(Cc+Cs)) > 0.001*T:
        i = i+1

        if T > (Cc+Cs):
            c = c + 0.001
        else:
            c = c - 0.001

        # Compression concrete
        a = b1*c
        Cc = 0.85*fc*a*b

        # Compression steel
        esp = (c-dp)/c*0.003
        fsp = abs(E*esp)
        if fsp > fy:
            fsp = fy
        if dp < a:
            fsp = fsp-0.85*fc
        Cs = Asp*fsp

        # Tension steel
        es = (d-c)/c*0.003
        fs = abs(E*es)
        if fs > fy:
            fs = fy
        T = As*fs

    es = (d-c)/c*0.003
    phi = beamPhi(es)

    Mn = Cc*(d-0.5*a) + Cs*(d-dp)

    return [phi,Mn,c]
    

def designStrength(fc, fy, E, b, h, Nlayers, d, As, epst):
    """
    Calculate the available design strength
    for a rectangular RC section with multiple layers of steel
    
    OUTPUTS [Pn,Mn,phiPn,phiMn]
    Pn - nominal axial strength (lb)
    phiPn - available axial strength (lb)
    Mn - nominal flexural strength (lb-in)
    phiMn - available flexural strength (lb-in)

    INPUTS
    fc - concrete compressive strength (psi)
    fy - steel strength (psi)
    E - steel modulus of elasticity (psi)
    b - section width (in)
    h - section depth (in)
    Nlayers - number of steel layers
    d[] - list of steel layer depths (in) (index 0 is extreme tension layer)
    As[] - list of steel layer areas (total steel in layer) (in^2) (index 0 is extreme tension layer)
    epst - strain in extreme tension steel (negative compression, positive tension)
    """

    b1 = beta1(fc)

    c = 0.003/(0.003+epst)*d[0]
    a = min(h,b1*c)
    Cc = 0.85*fc*a*b
        
    Pn = Cc
    Mn = Cc*(0.5*h-0.5*a)

    for i in range(Nlayers):
        eps = (c-d[i])/c*-0.003
        fs = min(fy,math.fabs(eps*E))
        if d[i] < a:
            fs = fs - 0.85*fc
        Fs = np.sign(eps)*fs*As[i]
        Pn = Pn - Fs
        Mn = Mn + Fs*(d[i]-0.5*h)
        
    phi = beamPhi(epst)

    phiPn = phi*Pn
    phiMn = phi*Mn

    return [Pn,Mn,phiPn,phiMn]


def interactionDiagram(fc, fy, E, b, h, rhog, Nbars, gamma, Npts=100):
    """
    Calculate the interaction diagram for a rectangular RC section
    
    OUTPUTS
    [Pn/Ag,Mn/(Ag*h),phiPn/Ag,phiMn/(Ag*h),Pn,Mn,phiPn,phiMn]
    Pn - nominal axial strength (lb)
    phiPn - available axial strength (lb)
    Mn - nominal flexural strength (lb-in)
    phiMn - available flexural strength (lb-in)
    Ag - gross section area (b*h)
    
    INPUTS
    fc - concrete compressive strength (psi)
    fy - steel strength (psi)
    E - steel modulus of elasticity (psi)
    b - section width (in)
    h - section depth (in)
    rhog - gross reinforcing ratio, e.g., 0.02 for 2%
    Nbars - number of bars on any *one* side of the section
    gamma - ratio of steel moment arm to section depth, h
    """

    if Npts < 2:
        Npts = 100
    output = []

    b1 = beta1(fc)

    Ag = b*h
    Ast = rhog*Ag

    d = [0]*Nbars
    As = [0]*Nbars

    As[0] = Ast*Nbars/(2*Nbars+2*(Nbars-2))
    d[0] = h-0.5*(h-gamma*h)
    for i in range(1,Nbars-1):
        As[i] = Ast*2/(2*Nbars+2*(Nbars-2))
        d[i] = d[Nbars-1] + (gamma*h)*i/(Nbars-1)
    As[Nbars-1] = As[0]
    d[Nbars-1] = 0.5*(h-gamma*h)
    
    Pno = 0.8*(0.85*fc*(Ag-Ast) + fy*Ast)
    phi = beamPhi(0)
    phiPn = phi*Pno

    phiPnT = -beamPhi(0.1)*fy*Ast

    output[0,:] = [Pno/Ag,0.0,phiPn/Ag,0.0,Pno,0.0,phiPn,0.0]

    epst = -0.003 + 1e-16

    start = 2*h
    stop = 0.5*d[Nbars-1]
    step = (stop-start)/Npts

    ii = 1
    for c in np.arange(start,stop,step):
        a = min(h,b1*c)
        Cc = 0.85*fc*a*b
        
        Pn = Cc
        Mn = Cc*(0.5*h-0.5*a)

        for i in range(Nbars):
            eps = (c-d[i])/c*-0.003
            fs = min(fy,math.fabs(eps*E))
            if d[i] < a:
                fs = fs - 0.85*fc
            Fs = np.sign(eps)*fs*As[i]
            Pn = Pn - Fs
            Mn = Mn + Fs*(d[i]-0.5*h)
        
        if Pn > Pno:
            Pn = Pno
        
        eps1 = (c-d[0])/c*-0.003
        phi = beamPhi(eps1)

        phiPn = phi*Pn
        phiMn = phi*Mn

        output[ii,:] = [Pn/Ag,Mn/(Ag*h),phiPn/Ag,phiMn/(Ag*h),Pn,Mn,phiPn,phiMn]
        ii = ii+1

    PnT = -fy*Ast
    phiPnT = beamPhi(0.1)*PnT

    output[Npts+1,:] = [PnT/Ag,0.0,phiPnT/Ag,0.0,PnT,0.0,phiPnT,0.0]

    return output


def interactionDiagramRound(fc, fy, E, h, rhog, Nbars, gamma, Npts=100):
    """
    Calculate the interaction diagram for a circular RC section with
    conforming spiral transverse reinforcement
    
    OUTPUTS
    [Pn/Ag,Mn/(Ag*h),phiPn/Ag,phiMn/(Ag*h),Pn,Mn,phiPn,phiMn]
    Pn - nominal axial strength (lb)
    phiPn - available axial strength (lb)
    Mn - nominal flexural strength (lb-in)
    phiMn - available flexural strength (lb-in)
    Ag - gross section area (pi*h*h/4)
    
    INPUTS
    fc - concrete compressive strength (psi)
    fy - steel strength (psi)
    E - steel modulus of elasticity (psi)
    h - section diameter (in)
    rhog - gross reinforcing ratio, e.g., 0.02 for 2%
    Nbars - total number of bars in the section
    gamma - ratio of steel moment arm to section diameter, h
    """

    if Npts < 2:
        Npts = 100
    output = []
    
    b1 = beta1(fc)

    Ag = h*h*3.14159/4.0
    Ast = rhog*Ag

    d = [0]*(Nbars//2)
    As = [0]*(Nbars//2)

    for i in range(Nbars//2):
        As[i] = 2*Ast/Nbars
        theta = (i+0.5)*2*3.14159/Nbars
        d[i] = 0.5*h - 0.5*gamma*h*math.cos(theta)
    
    Pno = 0.85*(0.85*fc*(Ag-Ast) + fy*Ast)
    phi = beamPhiRound(0)
    phiPn = phi*Pno

    output[0,:] = [Pno/Ag,0.0,phiPn/Ag,0.0,Pno,0.0,phiPn,0.0]
    
    epst = -0.003 + 1e-16

    start = 2*h
    stop = 0.5*d[0]
    step = (stop-start)/Npts
    
    ii = 1    
    for c in np.arange(start,stop,step):
        a = min(h,b1*c)
        if a <= 0.5*h:
            theta = math.acos(1.0-a/(0.5*h))
        else:
            theta = 3.14159 - math.acos(a/(0.5*h)-1.0)

        Ac = h*h*(theta-math.sin(theta)*math.cos(theta))/4.0
        Cc = 0.85*fc*Ac
        Pn = Cc

        ybar = h*h*h/12.0*(math.sin(theta))**3/Ac
        
        Mn = Cc*ybar

        for i in range(Nbars//2):
            eps = (c-d[i])/c*-0.003
            fs = min(fy,math.fabs(eps*E))
            if d[i] < a:
                fs = fs - 0.85*fc
            Fs = np.sign(eps)*fs*As[i]
            Pn = Pn - Fs
            Mn = Mn + Fs*(d[i]-0.5*h)
        
        if Pn > Pno:
            Pn = Pno
        
        phi = beamPhiRound(epst)

        phiPn = phi*Pn
        phiMn = phi*Mn

        output[ii,:] = [Pn/Ag,Mn/(Ag*h),phiPn/Ag,phiMn/(Ag*h),Pn,Mn,phiPn,phiMn]
        ii = ii+1        

        epst = epst + 0.00005

    PnT = -fy*Ast
    phiPnT = beamPhi(0.1)*PnT

    output[Npts+1,:] = [PnT/Ag,0.0,phiPnT/Ag,0.0,PnT,0.0,phiPnT,0.0]

    return output

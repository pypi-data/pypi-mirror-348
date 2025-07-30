def LiveLoadReduction(AT, KLL=1):
    """
    ASCE 7 live load reduction factor

    AT - tributary area (ft^2)
    KLL - component factor (default = 1)
    """

    KLLAT = KLL*AT
    
    if KLLAT > 400.0:
        return max(0.4,0.25 + 15/KLLAT**0.5)
    else:  
        return 1.0

def VelocityPressure(z, exposure):
    """
    ASCE 7 wind velocity pressure

    z - height above ground (ft)
    exposure - category ('B', 'C', or 'D')
    """
    
    if exposure == 'B':
        zg = 1200.0
        alpha = 7.0
    if exposure == 'C':
        zg = 900.0
        alpha = 9.5
    if exposure == 'D':
        zg = 700.0
        alpha = 11.5

    if z < 0.0:
        return 0.0
        
    if z < 15.0:
        return 2.01*(15.0/zg)**(2.0/alpha)
    else:
        return 2.01*(z/zg)**(2.0/alpha)

def SiteFactorShortPeriod(soil, Ss):
    """
    ASCE 7 soil site factor for short period spectral acceleration

    soil - classification ('A', 'B', 'C', 'D', or 'E')
    Ss - short period spectral acceleration (g)
    """
    
    if soil == 'A':
        return 0.8
    if soil == 'B':
        return 0.9
    if soil == 'C':
        if Ss <= 0.5:
            return 1.3
        else:
            return 1.2
    if soil == 'D':
        if Ss <= 0.25:
            return 1.6
        if Ss <= 0.5:
            return 1.4
        if Ss <= 0.75:
            return 1.2
        if Ss <= 1.0:
            return 1.1
        return 1.0
    if soil == 'E':
        if Ss <= 0.25:
            return 2.4
        if Ss <= 0.5:
            return 1.7
        if Ss <= 0.75:
            return 1.3
        return None
    return None

def SiteFactorLongPeriod(soil, S1):
    """
    ASCE 7 soil site factor for long period spectral acceleration

    soil - classification ('A', 'B', 'C', 'D', or 'E')
    S1 - long period spectral acceleration (g)
    """
    
    if soil == 'A':
        return 0.8
    if soil == 'B':
        return 0.8
    if soil == 'C':
        if S1 <= 0.5:
            return 1.5
        else:
            return 1.4
    if soil == 'D':
        if S1 <= 0.1:
            return 2.4
        if S1 <= 0.2:
            return 2.2
        if S1 <= 0.3:
            return 2.0
        if S1 <= 0.4:
            return 1.9
        if S1 <= 0.5:
            return 1.8        
        return 1.7
    if soil == 'E':
        if S1 <= 0.1:
            return 4.2
        return None
    return None

import csv
import math
import re
import os.path

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False

shapes = open(os.path.join(os.path.dirname(__file__),'AISC_Shapes_Database_v15.csv'),'r')
#shapes = open('./AISC_Shapes_Database_v15.csv')
shapesReader = csv.DictReader(shapes)

#shapes.seek(0)
allWshapes = []
allWTshapes = []
allCshapes = []
allMCshapes = []
allLshapes = []
all2Lshapes = []
allLLBBshapes = []
allSLBBshapes = []
allHSSshapes = []
allRoundHSSshapes = []
for row in shapesReader:
        row['AISC_Manual_Label'] = row['AISC_Manual_Label'].replace('X','x')
        if row['Type'] == 'W':
                allWshapes.append(row)
        if row['Type'] == 'WT':
                allWTshapes.append(row)
        if row['Type'] == 'C':
                allCshapes.append(row)
        if row['Type'] == 'MC':
                allMCshapes.append(row)        
        if row['Type'] == 'L':
                allLshapes.append(row)
        if row['Type'] == '2L':
                all2Lshapes.append(row)
        if 'LLBB' in row['AISC_Manual_Label']:
                allLLBBshapes.append(row)
        if 'SLBB' in row['AISC_Manual_Label']:
                allSLBBshapes.append(row)                        
        if row['Type'] == 'HSS':
                allHSSshapes.append(row)
                if isfloat(row['OD']) and isfloat(row['tnom']):
                        allRoundHSSshapes.append(row)

def FindShape (label, shapes):
	"""
	Return shape dictionary that matches label
	Searches among shapes in Wshapes list

	label - search string, e.g., 'W14x90' or 'L4x4x1/4'
		Note: function will handle X or x
	shapes - shapes to search 
	"""
	label = label.replace('X','x')
	for shape in shapes:
		if label == shape['AISC_Manual_Label']:
			return shape
	return []

def StandardBoltHole (db):
        if db < 1.0:
                return db + 1.0/16
        else:
                return db + 1.0/8
        
def BoltShearStrength (db, type, m=1):
	if m < 1:
		m = 1;
	if m > 2:
		m = 2;

	[FnvOmega,phiFnv] = [0.0,0.0]
	if type == 'A325N':
		[FnvOmega,phiFnv] = [27.0,40.5]
	if type == 'A325X':
		[FnvOmega,phiFnv] = [34.0,51.0]
	if type == 'A490N':
		[FnvOmega,phiFnv] = [34.0,51.0]
	if type == 'A490X':
		[FnvOmega,phiFnv] = [42.0,63.0]
	if type == 'A307':
		[FnvOmega,phiFnv] = [13.5,20.3]

	Ab = math.pi*db**2/4.0
	return [FnvOmega*Ab*m,phiFnv*Ab*m]

def BoltTensionStrength (db, type):
	[FntOmega,phiFnt] = [0.0,0.0]
	if re.match('A325',type):
		[FntOmega,phiFnt] = [45.0,67.5]
	if re.match('A490',type):
		[FntOmega,phiFnt] = [56.5,84.8]
	if re.match('A307',type):
		[FntOmega,phiFnt] = [22.5,33.8]

	Ab = math.pi*db**2/4.0
	return [FntOmega*Ab,phiFnt*Ab]

def PlasticUnbracedLength (Wshape, Fy, E):
        ry = float(Wshape['ry'])
        Lp = 1.76*ry*math.sqrt(float(E)/Fy)
        return Lp

def ElasticLTBUnbracedLength (Wshape, Fy, E):
        Iy = float(Wshape['Iy'])
        Cw = float(Wshape['Cw'])
        Sx = float(Wshape['Sx'])
        J  = float(Wshape['J'])
        c  = 1.0
        d  = float(Wshape['d'])   
        tf = float(Wshape['tf'])
        rts = math.sqrt(math.sqrt(Iy*Cw)/Sx)
        ho = d - tf
        JcSxho = J*c/(Sx*ho)
        Lr = 1.95*rts*E/(0.7*Fy)*math.sqrt(JcSxho+math.sqrt(JcSxho**2+6.76*(0.7*Fy/E)**2))
        return Lr

def ElasticLTBFlexuralStress (Wshape, Lb, Fy, E):
        Iy = float(Wshape['Iy'])
        Cw = float(Wshape['Cw'])
        Sx = float(Wshape['Sx'])
        J  = float(Wshape['J']) 
        c  = 1.0
        d  = float(Wshape['d'])
        tf = float(Wshape['tf'])
        rts = math.sqrt(math.sqrt(Iy*Cw)/Sx)
        ho = d - tf
        JcSxho = J*c/(Sx*ho)
        Fcr = (math.pi)**2*E/(Lb/rts)**2*math.sqrt(1.0+0.078*JcSxho*(Lb/rts)**2)
        return Fcr

def FlexuralStrength (Wshape, Lb, Fy, E):
        Lp = PlasticUnbracedLength(Wshape, Fy, E)
        Lr = ElasticLTBUnbracedLength(Wshape, Fy, E)
        Sx = float(Wshape['Sx'])
        Zx = float(Wshape['Zx'])
        d  = float(Wshape['d'])
        
        #if Lb > 30.0*d:
        #        return [0.1,0.1] # Beam chart won't go this far out, but it seems it does if this shape is the lightest	Mp = Fy*Zx
	
        Mp = Fy*Zx

        if Lb <= Lp:
                Mn = Mp
        elif Lb > Lr:
                Fcr = ElasticLTBFlexuralStress(Wshape, Lb, Fy, E)
                Mn = Fcr*Sx
        else:
                Mp = Fy*Zx
                Mr = 0.7*Fy*Sx
                Mn = Mp-(Mp-Mr)*(Lb-Lp)/(Lr-Lp)

        if Wshape['Type'] != 'W':
                return [Mn/1.67,0.9*Mn]
        
        lam = float(Wshape['bf/2tf'])
        lamp = 0.38*math.sqrt(float(E)/Fy)
        if lam <= lamp: # Compact flange
                Mnb = Mn
        lamr = 1.00*math.sqrt(float(E)/Fy)
        if lam >= lamr: # Slender flange
                htw = float(Wshape['h/tw'])
                kc = 4.0/math.sqrt(htw)
                kc = max(kc,0.35)
                kc = min(kc,0.76)
                Mnb = 0.9*E*kc*Sx/lam**2
        if lam > lamp and lam < lamr: # Noncompact flange
                Mr = 0.7*Fy*Sx
                Mnb = Mp-(Mp-Mr)*(lam-lamp)/(lamr-lamp)
		
        Mn = min(Mn,Mnb)

        return [Mn/1.67,0.9*Mn]

def TensionRuptureStrength (Wshape, Fu, Ae=-1):
    if Ae <= 0:
        Ag = float(Wshape['A'])
        Ae = 0.75*Ag
    Pn = Fu*Ae
    return [Pn/2.0,0.75*Pn]

def GrossTensionStrength (Wshape, Fy):
	Ag = float(Wshape['A'])
	Pn = Fy*Ag
	return [Pn/1.67,0.9*Pn]

def LightestShapeGrossTension (Wshapes, Pu, Fy):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		[PnOmega,phiPn] = GrossTensionStrength(Wshape,Fy)
		if phiPn > Pu and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeGrossTensionASD (Wshapes, Pa, Fy):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		[PnOmega,phiPn] = GrossTensionStrength(Wshape,Fy)
		if PnOmega > Pa and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeAg (Wshapes, Agreq):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		Ag = float(Wshape['A'])
		if Ag >= Agreq and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeIx (Wshapes, Ixreq):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		Ix = float(Wshape['Ix'])
		if Ix >= Ixreq and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeIy (Wshapes, Iyreq):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		Iy = float(Wshape['Iy'])
		if Iy >= Iyreq and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeZx (Wshapes, Zxreq):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		Zx = float(Wshape['Zx'])
		if Zx >= Zxreq and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeZy (Wshapes, Zyreq):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		Zy = float(Wshape['Zy'])
		if Zy >= Zyreq and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeFlexure (Wshapes, Mu, Lb, Fy, E):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		[MnOmega,phiMn] = FlexuralStrength (Wshape, Lb*12.0, Fy, E)
		if phiMn/12.0 >= Mu and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeFlexureASD (Wshapes, Ma, Lb, Fy, E):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		[MnOmega,phiMn] = FlexuralStrength (Wshape, Lb*12.0, Fy, E)
		if MnOmega/12.0 >= Ma and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeCompression (Wshapes, Pu, KLx, KLy, Fy, E):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		[PnOmega,phiPn] = AxialCompressionStrength (Wshape, KLx, KLy, Fy, E)
		if phiPn >= Pu and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def LightestShapeCompressionASD (Wshapes, Pa, KLx, KLy, Fy, E):
	shape = []
	minWt = 1.0e10
	for Wshape in Wshapes:
		Wt = float(Wshape['W'])
		[PnOmega,phiPn] = AxialCompressionStrength (Wshape, KLx, KLy, Fy, E)
		if PnOmega >= Pa and Wt <= minWt:
			minWt = Wt
			shape = Wshape
	return shape

def ShearStrength (Wshape, Fy, E):
        d = float(Wshape['d'])
        tw = float(Wshape['tw'])
        Vn = 0.6*Fy*d*tw
        if float(Wshape['h/tw']) > 2.24*math.sqrt(float(E)/Fy):
                return [Vn/1.67,0.9*Vn]
        else:
                return [Vn/1.5,Vn]

def MaximumTotalUniformLoad (Wshape, L, Fy, E):
	[MpOmega,phiMp] = FlexuralStrength (Wshape, 0.0, Fy, E)
	wLOmega = MpOmega*8.0/L
	phiwL = phiMp*8.0/L
	[VnOmega,phiVn] = ShearStrength(Wshape, Fy, E)
	return [min(wLOmega,2*VnOmega),min(phiwL,2*phiVn)]

def SlenderCompression (Wshape, Fy, E):
        bftf = float(Wshape['bf/2tf'])
        htw = float(Wshape['h/tw'])
        if bftf > 0.56*math.sqrt(float(E)/Fy) or htw > 1.49*math.sqrt(float(E)/Fy):
                return True
        else:
                return False

def AxialCompressiveStress (KLr, Fy, E):
        Fe = (math.pi)**2*E/KLr**2
        if KLr <= 4.71*math.sqrt(float(E)/Fy):
                Fcr = 0.658**(Fy/Fe)*Fy
        else:
                Fcr = 0.877*Fe
        return [Fcr/1.67,0.9*Fcr]

def AxialCompressionStrength (shape, KLx, KLy, Fy, E):
	Ag = float(shape['A'])
	rx = float(shape['rx'])
	ry = float(shape['ry'])
	KLry = math.ceil(KLy)/ry
	[FcrOmega,phiFcr] = AxialCompressiveStress(KLry, Fy, E)
	KLryeq = math.ceil(KLx/(rx/ry))/ry
	[asd,lrfd] = AxialCompressiveStress(KLryeq, Fy, E)
	if asd < FcrOmega:
		FcrOmega = asd
		phiFcr = lrfd
	return [FcrOmega*Ag,phiFcr*Ag]

def LightestKSeries(wu, L):
        if L == 30.0:
                if wu < 241:
                        return "None"
                if wu < 270:
                        return "16K2"
                if wu < 324:
                        return "16K3"
                if wu < 366:
                        return "16K4"
                if wu < 399:
                        return "16K5"

        return "None"

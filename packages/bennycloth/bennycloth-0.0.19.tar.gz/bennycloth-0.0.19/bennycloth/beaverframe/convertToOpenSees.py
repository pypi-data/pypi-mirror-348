def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def ConvertToOpenSees(infile, outfile, json=None):
    """
    Convert a beaverFrame input file to an OpenSeesPy script

    infile - name of beaverFrame input file to read
    outfile - name of OpenSeesPy script to write
    """
    
    inputt = open(infile,'r')
    output = open(outfile,'w')
    output2 = open('bennyFrame.py','w')

    output.write('import openseespy.opensees as ops\n')
    output.write('import numpy as np\n')
    output.write('import json\n')
    output.write('ops.wipe()\n')

    Nloadcase = 0

    nodeTag = 1
    matTag = 1
    secTag = 1
    transfTag = 1
    eleTag = 1
    patternTag = 1

    springTag = 1

    for line in inputt:

        info = line.split()
        if len(info) < 1:
            continue

        if info[0] == 'NDM':
            ndm = int(info[1])
            if ndm < 1 or ndm > 3:
                print(f'ERROR in NDM={ndm}')
            ndf = 6
            if ndm == 2:
                ndf = 3
            output.write(f"ops.model('basic','-ndm',{ndm},'-ndf',{ndf})\n")

        if info[0] == 'NODES':
            Nnode = int(info[1])
            output2.write(f'NODES = np.zeros(({Nnode},{ndm}))\n')
            output2.write(f'SUPPORTS = np.zeros(({Nnode},{ndf}))\n')
            output2.write(f'NODALLOADS = np.zeros(({Nnode},{ndf}))\n')
            output2.write(f'SUPPORTDISPS = np.zeros(({Nnode},{ndf}))\n')                
            for i in range(Nnode):
                nodeInfo = inputt.readline().split()

                tag = int(nodeInfo[0])
                if ndm == 1:
                    X = float(nodeInfo[1])
                    output.write(f"ops.node({tag},{X})\n")
                    DX = int(nodeInfo[2]) if isint(nodeInfo[2]) else 0;
                    output.write(f"ops.fix({tag},{DX})\n")            
                if ndm == 2:
                    X = float(nodeInfo[1])
                    Y = float(nodeInfo[2])
                    output.write(f"ops.node({tag},{X},{Y})\n")            
                    DX = int(nodeInfo[3]) if isint(nodeInfo[3]) else 0;
                    DY = int(nodeInfo[4]) if isint(nodeInfo[4]) else 0;
                    RZ = int(nodeInfo[5]) if isint(nodeInfo[5]) else 0;                    
                    output.write(f"ops.fix({tag},{DX},{DY},{RZ})\n")                        
                if ndm == 3:
                    X = float(nodeInfo[1])
                    Y = float(nodeInfo[2])
                    Z = float(nodeInfo[3])
                    output.write(f"ops.node({tag},{X},{Y},{Z})\n")
                    output2.write(f'NODES[{tag-1},:]=[{X},{Y},{Z}]\n')

                    DX = float(nodeInfo[4])
                    DY = float(nodeInfo[5])
                    DZ = float(nodeInfo[6])
                    RX = float(nodeInfo[7])
                    RY = float(nodeInfo[8])
                    RZ = float(nodeInfo[9])
                    isSupport = False
                    flexibleSupport = False
                    supportDOFs = []
                    for idof,dof in enumerate([DX,DY,DZ,RX,RY,RZ]):
                        if dof < 0:
                            isSupport = True
                            supportDOFs.append(1)
                        if dof == 0:
                            supportDOFs.append(0)
                        if dof > 0:
                            isSupport = True
                            flexibleSupport = True
                            output.write(f"ops.uniaxialMaterial('Elastic',{springTag},{dof})\n")
                            supportDOFs.append(-springTag)
                            springTag += 1
                    if isSupport and not flexibleSupport:
                        output.write(f"ops.fix({tag}")
                        for dof in supportDOFs:
                            output.write(f",{dof}")
                        output.write(")\n")
                        output2.write(f'SUPPORTS[{tag-1},:]=[{DX},{DY},{DZ},{RX},{RY},{RZ}]\n')
                    if flexibleSupport:
                        output.write(f"ops.node({-tag},{X},{Y},{Z})\n")
                        output.write(f"ops.fix({-tag},1,1,1,1,1,1)\n")
                        #output.write(f"ops.element('zeroLength',{-tag},{-tag},{tag},'-mats','-dirs')\n")
                        
        if info[0] == 'MATERIALS':
            Nmat = int(info[1])
            matData = [0]*(2*Nmat)
            for i in range(Nmat):
                matInfo = inputt.readline().split()
                tag = int(matInfo[0])
                E = float(matInfo[1])
                G = float(matInfo[2])
                matData[2*i    ] = E
                matData[2*i + 1] = G

        if info[0] == 'FORCEDEFS':
            Nmat = int(info[1])
            for i in range(Nmat):
                matInfo = inputt.readline().split()
                tag = int(matInfo[0])
                type = matInfo[1]
                if type == 'Elastic':
                    k = float(matInfo[2])
                    output.write(f"ops.uniaxialMaterial('Elastic',{tag},{k})\n")
                if type == 'Elastic2':
                    kp = float(matInfo[2])
                    kn = float(matInfo[3])
                    output.write(f"ops.uniaxialMaterial('Elastic',{tag},{kp},0,{kn})\n")

        if info[0] == 'SECTIONS':
            Nsec = int(info[1])
            output2.write(f'SECTIONS = np.zeros(({Nsec},6))\n')                
            secData = [0]*(6*Nsec)
            for i in range(Nsec):
                secInfo = inputt.readline().split()
                tag = int(secInfo[0])
                type = secInfo[1]
                E = float(secInfo[2])
                nu = float(secInfo[3])
                G = 0.5*E/(1+nu)
                A   = float(secInfo[4])
                Iz  = float(secInfo[5])
                Avy = float(secInfo[6])
                secData[6*i    ] = A
                secData[6*i + 1] = Iz
                secData[6*i + 2] = Avy
                if ndm == 2:
                    output2.write(f'SECTIONS[{tag-1},:]=[{E},{A},{Iz}]\n')
                    if Avy <= 0.0:
                        output.write(f"ops.section('Elastic',{tag},{E},{A},{Iz})\n")
                    else:
                        output.write(f"ops.section('Elastic',{tag},{E},{A},{Iz},{G},{Avy/A})\n")
                if ndm == 3:
                    Iy  = float(secInfo[7])
                    Avz = float(secInfo[8])
                    J   = float(secInfo[9])
                    secData[6*i + 3] = Iy
                    secData[6*i + 4] = Avz
                    secData[6*i + 5] = J
                    output2.write(f'SECTIONS[{tag-1},:]=[{E},{A},{Iz},{Iy},{G},{J}]\n')
                    if Avy <= 0.0 or Avz <= 0.0:
                        output.write(f"ops.section('Elastic',{tag},{E},{A},{Iz},{Iy},{G},{J})\n")
                    else:
                        output.write(f"ops.section('Elastic',{tag},{E},{A},{Iz},{Iy},{G},{J},{Avy/A},{Avz/A})\n")

        if info[0] == 'TRANSFORMATIONS':
            Ntransf = int(info[1])
            transfData = [0]*(4*Ntransf)
            for i in range(Ntransf):
                transfInfo = inputt.readline().split()
                tag = int(transfInfo[0])
                if ndm == 2:
                    transfData[4*i + 3] = float(transfInfo[1])                                                
                if ndm == 3:
                    transfData[4*i    ] = float(transfInfo[1])
                    transfData[4*i + 1] = float(transfInfo[2])
                    transfData[4*i + 2] = float(transfInfo[3])
                    transfData[4*i + 3] = float(transfInfo[4])                                
                
        if info[0] == 'ELEMENTS':
            Nele = int(info[1])
            output2.write(f'ELEMS = np.zeros(({Nele},6))\n')
            output2.write(f'MEMBERLOADS = np.zeros(({Nele},3))\n')                        
            for i in range(Nele):
                eleInfo = inputt.readline().split()
                tag = int(eleInfo[0])
                type = eleInfo[1]
                if type == 'Spring':
                    ndI = int(eleInfo[2])
                    ndJ = int(eleInfo[3])
                    x = [1,0,0]
                    x[0] = float(eleInfo[4])
                    x[1] = float(eleInfo[5])
                    x[2] = 0
                    iarg = 6
                    yp = [0,1,0]
                    if ndm == 3:
                        x[2] = float(eleInfo[6])
                        yp[0] = float(eleInfo[7])
                        yp[1] = float(eleInfo[8])
                        yp[2] = float(eleInfo[9])
                        iarg += 4
                    matTag = int(eleInfo[iarg])
                    dir = int(eleInfo[iarg+1])
                    if ndm == 2:
                        output.write(f"ops.element('zeroLength',{tag},{ndI},{ndJ},'-mat',{matTag},'-dir',{dir},'-orient',{x[0]},{x[1]},{x[2]})\n")
                    if ndm == 3:
                        output.write(f"ops.element('zeroLength',{tag},{ndI},{ndJ},'-mat',{matTag},'-dir',{dir},'-orient',{x[0]},{x[1]},{x[2]},{yp[0]},{yp[1]},{yp[2]})\n")
                       
                if type == 'Frame':      
                    ndI = int(eleInfo[2])
                    ndJ = int(eleInfo[3]) 
                    iarg = 4
                    if ndm == 3:                 
                        output.write(f'x = np.array(ops.nodeCoord({ndJ})) - np.array(ops.nodeCoord({ndI}))\n')
                        yx = float(eleInfo[4])
                        yy = float(eleInfo[5])
                        yz = float(eleInfo[6])
                        output2.write(f'ELEMS[{tag-1},:]=[{ndI},{ndJ},{tag-1},{yx},{yy},{yz}]\n')
                        output.write(f'yp = np.array([{yx},{yy},{yz}])\n')
                        output.write(f'z = np.cross(x,yp)\n')
                        #output.write(f'y = np.cross(z,x)\n')
                        #output.write(f'z = np.cross(x,y)\n')           
                        iarg = 7
                    secTag = int(eleInfo[iarg])
                    iarg += 1

                    transfType = 'Linear'
                    # Check second to last entry for P-DELTA
                    if float(eleInfo[-2]) > 0.0:
                        transfType = 'PDelta'
                    if ndm == 2:
                        output.write(f"ops.geomTransf('{transfType}',{tag})\n")
                    else:
                        output.write(f"ops.geomTransf('{transfType}',{tag},*z)\n")

                    kzI = float(eleInfo[iarg])
                    kzJ = float(eleInfo[iarg+1])
                    kyI = -1
                    kyJ = -1
                    iarg += 2
                    if ndm == 3:
                        kyI = float(eleInfo[iarg])
                        kyJ = float(eleInfo[iarg+1])
                        iarg += 2

                    # An element with rigid,infinitesimal joints
                    if kzI < 0 and kzJ < 0 and kyI < 0 and kyJ < 0:
                        output.write(f"ops.beamIntegration('NewtonCotes',{tag},{secTag},7)\n")
                        output.write(f"ops.element('forceBeamColumn',{tag},{ndI},{ndJ},{tag},{tag})\n")
                        continue

                    relz = 0
                    if kzI == 0:
                        relz = 1
                    if kzJ == 0:
                        relz = 2
                    if kzI == 0 and kzJ == 0:
                        relz = 3

                    rely = 0
                    if kyI == 0:
                        rely = 1
                    if kyJ == 0:
                        rely = 2
                    if kyI == 0 and kyJ == 0:
                        rely = 3

                    # An element with moment releases at one or both ends
                    if relz > 0 or rely > 0:
                        if ndm == 2:
                            output.write(f"ops.element('elasticBeamColumn',{tag},{ndI},{ndJ},{secTag},{tag},'-release',{relz})\n")
                        if ndm == 3:
                            output.write(f"ops.element('elasticBeamColumn',{tag},{ndI},{ndJ},{secTag},{tag},'-releasez',{relz},'-releasey',{rely})\n")
                        continue

                    output.write(f"ops.uniaxialMaterial('Elastic',{springTag},{kzI})\n")
                    springTag += 1
                    output.write(f"ops.uniaxialMaterial('Elastic',{springTag},{kzJ})\n")
                    springTag += 1
                    if kyI < 0.0:
                        kyI = 1e4*kzI
                    output.write(f"ops.uniaxialMaterial('Elastic',{springTag},{kyI})\n")
                    springTag += 1
                    if kyJ < 0.0:
                        kyJ = 1e4*kzJ            
                    output.write(f"ops.uniaxialMaterial('Elastic',{springTag},{kyJ})\n")
                    springTag += 1
                    
                    secIndex = secTag - 1
                    A   = secData[6*secIndex    ]
                    Iz  = secData[6*secIndex + 1]
                    Avy = secData[6*secIndex + 2]
                    Iy  = secData[6*secIndex + 3]
                    Avz = secData[6*secIndex + 4]
                    J   = secData[6*secIndex + 5]

                    # An element with rotational springs at both ends
                    if ndm == 2:
                        output.write(f"ops.element('componentElement',{tag},{ndI},{ndJ},{A},{E},{Iz},{tag},{springTag-4},{springTag-3})\n")
                    if ndm == 3:
                        output.write(f"ops.element('componentElement',{tag},{ndI},{ndJ},{A},{E},{G},{J},{Iy},{Iz},{tag},{springTag-4},{springTag-3},{springTag-2},{springTag-1})\n")


        if info[0] == 'LOADCASES':
            Nloadcase += 1
            output.write("ops.constraints('Transformation')\n")
            output.write("ops.analysis('Static')\n")
            output.write("ops.timeSeries('Constant',1)\n")        
            output.write("output = open('beaverFrame.out','w')\n")
                
        if info[0] == 'LOADCASE':
            tag = int(info[1])
            output.write(f"ops.pattern('Plain',{tag},1)\n")

            # Support displacements
            sdInfo = inputt.readline().split()
            Nsupportdisp = int(sdInfo[1])
            for i in range(Nsupportdisp):
                sdInfo = inputt.readline().split()
                nd = int(sdInfo[0])
                D = [0]*ndf
                for j in range(ndf):
                    D[j] = float(sdInfo[j+1])
                output.write(f'ops.sp({nd},*{D})\n')            

            # Point loads
            plInfo = inputt.readline().split()
            Npointload = int(plInfo[1])
            for i in range(Npointload):
                plInfo = inputt.readline().split()
                nd = int(plInfo[0])
                P = [0]*ndf
                for j in range(ndf):
                    P[j] = float(plInfo[j+1])
                output.write(f'ops.load({nd},*{P})\n')

            # Member loads
            mlInfo = inputt.readline().split()
            Nmemberload = int(mlInfo[1])
            for i in range(Nmemberload):
                mlInfo = inputt.readline().split()
                ele = int(mlInfo[0])
                if ndm == 2:
                    pass
                if ndm == 3:
                    wX = float(mlInfo[1])
                    wY = float(mlInfo[2])
                    wZ = float(mlInfo[3])
                    output.write(f"x = ops.eleResponse({ele},'xaxis')\n")
                    output.write(f"y = ops.eleResponse({ele},'yaxis')\n")
                    output.write(f"z = ops.eleResponse({ele},'zaxis')\n")                
                    output.write(f"wx = np.dot(x,[{wX},{wY},{wZ}])\n")
                    output.write(f"wy = np.dot(y,[{wX},{wY},{wZ}])\n")
                    output.write(f"wz = np.dot(z,[{wX},{wY},{wZ}])\n")                
                    output.write(f"ops.eleLoad('-ele',{ele},'-type','beamUniform',wy,wz,wx)\n")

            # First clear out old mass
            output.write(f'for nd in ops.getNodeTags():\n')
            P = [0]*ndf
            output.write(f'\tops.mass(nd,*{P})\n')

            # Member masses
            mmInfo = inputt.readline().split()
            Nmembermass = int(mmInfo[1])
            for i in range(Nmembermass):
                mmInfo = inputt.readline().split()
                ele = int(mmInfo[0])
                output.write(f"ndI,ndJ = ops.eleNodes({ele})\n")
                output.write(f"XYZI = ops.nodeCoord(ndI)\n")
                output.write(f"XYZJ = ops.nodeCoord(ndJ)\n")
                output.write(f"Lele = np.linalg.norm(np.subtract(XYZJ,XYZI))\n")
                mX = float(mmInfo[1])
                mY = float(mmInfo[2])
                mZ = 0
                if ndm == 2:
                    mZ = mY
                if ndm == 3:
                    mZ = float(mmInfo[3])
                P = [0]*ndf
                for j in range(ndm):
                    P[j] = 0.5*mZ
                output.write(f"mass = ops.nodeMass(ndI)\n")
                output.write(f"mass2 = np.multiply({P},Lele)\n")
                output.write(f"ops.mass(ndI,*(np.add(mass,mass2)))\n")
                output.write(f"ops.mass(ndJ,*(np.add(mass,mass2)))\n")                
                    
            # Point masses
            pmInfo = inputt.readline().split()
            Npointmass = int(pmInfo[1])
            for i in range(Npointmass):
                pmInfo = inputt.readline().split()
                nd = int(pmInfo[0])
                P = [0]*ndf
                for j in range(ndf):
                    P[j] = float(pmInfo[j+1])
                output.write(f'ops.mass({nd},*{P})\n')

            output.write('ops.analyze(1)\n')
            output.write('ops.reactions()\n')
            output.write(f"ops.remove('loadPattern',{tag})\n")

            output.write(f"output.write('LOAD CASE {tag}\\n')\n")

            if json is not None:
                output.write(f'ndm={ndm}\n')
                output.write(f'ndf={ndf}\n')        
                output.write(f'''
nodeData = {{}}
nodeData[{tag}] = {{}}
for nd in ops.getNodeTags():
    nodeData[{tag}][nd] = {{}}
    nodeData[{tag}][nd]['disp'] = ops.nodeDisp(nd)
    nodeData[{tag}][nd]['force'] = ops.nodeReaction(nd)
''')
                output.write(f'''
with open('{json}','w') as outjson:
    json.dump(nodeData,outjson,indent=2)
''')
                output.write('\n')

                output.write("output.write('\\n')\n")
            
    output.write('output.close()\n')
    output.close()
    output2.close()
    inputt.close()

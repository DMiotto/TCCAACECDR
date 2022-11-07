import math
from re import T
import numpy as npy
log = npy.log

# Informações dos dados de entrada

def Reltrans(i):
    if i != 0:
        info_reltrans = "%.2f" %i
    else:
        info_reltrans = "-"
    return info_reltrans

def Modulo(m):
    if m != 0:
        info_modulo = "%.2f" %m
    else:
        info_modulo = "-"
    return info_modulo

def Rotacao(n):
    if n != 0:
        info_rpm = "%.2f" %n
    else:
        info_rpm = "-"
    return info_rpm

def DentesPinhao(Np):
    if Np != 0:
        info_dentespinhao = "%.2f" %Np
    else:
        info_dentespinhao = "-"
    return info_dentespinhao

def TVida(L):
    if L != 0:
        info_tvida = "%.2f" %L
    else:
        info_tvida = "-"
    return info_tvida

def Torque(T):
    if T != 0:
        info_torque = "%.2f" %T
    else:
        info_torque = "-"
    return info_torque

def Potencia(P):
    if P != 0:
        info_potencia = "%.2f" %P
    else:
        info_potencia = "-"
    return info_potencia

def FTangencial(Wt):
    if Wt != 0:
        info_ftangencial = "%.2f" %Wt
    else:
        info_ftangencial = "-"
    return info_ftangencial

def Material(Mat):
    if Mat == 1:
        info_Mat = "Aço x Aço"
    elif Mat == 2:
        info_Mat = "Ferro Fundido x Ferro Fundido"
    else:
        info_Mat = "Dados Aplicados Manualmente"
    return info_Mat

def FonteAlimentacao(FA):
    if FA == 1:
        info_FA = "Uniforme"
    elif FA == 2:
        info_FA = "Choque Leve"
    else:
        info_FA = "Choque Moderado"
    return info_FA

def TipoMaquina(TM):
    if TM == 1:
        info_TM = "Uniforme"
    elif TM == 2:
        info_TM = "Choque Leve"
    elif TM == 3:
        info_TM = "Choque Moderado"
    else:
        info_TM = "Choque Pesado"
    return info_TM

def ValorAv(Av):
    if Av != 0:
        info_av = "%.2f" %Av
    else:
        info_av = "-"
    return info_av

def FormatoFaceDente(Khmc):
    if Khmc == 1:
        info_khmc = "Dente sem coroamento"
    elif Khmc == 2:
        info_khmc = "Dente coroado ou com correção de desvio"
    else:
        info_khmc = "Nulo"
    return info_khmc

def FatoCargaDeflexao(Khpm):
    if Khpm == 1:
        info_khpm = "S1/S < 0.175"
    elif Khpm == 2:
        info_khpm = "S1/S <= 0.175"
    else:
        info_khpm = "Nulo"
    return info_khpm

def FatorAlinhamento(FAl):
    if FAl == 1:
        info_fal = "Engrenagem aberta"
    elif FAl == 2:
        info_fal = "Engrenagem fechada/comercial"
    elif FAl == 3:
        info_fal = "Engrenagem fechada de precisão"
    elif FAl == 4:
        info_fal = "Engrenagem fechada de alta precisão"
    else:
        info_fal = "Nulo"
    return info_fal

def FatorAjuste(Khe):
    if Khe == 1:
        info_khe = "Engrenagem ajustada na montagem"
    elif Khe == 2:
        info_khe = "Compatibilidade da engrenagem e melhorada lapidando"
    elif Khe == 3:
        info_khe = "Todos os outros casos"
    else:
        info_khe = "Nulo"
    return info_khe

def Confiabilidade(R):
    if R == 1:
        info_conf = "50%"
    elif R == 2:
        info_conf = "90%"
    elif R == 4:
        info_conf = "99%"
    elif R == 5:
        info_conf = "99.9%"
    elif R == 6:
        info_conf = "99.99%"
    else:
        info_conf = "Nulo"
    return info_conf

def Dureza(HBt):
    if HBt != 0:
        info_dureza = "%.2f" %HBt
    else:
        info_dureza = "-"
    return info_dureza

def Entrada(a):
    if a == 1:
        info_a = "Torque"
    elif a == 2:
        info_a = "Potência"
    else:
        info_a = "Força Tangencial"
    return info_a


q = 1
Zw = 1
Yθ = 1
Zr = 1
Sh = 1.0
θ = 20
# Início do código

# Contas Background

def DentesCoroa(i, Np):
    Ng = i*Np
    return Ng

def RotacaoP(n):
    np = n
    return int(np)

def RotacaoC(np, i):
	ng = np/i 
	return ng

def Diametropp(m, Np):
	Dpp = m*Np
	return int(Dpp)

def Diametropc(m, Ng):
	Dpg = m*Ng
	return Dpg

def Raiopp(Dpp):
	rpp = Dpp/2
	return rpp

def Raiopc(Dpg):
	rpg = Dpg/2
	return rpg

def LargFace(m):
	b = m*12
	return b

def ValP(Dpp, np):
	Vp = math.pi*Dpp*1e-3*np/60
	return Vp

def FatorDinamico(Dpp,n, Av):    
    V = math.pi*(Dpp/1000)*(n/60)
    B = 0.25 * (float(Av) - 5.0) ** (2 / 3)
    C = 3.5637 + 3.9914 * (1 - B)
    Kv = (C / (C + math.sqrt(V))) ** (-B)
    return Kv

def FatorTamanho(m):
    a = [5, 6, 8, 12, 20]
    b = [1, 1.05, 1.15, 1.25, 1.40]

    if m <= 5:
        Ks = 1
    elif m > 20:
        Ks = 1.50
    else:
        Ks = npy.interp(m, a, b)
    return Ks

def fatorkhpf(b, Dpp):
    if b <= 25:
        Khpf = -0.025 + (b / (10 * Dpp))
    elif 25 < b <= 432:
        Khpf = (b / (10 * Dpp)) - 0.0375 + (0.000492 * b)
    else:
        Khpf = (b / (10 * Dpp)) - 0.1109 + 0.000815 * b - 0.000000353 * b ** 2
    return Khpf

def FatorAlinhamento(FAl, b):
    if FAl == 1:
        A = 2.47e-1
        B = 0.657e-3
        C = -1.186e-7
    elif FAl == 2:
        A = 1.27e-1
        B = 0.622e-3
        C = -1.69e-7
    elif FAl == 3:
        A = 0.675e-1
        B = 0.504e-3
        C = -1.44e-7
    elif FAl == 4:
        A = 0.380e-1
        B = 0.402e-3
        C = -1.27e-7
    return A + (B*b) + (C*b)**2

def FatorCarga(Khmc, Khpm, Khma, Khe, Khpf):
    Kh = 1 + float(Khmc)*(float(Khpf)*float(Khpm) + float(Khma)*float(Khe))
    return Kh

def FatorGeometrico(Np,θ,i):
    C1 = (Np*math.sin(math.radians(θ)))/2
    C2 = C1*i
    C3 = (math.pi)*(math.cos(math.radians(θ)))
    C4 = 0.5*(math.sqrt((Np+2)**2 - (Np*math.cos(math.radians(θ)))**2) - math.sqrt(Np**2 - (Np*math.cos(math.radians(θ)))**2))
    Cc = ((math.cos(math.radians(θ))*math.sin(math.radians(θ)))/2)*(i/(i+1))
    Cx = ((C1-C3+C4)*(C2+C3-C4))/(C1*C2)
    Zi = Cc*Cx
    return Zi

def sigmaH(Wt, Ko, Kv, Ks, Kh, Zr, Dpp, b, Zi, Ze):
    σH = Ze * math.sqrt(Wt * Ko * Kv * Ks * Kh * Zr / (Dpp * b * Zi))
    return σH

def FatorCiclagem(L,n,q):
    nl = 60*L*n*q
    Zn = 1.4488*(nl**(-0.023))
    return Zn

def FatorConfiabilidade(R):
    if 0.5 <= R < 0.99:
        Yz = 0.658-0.0759*math.log(1-R)
    elif 0.99 <= R <= 0.9999:
        Yz = 0.5-0.109*math.log(1-R)
    return Yz

def σhp12(σH, Sh, Yθ, Yz, Zn, Zw):
    σhp = (σH*Sh*Yθ*Yz)/(Zn*Zw)
    return σhp

def Brinnel(σhp):
    HB = (σhp-200)/2.22
    return HB

def Brinnelt(HBt):
    σhpf = 2.22*HBt + 200
    return σhpf

def fatordeseguranca(σhp, Zn, Zw, σH, Yθ, Yz):
    Shr = (σhp*Zn*Zw)/(σH*Yθ*Yz)
    return Shr

def resultado(σhp, Zn, Zw, σH, Yθ, Yz, Wt, Ko, Kv, Ks, Kh, Zr, Dpp, b, Zi, Ze):
    rShr = fatordeseguranca(σhp, Zn, Zw, σH, Yθ, Yz)
    rσH = sigmaH(Wt, Ko, Kv, Ks, Kh, Zr, Dpp, b, Zi, Ze)
    resposta = "Sigma H de %.2f e fator de segurança %.2f" % (rσH, rShr)
    return resposta
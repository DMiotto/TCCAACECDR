from re import A
from django.http import response

from django.shortcuts import render, HttpResponse
from .functions import *

def sobrepage(request):
    return render(request, template_name='sobre.html')

def indexpage(request):
    return render(request, template_name='index.html')

def results(request): 
    try:   
        i = request.POST['p_transmissao']
        m = request.POST['p_modulo']
        n = request.POST['p_rpm']
        Np = request.POST['dentes_pinhao']
        L = request.POST['t_vida']
        T = request.POST['p_torque']
        P = request.POST['p_potencia']
        Wt = request.POST['p_forca_tangencial']
        Mat = request.POST['material']
        Ep = request.POST['E_p']
        Eg = request.POST['E_g']
        v1 = request.POST['poison_p']
        v2 = request.POST['poison_c']
        FA = request.POST['fontealimentacao']
        TM = request.POST['tipomaquina']
        Av = request.POST['carga']
        Khmc_z = request.POST['khmc']
        Khpm_z = request.POST['khpm']
        FAl = request.POST['fatoralinhamento']
        Khe_z = request.POST['khe']
        Rr = request.POST['confiabilidade']
        HBt = request.POST['dureza']
        a = request.POST['dado_entrada1']

        i = float(i)
        n = float(n)
        Np = int(Np)
        m = int(m)
        L = float(L)
        T = float(T)
        P = float(P)
        Wt = float(Wt)
        Mat = int(Mat)
        FA = int(FA)
        TM = int(TM)
        Av = float(Av)
        Khmc_z = int(Khmc_z)
        Khpm_z = int(Khpm_z)
        FAl = int(FAl)
        Khe_z = int(Khe_z)
        Rr = int(Rr)  
        Ep = float(Ep)
        Eg = float(Eg)
        v1 = float(v1)
        v2 = float(v2)
        HBt = float(HBt)
        a = int(a)

        # Cálculos básicos
        np1 = RotacaoP(n)
        Dpp1 = Diametropp(m, Np)
        rpp1 = Raiopp(Dpp1)
        Vp1 = ValP(Dpp1, np1)
        Kv1 = FatorDinamico(Dpp1,n, Av)
        Ks1 = FatorTamanho(m)
        

        #Escolha de Entrada
    
        if a == 1:
            Wt = T/(rpp1*1e-3)
            P = Wt*Vp1
        elif a == 2:
            Wt = P/Vp1
            T = Wt*rpp1*1e-3
        else:
            Tp = Wt*rpp1*1e-3
            P = Wt*Vp1
                
        if Mat == 1:
            Ze = 191.00
        elif Mat == 2:
            Ze = 163.00
        else:
            Ze = math.sqrt(1/(math.pi*(((1 - v1**2)/Ep) + ((1 - v2**2)/Eg))))

        #Fa e Tm

        if FA == 1 and TM == 1:
            Ko = 1.0
        elif FA == 1 and TM == 2:
            Ko = 1.25
        elif FA == 1 and TM == 3:
            Ko = 1.50
        elif FA == 1 and TM == 4:
            Ko = 1.75
        elif FA == 2 and TM == 1:
            Ko = 1.20
        elif FA == 2 and TM == 2:
            Ko = 1.40
        elif FA == 2 and TM == 3:
            Ko = 1.75
        elif FA == 2 and TM == 4:
            Ko = 2.25
        elif FA == 3 and TM == 1:
            Ko = 1.30
        elif FA == 3 and TM == 2:
            Ko = 1.70
        elif FA == 3 and TM == 3:
            Ko = 2.00
        else:
            Ko = 2.75
        
        #Khmc
        if Khmc_z == 1:
            Khmc = 1.0
        else:
            Khmc = 0.8

        #Khpm
        if Khpm_z == 1:
            Khpm = 1.0
        else:
            Khpm = 1.1

        #Khe
        if Khe_z == 1:
            Khe = 0.8
        elif Khe_z == 2:
            Khe = 0.8
        else:
            Khe = 1.0

        #R
        if Rr == 1:
            R = 0.50
        elif Rr == 2:
            R = 0.90
        elif Rr == 3:
            R = 0.99
        elif Rr == 4:
            R = 0.999
        elif Rr == 5:
            R = 0.9999
        
        # Obtendo informações dos dados de entrada

        info_reltrans1 = Reltrans(i)
        info_modulo1 = Modulo(m)
        info_rpm1 = Rotacao(n)
        info_dentespinhao1 = DentesPinhao(Np)
        info_tvida1 = TVida(L)
        info_torque1 = Torque(T)
        info_potencia1 = Potencia(P)
        info_ftangencial1 = FTangencial(Wt)
        info_FA1 = FonteAlimentacao(FA)
        info_TM1 = TipoMaquina(TM)
        info_av1 = ValorAv(Av)
        info_khmc1 = FormatoFaceDente(Khmc)
        info_khpm1 = FatoCargaDeflexao(Khpm)
        info_khe1 = FatorAjuste(Khe)
        info_conf1 = Confiabilidade(R)
        info_dureza1 = Dureza(HBt)
        info_a1 = Entrada(a)
        info_material1 = Material(Mat)

        #Cálculos básicos

        Zr1 = Zr
        θ1 = θ 
        Zi1 = FatorGeometrico(Np,θ1,i)
        b1 = LargFace(m)
        Khpf1 = fatorkhpf(b1, Dpp1)
        Khma1 = FatorAlinhamento(FAl, b1)
        Sh1 = Sh
        Yz1 = FatorConfiabilidade(R)
        Zn1 = FatorCiclagem(L,n,q)
        Kh1 = FatorCarga(Khmc, Khpm, Khma1, Khe, Khpf1)
        σH1 = sigmaH(Wt, Ko, Kv1, Ks1, Kh1, Zr1, Dpp1, b1, Zi1, Ze)
        σhp1 = σhp12(σH1, Sh1, Yθ, Yz1, Zn1, Zw)
        σhpf1 = Brinnelt(HBt)
        HB1 = Brinnel(σhp1)
        

        # Resultado final

        result = resultado(σhp1, Zn1, Zw, σH1, Yθ, Yz1, Wt, Ko, Kv1, Ks1, Kh1, Zr, Dpp1, b1, Zi1, Ze)
        return render(request, "results.html", {"info_reltrans1": info_reltrans1, "info_modulo1": info_modulo1, "info_material1": info_material1, "info_rpm1": info_rpm1, "info_Ze": Ze , "info_Kh": Kh1, "info_Khma": Khma1, "info_Khpf": Khpf1, "info_Vp": Vp1, "info_Kv": Kv1, "info_Ks": Ks1, "info_Zi": Zi1, "info_σhpf": σhpf1, "info_HB": HB1, "info_Zn": Zn1, "info_σhp": σhp1, "result": result})


    # Tratamento de exceção

    except:
        return render(request, "error.html")
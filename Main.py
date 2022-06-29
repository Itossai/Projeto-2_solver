from Formula import *
from semantics import *
from Functions import *
import csv 


with open("column_bin_3a_3p.csv", "r") as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=",")
    atributos=[]
    patologia=[]
    pacientes=[]
    for i, linha in enumerate(arquivo_csv):
        if(i==0):
            atributos= linha
            patologia.append(linha.pop())
        else:
            patologia.append(linha.pop())
            pacientes.append(linha)
patologia.remove("P")

def restricao_2 (atributos,m):
    restricao_2=[]
    restricao_aux=[]
    for i in range(m):
        for atr in range(len(atributos)):
            restricao_aux.append(Not(Atom(str(atributos[atr])+'_'+str(i+1)+'_s')))
        restricao_2.append(or_all(restricao_aux.copy()))
        restricao_aux=[]
    return and_all(restricao_2.copy())

def restricao_1 (atributos,m):
    restricao1=[]

    classificacao=["p","n","s"]
    for i in range(m):
        for atr in range(len(atributos)):
            restricao_aux2=[]
            for c in range(len(classificacao)):
                restricao_aux=[]
                for l in range(len(classificacao)):
                    if l==c:
                        restricao_aux.append(Atom(atributos[atr]+"_"+str(i+1)+"_"+str(classificacao[l])))
                    else:
                        restricao_aux.append(Not(Atom(atributos[atr]+"_"+str(i+1)+"_"+str(classificacao[l]))))
                restricao_aux2.append(and_all(restricao_aux.copy()))
            restricao1.append(or_all(restricao_aux2.copy()))
    return and_all(restricao1.copy())

def restricao_5(patologia,m):
    restricao_5=[]
    restricao_aux=[]
    for p in range(len(patologia)):
        if(patologia[p]=='1'):
            for i in range(m):
                restricao_aux.append(Atom('C'+str(i+1)+'_'+str(p+1)))
            restricao_5.append(or_all(restricao_aux.copy()))
            restricao_aux=[]
    return and_all(restricao_5.copy())

def restricao_4(atributos,patologia,pacientes,m):
    restricao_4=[]
    restr=[]
    for p in range(len(patologia)):
        if patologia[p]=="1":
            aux=pacientes[p]
            for i in range(m):
                for a in range(len(atributos)):
                    if aux[a]=="0":
                        restr.append(Implies(Atom(str(atributos[a])+'_'+str(i+1)+'_p'),Not(Atom("C"+str(i+1)+"_"+str(p+1)))))
                    else:
                        restr.append(Implies(Atom(str(atributos[a])+'_'+str(i+1)+'_n'),Not(Atom("C"+str(i+1)+"_"+str(p+1)))))
                restricao_4.append(and_all(restr.copy()))
                restr=[]
    return and_all(restricao_4.copy())

def restricao_3(atributos,patologia,pacientes,m):
    restr=[]
    restricao3=[]
    for p in range(len(patologia)):
        if patologia[p]=="0":
            aux=pacientes[p]
            for i in range(m):
                for a in range(len(atributos)):
                    if aux[a]=="0":
                        restr.append(Atom(atributos[a]+'_'+str(i+1)+'_p'))
                    else:
                        restr.append(Atom(atributos[a]+"_"+str(i+1)+"_n"))
                restricao3.append(or_all(restr.copy()))
                restr=[]   
    return and_all(restricao3.copy()) 
m=1
final_formula=And(
                And(
                And(restricao_1(atributos,m),
                    restricao_2(atributos,m)
                    ),    
                And(
                    restricao_3(atributos,patologia,pacientes,m),
                    restricao_4(atributos,patologia,pacientes,m)   
                ),    
            ),  
            restricao_5(patologia,m)
)
print(str(restricao_1(atributos,m))+"\n")
print(str(restricao_2(atributos,m))+"\n")
print(str(restricao_3(atributos,patologia,pacientes,m))+"\n")
print(str(restricao_4(atributos,patologia,pacientes,m))+"\n")
print(restricao_5(patologia,m))
valoracao=satisfiability_brute_force(final_formula)
if valoracao==False:
    print(valoracao)

if valoracao:
    for atom,interpretacao in valoracao.items():
        print(atom.name+":"+str(interpretacao))
    conjunto_regras=[]
    
    for i in range(m):
        conjunto=[]
        for a in range(len(atributos)):
                if valoracao[Atom(atributos[a]+"_"+str(i+1)+"_p")]:
                    if atributos[a] not in conjunto:
                        conjunto.append(atributos[a])
                if valoracao[Atom(atributos[a]+"_"+str(i+1)+"_n")]:
                    if "<=" in atributos[a]:
                        if atributos[a] not in conjunto:
                            atributo=atributos[a]
                            conjunto.append(atributo.replace("<=",">"))
                        else:
                            if atributos[a] not in conjunto_regras:
                                atributo=atributos[a]
                                conjunto.append(atributo.replace(">","<="))                         
        if len(conjunto)>0:
            conjunto_regras.append(conjunto)
            conjunto_regras.append(u"\u21D2"+" "+"P")
    print(conjunto_regras)
    print(" ")

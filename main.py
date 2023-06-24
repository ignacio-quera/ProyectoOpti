from gurobipy import GRB, Model, quicksum
from random import seed
import csv
import datos

seed(10)
# Generar el modelo
model = Model()
model.setParam("TimeLimit", 1800)

# Sets
T = datos.dias
E = datos.empresas
Cañerias = datos.canerias

# Parámetros
C = datos.coste_diario_arreglo
L = datos.tiempo_demora_empresa
P = datos.litros_perdidos_por_caneria 
Q = datos.presupuesto_anual
G = datos.costos_corte_agua 
H = datos.dia_caneria_rota  
gamma = datos.dias_max

# Se instancian variables de decision
U = model.addVars(Cañerias, vtype = GRB.INTEGER, name = "U_j")
W = model.addVars(Cañerias, vtype = GRB.INTEGER, name = "W_j")
F  = model.addVars(Cañerias, vtype = GRB.BINARY, name = "F_j")
R  = model.addVars(Cañerias,E,T, vtype = GRB.BINARY, name = "R_j,i,t")
Z  = model.addVars(Cañerias,E,T,vtype = GRB.BINARY, name = "Z_j,i,t")

# Llamamos a update
model.update()

# Restricciones
#El costo anual de reparacion de canerıas no puede superar el presupuesto anual Q.
model.addConstr((Q >= quicksum(R[j,i,t]*(C[i] + G[j]) for t in T for i in E for j in Cañerias)), name="R1")

# Una empresa no puede reparar más de una cañería a la vez
model.addConstrs((1 >= quicksum(R[j,i,t] for j in Cañerias) for i in E for t in T),name="R2")

# Una cañeria se repara sin interrupciones y en el tiempo exacto desde el día en que se decide comenzar a repararla
model.addConstrs((L[i,j]*Z[j,i,t] <= quicksum(R[j,i, alpha] for alpha in range(t, t+L[i,j]) if (t+L[i,j] <= 365)) for i in E for j in Cañerias for t in T), name="R3")

# Una cañería no puede estar siendo reparada por más de una empresa al mismo tiempo
model.addConstrs((1 >= quicksum(R[j,i,t] for i in E) for j in Cañerias for t in T ),name="R4") 

# La caneria j se repara a lo más una vez al año
model.addConstrs((1 >= quicksum(Z[j,i,t] for t in T) for j in Cañerias for i in E), name="R5")

#La cañería j no puede estar siendo reparada por i por más tiempo que L_i,j
model.addConstrs((quicksum(R[j,i,t] for t in T) <= L[i,j] for i in E for j in Cañerias for t in T),name="R6")

# No se puede dejar ninguna repracion incompleta a final de año
model.addConstrs((Z[j,i,t]*t+L[i,j]<=365 for i in E for j in Cañerias for t in T),name="R7")

# Definir la variable F_j
model.addConstrs((quicksum(Z[j,i,t] for i in E for t in T) == F[j] for j in Cañerias),name="R8")

# Definir W_j
model.addConstrs((W[j] >= F[j]*(U[j]-H[j])+(1-F[j])*(365-H[j]) for j in Cañerias),name = "R9")

# U[j] es igual al valor de t cuando Z es 1
model.addConstrs((quicksum(Z[j,i,t] * t for t in T for i in E) <= U[j] for j in Cañerias),name="R10")

# La cañeria j no puede estar rota por más de gamma dias
model.addConstrs((W[j] <= gamma for j in Cañerias),name="R11")

# Una caneria no se puede empezar a reparar antes de que se rompa
model.addConstrs((Z[j,i,t]*t + (1 - Z[j,i,t])*365 >= H[j] for j in Cañerias for i in E for t in T), name="R12")

# Funcion Objetivo y optimizar el problema
objetivo = quicksum(W[j]*P[j] for j in Cañerias)
model.update()
model.setObjective(objetivo, GRB.MINIMIZE)

model.optimize()

# Manejo Soluciones
# print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
print(f"El valor objetivo es de: {model.ObjVal}")
varInfo = [(v.varName, v.X) for v in model.getVars() if v.X > 0]
with open('resultados_empresas_muy_acotadas_mas_canerias .csv', 'w') as myfile:
    myfile.write(f"El valor objetivo es de: {model.ObjVal}\n")
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(varInfo)
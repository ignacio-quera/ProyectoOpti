from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform

seed(10)
# Generar el modelo
model = Model()
# Sets
T = range(366)
E = range(5) 
J = range(6) # Definar la forma en la que seccionan las cañerias  

# Dinero se encuentra miles de pesos

# Parámetros
C = {(i): uniform(350, 550) for i in E}
L = {(i,j): randint(1, 2) for i in E for j in J} # tiempo en horas
P = {(j): uniform(3000, 4000) for j in J} # Miles de litros perdidos por dia
Q = 10000000000000000000 # 100 millones de pesos
# D = {(j): uniform(25, 45) for j in J}
G = {(j): uniform(100, 500) for j in J}
# K = {(j): uniform(2000, 10000) for j in J}
H = {(j): randint(1, 365) for j in J}
gamma = 90

# Se instancian variables de decision
X = model.addVars(J,T, vtype = GRB.BINARY, name = "X_j,t")
# Y  = model.addVar(J, vtype = GRB.BINARY, name = "Y_j")
R  = model.addVars(J,E,T, vtype = GRB.BINARY, name = "R_j,i,t")
Z  = model.addVars(J,E,T,vtype = GRB.BINARY, name = "Z_j,i,t")

# W = model.addVars(J, vtype = GRB.CONTINUOUS, name = "W_j")
# Llamamos a update
model.update()

# Restricciones
# El costo mensual de reparación de cañerías más la multa por cañerías dañadas no puede superar el presupuesto mensual Q
# model.addConstrs((Q >= quicksum(R[j,i,t ]*(C[i] + G[i]) for t in T for i in E for j in J) + quicksum(Y[j]*K[j] for j in J)),name="R1")
# model.addConstr((Q >= quicksum(R[j,i,t ]*(C[i] + G[j]) for t in T for i in E for j in J)), name="R1")

# Una empresa no puede reparar más de una cañería a la vez
model.addConstrs((1 >= quicksum(R[j,i,t ] for j in J) for i in E for t in T),name="R2")

# Una cañería no puede estar rota y en reparación a la vez
model.addConstrs((X[j,t] + quicksum(R[j,i,t ] for i in E) <= 1 for j in J for t in T ),name="R3")

# Una cañería no puede estar siendo reparada por más de una empresa al mismo tiempo
model.addConstrs((1 >= quicksum(R[j,i,t ] for i in E) for j in J for t in T ),name="R4")

# Una caneria se repara sin interrupciones
model.addConstrs((L[i,j]*Z[j,i,t] == quicksum(R[j,i, alpha] for alpha in range(t, t+L[i,j]) if (t+L[i,j] <= 365)) for i in E for j in J for t in T),name="R5")

# No se puede dejar ninguna repracion incompleta a final de año
model.addConstrs((Z[j,i,t]*t+L[i,j]<=365 for i in E for j in J for t in T),name="R6")

# La variable X debe ser 1 el dia que se rompe la caneria j
model.addConstrs((1 <= X[j, H[j]] for j in J), name="R7")

# Una caneria no puede estar mas de una cantidad determinada de dias sin ser reparada
# model.addConstrs((X[j, H[j]+gamma] == 0 for j in J if (H[j]+gamma < 365)), name="R8")

# La caneria j solo se rompe una vez al año
model.addConstrs((quicksum(Z[j,i,t] for t in T) <= 1 for j in J for i in E), name="R9")

# La caneria j debe permanecer rota desde el dia en que se rompio hasta el dia que comience a ser reparada
model.addConstrs((quicksum(X[j,t] for t in range(H[j], 365)) >= Z[j,i,t]*(t - H[j]) for t in T for j in J for i in E), name="R10")

# La caneria j no se encuentra rota hasta el dia que se rompe
model.addConstrs((quicksum(X[j,t] for t in range(1, H[j])) <= 0 for j in J), name="R11")

# model.addConstrs((X[j,t] >= (1 - Z[j,i,t]) for j in J for i in E for t in range(H[j], 365)))
# model.addConstrs((W[j] >= 365*(1-quicksum(Z[j,i,t] for t in T for i in E)+(quicksum(Z[j,i,t] for t in T for i in E) - H[j])) for j in J))

# model.addConstrs((quicksum(X[j, t] for t in range(H[j], 365)) >= W[j] for j in J))

model.addConstrs((X[j,t] <= quicksum(Z[j,i,t+1] for i in E) for j in J for t in range(1, 365)))

# model.addConstrs((X[j,t] + quicksum(Z[j,i,t] for i in E) <= 1 for j in J for t in T ))

# Funcion Objetivo y optimizar el problema
objetivo = quicksum(X[j,t ]*P[j]  for t in T for j in J)
model.update()
model.setObjective(objetivo, GRB.MINIMIZE) 
model.optimize()

# Manejo Soluciones
# print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
print(f"El valor objetivo es de: {model.ObjVal}")
model.printAttr('X')

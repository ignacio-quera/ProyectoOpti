from random import randint, seed, uniform
seed(10)
# Cantidad de dias del año
dias = range(1,366)

# Cantidad de empresas que se dedican a la reparacion de cañerías en Santiago
empresas = range(1, 4)

# Cantidad de cañerías en mal estado durante un año en Santiago
canerias = range(1, 296)

# Costo diario de arreglar la caneria
coste_diario_arreglo = {(i): uniform(350, 550) for i in empresas} 

# tiempo de demora de reparacion de caneria por empresa
tiempo_demora_empresa = {(i,j): randint(0, 3) for i in empresas for j in canerias} 

# Miles de litros perdidos por dia
litros_perdidos_por_caneria = {(j): uniform(3000, 4000) for j in canerias} 

# Presuepuesto anual en miles de pesos para el arreglo de cañerias
presupuesto_anual = 100000

# Costo diario de mantener el agua cortada
costos_corte_agua = {(j): uniform(100, 500) for j in canerias} 

# Dia en el que cada cañería se rompe. Esto se asume que se obtiene de un inspector de las diversas empresas
dia_caneria_rota = {(j): randint(1, 365) for j in canerias}

# Cantidad maxima de dias en la que una caneria puede estar rota
dias_max = 90
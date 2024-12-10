import os

########
# Running simulations with an HA mutation
# Parameters used in SLiM
s = -0.1
h = -2
N = 5000
L = 3000
location = int(0.5*L)
Mu = 1e-07
Rho = 1e-08
G_start = int(10*N)
G_end = int(10*N + 8*N)
G_check = int(10*N + 300)
G_check_end = int(10*N + 4*N)

nSample = 200
slim = "/usr/local/bin/slim"
slim_file = "~/Desktop/HA_trace_allele.slim"
command = "-d s=" + str(s) + " -d h=" + str(h) + " -d N=" + str(N) + " -d L="+ str(L) + " -d location="+str(location) +" -d Mu="+ str(Mu) +" -d Rho="+ str(Rho) +" -d G_start="+ str(G_start) +" -d G_end="+ str(G_end) +" -d G_check="+ str(G_check) + " -d G_check_end="+ str(G_check_end)
# Takes around 2 minutes per sample
for i in range(nSample):
    os.system(slim + " " + command + " " + slim_file)

# Running simulation with only neutral evolution
# Takes around 14 seconds per sample
neutral_file = "~/Documents/GitHub/CompMethods/neutral.slim"
for i in range(nSample):
    os.system(slim + " " + command + " " + neutral_file)

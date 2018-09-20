import functions as func
import tkinter as tk
import simulation as sim
import random

def runProposedAlgorithm(g, lg):
    C = func.findCycles(lg)
    E = func.eliminateSmallCycles(C, 2)
    H = func.simplification(E)
    T = func.findTransversal(H)
    colors = []
    for edge in g.edges:
        isThere = False
        for t in T:
            if edge == t:
                isThere = True
                break
        if isThere:
            colors.append('g')
        else:
            colors.append('black')
    print("Emisyon ölçüm cihazı yerleştirilecek yollar(Proposed Algorithm):")
    print(T)
    return T

def runRandomly(monitorCount, g):
    R = func.randomly(g, monitorCount)
    print("Emisyon ölçüm cihazı yerleştirilecek yollar(Randomly):")
    print(R)
    return R

def runExperienceBased(monitorCount, g):
    E = func.experienceBased(g, monitorCount)
    print("Emisyon ölçüm cihazı yerleştirilecek yollar(Experience Based):")
    print(E)
    return E

def run(roadNetwork):
    g = None
    L = None
    lg = None
    if roadNetwork == 1:
        g = func.createGraph1()
        lg = func.convertToLineGraph(g)
        L = func.generateTurnConstraints1(lg)
        lg = func.deleteTurnConstraints(lg, L)
    elif roadNetwork == 2:
        g = func.createGraph2()
        lg = func.convertToLineGraph(g)
        L = func.generateTurnConstraints2(lg)
        lg = func.deleteTurnConstraints(lg, L)
    elif roadNetwork == 3:
        g = func.createGraph3()
        lg = func.convertToLineGraph(g)
    T = runProposedAlgorithm(g, lg)
    R = runRandomly(len(T), g)
    E = runExperienceBased(len(T), g)
    runSimulator(lg, T, R, E, roadNetwork)

def runSimulator(lg, T, R, E, roadNetwork):
    routingTable = sim.createRoutingTable(lg)
    trips = []
    catchT = 0
    catchR = 0
    catchE = 0
    catchedCarsT = []
    catchedCarsR = []
    catchedCarsE = []
    for i in range(3000):
        trip = []
        t = sim.generateTrip(routingTable, lg, roadNetwork, i)
        for route in t:
            trip.append(route)
        trips.append(trip)
    carNumber = 0
    for trip in trips:
        for t in trip:
            for road in t:
                if func.isThere(T, road):
                    catchT = catchT + 1
                    if func.isThere(catchedCarsT, carNumber) == False:
                        catchedCarsT.append(carNumber)
                if func.isThere(E, road):
                    catchE = catchE + 1
                    if func.isThere(catchedCarsE, carNumber) == False:
                        catchedCarsE.append(carNumber)
                if func.isThere(R, road):
                    catchR = catchR + 1
                    if func.isThere(catchedCarsR, carNumber) == False:
                        catchedCarsR.append(carNumber)
        carNumber = carNumber + 1
    print("Catched number in Proposed Algorithm -> " + str(catchT))
    print("Catched cars number in Proposed Algorithm -> " + str(len(catchedCarsT)))
    print("Average Degree in Proposed Algorithm -> " + str(catchT/len(catchedCarsT)))
    print("Catched number in Randomly Algorithm -> " + str(catchR))
    print("Catched cars number in Randomly Algorithm -> " + str(len(catchedCarsR)))
    print("Average Degree in Randomly Algorithm -> " + str(catchR/len(catchedCarsR)))
    print("Catched number in Experince Based Algorithm -> " + str(catchE))
    print("Catched cars number in Experince Based Algorithm -> " + str(len(catchedCarsE)))
    print("Average Degree in Experience Based Algorithm -> " + str(catchE/len(catchedCarsE)))
    sim.analyzeResults(len(trips), catchT, catchR, catchE, catchedCarsT, catchedCarsR, catchedCarsE)
    
root = tk.Tk()

#labelEntry = tk.Label(root, text="Emisyon Ölçüm Cihazı Sayısı").grid(row=0, column=1)
#e1 = tk.Entry(labelEntry)
#e1.grid(row=1, column=1)
labelSpace1 = tk.Label(root).grid(row=2, column=0)
labelSpace2 = tk.Label(root).grid(row=2, column=1)
labelSpace3 = tk.Label(root).grid(row=2, column=2)
photo_1 = tk.PhotoImage(file="img/road_1.png")
photo_2 = tk.PhotoImage(file="img/road_2.png")
photo_3 = tk.PhotoImage(file="img/road_3.png")
button_1 = tk.Button(root, command= lambda: run(1))
button_1.grid(row=3, column=0)
button_1.config(image=photo_1, compound=tk.RIGHT, width="400", height="299")
button_2 = tk.Button(root, command= lambda: run(2))
button_2.grid(row=3, column=1)
button_2.config(image=photo_2, compound=tk.RIGHT, width="400", height="299")
button_3 = tk.Button(root, command= lambda: run(3))
button_3.grid(row=3, column=2)
button_3.config(image=photo_3, compound=tk.RIGHT, width="400", height="299")

root.mainloop()

"""print("C nodes:")
for node in C[0]:
    print(node)

print("C edges:")
for edge in C[1]:
    print(edge)

print("C edges after eliminating:")
for edge in E[1]:
    print(edge)

print("C edges after simplification:")
for edge in H[1]:
    print(edge)

print("T:")
print(T)"""

print("Tamamlandı")


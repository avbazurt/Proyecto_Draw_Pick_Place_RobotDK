from robolink import *  # RoboDK API
from robodk import *  # Robot toolbox
from time import *
from random import randint

class RobotDraw():
    def __init__(self):
        # Caracteristicas ROBOT
        self.RDK = Robolink()

        self.robot = self.RDK.Item('ABB IRB 4600-20/2.50',ITEM_TYPE_ROBOT)
        if not self.robot.Valid():
            quit()

        self.reference = self.robot.Parent()  # devuelve el artículo

        self.robot.setPoseFrame(self.reference)  # establece el marco de referencia de un robot
        self.pose_ref = self.robot.Pose()  # devuelve la posición actual del robot con matriz

        self.frameletras = self.RDK.Item("FrameLetras", ITEM_TYPE_FRAME)
        self.robot.setPoseFrame(self.frameletras)

        self.tarletras = self.RDK.Item("Letras")
        self.tarletras = self.tarletras.Pose()

        #Creamos el Pencil
        self.pencil = self.RDK.Item("Pencil", ITEM_TYPE_TOOL)
        self.pencil_id = self.RDK.getParam("Pencil")

        #Creamos la hoja
        self.hoja = self.RDK.Item("HojaP", ITEM_TYPE_OBJECT)

        # Limpiamos la pizarra
        self.RDK.Spray_Clear(-1)
        self.RDK.setSimulationSpeed(3)

        # Lo colocamos en su posicion de espera
        self.PosEspera = self.tarletras * transl(600, -100, 0)
        self.robot.MoveL(self.PosEspera)

        # FILA
        self.fila = 0
        self.columna = 0

        # CARACTERISTICAS LETRAS
        self.k = 35
        self.res_x = 3 * self.k / 4
        self.res_y = 4 * self.k / 8

        # CARACTERISTICAS LETRAS
        self.X0 = None
        self.Y0 = None
        self.Z0 = None

        self.COLOR = None

        # LISTA MOVIMIENTO LETRA
        self.l_letra = []

    def UpdateHoja(self,text):
        self.hoja = self.RDK.Item(text, ITEM_TYPE_OBJECT)

    def UpdateCaracteristicas(self, num) -> None:
        self.k = int(num)
        self.res_x = 3 * self.k / 4
        self.res_y = 4 * self.k / 8

        # CARACTERISTICAS LETRAS
        self.X0 = 80
        self.Y0 = 80 + self.res_y * 8
        self.Z0 = 0



    def UpdateList(self, letra: str) -> None:
        X1 = self.X0 + 4 * self.fila * self.k
        Y1 = self.Y0 + 5 * self.columna * self.k
        Z0 = self.Z0

        P = [transl(X1, Y1 - self.res_y * i, Z0) for i in range(0, 9)]
        Q = [transl(X1 + self.res_x * i, Y1 - self.res_y * 8, Z0) for i in range(0, 5)]
        R = [transl(X1 + self.res_x * i, Y1 - self.res_y * 4, Z0) for i in range(0, 5)]
        S = [transl(X1 + self.res_x * i, Y1, Z0) for i in range(0, 5)]
        T = [transl(X1 + self.res_x * 4, Y1 - self.res_y * i, Z0) for i in range(0, 9)]

        dic = {
            "A": [P[0], P[7], Q[1], Q[3], T[7], T[4], P[4], T[4], T[0]],
            "B": [P[0], P[8], Q[3], T[7], T[5], R[3], P[4], R[3], T[3], T[1], S[3], P[0]],
            "C": [T[7], Q[3], Q[1], P[7], P[1], S[1], S[3], T[1]],
            "D": [P[0], P[8], Q[3], T[6], T[2], S[3], P[0]],
            "E": [P[0], S[4], P[0], P[4], R[2], P[4], P[8], Q[4]],
            "F": [P[0], P[4], R[2], P[4], P[8], Q[4]],
            "G": [R[1], R[3], T[3], T[1], S[3], S[1], P[1], P[7], Q[1], Q[4]],
            "H": [P[0], P[8], P[4], T[4], T[8], T[0]],
            "I": [P[8], T[8], Q[2], S[2], S[4], S[0]],
            "J": [T[8], T[1], S[3], P[0]],
            "K": [P[0], P[8], P[4], Q[4], P[4], T[0]],
            "L": [P[8], P[0], T[0]],
            "M": [P[0], P[8], R[2], T[8], T[0]],
            "N": [P[0], P[8], T[0], T[8]],
            "O": [P[1], P[7], Q[1], Q[3], T[7], T[1], S[3], S[1], P[1]],
            "P": [P[0], P[8], Q[3], T[7], T[5], R[3], P[4]],
            "Q": [P[1], P[7], Q[1], Q[3], T[7], T[1], S[3], S[1], P[1], P[4], T[0]],
            "R": [P[0], P[8], Q[3], T[7], T[5], R[3], P[4], T[0]],
            "S": [Q[4], Q[1], P[7], P[5], R[1], R[3], T[3], T[1], S[3], P[0]],
            "T": [P[8], T[8], Q[2], S[2]],
            "U": [P[8], P[1], S[1], S[3], T[1], T[8]],
            "V": [P[8], S[2], T[8]],
            "W": [P[8], P[0], R[2], T[0], T[8]],
            "X": [P[8], R[2], P[0], R[2], T[8], R[2], T[0]],
            "Y": [P[8], R[2], T[8], R[2], S[2]],
            "Z": [P[8], T[8], P[0], T[0]]
        }

        self.l_letra = dic[letra.upper()]

    def Dec_Hex(self, numero) -> str:
        n = numero
        base = 16
        l = []
        bandera = True
        while bandera:
            cociente = n // base
            residuo = n % base
            l.append(residuo)
            if residuo < base:
                l.append(cociente)
                n = residuo
                bandera = False
        text = ""
        for i in l[::-1]:
            if i >= 10:
                text += "ABCDEF"[i - 10]
            else:
                text += str(i)
        return text

    def GenerarRGBACode(self, R, G, B, A):
        texto = "#" + self.Dec_Hex(A) + self.Dec_Hex(R) + self.Dec_Hex(G) + self.Dec_Hex(B)
        return texto

    def GenerateRandomColor(self) -> str:
        R = randint(0, 255)
        G = randint(0, 255)
        B = randint(0, 255)
        A = randint(0, 255)
        COLOR = self.GenerarRGBACode(A, R, G, B)
        return COLOR

    def LimpiarPizarra(self):
        self.RDK.RunProgram("WeldOn(-1)")
        sleep(2)

    def ActivarTinta(self,color):
        options_command = "NO_PROJECT PARTICLE=SPHERE(2,8,5,5,1) STEP=1x0 RAND=0 COLOR={}".format(color)
        spray_id = self.RDK.Spray_Add(self.pencil,self.hoja,options_command)
        self.RDK.Spray_SetState(SPRAY_ON, spray_id)

    def ApagarTinta(self):
        self.RDK.Spray_SetState(SPRAY_OFF, -1)


    def BorrarPizarra(self):
        self.RDK.Spray_Clear(-1)
        sleep(2)

    def DrawLetra(self, letra, tamaño, color=None) -> None:
        # Actualizamos
        self.UpdateCaracteristicas(tamaño)
        self.UpdateList(letra)


        lista = self.l_letra

        # Lo colocamos en su posicion inicial
        #self.RDK.setSimulationSpeed(3)
        self.robot.MoveL(self.tarletras * lista[0])

        # Definimos las variables
        self.robot.setSpeed(150, 150)
        #self.RDK.setSimulationSpeed(0.75)
        self.robot.setPoseFrame(self.frameletras)

        # Definimos un color
        if color is None:
            color = '#CC3344FF'

        # Generamos los movimientos
        for i in range(len(lista)):
            #self.RDK.RunProgram("WeldOn(OFF)")
            if i < len(lista) - 1:
                self.robot.MoveL(self.tarletras * lista[i])
                self.ActivarTinta(color)
                self.robot.MoveL(self.tarletras * lista[i + 1])
                self.ApagarTinta()
            else:
                self.robot.MoveL(self.tarletras * lista[i])

        self.ApagarTinta()

        if self.fila >= 10:
            self.fila = 0
            self.columna += 1
        else:
            self.fila += 1

        #self.RDK.RunProgram("WeldOn(0)")

    def Enter(self) -> None:
        # Lo colocamos en su posicion de espera
        self.columna += 1
        self.fila = 0

    def Final(self) -> None:
        self.RDK.RunProgram("WeldOn(0)")
        sleep(2)
        self.RDK.setSimulationSpeed(3)
        self.robot.MoveL(self.PosEspera)
        self.columna = 0
        self.fila = 0

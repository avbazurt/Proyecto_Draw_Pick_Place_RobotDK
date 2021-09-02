from robolink import *  # RoboDK API
from robodk import *  # Robot toolbox
from time import sleep

class RobotMove():
    def __init__(self):
        self.RDK = Robolink()

        self.robot = self.RDK.Item('ABB IRB 4600-40/2.55',ITEM_TYPE_ROBOT)
        if not self.robot.Valid():
            quit()

        self.reference = self.robot.Parent()  # devuelve el artículo

        self.robot.setPoseFrame(self.reference)  # establece el marco de referencia de un robot
        self.pose_ref = self.robot.Pose()  # devuelve la posición actual del robot con matriz

        self.robot.setSpeed(150, 150)

        self.tarPapel = self.RDK.Item("PosHoja")
        self.Pos1 = self.tarPapel.Pose()
        self.Pos2 = transl(0,0,500)*self.Pos1

        self.Pos3 = transl(0, 1500, 0) * self.Pos1
        self.Pos4 = transl(0, 0, 500) * self.Pos3

        self.Pos0 = transl(-800, 0, 0) * self.Pos3

        self.Pos5 = transl(0, 2 * 1500, 0) * self.Pos1
        self.Pos6 = transl(0, 0, 500) * self.Pos5


        self.robot.MoveJ(self.Pos0)

        self.piston = self.RDK.Item('Piston', ITEM_TYPE_TOOL)
        self.hoja = self.RDK.Item('Blanco')

        self.actual = "Hoja_0"
        self.anterior = "Hoja_X"

        self.contador = 0



    def ColocarHojaNueva(self):
        self.robot.MoveJ(self.Pos1)

        self.RDK.Copy(self.hoja)
        self.new = self.RDK.Paste(self.RDK.Item('ABB IRB 4600-40/2.55 Base'))
        self.new.setPose(self.Pos1)
        self.new.setName(self.actual)

        self.new.setVisible(True, True)
        self.piston.AttachClosest()
        self.robot.MoveJ(self.Pos2)
        self.robot.MoveJ(self.Pos4)
        self.robot.MoveJ(self.Pos3)
        self.piston.DetachAll()

        self.robot.MoveJ(self.Pos0)


    def QuitarHoja(self):
        self.robot.MoveJ(self.Pos3)
        self.piston.AttachClosest()
        self.robot.MoveJ(self.Pos4)
        self.robot.MoveJ(self.Pos6)


        self.robot.MoveJ(transl(0, 0, 20*self.contador)*self.Pos5)



        self.piston.DetachAll()

        #self.RDK.Delete(self.RDK.Item(self.anterior))
        self.robot.MoveJ(self.Pos0)
        self.anterior = self.actual
        self.contador+=1
        self.actual = "Hoja_{}".format(self.contador)








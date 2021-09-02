from robolink import *  # RoboDK API
from robodk import *  # Robot toolbox
from time import sleep

class RobotPicture():
    def __init__(self):
        self.RDK = Robolink()

        self.robot = self.RDK.Item('Kawasaki YF003N',ITEM_TYPE_ROBOT)
        if not self.robot.Valid():
            quit()

        self.reference = self.robot.Parent()  # devuelve el artículo

        self.robot.setPoseFrame(self.reference)  # establece el marco de referencia de un robot
        self.pose_ref = self.robot.Pose()  # devuelve la posición actual del robot con matriz

        self.tarCamara = self.RDK.Item("Base")
        self.tarCamara = self.tarCamara.Pose()

        self.robot.MoveL(self.tarCamara)

        self.camref = self.RDK.Item('Camara')

        self.robot.setSpeed(150, 150)

    def TomarFoto(self):
        camara = self.RDK.Cam2D_Add(self.camref)


        self.robot.MoveL(transl(0,0,-350)*self.tarCamara)

        image_file = self.RDK.getParam('PATH_OPENSTATION') + "/recourses/foto.png"
        print("Saving camera snapshot to file:" + image_file)
        self.RDK.Cam2D_Snapshot(image_file)

        self.robot.MoveL(self.tarCamara)

        self.RDK.Cam2D_Close()
        self.RDK.Delete(camara)



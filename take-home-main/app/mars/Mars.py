from enum import Enum
from typing import List
from datetime import datetime


class FullName(Enum):
    ChemistryandCameraComplex = "Chemistry and Camera Complex"
    FrontHazardAvoidanceCamera = "Front Hazard Avoidance Camera"
    MarsDescentImager = "Mars Descent Imager"
    MarsHandLensImager = "Mars Hand Lens Imager"
    MastCamera = "Mast Camera"
    NavigationCamera = "Navigation Camera"
    RearHazardAvoidanceCamera = "Rear Hazard Avoidance Camera"


class CameraName(Enum):
    CHEMCAM = "CHEMCAM"
    FHAZ = "FHAZ"
    MAHLI = "MAHLI"
    MARDI = "MARDI"
    MAST = "MAST"
    NAVCAM = "NAVCAM"
    RHAZ = "RHAZ"


class PhotoCamera:
    fullname: FullName
    name: CameraName
    id: int
    roverid: int

    def __init__(self, fullname: FullName, name: CameraName, id: int, roverid: int) -> None:
        self.fullname = fullname
        self.name = name
        self.id = id
        self.roverid = roverid


class CameraElement:
    fullname: FullName
    name: CameraName

    def __init__(self, fullname: FullName, name: CameraName) -> None:
        self.fullname = fullname
        self.name = name


class RoverName(Enum):
    Curiosity = "Curiosity"


class Status(Enum):
    active = "active"


class Rover:
    maxsol: int
    cameras: List[CameraElement]
    maxdate: datetime
    totalphotos: int
    name: RoverName
    id: int
    launchdate: datetime
    landingdate: datetime
    status: Status

    def __init__(self, maxsol: int, cameras: List[CameraElement], maxdate: datetime, totalphotos: int, name: RoverName, id: int, launchdate: datetime, landingdate: datetime, status: Status) -> None:
        self.maxsol = maxsol
        self.cameras = cameras
        self.maxdate = maxdate
        self.totalphotos = totalphotos
        self.name = name
        self.id = id
        self.launchdate = launchdate
        self.landingdate = landingdate
        self.status = status


class Photo:
    sol: int
    earthdate: datetime
    id: int
    camera: PhotoCamera
    rover: Rover
    imgsrc: str

    def __init__(self, sol: int, earthdate: datetime, id: int, camera: PhotoCamera, rover: Rover, imgsrc: str) -> None:
        self.sol = sol
        self.earthdate = earthdate
        self.id = id
        self.camera = camera
        self.rover = rover
        self.imgsrc = imgsrc


class Mars:
    photos: List[Photo]

    def __init__(self, photos: List[Photo]) -> None:
        self.photos = photos

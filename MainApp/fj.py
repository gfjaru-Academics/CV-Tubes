import cv2, os
from scipy import ndimage
from numpy import asarray
from shutil import copyfile


class ComputerVision:
  def __init__(self, origin, output, fileType):
    self.originDirectory = origin
    self.outputDirectory = output
    self.supportedFileType = fileType

  def initiateOutputDirectory(self):
    ## List all files in origin folder
    originListAllFiles = [name for name in os.listdir(self.originDirectory)]

    ## Initlize root folder for output
    if os.path.isdir(self.outputDirectory) == False:
      usedDir = [
                 '',
                 'pas_foto',
                   'pas_foto/half', ## recognize upperbody 
                   'pas_foto/full', ## recognize full body
                 'bersama', ## recognize more than one person
                 'selfie', ## recognize face ratio > 60
                 'ig', ## classify rules of third
                 'uncategorized', ## neither
                 'unused' ## wrong file format
                ]
      for dirs in usedDir:
        os.mkdir(self.outputDirectory + dirs)

    ## Filtering file format, move unnecessary format
    for fileName in originListAllFiles:
      extension = fileName.split('.')
      if extension[-1] not in self.supportedFileType:
        os.rename(self.originDirectory + fileName, self.outputDirectory + 'unused/' + fileName)
  
  def classifyImage(self):
    for images in [name for name in os.listdir(self.originDirectory)]:
      self.checkImage(self.originDirectory + images)

  def RuleOfThird(self, img, output):
    Image = cv2.imread(img)
    Height, Width, ColChannel = Image.shape
    ConvertGrayscale = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    (Threshold, BoWImage) = cv2.threshold(ConvertGrayscale, 127, 255, cv2.THRESH_BINARY)
    Data = asarray(BoWImage)
    MeasureCoM = ndimage.measurements.center_of_mass(Data)

    if (float(Width) * 0.27) <= float(MeasureCoM[1]) <= (float(Width) * 0.39) and (float(Height) * 0.27) <= float(MeasureCoM[0]) <= (float(Height) * 0.39):
      output['rot'] = 1
    if (float(Width) * 0.27) <= float(MeasureCoM[1]) <= (float(Width) * 0.39) and (float(Height) * 0.6) <= float(MeasureCoM[0]) <= (float(Height) * 0.72):
      output['rot'] = 1
    if (float(Width) * 0.6) <= float(MeasureCoM[1]) <= (float(Width) * 0.72) and (float(Height) * 0.27) <= float(MeasureCoM[0]) <= (float(Height) * 0.39):
      output['rot'] = 1
    if (float(Width) * 0.6) <= float(MeasureCoM[1]) <= (float(Width) * 0.72) and (float(Height) * 0.6) <= float(MeasureCoM[0]) <= (float(Height) * 0.72):
      output['rot'] = 1

  def PortraitUpper(self, img, classifier, output): 
    Classifier = cv2.CascadeClassifier(classifier['upperbody'])
    Image = cv2.imread(img)
    Height, Width, ColChannel = Image.shape
    ConvertGrayscale = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    Faces = Classifier.detectMultiScale(ConvertGrayscale, 1.3, 5)

    FaceSize = []
    for (x, y, w, h) in Faces:
      FaceSize.append((x+w)*(y+h))
    
    if FaceSize:
      output['pas_foto_half'] = 1
  
  def PortraitFull(self, img, classifier, output): 
    Classifier = cv2.CascadeClassifier(classifier['fullbody'])
    Image = cv2.imread(img)
    Height, Width, ColChannel = Image.shape
    ConvertGrayscale = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    Faces = Classifier.detectMultiScale(ConvertGrayscale, 1.3, 5)

    FaceSize = []
    for (x, y, w, h) in Faces:
      FaceSize.append((x+w)*(y+h))
    
    Calculated = []
    for xFaces in FaceSize:
      ratio = ((xFaces/(Width*Height))*100)
      Calculated.append(ratio)
    
    if Calculated:
      output['pas_foto_full'] = 1

  def Bersama(self, img, classifier, output):
    Classifier = cv2.CascadeClassifier(classifier['frontalface'])
    Image = cv2.imread(img)
    Height, Width, ColChannel = Image.shape
    ConvertGrayscale = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    Faces = Classifier.detectMultiScale(ConvertGrayscale, 1.3, 5)

    FaceSize = []
    for (x, y, w, h) in Faces:
      FaceSize.append((x+w)*(y+h))
    
    if len(FaceSize) > 2:
      output['bersama'] = 1
  
  def RatioFace(self, img, classifier, output):
    Classifier = cv2.CascadeClassifier(classifier['frontalface'])
    Image = cv2.imread(img)
    Height, Width, ColChannel = Image.shape
    ConvertGrayscale = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    Faces = Classifier.detectMultiScale(ConvertGrayscale, 1.3, 5)

    FaceSize = []
    for (x, y, w, h) in Faces:
      FaceSize.append((x+w)*(y+h))
    
    Calculated = []
    for xFaces in FaceSize:
      ratio = ((xFaces/(Width*Height))*100)
      if ratio > 60:
        Calculated.append(ratio)
    
    if Calculated:
      output['selfie'] = 1

  def checkImage(self, img): 
    result = {
      'pas_foto_half': 0,
      'pas_foto_full': 0,
      'selfie': 0,
      'bersama': 0,
      'rot': 0
    }

    classifier = {
      'frontalface': './classifier/haarcascade_frontalface_default.xml',
      'fullbody': './classifier/haarcascade_fullbody.xml',
      'upperbody': './classifier/haarcascade_upperbody.xml'
    }
    
    self.PortraitUpper(img, classifier, result)
    self.RatioFace(img, classifier, result)
    self.Bersama(img, classifier, result)
    self.RuleOfThird(img, result)
    self.PortraitFull(img, classifier, result)
    
    newName = img.split('/')

    moved = 0
    if result['selfie']:
      copyfile(img, self.outputDirectory + 'selfie/' + newName[-1])
      moved = 1
    if result['bersama']:
      copyfile(img, self.outputDirectory + 'bersama/' + newName[-1])
      moved = 1
    if result['rot']:
      copyfile(img, self.outputDirectory + 'ig/' + newName[-1])
      moved = 1
    if result['pas_foto_full']:
      copyfile(img, self.outputDirectory + 'pas_foto/full/' + newName[-1])
      moved = 1
    if result['pas_foto_half']:
      copyfile(img, self.outputDirectory + 'pas_foto/half/' + newName[-1])
      moved = 1
    if moved == 0:
      os.rename(img, self.outputDirectory + 'uncategorized/' + newName[-1])
    else:
      os.remove(img)

    print(result)

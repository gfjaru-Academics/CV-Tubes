from fj import ComputerVision
## (origin, output, format)
myCV = ComputerVision('./origin/', './hsl/', ['jpg', 'png'])
myCV.initiateOutputDirectory()
myCV.classifyImage()
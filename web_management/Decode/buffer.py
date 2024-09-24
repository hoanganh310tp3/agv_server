import functools

def spliceBuffer(messageFrame, payloadBuffer):
    bufferFrame = [0]
    bufferData = []
    for i in range(len(messageFrame)):
        sliced = messageFrame[0 : i+1]
        sum = functools.reduce(lambda a, b: a+b, sliced, 0)
        bufferFrame.append(sum)

    subBuffer = []
    for i in range(len(bufferFrame)-1):
        subBuffer = payloadBuffer[bufferFrame[i] : bufferFrame[i+1]]
        bufferData.append(subBuffer)
    return bufferData
    
def spliceCommands(payloadBuffer):
    bufferData = []

    if (len(payloadBuffer)-4)%6 != 0:
        print("Error")
    
    index = 3
    while index < len(payloadBuffer) - 7:
        node = payloadBuffer[index : index+1]
        speed = payloadBuffer[index+2]
        sectionLen = payloadBuffer[index+3 : index+4]
        action = payloadBuffer[index+5]
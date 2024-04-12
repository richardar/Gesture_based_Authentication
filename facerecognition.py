from deepface import DeepFace
import os




def recognize(database,imagetofind):
    folders = os.listdir(database)
    
    try:

        for folder in folders:
            possibleimages=os.listdir(os.path.join(database,folder))
            imagelist=[]
            for possibleimage in possibleimages:
                if possibleimage.endswith('.jpeg') or possibleimage.endswith('.png') or possibleimage.endswith('.jpg'):
                    imagelist.append(possibleimage)
                else:
                    continue
            for image in imagelist:
                result = DeepFace.verify(imagetofind,os.path.join(database,folder,image),)
                if result['verified'] == True :

                    return folder
                


     
     
        return 0
    except Exception as e:
        print(e)
        return 2
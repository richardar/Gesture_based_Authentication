from deepface import DeepFace
import os




def recognize(database,imagetofind):
    images = os.listdir(database)
    try:

        for image in images:
            result = DeepFace.verify(imagetofind,os.path.join(database,image))
            if result['verified'] == True :

                if image.endswith('.jpeg'):
                    return image[:-5]
                elif image.endswith('.jpg'):
                    return image[:-4]
                elif image.endswith('.png'):
                    return image[:-4]
                else:
                    return image
                


     
     
        return 0
    except Exception as e:
        print(e)
        return 2
import face_recognition
from urllib.request import urlopen
import base64
from io import BytesIO
import validators
import json
import config
# base64Img = "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"


# byteData = base64.b64decode(base64Img)
# imageData = BytesIO(byteData)
# image = face_recognition.load_image_file(imageData)
# faceEncoding = face_recognition.face_encodings(image)
# face_locations = face_recognition.face_locations(image)
# result = base64.b64encode(repr(json.dumps(face_locations)).encode())
# print(eval(base64.b64decode(result).decode()))

class FaceUtils:
    """
    face utils for  face recognition
    """
    @staticmethod
    def get_image_data(face):
        """
         charge face is  url or base64
        :param face:
        :return:image_data
        """

        if validators.url(face):
            '''is url or base64 str'''
            image_bytes = urlopen(face).read()
            image_data = BytesIO(image_bytes)
        else:
            missed_padding = 4 - len(face) % 4
            if missed_padding > 0:
                face = face + '=' * missed_padding
            print(face)
            byte_data = base64.b64decode(face)
            image_data = BytesIO(byte_data)

        return image_data

    @staticmethod
    def compare_faces(known_face_encodings, face_encoding_to_check):
        """
        Compare a list of face encodings against a candidate encoding to see if they match.

        :param known_face_encodings: A list of known face encodings
        :param face_encoding_to_check: A single face encoding to compare against the list
        :return: A similar float number is 1 - distance
        """
        return 1.0 - face_recognition.face_distance(known_face_encodings, face_encoding_to_check)

    @staticmethod
    def detect_face(face):
        """
        face  detect
        :param face: a face url or base64 data
        :return:
        """
        image = face_recognition.load_image_file(FaceUtils.get_image_data(face))
        face_landmarks = face_recognition.face_landmarks(image, model='small')
        face_encodings = face_recognition.face_encodings(image)
        face_locations = face_recognition.face_locations(image)
        characters = []
        for face_encoding in face_encodings:
            base64_encode = base64.b64encode(repr(json.dumps(face_encoding.tolist())).encode())
            # face_encoding 需要转成list ,在还原的时候需要将list 转np.array
            characters.append(base64_encode)
        return dict(faceModel=face_landmarks, faceEncoding=characters, faceLocations=face_locations,
                    faceCount=len(characters))

    @staticmethod
    def compare_face(known_face, unknown_face):
        """
        compare face with two image data
        :param known_face: known face
        :param unknown_face: unknown face
        :return:{similar:1.0}
        """
        # 加载图像
        unknown_face_image = face_recognition.load_image_file(FaceUtils.get_image_data(unknown_face))
        #  判断是否存在仅有的一张人脸
        face_locations2 = face_recognition.face_locations(unknown_face_image)
        if len(face_locations2) == 0:
            return dict(code=config.CONST_COMPARE_UNKNOWN_FACE_NO_FACE_FOUND, errorinfo='unknown_face no face found',
                        result=False)
        if len(face_locations2) > 1:
            return dict(code=config.CONST_COMPARE_UNKNOWN_FACE_FACE_TOO_MANY, errorinfo='unknown face too many',
                        result=False)

        known_face_image = face_recognition.load_image_file(FaceUtils.get_image_data(known_face))
        face_locations1 = face_recognition.face_locations(known_face_image)
        if len(face_locations1) == 0:
            return dict(code=config.CONST_COMPARE_KNOWN_FACE_NO_FACE_FOUND, errorinfo='known_face no face found',
                        result=False)
        if len(face_locations1) > 1:
            return dict(code=config.CONST_COMPARE_KNOWN_FACE_FACE_TOO_MANY, errorinfo='known_face face too many',
                        result=False)

        known_face_encodings = face_recognition.face_encodings(known_face_image)
        unknown_face_encodings = face_recognition.face_encodings(unknown_face_image)

        distances = FaceUtils.compare_faces(known_face_encodings, unknown_face_encodings[0])
        return dict(similar=round(distances[0], 6),  code=config.CONST_COMPARE_FACE_SUCCESS, errorinfo="SUCCESS",
                    result=True)

    @staticmethod
    def compare_face_encoding(known_face_encodings, unknown_face):
        """
        compare face by known encoding
        :param known_face_encodings:
        :param unknown_face:
        :return: similar
        """
        # 加载图像
        unknown_face_image = face_recognition.load_image_file(FaceUtils.get_image_data(unknown_face))
        #  判断是否存在仅有的一张人脸
        face_locations2 = face_recognition.face_locations(unknown_face_image)
        if len(face_locations2) == 0:
            return dict(code=config.CONST_COMPARE_UNKNOWN_FACE_NO_FACE_FOUND, errorinfo='unknown_face no face found',
                        result=False)
        if len(face_locations2) > 1:
            return dict(code=config.CONST_COMPARE_UNKNOWN_FACE_FACE_TOO_MANY, errorinfo='unknown face too many',
                        result=False)

        unknown_face_encodings = face_recognition.face_encodings(unknown_face_image)

        distances = FaceUtils.compare_faces(known_face_encodings, unknown_face_encodings[0])
        return dict(similar=round(distances[0], 6), code=config.CONST_COMPARE_FACE_SUCCESS, errorinfo="SUCCESS",
                    result=True)

    @staticmethod
    def compare_face_encoding_tolerance(known_face_encodings, unknown_face, tolerance=0.6):
        """
        compare face by known face encoding for tolerance
        :param known_face_encodings:
        :param unknown_face:
        :param tolerance:
        :return: similar
        """
        # 加载图像
        unknown_face_image = face_recognition.load_image_file(FaceUtils.get_image_data(unknown_face))
        #  判断是否存在仅有的一张人脸
        face_locations2 = face_recognition.face_locations(unknown_face_image)
        if len(face_locations2) == 0:
            return dict(code=config.CONST_COMPARE_UNKNOWN_FACE_NO_FACE_FOUND, errorinfo='unknown_face no face found',
                        result=False)
        if len(face_locations2) > 1:
            return dict(code=config.CONST_COMPARE_UNKNOWN_FACE_FACE_TOO_MANY, errorinfo='unknown face too many',
                        result=False)

        unknown_face_encodings = face_recognition.face_encodings(unknown_face_image)

        distances = face_recognition.compare_faces(known_face_encodings, unknown_face_encodings[0], tolerance)
        return distances


# print(FaceUtils.detect_face('http://a3.att.hudong.com/14/30/01300000242726135937305018468.jpg'))

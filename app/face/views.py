from flask import request, jsonify,abort
import config
import base64, json
import numpy as np
from . import face
from .faceutil import FaceUtils
from .mongoutils import MongoUtil
import logging


@face.route('/FaceDetect', methods=['POST'])
def face_detect():
    """
    {
       "faceimage":"img(base64 or url)"

    }
    :return: {
      "similar":1.0,
      "code":"00000",
      "errorinfo":"message",
      "result":true
    }
    """
    try:
        face_base64 = request.json
        face_detect_result = FaceUtils.detect_face(face_base64['faceimage'])
        return jsonify(dict(facemodels=face_detect_result['faceModel'], code=config.CONST_COMPARE_FACE_SUCCESS,
                            errorinfo='success',  result=True))
    except KeyError as e:
        logging.error(e)
        abort(500)


@face.route('/FaceCompare', methods=['POST'])
def face_compare_encoding_base64():
    """
      compare face by encoding ,encoding is saved in mongodb,the encoding is unique search by userId
     {
       "base64image":"img(base64 or url)",
       "userId":"userId"
    }
    return: {
      "similar":1.0,
      "code":"00000",
      "errorinfo":"message"
      "result":true
    }
    """
    try:
        user_info = request.json
        user = MongoUtil().find_face_user(user_info['userId'])
        base64_image = user_info['base64image']
        encoding = user['encoding']
        result = [np.array(json.loads(eval(base64.b64decode(encoding).decode())))]
        return jsonify(FaceUtils.compare_face_encoding(result, base64_image))
    except KeyError as e:
        logging.error(e)
        abort(500)
    return jsonify(dict(code=config.CONST_COMPARE_USER_NOT_FOUND, errorinfo='no user found',
                        result=False))


@face.route('/Face2Face', methods=['POST'])
def face_compare_face():
    """
      compare base64 image with face to face

    :param:{
          "faceimage1":"img(base64 or url)",
          "faceimage2":"img(base64 or url)"
    }
    :return:{
      "similar":1.0
      "code":"00000",
      "errorinfo":"message"
      "result":true
    }
    """
    try:
        face_base64 = request.json
        result = FaceUtils.compare_face(known_face=face_base64['faceimage1'], unknown_face=face_base64['faceimage2'])
        return jsonify(result)
    except KeyError as e:
        logging.error(e)
        abort(500)


@face.route('/AddUser', methods=["POST"])
def add_user():
    """
    add user
    :param:{
        "userId":"id",
        "userName":"userName",
        "idCard":"idCard",
        "base64image":"img(base64 or url)"
    }
    :return:{
      "code":"00000",
      "errorinfo":"message",
       "result": True,
    }
    """
    try:
        user_info = request.json
        encoding = FaceUtils.detect_face(user_info['base64image'])['faceEncoding']
        if len(encoding) == 1:
            user = MongoUtil().insert_face_user({
                'userId': user_info.get('userId'),
                "userName": user_info.get('userName'),
                "idCard": user_info.get('idCard'),
                "encoding": encoding[0]
            })
            if user is not None:
                return jsonify({"code": config.CONST_COMPARE_FACE_SUCCESS,
                                "result": True,
                                "errorinfo": "success"})
            else:
                return jsonify({"code": config.CONST_COMPARE_FACE_INSERT_ERROR,
                                "result": False,
                                "errorinfo": "insert database error"})
        else:
            return jsonify({
                "result": False,
                "code": config.CONST_COMPARE_UNKNOWN_FACE_NO_FACE_FOUND,
                "errorinfo": "no face detect"
            })
    except KeyError as e:
        logging.error(e)
        abort(500)


@face.route('/DeleteUser', methods=["POST"])
def delete_user():
    """
    delete user
    :param:{
    "userId":"userId",
    "base64image":"image"
    }
    :return:{
      "code":"00000",
      "errorinfo":"message",
       "result": True,

    }
    """
    try:
        user_id = request.json['userId']
        result = MongoUtil().delete_face_user_user_id(user_id)
        if result.deleted_count > 0:
            return jsonify({
                "code": config.CONST_COMPARE_FACE_SUCCESS,
                "result": True,
                "errorinfo": "deleted %d faces" % result.deleted_count
            })
        else:
            return jsonify({
                "result": False,
                "code": config.CONST_COMPARE_FACE_DELETE_ERROR,
                "errorinfo": "no face delete"
            })
    except KeyError as e:
        logging.error(e)
        abort(500)

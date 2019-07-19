from flask import current_app
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from bson import ObjectId
import threading


class MongoUtil:
    """
        operate mongodb curd, singleton class
        example:
        MongoUtil().insert_face_user
    """

    _instance_lock = threading.Lock()

    def __init__(self):
        # mongo = MongoClient("mongodb://faceDetectAdmin:admin@localhost/face")
        mongo = PyMongo(current_app)
        self._db = mongo.db

    def __new__(cls, *args, **kwargs):
        if not hasattr(MongoUtil, "_instance"):
            with MongoUtil._instance_lock:
                if not hasattr(MongoUtil, "_instance"):
                    MongoUtil._instance = object.__new__(cls)
        return MongoUtil._instance

    def insert_face_user(self, face_user):
        """
        insert face user,is exists modify
        :param face_user:
        :return:
        """
        user = self.find_face_user(face_user['userId'])
        if user is None:
            return self._db.faceUsers.insert_one(face_user)
        else:
            user['userName'] = face_user['userName']
            user['idCard'] = face_user['idCard']
            user['encoding'] = face_user['encoding']
            return self._db.faceUsers.find_one_and_update({'userId': face_user['userId']}, {'$set': user},
                                                          return_document=ReturnDocument.AFTER)

    def find_face_user(self, user_id):
        """
        search single face user
        :param user_id:
        :return:
        """
        return self._db.faceUsers.find_one({'userId': user_id})

    def find_face_users(self, page):
        """
        search single face user
        :param page:{num,size}
        :return:
        """
        page_size = page['size']
        page_num = page['num']
        __last_id = None
        cursor_less = None
        # MongoDB在小于指定条件下，集合总大小
        count_less = self._db.faceUsers.count_documents({})

        if count_less == 0:
            return None

        if page_size > count_less:
            page_size = count_less
        # 查询遍历的次数    circleCountless + 1
        circle_countless = int(count_less / page_size)
        if page_num < circle_countless:
            circle_countless = page_num
            modless = page_size
        else:
            # 取模，这是最后一次循环遍历的次数
            modless = count_less % page_size
        print(modless)
        for i in range(1, circle_countless + 1):
            obj = None
            print(__last_id)
            if __last_id is not None:
                query_less = {'_id': {'$gt': __last_id}}
            else:
                query_less = {}
            cursor_less = self._db.faceUsers.find(query_less).sort('_id').limit(modless)
            if i < circle_countless:
                while cursor_less.alive:
                    obj = cursor_less.next()
                if obj is not None:
                    __last_id = obj['_id']
        result = []
        while cursor_less.alive:
            result.append(cursor_less.next())

        return result

    def delete_face_user_user_id(self, user_id):
        """
        delete user by user id
        :param user_id:
        :return:
        """
        return self._db.faceUsers.delete_one({'userId': user_id})

    def delete_face_user_oid(self, object_id):
        """
        delete user by object id,object is instance by ObjectId class
        :param object_id:
        :return:
        """
        return self._db.faceUsers.delete_one({'_id': ObjectId(object_id)})


# user1 = {
#     "userId": "testUser",
#     "userName": "niuwenji14",
#     "idCard": "idCard",
#     "encoding": "img(base64 or url)"
# }
#
# for i in range(1, 100000):
#     user1 = {
#         "userId": ("testUser" + str(i)),
#         "userName": str("niuwenji" + str(i)),
#         "idCard": "idCard",
#         "encoding": "img(base64 or url)"
#     }
#     MongoUtil.insert_face_user(user1)

# pprint.pprint(len(MongoUtil.find_face_users({'num': 10, 'size': 200})))
# obj1 = MongoUtil()
# obj2 = MongoUtil()
# print(obj1, obj2)
#
#
# def task(arg):
#     obj = MongoUtil()
#     print(obj)
#
#
# for i in range(10):
#     t = threading.Thread(target=task,args=[i,])
#     t.start()
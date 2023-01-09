import redis

redis = redis.Redis(host='singapore-redis.render.com', port=6379, db=0, password='DAe95s9HP2CTSrgheLMDdkfuaoGc10a8',
                    username='red-ceu2v3pa6gdut0r7ca50', ssl=True)
redis.set('test', 'test')

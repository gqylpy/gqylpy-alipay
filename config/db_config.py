class DBS:
    # Database alias
    gqylpy = 'gqylpy'
    hello_world = 'hello_world'

    class Config:
        # Database Config
        gqylpy = dict(
            host='localhost',
            port=3380,
            user='gqy',
            password='user@gqy',
            db='gqylpy',
            charset='utf8',
            autocommit=True,
            connect_timeout=60 * 60 * 24 * 15
        )
        hello_world = dict(
            host='localhost',
            port=3380,
            user='hlwd',
            password='user@hlwd',
            db='hello_world',
            charset='utf8',
            autocommit=True,
            connect_timeout=60 * 60 * 24 * 15
        )


# class DBS:
#     # Database alias
#     gqylpy = 'gqylpy'
#     hello_world = 'hello_world'
#
#     class Config:
#         # Database Config
#         gqylpy = dict(
#             host='106.13.73.98',
#             port=3380,
#             user='zyk',
#             password='Two_cic1314',
#             db='gqylpy',
#             charset='utf8',
#             autocommit=True,
#             connect_timeout=60 * 60 * 24 * 15  # 15 Day
#         )
#         hello_world = dict(
#             host='106.13.73.98',
#             port=3380,
#             user='zyk',
#             password='Two_cic1314',
#             db='hello_world',
#             charset='utf8',
#             autocommit=True,
#             connect_timeout=60 * 60 * 24 * 15
#         )

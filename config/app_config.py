class AppInitConfig:
    # App init config
    ...


# App startup parameter config
START_PARAMETER = dict(
    host='127.0.0.1',
    port=98,
    debug=False,
    workers=2,
)


class Response:
    code: int
    msg: str
    data: dict

    @property
    def dict(self):
        return self.__dict__

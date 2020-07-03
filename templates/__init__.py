from tools import gen_path
from config import FE
from config import TEMPLATES_DIR


class HTMLData:

    _flags = '-1234567890'  # Don't change

    def __init__(self):
        self.index_html = self._load_html('index.html')
        self.download = self._load_html('download.html')
        self.get_pwd = self._load_html('get_pwd.html')
        self.show_pwd = self._load_html('show_pwd.html')
        self.query_order = self._load_html('query_order.html')
        self.goods = self._load_html('goods.html')
        self.purchase_good = self._load_html('purchase_good.html')
        self.un_show = self._load_html('un_show.html')
        self.get_wlmj_pwd = self._load_html('get_wlmj_pwd.html')
        self.batch_download = self._load_html('batch_download.html')

    def _load_html(self, filename: str) -> str:
        # HTML data is added from disk to memory.
        fp = open(gen_path(TEMPLATES_DIR, filename), encoding=FE)
        data = fp.read()
        fp.close()
        return data

    def _replace(self, data: str, mapping: dict) -> str:
        for original, update in mapping.items():
            original += self._flags
            data = data.replace(original, str(update))
        return data

    def come_on(self, data: str, mapping: dict) -> str:
        """Replace characters in HTML pages.

        Substitution characters:
            index.html: tip
            download.html: title, rid
            get_pwd.html: title, price, rid, QQ
            show_pwd.html: title, QQ
            query_order.html:
            get_wlmj_pwd.html: title, rid, price, QQ
        """
        return self._replace(data, mapping)


# Singleton class.
hd = HTMLData()

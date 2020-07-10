#!python3
# coding: utf-8
"""
歌唱データベース用のLABファイルとデータを扱うモジュールです。
"""


def main():
    """実行されたときの挙動"""
    print('呼び出しても使えませんが...')


def load(path, mode='r', encoding='utf-8', kiritan=False):
    """
    labファイルを読み取ってLabクラスオブジェクトにする
    時刻を整数にすることに注意
    """
    # labファイル読み取り
    with open(path, mode=mode, encoding=encoding) as f:
        lines = [s.strip().split() for s in f.readlines()]
    # 入力ファイル末尾の空白行を除去
    while lines[-1] == ['']:
        del lines[-1]

    # リストにする [[開始時刻, 終了時刻, 発音], [], ...]
    if kiritan:
        # きりたんDBのモノラベル形式の場合、時刻が 0.0000000[s] なのでfloatを経由する。
        l = [[int(10000000 * float(v[0])), int(10000000 * float(v[1])), v[2]] for v in lines]
    else:
        # Sinsyのモノラベル形式の場合、時刻が 1234567[100ns] なのでintにする。
        l = [[int(v[0]), int(v[1]), v[2]] for v in lines]
    # Labelクラスオブジェクト化
    lab = Label()
    lab.values = l
    return lab


class Label:
    """
    歌唱ラベルLABファイルを想定したクラス(2019/04/19から)
    """

    def __init__(self):
        """二次元リスト [[開始時刻, 終了時刻, 発音], [], ...]"""
        self.__values = []

    @property
    def values(self):
        """propertyはgetterも兼ねるらしい"""
        return self.__values

    @values.setter
    def values(self, lines):
        """値を登録"""
        if not isinstance(lines, list):
            raise TypeError('"lines" must be list instance (values.setter in label.py)')
        self.__values = lines

    def write(self, path, mode='w', encoding='utf-8', newline='\n', kiritan=False):
        """LABを保存"""
        # 出力用の文字列
        s = ''
        lines = self.values
        if kiritan:
            for l in lines:
                s += '{:.7f} {:.7f} {}\n'.format(*l)
        else:
            for l in lines:
                s += '{} {} {}\n'.format(*l)
        # ファイル出力
        with open(path, mode=mode, encoding=encoding, newline=newline) as f:
            f.write(s)
        return s


if __name__ == '__main__':
    main()

if __name__ == '__init__':
    pass

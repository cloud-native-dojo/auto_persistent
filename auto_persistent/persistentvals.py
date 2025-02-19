import pickle
import os

class PersistentVals:
    def __init__(self, filepath):
        """コンストラクタ: ファイルパスを設定し、データをロードする"""
        self.filepath = filepath
        self._data = self._load()
        self.first_write = True
        print(f"[DEBUG] ロードされたデータ: {self._data}")
    
    def _load(self):
        """ファイルからデータをロードする"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "rb") as f:
                    print("[DEBUG] データをロード中...")
                    data = pickle.load(f)
                    print(f"[DEBUG] 読み込まれたデータ: {data}")
                    return data
            except Exception as e:
                print(f"[ERROR] データの読み込みに失敗しました: {e}")
        print("[DEBUG] 保存されたデータが見つかりません。新しいデータを作成します。")
        return {}
    
    def _save(self):
        """データをファイルに保存する"""
        try:
            with open(self.filepath, "wb") as f:
                pickle.dump(self._data, f)
                print("[DEBUG] データを保存しました。")
        except Exception as e:
            print(f"[ERROR] データの保存に失敗しました: {e}")
    
    def __setattr__(self, key, value):
        """属性を設定するときにデータを保存する"""
        if key in ["filepath", "_data", "_load", "_save", "__setattr__"]:
            super().__setattr__(key, value)
        else:
            if key not in self._data:
                print(f"[DEBUG] {key} が見つかりません。初期値を設定します。")
                self._data[key] = value
                self._save()
            else:
                if self.first_write:
                    pass
                else:
                    print(f"[DEBUG] {key} に値 {value} を設定し、保存します。")
                    self._data[key] = value
                    self._save()
                    self.first_write = False
    
    def __getattr__(self, key):
        """属性を取得する際にデフォルトを提供"""
        if key in self.__dict__:
            return self.__dict__[key]
        print(f"[DEBUG] {key} の値を取得します。")
        self._save()
        return self._data.get(key, [])
    
    def __getitem__(self, key):
        """辞書のようにキーを取得"""
        print(f"[DEBUG] __getitem__ で {key} を取得します。")
        return self._data.get(key, [])
    
    def __setitem__(self, key, value):
        """辞書のようにキーに値をセットし、保存"""
        print(f"[DEBUG] __setitem__ で {key} に値 {value} を設定し、保存します。")
        self._data[key] = value
        self._save()

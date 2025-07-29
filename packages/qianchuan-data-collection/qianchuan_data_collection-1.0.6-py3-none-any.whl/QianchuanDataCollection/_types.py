class DotDict(dict):
    """
    支持点号访问的 dict，支持严格模式控制：
    - strict=True 时，访问不存在的属性抛出 AttributeError
    - strict=False 时，访问不存在的属性返回 None
    """

    def __init__(self, *args, strict=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._strict = strict

    def __getattr__(self, key):
        if key not in self:
            if self._strict:
                raise AttributeError(f"属性 '{key}' 不存在")
            return None
        value = self[key]
        if isinstance(value, dict):
            return DotDict(value, strict=self._strict)
        elif isinstance(value, (list, tuple)):
            # 列表/元组中如果包含 dict，也递归转换
            return [
                DotDict(v, strict=self._strict) if isinstance(v, dict) else v
                for v in value
            ]
        elif isinstance(value, (int, float, str, bool, type(None))):
            return value
        else:
            raise TypeError(f"属性 '{key}' 的值不是 dict，无法使用 '.' 访问")

    def __setattr__(self, key, value):
        if key == '_strict':
            super().__setattr__(key, value)
        else:
            self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]
        else:
            raise AttributeError(f"没有属性 '{key}'")

import inspect


class DiContainer:
    def __init__(self):
        self.objects = dict()

    def __getitem__(self, item):
        if item not in self.objects:
            self.objects[item] = self.construct_obj(item)
        return self.objects[item]

    def construct_obj(self, item):
        sign = inspect.signature(item)
        params = sign.parameters
        dict_params = {}
        for param_name in params:
            param = params[param_name]
            dict_params[param.name] = self[param.annotation]

        return item(**dict_params)

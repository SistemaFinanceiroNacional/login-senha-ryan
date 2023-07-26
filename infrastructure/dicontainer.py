import inspect


class DiContainer:
    def __init__(self):
        self.objects = dict()
        self.parameters = dict()
        self.provision = dict()

    def __getitem__(self, item):
        if item not in self.objects:
            self.objects[item] = self.construct_obj(item)
        return self.objects[item]

    def __setitem__(self, key, value):
        self.objects[key] = value

    def set_parameter(self, key, value):
        self.parameters[key] = value

    def construct_obj(self, item):
        if item in self.provision:
            return self[self.provision[item]]

        sign = inspect.signature(item)
        params = sign.parameters
        dict_params = {}
        for param_name, param in params.items():
            if param_name in self.parameters:
                dict_params[param_name] = self.parameters[param_name]
            else:
                dict_params[param_name] = self[param.annotation]

        return item(**dict_params)

    def provide(self, interface, implementation):
        self.provision[interface] = implementation

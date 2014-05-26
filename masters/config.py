# vim: set ts=8 sw=4 sts=4 tw=99 et ft=python :
import yaml

class Config(object):
    def __init__(self, filename):
        super(Config, self).__init__()

        with open(filename, 'r') as fp:
            self.cfg = yaml.load(fp)
            self.globals_ = self.cfg['global']

    def slave_password(self, name):
        return self.globals_['slave-password']

    def debug_password(self):
        return self.globals_.get('debug-password', None)

    def get_list(self, name):
        return self.globals_.get(name, [])

    def get(self, name):
        return self.globals_[name]

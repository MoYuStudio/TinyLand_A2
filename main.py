
import sys
sys.dont_write_bytecode = True

import moyu_engine as engine
import moyu_engine.system.module as module

a = module.jsondata.JsonData()

print(a.__doc__)
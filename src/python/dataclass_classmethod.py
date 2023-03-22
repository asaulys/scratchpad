from dataclasses import dataclass

# this is nice when you want to store data
@dataclass
class Grid(object):
  x = 1
  y = 2
  z = 3

  @classmethod
  def resolve(cls,item):
    return getattr(cls, item)

# Grid.resolve("x")
# 1


# if the data is static, use an enum
# WARNING: remember to unpack the value via method call value()
class Grid2(Enum):
  x = 1
  y = 2
  z = 3

  @classmethod
  def resolve(cls, item):
    return getattr(cls, item).value
 

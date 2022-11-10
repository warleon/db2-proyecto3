import flask

dataPath = "../data/"
indexPath="../index/Rtree"
config =index.Property()
config.dimension = 128
idx = index.Rtree(indexPath,properties=config,interleaved=False)
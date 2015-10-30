# IdxFileParser #

IdxFileParser is parser to read IDX format file, such as [MNIST Database](http://yann.lecun.com/exdb/mnist/).

## usage ##

```python
import IdxFileParser as idx

images = idx.IdxFileParser("./train-images-idx3-ubyte").to_ndary()
labels = idx.IdxFileParser("./train-labels-idx1-ubyte").to_ndary()
```

See IdxFileParserNotebook.ipynb.

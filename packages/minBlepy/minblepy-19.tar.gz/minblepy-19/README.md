# minBlepy
MinBLEPs library including fast naive waveform conversion.

## Install
These are generic installation instructions.

### To use, disposably
Install the current release from PyPI to a virtual environment:
```
python3 -m venv venvname
venvname/bin/pip install -U pip
venvname/bin/pip install minBlepy
. venvname/bin/activate
```

### To use, permanently
```
pip3 install --break-system-packages --user minBlepy
```
See `~/.local/bin` for executables.

### To develop
First install venvpool to get the `motivate` command:
```
pip3 install --break-system-packages --user venvpool
```
Get codebase and install executables:
```
git clone git@github.com:combatopera/minBlepy.git
motivate minBlepy
```
Requirements will be satisfied just in time, using sibling projects with matching .egg-info if any.

## API

<a id="minBlepy"></a>

### minBlepy

<a id="minBlepy.floatdtype"></a>

###### floatdtype

Common data type of naive values and digital audio sample points, effectively about 24 bits.

<a id="minBlepy.minblep"></a>

### minBlepy.minblep

<a id="minBlepy.minblep.MinBleps"></a>

#### MinBleps Objects

```python
class MinBleps()
```

<a id="minBlepy.minblep.MinBleps.paste"></a>

###### paste

```python
def paste(naivex, diffbuf, outbuf)
```

Add minBLEPs to `outbuf` for the differentiated naive signal block in `diffbuf`.
The first element of `diffbuf` should be the first naive value in the current block minus the last naive value of the previous block.
The `naivex` is the index of the first naive value, modulo `naiverate`.
The `outbuf` must have enough space for overflow of the last possible minBLEP, and should be initialised to the overflow section of the previous `outbuf` and otherwise zero.


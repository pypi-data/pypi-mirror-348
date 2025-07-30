# winmemory

Open progress

```python
from winmemory import *
game=winmemory.winmemory('game.exe')
```
Write and read data of an address
```python
game.write_int(0xE2CA7FF85C,10)
data=game.read_int(0xE2CA7FF85C)
print(data)
#--->Address a is assigned the value 10
#Can also read and write to many other data types, such as string, byte, long, double, float,...

```
Get base address of module
```python
module_addr=game.get_module_base_address('game.exe')
```
Find_pointer_address
```python
pointer=game.find_pointer_address(base,offset)
```
Get pip of progress
```python
pid=getpid('ganme.exe')
```
Scan all addresses with the value you want
```python
pid=getpid('ganme.exe')
scaned=scan_all_addresses_with_value(pid,10)
#scan all addresses with value 10
```
Thanks from Phan Huynh Thien Phu


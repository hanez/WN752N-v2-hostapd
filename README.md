#HOW TO USE IT 
## install dependencies
```
sudo apt-get install libnl-genl-3-dev
sudo apt-get install libnl-3-dev
```
## builds
```
cd hostapd
cp defconfig .config
echo CONFIG_DRIVER_RTW=y >> .config
echo CONFIG_LIBNL32=y >> .config
make -j4
```



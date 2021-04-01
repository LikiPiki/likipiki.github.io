---
title: "NRF Micro bootloader unlock"
date: 2021-03-01T20:52:39+03:00
tags: ["keyboard", "QMK", "nrfmicro"]
author: ["likipiki"]
categories: ["keyboards"]
ShowToc: true
cover:
    image: "/posts/images/nrf.JPG"
weight: 1
draft: false
---

## Разблокировка загрузчика NrfMicro 1.4

Я использую Arch linux поэтому все команды приведены для этой операционной
системы.

### Делаем из BluePill Blackmagic

```
sudo pacman -S stlink arm-none-eabi-gdb
```

Подключаем ST-Link к BluePill, `boot0` ставит в положение 0. И зашиваем два
бинарника следующими командами. Файлы [`blackmagic_dfu.bin`](/posts/files/blackmagic_dfu.bin) и [`blackmagic.bin`](/posts/files/blackmagic.bin).

```
st-flash write blackmagic_dfu.bin 0x08000000
st-flash write blackmagic.bin 0x08002000
```

После успешной прошивки, необходимо переставить `boot0` в положение 0 воткнуть
BluePill через USB в компьютер.

Проверим что устройство появилось:

```
lsusb
```

Наша устройство должно появиться в списке USB устройств.

```bash3
...
Bus 001 Device 009: ID 1d50:6018 OpenMoko, Inc. Black Magic Debug Probe (Application)
...
```

Так же посмотрим порт нашего устройства:
```
sudo dmesg | grep tty
```

## Разблокировка Загрузчика NRF52840

```
[ 6813.936071] cdc_acm 1-3:1.0: ttyACM0: USB ACM device
[ 6813.941697] cdc_acm 1-3:1.2: ttyACM1: USB ACM device
```
В последних подключенных устройствах мы увидим следующее:

* `ttyACM0` --- это Black Magic GDB server.
* `ttyACM1` --- Это Black Magic UART Port

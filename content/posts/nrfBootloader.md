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

### Подготовка
Я использую linux поэтому все команды приведены для этой операционной системы.
Для начала установим все необходимые зависимости:

Arch Linux:
```
sudo pacman -S stlink arm-none-eabi-gdb
```
Mac OS:
```
brew install stlink arm-none-eabi-gdb
```

### Необходимые файлы 
1. Для Black Magic [`blackmagic_dfu.bin`](/posts/files/blackmagic_dfu.bin),  [`blackmagic.bin`](/posts/files/blackmagic.bin).
2. Бутлоадер для NRF52840 [`bootloader.hex`](/posts/files/bootloader.hex).

Для удобства можно закинуть все файлы в одну папку, все последующие команды
запускать из нее.
```bash
./nrf/
  |  bootloader.hex
  |  blackmagic_dfu.bin
  |  blackmagic.bin
```
### Делаем из BluePill Blackmagic

Подключаем ST-Link к BluePill, `boot0` ставит в положение 0. И зашиваем два
бинарника следующими командами:

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

Black Magic должен появиться в списке USB устройств.

```bash3
...
Bus 001 Device 009: ID 1d50:6018 OpenMoko, Inc. Black Magic Debug Probe (Application)
...
```

### Разблокировка Загрузчика NRF52840
Посмотрим порты, которые используются Black Magicом:

```
sudo dmesg | grep tty
```

```
[ 6813.936071] cdc_acm 1-3:1.0: ttyACM0: USB ACM device
[ 6813.941697] cdc_acm 1-3:1.2: ttyACM1: USB ACM device
```
В последних подключенных устройствах мы увидим следующее:

* `ttyACM0` --- Black Magic GDB server.
* `ttyACM1` --- Black Magic UART Port

Для загрузки бутлоадера в NrfMicro нам нужен только GDB server. Поэтому дальше я
буду использовать `/dev/ttyACM0`.

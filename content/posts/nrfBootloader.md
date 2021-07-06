---
title: Разблокировка загрузчика nRFMicro 1.4
date: 2021-04-01T20:52:39.000+03:00
description: Разблокировка загрузчика nRFMicro 1.4 на Linux
tags:
- Keyboard
- NRFMicro
- ZMK
- Linux
author:
- likipiki
categories:
- keyboards
ShowToc: true
cover:
  image: "/posts/nrfBootloader/nrf.jpeg"
editPost:
    URL: "https://gitlab.com/likipiki/likipiki.gitlab.io/-/tree/master/content/"
    Text: "Предложить изменения"
    appendFilePath: true
---
### Подготовка

Я использую linux поэтому все команды приведены для этой операционной системы. Для начала, установим все необходимые зависимости:

Arch Linux:
```
sudo pacman -S stlink arm-none-eabi-gdb
```

Mac OS:
```
brew install stlink arm-none-eabi-gdb lsusb
```
### Необходимые файлы

1. Для Black Magic [`blackmagic_dfu.bin`](/posts/files/blackmagic_dfu.bin),  [`blackmagic.bin`](/posts/files/blackmagic.bin).
2. Бутлоадер для nRF52840 [`bootloader.hex`](/posts/files/bootloader.hex).
> С недавнего времени появился новый бутлоадер, в котором используется синий
   светодиод на плате nRFMicro. Мигает при ресете и режиме бутлоадера. Очень
   удобно советую использовать далее его
   [`led_bootloader.hex`](/posts/files/led_bootloader.hex) команды для прошивки
   такие же. Просто скачайте и переименуйте в `bootloader.hex`.

Для удобства можно закинуть все файлы в одну папку, все последующие команды запускать из нее.

```bash
./nrf/
  |  bootloader.hex
  |  blackmagic_dfu.bin
  |  blackmagic.bin
```

### Делаем из BluePill Blackmagic

Подключаем ST-Link к BluePill, `boot0` ставит в положение `1`. И зашиваем два бинарника следующими командами:
```bash
st-flash write blackmagic_dfu.bin 0x08000000
st-flash write blackmagic.bin 0x08002000
```
После успешной прошивки, необходимо переставить `boot0` в положение `0` воткнуть BluePill через USB в компьютер.

Проверим что устройство появилось:
```
lsusb
```

Black Magic должен появиться в списке USB устройств.

```
...
Bus 001 Device 009: ID 1d50:6018 OpenMoko, Inc. Black Magic Debug Probe (Application)
...
```

### Разблокировка Загрузчика nRF52840

Посмотрим порты, которые используются Black Magicом:
```bash
sudo dmesg | grep tty

[ 6813.936071] cdc_acm 1-3:1.0: ttyACM0: USB ACM device
[ 6813.941697] cdc_acm 1-3:1.2: ttyACM1: USB ACM device
```

> Есть еще один способ посмотреть чем заняты порты `ls /dev/tty.*`

В последних подключенных устройствах мы увидим следующее:

* `ttyACM0` --- Black Magic GDB server
* `ttyACM1` --- Black Magic UART Port

Для загрузки бутлоадера в nRFMicro нам нужен только GDB server. Поэтому дальше я буду использовать `/dev/ttyACM0`.

Подключаем джамперы к `STM32F103C8T6` Black Magic. `B14` --- `SWD`, `A5` ---
`SWC`. Вторые концы джамперов соединяем с соответствующими контактами на nRFMicro.

Разблокируем загрузчик:

```bash
sudo arm-none-eabi-gdb --batch -ex "target extended-remote /dev/ttyACM0" -ex "mon swdp_scan" -ex "att 1" -ex "mon erase_mass"

Target voltage: unknown
Available Targets:
No. Att Driver
 1      Nordic nRF52 M3/M4
 2      Nordic nRF52 Access Port
0x00000a60 in ?? ()
erase..
Error erasing flash with vFlashErase packet
Can't detach process.
```

Зашиваем бутлоадер:

```bash
sudo arm-none-eabi-gdb --batch -ex "target extended-remote /dev/ttyACM0" -ex "mon swdp_scan" -ex "file bootloader.hex" -ex "att 1" -ex "mon erase" -ex load

Target voltage: unknown
Available Targets:
No. Att Driver
 1      Nordic nRF52 M3/M4
 2      Nordic nRF52 Access Port
0xfffffffe in ?? ()
erase..
Loading section .sec1, size 0xb00 lma 0x0
Loading section .sec2, size 0xf000 lma 0x1000
Loading section .sec3, size 0x10000 lma 0x10000
Loading section .sec4, size 0x5de8 lma 0x20000
Loading section .sec5, size 0x70c8 lma 0xf4000
Loading section .sec6, size 0x8 lma 0x10001014
Start address 0x00000000, load size 182712
Transfer rate: 27 KB/sec, 966 bytes/write.
[Inferior 1 (Remote target) detached]
```

Если все сделано правильно, то можно перевоткнуть USB-C у прожоры. После этого
на компьютере появится Mass Storage Device в который можно будет заливать
прошивку для клавиатуры.

### Проблемы и их решения

> #### 1. Модуль не прошивается

Если модуль не прошивается или не стирается бутлоадер, проверьте мультиметром
плату на короткое замыкание. Между `GND` и `VCC` должно быть напряжение отличное
от 0 вольт.

Проверьте пайку контактов 37 -- `SWD`, 39 -- `SCL`. Это два вывода около пина `0.09`.

![SWD пады](/posts/nrfBootloader/swdfix.png)

> #### 2. Не работает OLED дисплей

Скорее всего не допаяны пины шины `I2C`, это внутренние два пада (28, 30) на модуле.
Пройдитесь хорошо по ним паяльником с флюсом, если у вас есть тонкое жало,
можно залезть им в сквозное отверстие и хорошо прогреть.

![I2C пады](/posts/nrfBootloader/i2cfix.png)

### Ссылки
- [Сборка nRFMicro 1.4]({{< ref "nrfBuild.md" >}})

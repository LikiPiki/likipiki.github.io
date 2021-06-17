---
title: "QMK. Сборка и прошивка"
date: 2021-04-29T09:54:44+03:00
description: ""
categories:
- keyboards
tags:
- keyboard
- QMK
author:
- likipiki
ShowToc: true
TocOpen: false
draft: false
---
# Сборка из официального репозитория

Для того чтобы начать вам понадобиться установить несколько утилит:
- `git` --- для работы с git репозиторием `QMK`
- `make` --- утилита для сборки `QMK` прошивки
- `avrdude` --- утилита для прошивки микроконтроллеров `Atmel`

Пример установки для операционной системы Arch Linux и пакетного менеджера
pacman:

```bash
sudo pacman -S git make avrdude
```

Если вы используете другую операционную систему или пакетный менеджер, то
процесс установки будут отличаться.

## Шаг 1. Клонируем репозиторий QMK

```
git clone https://github.com/qmk/qmk_firmware
cd qmk_firmware
```

## Шаг 2. Устанавливаем подмодули
```
git submodule init
git submodule update
```

## Шаг 3. Устанавливаем зависимости

```
bash ./util/qmk_install.sh
```

Здесь потребуется ввести пароль от `sudo`, установятся необходимые зависимости
для сборки, немного подождать пока все скачается и установится.

## Шаг 4. Сборка прошивки для клавиатуры
### Структура файлов

`QMK` использует очень удобную структуру файлов. В папке
[keyboards](https://github.com/qmk/qmk_firmware/tree/master/keyboards)
располагаются
всевозможные клавиатуры доступные для сборки.

Внутри каждой папке с клавиатурой (для примера я взял
[crkbd](https://github.com/qmk/qmk_firmware/tree/master/keyboards/crkbd))
используется следующая структура файлов:

```bash
./crkbd/
  default/
    |  config.h
    |  rules.mk
    |  keymap.c
```

В каждом кеймапе содержатся настройки и раскладка `keymap.c`.

### Сборка
Для сборки используется команда `make`. В общем виде это можно записать так:
```bash
make клавиатура:раскладка
```
Если не указывать раскладку то соберется с раскладкой `default`. А вот так можно
собрать прошивку для клавиатуры `crkbd` с раскладкой `edvorakjp`.

```bash
make crkbd:edvorakjp
```

```
QMK Firmware 0.12.41
Making crkbd/rev1/legacy with keymap edvorakjp
...
Creating load file for flashing: .build/crkbd_rev1_legacy_edvorakjp.hex  [OK]
Copying crkbd_rev1_legacy_edvorakjp.hex to qmk_firmware folder           [OK]
Checking file size of crkbd_rev1_legacy_edvorakjp.hex                    [OK]
 * The firmware size is fine - 24770/28672 (86%, 3902 bytes free)
```

В результате сборки мы получим файл `crkbd_rev1_legacy_edvorakjp.hex` который
находится в директории `.build`.

## Шаг 5. Прошивка

Есть несколько способов прошивки, первый самый простой, второй немного
посложнее. В каждом из них перед тем как вызывать последнюю команду, которая
прошивает микроконтроллер, вам необходимо:
- Подключить промикру в компьютер
- Нажать ресет на промикре
- У вас есть несколько секунд чтобы начать загружать прошивку

### Способ 1

Собираем (keymap default) и сразу прошиваем:
```
make crkbd:default:flash
```

```bash
QMK Firmware 0.12.41
Making crkbd/rev1/legacy with keymap default and target flash

avr-gcc (GCC) 8.3.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Size before:
   text	   data	    bss	    dec	    hex	filename
      0	  21766	      0	  21766	   5506	.build/crkbd_rev1_legacy_default.hex

Copying crkbd_rev1_legacy_default.hex to qmk_firmware folder         [OK]
Checking file size of crkbd_rev1_legacy_default.hex                  [OK]
 * The firmware size is fine - 21766/28672 (75%, 6906 bytes free)
Detecting USB port, reset your controller now........
```
Теперь нужно только нажать ресет на промикре и подождать пока прошивка
загрузится.

### Способ 2
Подключаем промикру к компьютеру.

```
lsusb
```

В списке устройств должна появиться наша подключенная промикра:

```
...
Bus 001 Device 004: ID 2341:0037 Arduino SA Arduino Micro
...
```

Посмотрим на каком порту она находится с помощью команды:

```
sudo dmesg | grep tt
```

Вводим пароль от `sudo` и в самом конце вывода (последнее подключенное в USB
устройство) получаем что-то на подобие такого:
```bash
[ 5154.894321] cdc_acm 1-3:1.0: ttyACM0: USB ACM device
```

Значит наша промикра использует порт `/dev/ttyACM0`. Это именно в моем случае,
естественно у вас это может любой другой порт.

Прошиваем (обязательно жмем ресет на промикре перед этим).
```bash
avrdude -p atmega32u4 -P /dev/ttyACM0 -c avr109  -e -U flash:w:crkbd_rev1_legacy_default.hex
```

### Сплит клавиатуры

Для того чтобы можно было подключать по проводу любую половинку в компьютер, а
не только правую, необходимо загрузить в энергонезависимую память
микроконтроллера (EEPROM) следующие данные. Они хранятся в официальном репозитории вот
тут
[/quantum/split_common](https://github.com/qmk/qmk_firmware/tree/master/quantum/split_common).
Для левой половинки
[eeprom-lefthand.epp](https://github.com/qmk/qmk_firmware/blob/master/quantum/split_common/eeprom-lefthand.eep),
и для правой половинки
[eeprom-righthand.epp](https://github.com/qmk/qmk_firmware/blob/master/quantum/split_common/eeprom-righthand.eep)

Прошиваем (EEPROM) левой половинки:
```
avrdude -p atmega32u4 -P /dev/ttyACM0 -c avr109 -U eeprom:w:eeprom-lefthand.eep
```

Прошиваем (EEPROM) правой половинки:
```
avrdude -p atmega32u4 -P /dev/ttyACM0 -c avr109 -U eeprom:w:eeprom-lefthand.eep
```

# Ссылки
- [Официальный репозиторий QMK](https://github.com/qmk/qmk_firmware)

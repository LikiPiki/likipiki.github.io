
---
title: "Macropad building guide"
date: 2021-01-26T20:52:39+03:00
tags: ["keyboard", "buildGuide", "macropad", "draft"]
author: ["Likipiki"]
draft: true
ShowToc: false
---

# BIll of materials

*Внимание, статья только в разработке!*

## Обязательно для сборки:
* STM32F103C8T6
* 12 Cherry MX Switches
* [SPDT переключатель](https://a.aliexpress.com/_ADvcqv). Необходим для настройки BOOT положений, для прошивки и отладки макропада.
* [Pin Headers](https://aliexpress.ru/item/4000694229610.html?spm=a2g0o.productlist.0.0.78436ce8m8DEWX&algo_pvid=27f529fa-ec0c-4d94-a61f-38ad9f635642&algo_expid=27f529fa-ec0c-4d94-a61f-38ad9f635642-0&btsid=0b8b15d416116924300031962eb5c8&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_&sku_id=10000006047835005), для пайки разъема отладки через программатор ST-Link.
* [LD11117S33TR](https://aliexpress.ru/item/32963420506.html?spm=a2g0o.productlist.0.0.59af385ajJGDAl&algo_pvid=f84067ac-eb15-4cd2-bcaa-0263204c0365&algo_expid=f84067ac-eb15-4cd2-bcaa-0263204c0365-0&btsid=0b8b035a16116928233891494ea9a3&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_&sku_id=66602096366) стабилизатор питания на 3.3 Вольта.

| Обозначение | Название | Тип корпуса | Количество |
|-------------|----------|-------------|------------|
|C1,  C2,  C4, C5, C6| 100 nf | 0805 |5|
|C3, C9 | 1 uf | 0805 |2|
|C7, C8| 20 pf| 0805| 2|
| R1, R2 | 470 Ом| 0805 | 2 |
| R3, R5 | 20 Ом | 0805 | 2 |
| R6, R7, R8, R9 | 4k7 | 0805 | 4 |
| SW13 (RESET) | [Кнопка сброса](https://aliexpress.ru/item/32696590759.html?spm=a2g0o.productlist.0.0.1c843ddazzfJiC&algo_pvid=9ba2d7e0-02ba-43e3-9c4d-d8ae568e61dc&algo_expid=9ba2d7e0-02ba-43e3-9c4d-d8ae568e61dc-26&btsid=0b8b035916116930670572095e3578&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_&sku_id=60650490848) | SMD | 1 |
| Y1 | [Кварц 8 Мгц](https://aliexpress.ru/item/4001044828705.html?spm=a2g0o.productlist.0.0.4b6476678qo18x&algo_pvid=f3fb7e40-1564-492a-b2a9-f8f3001ae0e3&algo_expid=f3fb7e40-1564-492a-b2a9-f8f3001ae0e3-0&btsid=0b8b035a16116929041211694ea9a3&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_&sku_id=10000013722210275) | 3225 | 1 |

## Опционально
* RGB светодиды [`SK6812MINI-e`](https://aliexpress.ru/item/4000475685852.html?spm=a2g0o.productlist.0.0.6d8650f7f1viuP&algo_pvid=165a11e3-f93a-423c-96a0-12d398eae10c&algo_expid=165a11e3-f93a-423c-96a0-12d398eae10c-0&btsid=0b8b034a16116919550132891eb60b&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_) (работают по протоколу WS2812), но не совместимые с ними. SK6812Mini-e развернуты на 90 градусов по пинам.



## Порядок сборки


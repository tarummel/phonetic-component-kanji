# Kanji Phonetic Component Sets

(or KPCS for short)

## Project Description

This repo attempts to programmatically generate all phonetic component and "semantic component" sets for roughly ~6900 
kanji. Technical details below. If you don't know what that is but you've studied kanji before, chances are you've seen 
this phenomena already maybe without realizing it.

## Background Information

To start, we need a quick lesson on the Chinese language. Japanese derives form Chinese. Chinese hanji are logograms 
or symbols that represent something. They do NOT represent a sound like in English alphabet. Instead of creating
a new sound for each hanzi, which would be impractical, they utilized **phonetic** and **semantic** component hints.
These hints, when known, can be interpreted to help guide our understanding of these characters. Flashback lesson over.

The criteria of a **phonetic component** is:
- they share at least one phonetic on'yomi reading
- they share a component (the original kanji being compared against)

A **phonetic component** (**phono_component_set** in the file) value manifests when other phonetic components of the same
family are grouped together. By identifying the baser kanji it is possible to learn a whole group of kanji's on'yomi 
reading.

A **semantic component** (**component_only_set** in the file) is any kanji that only shares the component. A kanji that 
fails the first criteria above falls into this set BUT sharing a component and sharing a kanji is more nuanced then that.
Example 3 below shows off the semantic component value when applicable.

But before you look at the examples. I recomend taking a look at the Content section if you haven't already. Familiarize
yourself as they'll be 

## Examples

### Example 1: (Nearly) Perfect Phonetic Component

|     | 交  |  較  | 絞  | 効  |  佼  | 郊  | 校  |  效  | 蛟  | 咬  |  鵁  | 纐  | 傚  |  餃  | 皎  | 狡  |  鮫  | 駮  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kou |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |     |

Shown above is 交's entry. Each column is either itself (added for your convenience) plus the kanji from the 
entry's **phono-component** and **component only** sets. With a row for each on'yomi reading in the entry (just "kou" in
this case). With "O" marks denoting a phonetic-component match. 

Notice how nearly every kanji is a match. What this means is that any time you see 交 in a kanji 
you can immediately determine its on'yomi pronunciation must be "kou". That hint is what it means to be a phonetic 
component. As for the exception 駮, conveniently its an archaic non-Jouyou kanji and so unimportant.

### Example 2: Normal Case

|      |  生  | 牲  | 惺  |  醒  | 猩  | 旌  | 姓  |  性  |  星 | 甥  |  腥  | 嶐  | 徃  |  薩  | 窿  |  甦  | 産  | 隆  |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sei  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |     |     |     |     |     |     |     |
| shou |  O  |     |     |     |  O  |  O  |  O  |  O  |  O  |  O  |  O  |     |     |     |     |     |     |     |

Here's a more average example. Not all kanji are created equally. We see here a some trends but also a lot of exception.
Personally I don't recommend memorizing every kanji, every reading and every exception. It's simply too much. Instead, 
being mindful of these patterns as you learn kanji can be extremely useful and is the whole reason for ~this~ to begin 
with. If you want to be pro-active, checking out the biggest, most reliable kanji in ths data set should be your next 
move.

### Example: Anti-Pattern or Semantic Component?

|     | 金  |  鈞  | 釿  | 錦  |  欽  | 欽  | 淦  |  鍾  | 瀏  | 鐔  |  鎬  | 鎹  | 鎧  |  鋳  | 鈑  | 鋲  |  鐃  | 鍬  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kin |  O  |  O  |  O  |  O  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| kon |  O  |     |     |     |  O  |  O  |     |     |     |     |     |     |     |     |     |     |     |     |
| gon |  O  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |

Let's go over a potential anti-pattern like 金. It has 160 matches in total and the 5 above are only phonetic matches 
(or about 3%). It's looks like the exact opposite of example 1. But bear with me.

First, consider the idea of a **semantic component**. If **phonetic components** are those that can clue us in on the 
*pronunciation* of a certain kanji. Then **semantic components** are clues to the *semantic* meaning of a kanji. Check
out this [Phono-Semantic Compound Character Wikipedia](https://en.wikipedia.org/wiki/Chinese_character_classification#Phono-semantic_compound_characters) page if you want.

Now all we need is Japanese dictionary to complete the puzzle. Consider 金 as a component
- in elemental metals: 銅 (copper), 鉄 (iron) and 鉛 (lead)
- in products made of metal: 針 (needle), 釜 (kettle) and 釣 (fishing)
- and in more abstract metal concepts: 鋭 (sharp tool, sharp mind) and 鈍 (dull tool, slow-witted) 

So in other words, 金 appearence in a kanji suggests a metal-related kanji. 金 is the **semantic component** representing
metal. Bear in mind that not all component matches imply a greater semantic meaning. Unfortunately finding these
groups specifically is outside of this project. Instead consider consulting a dictionary.

## Content

Each `phonetic-component-kanji` file follows the same data structure below. 

| Value Name            | Type                   | Description                                          |
| --------------------- | ---------------------- | ---------------------------------------------------- |
| literal               | String                 | string literal kanji                                 |
| components            | Array<String>          | radicals and kanji parts that form a kanji           | 
| onyomi*               | Array<String>          | the on'yomi reading(s) of the kanji                  |
| component_only_set    | Array<String>          | kanji with only a component match                    |
| phono_component_sets* | Array[Array[String]]   | sets of kanji that share a phono-component           |
| largest_perfect_set   | Integer                | length of the largest phono-component                |
| reliability_rating    | Float                  | percent of phono-component over component only kanji |

\*`phono_component_sets` is sorted by largest set first then the `onyomi` readings are re-arranged to reflect this 
pairing by index when there are phono-component kanji.

## File Formats

### JSON
```json
[
  ...   
  {
      "literal": "句",
      "components": [
          "口",
          "勹",
          "丿"
      ],
      "onyomi": [
          "ク"
      ],
      "component_only_set": [
          "跼",
          "檠",
          "局",
          "驚",
          "警",
          "敬",
          "拘",
          "齣"
      ],
      "phono_component_sets": [
          [
              "煦",
              "蒟",
              "鉤",
              "苟",
              "駒",
              "劬",
              "佝",
              "枸",
              "怐",
              "狗"
          ]
      ],
      "largest_phonetic_set_size": 10,
      "reliability_rating": 0.556
  },
  ...
]
```
Note: The JSON root is a JSON Array (of JSON entries)

### XML
```xml
<?xml version='1.0' encoding='UTF-8'?>
<kspc>
  ...
  <character>
    <literal>玉</literal>
    <components>
      <component>丶</component>
      <component>王</component>
    </components>
    <onyomi>
      <onyomi>ギョク</onyomi>
    </onyomi>
    <componentSet>
      <c_match>壬</c_match>
      <c_match>国</c_match>
      <c_match>宝</c_match>
      <c_match>璧</c_match>
      <c_match>掴</c_match>
      <c_match>璽</c_match>
      <c_match>瑩</c_match>
      <c_match>椢</c_match>
      <c_match>筺</c_match>
    </componentSet>
    <phonoComponentSets>
      <pc_match g="0">閠</pc_match>
    </phonoComponentSets>
    <largestPhoneticSetSize>1</largestPhoneticSetSize>
    <reliabilityRating>0.1</reliabilityRating>
  </character>
  ...
</kspc>
```

Notes:
- The XML root is the `<kspc>` element
- The `g` (group) attribute corresponds to the onyomi's reading at that index

### TVS
```csv
literal	components	onyomi	component_only_set	phono_component_sets	largest_phonetic_set_size	reliability_rating
...
末	['木', '丿']	['マツ', 'バツ']	[]	[['靺', '沫', '茉', '秣', '抹'], ['靺', '沫', '茉', '秣']]	5	1.0
...
```

## Credits
kanjidic2.xml is copyright under the [EDRDG licence](http://www.edrdg.org/edrdg/licence.html). 
KanjiVG's .svgs are copyright of the [KanjiVG Project](http://kanjivg.tagaini.net/)
Inspired by acm2010's WaniKanji Semantic-Phonetic Composition userscript
Shoutout to the (now defunct) Nanbanjin Nikki's melboiko and their writings on the topic

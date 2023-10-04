# Kanji Phonetic Component Sets

(or KPCS for short)

## Project Description

This repo attempts to programmatically generate all phonetic component sets, including "semantic" component sets for 
roughly ~6900 kanji. The final result can be found in any of the  `phonetic-component-kanji` files with additional technical
details provided below along with examples and explanations.

## Background Overview

To start, we need a quick lesson on the Chinese language. Japanese derives from Chinese after all. Chinese hanzi and kanji
are "logograms" or symbols that represent some *thing*. They do NOT represent a sound like in the English alphabet. Instead of
creating a new sound for each symbol, which would be impractical given how many there were, ancient Chinese utilized 
**phonetic** and **semantic** components to instead *embed* the pronunciation and meaning into the character.

Now within the context of Japanese / this project, the criteria for a **phonetic component** kanji is:

- they share at least one phonetic on'yomi reading with another kanji
- that kanji includes this kanji

A **phonetic component** value therefore manifests when other phonetic components of the same "family" are grouped together. 
Learning these specific kanji allows us to assign the on'yomi reading to a whole group of kanji at once.

A **semantic component** are therefore the kanji who meet the second criteria but NOT the first.

## Examples

### Example 1: (Nearly) Perfect Phonetic Component

|     | 交  |  較  | 絞  | 効  |  佼  | 郊  | 校  |  效  | 蛟  | 咬  |  鵁  | 纐  | 傚  |  餃  | 皎  | 狡  |  鮫  | 駮  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kou |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |     |

Shown above is 交's entry (table not normally included). Each column is either itself (added for your convenience) or the
kanji from the entry's `phono_component_sets` and `component_only_set`. One row for each on'yomi reading in the entry 
(just "kou" in this case). "O" marks denote a phonetic-component match. 

Notice how nearly every kanji is a phonetic-component match? It's essentially this, any time you see 交 in a kanji you now
know its on'yomi pronunciation is "kou". 交 is a *very* reliable phonetic component. Meaning it really is that easy. The 
exception 駮 conveniently is an archaic, non-Jouyou kanji and can be safely ignored.

### Example 2: Normal Case

|      |  生  | 牲  | 惺  |  醒  | 猩  | 旌  | 姓  |  性  |  星 | 甥  |  腥  | 嶐  | 徃  |  薩  | 窿  |  甦  | 産  | 隆  |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sei  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |  O  |     |     |     |     |     |     |     |
| shou |  O  |     |     |     |  O  |  O  |  O  |  O  |  O  |  O  |  O  |     |     |     |     |     |     |     |

Here's an example of what you'll usually see, which is low reliability. Unfortunately not all kanji are created equally. 
There are trends but there's also a lot of exceptions. Personally I don't recommend memorizing every kanji, reading and 
exception. Instead, being mindful of these patterns and their existance as you continue learning is what's important. It's 
half the reason for all ~this~ to begin with. If you want to be pro-active, checking out the biggest, most reliable kanji in
the files should be your next move. Prioritizing the "best" kanji is probably the most efficient use of one's time. Which
is kind of the whole other point for this project!

### Example 3: Semantic Component

|     | 金  |  鈞  | 釿  | 錦  |  欽  | 欽  | 淦  |  鍾  | 瀏  | 鐔  |  鎬  | 鎹  | 鎧  |  鋳  | 鈑  | 鋲  |  鐃  | 鍬  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kin |  O  |  O  |  O  |  O  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| kon |  O  |     |     |     |  O  |  O  |     |     |     |     |     |     |     |     |     |     |     |     |
| gon |  O  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |

Let's go over a semantic component like 金. It has 160 matches in total and the 5 above are only phonetic matches (or about
3%). It sorta looks like the opposite of example 1. What value is there in something so unreliable? Simply take a look at a
dictionary for details on all the most common matches for 金:

- elemental metals like 銅 (copper), 鉄 (iron) and 鉛 (lead)
- products made of metal like 針 (needle), 釜 (kettle) and 釣 (fishing)
- abstract metal concepts like 鋭 (sharp tool, sharp mind) and 鈍 (dull tool, slow-witted) 

Notice that 金's appearence is usually on the left position of each kanji? There's a reason. Traditionally the left
position for the semantic component, also called the "hen". It is therefore the first place you should look if you're
searching for a hint. But it's not the only place, like in 釜. This is all to say, 金 is a **semantic component** 
for/meaning metal. Just bear in mind that for various reasons components only matches may not imply a semantic meaning.
Always be sure to consult a dictionary!

## Content

The `phonetic-component-kanji` files all follow the same structure:

| Name                  | Type                   | Description                                           |
| --------------------- | ---------------------- | ----------------------------------------------------- |
| literal               | String                 | string literal kanji                                  |
| components            | Array<String>          | radicals and kanji parts that form a kanji            | 
| onyomi*               | Array<String>          | the on'yomi reading(s) of the kanji                   |
| component_only_set    | Array<String>          | kanji with only a component match                     |
| phono_component_sets* | Array[Array[String]]   | sets of kanji that share a phono-component match      |
| largest_perfect_set   | Integer                | length of the largest phono-component set             |
| reliability_rating    | Float                  | percent of phono-component matches out of all matches |

\*`phono_component_sets` and `onyomi` use matching indices, sorted by the largest phonetic set first when applicable.

## File Formats

### JSON

```json
[
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
]
```

### XML

```xml
<?xml version='1.0' encoding='UTF-8'?>
<kspc>
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
</kspc>
```

Notes:
- The XML root is the `<kspc>` element
- The `g` (group) attribute corresponds to the onyomi's reading at that index

### TVS

```csv
literal	components	onyomi	component_only_set	phono_component_sets	largest_phonetic_set_size	reliability_rating
末	['木', '丿']	['マツ', 'バツ']	[]	[['靺', '沫', '茉', '秣', '抹'], ['靺', '沫', '茉', '秣']]	5	1.0
```

## Credits

kanjidic2.xml is copyright under the [EDRDG licence](http://www.edrdg.org/edrdg/licence.html). 
KanjiVG's .svgs are copyright of the [KanjiVG Project](http://kanjivg.tagaini.net/)
Inspired by acm2010's WaniKani Semantic-Phonetic Composition userscript
Shoutout to the (now defunct) Nanbanjin Nikki's melboiko and their writings on the topic

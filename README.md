# Kakaobot.py
[![license]](/LICENSE)

---

<b>[Kakaobot.py]</b>는 [카카오톡 플러스친구 자동응답 API]를 더 쉽게 사용할 수 있도록 도와주는 라이브러리입니다.
Flask를 통해 구현되어 있습니다.

**Table of Contents**

- [Installation](#installation)
- [Example](#example)
- [Usage](#usage)
  - [Basic structure](#basic-structure)
  - [Class](#class)
    - [Client](#client)
	- [Kboard](#kboard)
	- [Message](#message)
	- [Mbutton](#mbutton)
	- [Photo](#photo)

## Installation

아직 pypi에는 등록을 안했습니다. 그냥 kakaobot 폴더째로 들고가서 쓰시면 되겠습니다.

## Example

https://github.com/Katinor/kakao_bot.py.prac

## Usage

### Basic structure

```py
import kakaobot
app = kakaobot.Client(port = 7900)

##############################
# 원하는 커맨드들을 넣어주세요 #
##############################

app.run()
```

기본적인 구조는 다음과 같습니다. kakaobot.Client를 선언하고, 커맨드들을 등록하고, 선언한 클라이언트가 동작하도록 합니다.

예를 들어 사용자가 "안녕" 이라고 하면 챗봇이 "반가워" 라고 답변하도록 만드는 방법은 다음과 같습니다.

```py
import kakaobot

app = kakaobot.Client(port = 7900)

@app.add_command
def 안녕():
	return kakaobot.Message(text = "반가워")

app.run()
```

카카오톡 플러스친구를 사용해보면, 텍스트 입력은 막혀있고, 버튼을 선택하도록 하는 경우도 있습니다. 이 경우에는 다음과 같이 선언합니다.

```py
import kakaobot

init_kb = kakaobot.Kboard(button = ["안녕"])
app = kakaobot.Client(port = 7900, kboard = init_kb)

@app.add_command
def 안녕():
	return kakaobot.Message(text = "반가워")

app.run()
```

### Class

#### Client

카카오톡 플러스친구 API와 통신하는 클라이언트를 의미합니다. 즉, 챗봇을 의미합니다.
kakaobot.py는 Client를 선언하고 Client.run()을 통해 챗봇을 활성화시킵니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| port | int | Optional | 카카오톡 플러스친구 API와 통신할 웹서버의 포트번호입니다. 생략시 Flask의 기본 포트번호인 5000이 적용됩니다. |
| kboard | [Kboard](#Kboard) | Optional | 챗봇 사용자가 처음으로 이 챗봇의 채팅방에 들어올 때 적용되는 Kboard입니다. 생략시 빈 Kboard 가 적용됩니다. |
| kboard | string | Optional | 사용자가 챗봇에게 전달한 메시지가 커맨드에 등록되어있지 않고, 별도의 처리가 없을 경우 사용자에게 전달되는 메시지입니다. 생략시 "Error occured" 라고 챗봇이 말합니다. |

##### `add_command()`

명령어를 등록하기 위한 데코레이터입니다. 반드시 [Message](#Message) 객체를 반환해야만 합니다.
데코레이터의 대상이 되는 `함수의 이름`이 명령어가 됩니다.
이 데코레이터로 등록된 함수는 사용자가 `명령어를 정확히 말했을 때` 동작합니다.
이 데코레이터로 등록된 함수는 `매개변수가 없어야 합니다.`

```py
@app.add_command
def 안녕(): # 챗봇이 "안녕" 이라는 말을 들을 경우
	return kakaobot.Message(text = "반가워") # "반가워" 라고 답합니다.
```
##### `add_prefix_command()`

명령어를 등록하기 위한 데코레이터입니다. 반드시 [Message](#Message) 객체를 반환해야만 합니다.
데코레이터의 대상이 되는 `함수의 이름`이 명령어가 됩니다.
이 데코레이터로 등록된 함수는 사용자가 `명령어를 첫 어절로 말했을 때` 동작합니다.
이 데코레이터로 등록된 함수는 `하나의 매개변수를 필요로 합니다.`

명령어 부분이 잘린 문자열이 매개변수로 들어가게 됩니다. 예시는 다음과 같습니다.
```py
@app.add_prefix_command
def 따라해(content):
	return kakaobot.Message(text = content)
```
이 경우 "따라해"가 채팅의 첫 단어일 때 동작합니다. 그리고 "따라해"를 제외한 내용이 매개변수로 들어옵니다.
예를 들어 `"따라해 나는 똑똑하다"` 일 경우 따라해가 빠지고 `"나는 똑똑하다"` 가 매개변수로 들어옵니다.

##### `add_regex_command(regex_string)`

`주의 : 아직 테스트하지 않았습니다`

명령어를 등록하기 위한 데코레이터입니다. 반드시 [Message](#Message) 객체를 반환해야만 합니다.
데코레이터로 전달된 `정규식 표현`이 명령어가 됩니다.
이 데코레이터로 등록된 함수는 사용자가 `명령어의 패턴을 만족하도록 말했을 때` 동작합니다.
이 데코레이터로 등록된 함수는 `하나의 매개변수를 필요로 합니다.`

정규식 표현에 의해 잘린 부분이 매개변수로 들어가게 됩니다. 예시는 다음과 같습니다.
```py
@app.add_regex_command('^(?:((?:(?!에서).)*)에서 )?((?:(?! 찾아줘).)*) 찾아줘')
def temp_regex_com(content):
	return kakaobot.Message(text = "반가워")
```
이 경우 매개변수로 들어가는 내용은 2개의 원소를 가진 배열이 됩니다.
예를 들어 `"구글에서 카티노르 찾아줘"` 일 경우 `"구글"` 이 content[0], `"카티노르"`가 content[1]이 됩니다.
더 나아가서, `"카티노르 찾아줘"` 일 경우 `""` 이 content[0], `"카티노르"`가 content[1]이 됩니다.

##### `set_extra()`

명령어를 등록하기 위한 데코레이터입니다. 반드시 [Message](#Message) 객체를 반환해야만 합니다.
이 데코레이터로 등록된 함수는 사용자가 `위의 세 데코레이터로 등록되지 않은 말을 했을 때` 동작합니다.
이 데코레이터로 등록된 함수는 `하나의 매개변수를 필요로 합니다.`

사용자가 한 말이 그대로 매개변수로 들어가게 됩니다. 예시는 다음과 같습니다.
```py
@app.set_extra
def extra_func(content):
	return kakaobot.Message(text = content)
```

##### `run()`

챗봇을 작동시키기 위한 웹서버가 켜집니다.

#### Kboard

사용자의 키보드 영역에 표현될 메시지 입력방식에 대한 정보입니다. 빈 Kboard는 사용자에게 주관식 응답을 허용하지만, 하나의 버튼이라도 등록되어 있다면, 사용자는 객관식 응답만 할 수 있습니다. (채팅창이 잠겨집니다.)

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| button | string 또는 List[string] | Optional | 사용자에게 제시할 객관식 응답의 목록입니다. |

##### `add_button(button)`

객관식 응답을 추가합니다. 선언시에는 행렬도 받지만, 이 함수를 이용할 경우에는 문자열만 받을 수 있습니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| button | string | Require | 추가할 객관식 응답입니다. |

#### Message

사용자에게 전달한 메시지 객체입니다. 커맨드 등록 데코레이터로 데코레이팅된 모든 함수들은 이 객체를 반환해야만 합니다.
`주의 : 이 객체를 반환할 때 text, photo, message_button 3가지 중 하나 이상이 Message 객체에 지정되어 있어야만 합니다.`

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| text | string | Optional | 전달할 텍스트 입니다. 1000자 제한이 있습니다. |
| photo | [Photo](#Photo) | Optional | 말풍선에 들어갈 이미지 정보입니다. |
| message_button | [Mbutton](#Mbutton) | Optional | 말풍선에 붙는 링크버튼입니다. |
| keyboard | [Kboard](#Kboard) | Optional | 이 메시지를 받은 사용자의 키보드 영역에 표현될 메시지 입력방식에 대한 정보를 담습니다. 생략시 빈 Kboard 가 적용됩니다. |

##### `set_text(text)`

메시지 객체의 텍스트를 교체합니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| text | string | Require | 교체할 텍스트 입니다. |

##### `set_photo(photo)`

메시지 객체의 사진을 교체합니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| text | [Photo](#Photo) | Require | 교체할 Photo 객체입니다. |

##### `set_button(message_button)`

메시지 객체의 링크버튼을 교체합니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| text | [Mbutton](#Mbutton) | Require | 교체할 Mbutton 객체입니다. |


##### `set_keyboard(keyboard)`

메시지 객체의 입력방식을 교체합니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| text | [Kboard](#Kboard) | Require | 교체할 Kboard 객체입니다. |

#### Mbutton

링크버튼(message_button) 객체입니다. Message 객체에 포함될 경우 말풍선 하단에 링크를 가진 버튼이 추가됩니다.

| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| label | string | Require | 링크버튼의 타이틀입니다. |
| url | string | Require | 버튼을 누를 경우 연결되는 주소입니다. |

#### Photo

이미지 객체입니다. Message 객체에 포함될 경우 말풍선에 이미지가 추가됩니다.

`주의 : 이미지는 jpg 또는 png 형식이어야만 합니다. 추가로 500KB 이하, 사이즈 720*630이 권장됩니다.`
| 매개변수 | 타입 | 필수여부 | 설명 |
| ---- | ---- | -------- | ----------- |
| url | string | Require | 이미지를 불어 올 주소입니다. |
| width | int | Optional | 이미지의 너비입니다. 생략시 720이 적용됩니다. |
| height | int | Optional | 이미지의 높이입니다. 생략시 630이 적용됩니다. |

[license]: https://img.shields.io/badge/license-MIT-blue.svg
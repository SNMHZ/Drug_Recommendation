### request message (from user)
| key         |  type             | description |
| -------     | -------------     | -           | 
| seq         | `int`               | 대화 순서, -1 일 시 end message |
| sys         | `vector<string>`    | `['os', 'model', ...]`, seq !=0 일 시 `None` |
| body        | `string`            | 상담 내용 |
| rating      | `int`               | 1 ~ 5, seq != -1 일 시 `None` |

### response message (from server)
| key         |  type             | description |
| -------     | -------------     | ------      |
| type        | `int`             | -1: 에러, 0 : 예측 메시지, 1 : 증상 리스트 전송 |
| date        | `vector<string>`    | 메시지 전송 시간 |
| predicts    | `vector<string>`    | top 3 condition and probs|
| symptoms    | `vector<string>`    | type == `0` 일 시 `None` |
| sym_words   | `vector<string>`    | type == `0` 일 시 `None` |
| drugs       | `vector<string>`    | type == `1` 일 시 `None` |
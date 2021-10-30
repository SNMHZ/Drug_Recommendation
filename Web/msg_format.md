### request message (from user)
| key         |  type             | description |
| -------     | -------------     | -           | 
| seq         | `int`               | 대화 순서, -1 일 시 end message |
| sys         | `vector<string>`    | `['os', 'model', ...]`, seq !=0 일 시 `None` |
| msg         | `string`            | 상담 내용 |
| rating      | `int`               | 1 ~ 5, seq != -1 일 시 `None` |
| auth        | `-`                 | 여유 있을 시 구현 |

### response message (from server)
| key         |  type             | description |
| -------     | -------------     | -           |
| seq         | `int`               | 대화 순서(request와 동일) |
| isClear     | `bool`              | `True` 일시 end message |
| predicts    | `vector<string>`    | top 3 |
| probs       | `vector<float>`     | top 3 |
| symptoms    | `vector<string>`    | isClear == `True` 일 시 `None` |
| drugs       | `vector<string>`    | isClear == `False` 일 시 `None` |
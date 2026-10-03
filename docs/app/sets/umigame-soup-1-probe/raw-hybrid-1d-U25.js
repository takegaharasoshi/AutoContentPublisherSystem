window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U25"] = [
  {
    "case_id": "U25-e01",
    "record": {
      "comment_id": "U25-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4225,
            "latency_s": 1.090891,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.91,
                "question": 0.09
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.03
              },
              "C": 0.5,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 368,
            "finish_reason": "stop",
            "latency_s": 4.147033,
            "model": "gpt-6-luna",
            "prompt_tokens": 2999,
            "reasoning_tokens": 294
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、二人は何も賭けていないと明示されています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。別のことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "中学時代に二人で何か賭けをしてたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.091142363002291,
      "judge_s": 4.1470722559897695,
      "luna_s": 4.1470722559897695,
      "total_s": 6.038327679998474,
      "writer_s": 1.8912554240087047
    }
  },
  {
    "case_id": "U25-e02",
    "record": {
      "comment_id": "U25-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4261,
            "latency_s": 1.117253,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.33,
                "question": 0.67
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.57,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 209,
            "finish_reason": "stop",
            "latency_s": 2.726254,
            "model": "gpt-6-luna",
            "prompt_tokens": 2998,
            "reasoning_tokens": 143
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "「勝った」が昔から続く勝負の結果を指すかの確認です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "「勝った」は、昔した勝負の結果について言ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1174659469979815,
      "judge_s": 2.726281410024967,
      "luna_s": 2.726281410024967,
      "total_s": 3.737872335012071,
      "writer_s": 1.0115909249871038
    }
  },
  {
    "case_id": "U25-e03",
    "record": {
      "comment_id": "U25-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4237,
            "latency_s": 1.141512,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.44,
                "question": 0.56
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.42,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 208,
            "finish_reason": "stop",
            "latency_s": 2.741548,
            "model": "gpt-6-luna",
            "prompt_tokens": 2999,
            "reasoning_tokens": 131
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、二人は毎年年賀状だけをやりとりしていたと分かります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "友人は毎年ずっと年賀状を送り続けていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1417291319812648,
      "judge_s": 2.7415737429982983,
      "luna_s": 2.7415737429982983,
      "total_s": 3.654797182971379,
      "writer_s": 0.9132234399730805
    }
  },
  {
    "case_id": "U25-e04",
    "record": {
      "comment_id": "U25-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4171,
            "latency_s": 1.142631,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.62,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.176286,
            "model": "gpt-6-luna",
            "prompt_tokens": 2991,
            "reasoning_tokens": 96
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、二人は中学の同級生とあります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人は中学の同級生ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1428720800031442,
      "judge_s": 2.176340853999136,
      "luna_s": 2.176340853999136,
      "total_s": 3.01549214599072,
      "writer_s": 0.839151291991584
    }
  },
  {
    "case_id": "U25-e05",
    "record": {
      "comment_id": "U25-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4219,
            "latency_s": 1.066271,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.81,
                "question": 0.19
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.18
              },
              "C": 0.71,
              "D": {
                "irrelevant": 0.0,
                "no": 0.02,
                "yes": 0.98
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.18"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 447,
            "finish_reason": "stop",
            "latency_s": 5.118558,
            "model": "gpt-6-luna",
            "prompt_tokens": 2997,
            "reasoning_tokens": 363
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "一つの事実を確かめる質問で、年賀状に勝負の決着を示す言葉が書かれていました。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状に勝負の答えが書かれていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0665583469963167,
      "judge_s": 5.118582505994709,
      "luna_s": 5.118582505994709,
      "total_s": 6.286956558004022,
      "writer_s": 1.1683740520093124
    }
  },
  {
    "case_id": "U25-e06",
    "record": {
      "comment_id": "U25-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4237,
            "latency_s": 1.115586,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.72,
                "question": 0.28
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.59,
              "D": {
                "irrelevant": 0.47,
                "no": 0.5,
                "yes": 0.03
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 3.435119,
            "model": "gpt-6-luna",
            "prompt_tokens": 2998,
            "reasoning_tokens": 158
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "友人を心配していたかは真相に記載がなく、勝負の結末にも関係しません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は友人がまだ生きているか気にしていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1160792490118183,
      "judge_s": 3.435174187994562,
      "luna_s": 3.435174187994562,
      "total_s": 5.405994942993857,
      "writer_s": 1.9708207549992949
    }
  },
  {
    "case_id": "U25-e07",
    "record": {
      "comment_id": "U25-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4219,
            "latency_s": 1.338154,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.31,
                "question": 0.69
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.0,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.35,
              "D": {
                "irrelevant": 0.35,
                "no": 0.5,
                "yes": 0.15
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 495,
            "finish_reason": "stop",
            "latency_s": 5.395996,
            "model": "gpt-6-luna",
            "prompt_tokens": 2996,
            "reasoning_tokens": 420
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男性の受取日は分かりますが、友人側の受取日は示されていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人とも元日に年賀状を受け取ったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.3385642150242347,
      "judge_s": 5.396027836977737,
      "luna_s": 5.396027836977737,
      "total_s": 7.003624458971899,
      "writer_s": 1.607596621994162
    }
  },
  {
    "case_id": "U25-e08",
    "record": {
      "comment_id": "U25-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4195,
            "latency_s": 1.327455,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.28,
              "D": {
                "irrelevant": 0.05,
                "no": 0.0,
                "yes": 0.95
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 215,
            "finish_reason": "stop",
            "latency_s": 3.15355,
            "model": "gpt-6-luna",
            "prompt_tokens": 2994,
            "reasoning_tokens": 145
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "年齢差は真相にも確定事実にも示されていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "友人は男と同じくらいの年齢ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.3277569610218052,
      "judge_s": 3.153585785999894,
      "luna_s": 3.153585785999894,
      "total_s": 4.821429852978326,
      "writer_s": 1.6678440669784322
    }
  },
  {
    "case_id": "U25-e09",
    "record": {
      "comment_id": "U25-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4219,
            "latency_s": 1.167695,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.04,
                "question": 0.96
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.39,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 330,
            "finish_reason": "stop",
            "latency_s": 3.858399,
            "model": "gpt-6-luna",
            "prompt_tokens": 2997,
            "reasoning_tokens": 246
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "家族が勝負を知っていたことは確定していますが、約束まで知っていたかは示されていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "男の家族は二人の約束を知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.168195132020628,
      "judge_s": 3.8584602079936303,
      "luna_s": 3.8584602079936303,
      "total_s": 5.546115716977511,
      "writer_s": 1.6876555089838803
    }
  },
  {
    "case_id": "U25-e10",
    "record": {
      "comment_id": "U25-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4237,
            "latency_s": 1.203697,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.06,
                "q_yesno": 0.94
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.04
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.02,
                "no": 0.98,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.04"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 354,
            "finish_reason": "stop",
            "latency_s": 4.327136,
            "model": "gpt-6-luna",
            "prompt_tokens": 2999,
            "reasoning_tokens": 276
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "年賀状が先に届いたことが勝因ではなく、相手の投了で決着しました。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "勝ったのは、年賀状が先に届いたからなんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2039580380078405,
      "judge_s": 4.327166094997665,
      "luna_s": 4.327166094997665,
      "total_s": 6.077552311006002,
      "writer_s": 1.7503862160083372
    }
  },
  {
    "case_id": "U25-e11",
    "record": {
      "comment_id": "U25-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2141,
            "latency_s": 0.578302,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.9,
                "question": 0.1
              },
              "A2": {
                "q_multi": 0.99,
                "q_open": 0.0,
                "q_yesno": 0.01
              },
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 149,
            "finish_reason": "stop",
            "latency_s": 2.042282,
            "model": "gpt-6-luna",
            "prompt_tokens": 3003,
            "reasoning_tokens": 70
          },
          "error": null,
          "kind": "q_multi",
          "reason": "中学時代の勝負と決着について、質問が二つあります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。どっちからいこうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人は中学のころに勝負したの？その勝負の決着がついたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5784738090005703,
      "judge_s": 2.0423248800216243,
      "luna_s": 2.0423248800216243,
      "total_s": 3.740726039017318,
      "writer_s": 1.6984011589956935
    }
  },
  {
    "case_id": "U25-e12",
    "record": {
      "comment_id": "U25-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_multi"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 2147,
            "latency_s": 0.616347,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.24,
                "question": 0.76
              },
              "A2": {
                "q_multi": 0.97,
                "q_open": 0.0,
                "q_yesno": 0.03
              },
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 212,
            "finish_reason": "stop",
            "latency_s": 3.966121,
            "model": "gpt-6-luna",
            "prompt_tokens": 3002,
            "reasoning_tokens": 129
          },
          "error": null,
          "kind": "q_multi",
          "reason": "年賀状のやり取りの期間と、今年の内容について二つ尋ねています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。どちらか一つから聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状は何十年も送り合ってたの？今年だけ特別な内容だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.616560421010945,
      "judge_s": 3.966180766990874,
      "luna_s": 3.966180766990874,
      "total_s": 5.697629701986443,
      "writer_s": 1.7314489349955693
    }
  },
  {
    "case_id": "U25-e13",
    "record": {
      "comment_id": "U25-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2614,
            "latency_s": 0.813303,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.09,
                "question": 0.91
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.03,
              "A_bare": 0.03
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.03"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 147,
            "finish_reason": "stop",
            "latency_s": 2.075801,
            "model": "gpt-6-luna",
            "prompt_tokens": 2992,
            "reasoning_tokens": 71
          },
          "error": null,
          "kind": "q_open",
          "reason": "何の勝負かを尋ねる、はい・いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男が何の勝負に勝ったのか、はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は何の勝負に勝ったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8134977289882954,
      "judge_s": 2.0758588839962613,
      "luna_s": 2.0758588839962613,
      "total_s": 5.030508144001942,
      "writer_s": 2.954649260005681
    }
  },
  {
    "case_id": "U25-e14",
    "record": {
      "comment_id": "U25-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_spoiler"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2630,
            "latency_s": 0.787166,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.12,
                "question": 0.88
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 1.0,
                "q_yesno": 0.0
              },
              "A3": 0.04,
              "A_bare": 0.04
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.04"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 311,
            "finish_reason": "stop",
            "latency_s": 3.59308,
            "model": "gpt-6-luna",
            "prompt_tokens": 2992,
            "reasoning_tokens": 235
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "年賀状に何が書かれていたか、答えの核心を尋ねています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問には答えられるけど、真相は教えられないよ。質問で少しずつ絞っていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "年賀状には何が書いてあったんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7873632720147725,
      "judge_s": 3.5931575979921035,
      "luna_s": 3.5931575979921035,
      "total_s": 5.798332525999285,
      "writer_s": 2.2051749280071817
    }
  },
  {
    "case_id": "U25-e15",
    "record": {
      "comment_id": "U25-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 2658,
            "latency_s": 0.770906,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.18,
                "question": 0.82
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
              },
              "A3": 0.04,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.04"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 213,
            "finish_reason": "stop",
            "latency_s": 3.013552,
            "model": "gpt-6-luna",
            "prompt_tokens": 3000,
            "reasoning_tokens": 128
          },
          "error": null,
          "kind": "q_open",
          "reason": "約束の内容を尋ねる、はい・いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "二人は中学を卒業するとき、どんな約束をしたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7712722279829904,
      "judge_s": 3.0136103259865195,
      "luna_s": 3.0136103259865195,
      "total_s": 4.701203578995774,
      "writer_s": 1.6875932530092541
    }
  },
  {
    "case_id": "U25-e16",
    "record": {
      "comment_id": "U25-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "consensus_ok",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 3214,
            "latency_s": 0.798201,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.94
              },
              "B2": 0.07
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.94, 矛盾=0.07"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 308,
            "finish_reason": "stop",
            "latency_s": 3.607788,
            "model": "gpt-6-luna",
            "prompt_tokens": 3002,
            "reasoning_tokens": 199
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "年賀状で将棋を一手ずつ指すというコアの要点をすべて述べています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は年賀状に将棋を1手ずつ書き、55年かけて1局を指していた。友人の年賀状に「参りました」とあり、男が勝った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "2人は年賀状で将棋を一手ずつ指し続けてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7997483430081047,
      "judge_s": 3.60785262400168,
      "luna_s": 3.60785262400168,
      "total_s": 3.607868426013738,
      "writer_s": 1.5802012057974935e-05
    }
  },
  {
    "case_id": "U25-e17",
    "record": {
      "comment_id": "U25-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "consensus_ok",
        "kind": "guess_correct"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 3330,
            "latency_s": 0.78767,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.98
              },
              "B2": 0.08
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.08"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 280,
            "finish_reason": "stop",
            "latency_s": 3.390116,
            "model": "gpt-6-luna",
            "prompt_tokens": 3026,
            "reasoning_tokens": 170
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "年賀状で将棋を一手ずつ続け、55年後に決着した核心を捉えています。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！2人は年賀状に将棋を1手ずつ書き、55年かけて1局を指していた。友人の年賀状に「参りました」とあり、男が勝った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "会えないまま、2人は年賀状で将棋を一手ずつ続けてたんだね。55年越しに相手が「参りました」と送ってきたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7879384749976452,
      "judge_s": 3.3902025159914047,
      "luna_s": 3.3902025159914047,
      "total_s": 3.3902077289822046,
      "writer_s": 5.212990799918771e-06
    }
  },
  {
    "case_id": "U25-e18",
    "record": {
      "comment_id": "U25-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "input_tokens": 1978,
            "latency_s": 0.609444,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 132,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.27
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.27"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 190,
            "finish_reason": "stop",
            "latency_s": 2.823472,
            "model": "gpt-6-luna",
            "prompt_tokens": 3003,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で勝負を続けた点には触れていますが、将棋を一手ずつ指した点までは特定できていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "2人は年賀状で何かの勝負をずっと続けてたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6096758650091942,
      "judge_s": 2.823533276998205,
      "luna_s": 2.823533276998205,
      "total_s": 3.7940328599943314,
      "writer_s": 0.9704995829961263
    }
  },
  {
    "case_id": "U25-e19",
    "record": {
      "comment_id": "U25-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 3286,
            "latency_s": 0.833851,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 154,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.91
              },
              "B2": 0.98
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.91, 矛盾=0.98"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 161,
            "finish_reason": "stop",
            "latency_s": 2.517273,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 95
          },
          "error": null,
          "kind": "guess_close",
          "reason": "年賀状で将棋を続けた点は合っていますが、毎年会っていた点が異なります。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状で将棋を一手ずつ続けてたけど、2人は毎年会って、その場で次の手を決めてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8342381149996072,
      "judge_s": 2.517333623021841,
      "luna_s": 2.517333623021841,
      "total_s": 4.237574357015546,
      "writer_s": 1.7202407339937054
    }
  },
  {
    "case_id": "U25-e20",
    "record": {
      "comment_id": "U25-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "guess_demoted": true,
            "input_tokens": 4375,
            "latency_s": 1.174342,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.03,
                "q_open": 0.34,
                "q_yesno": 0.63
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.44,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 216,
            "finish_reason": "stop",
            "latency_s": 2.813009,
            "model": "gpt-6-luna",
            "prompt_tokens": 3021,
            "reasoning_tokens": 150
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "核心の年賀状での勝負に触れておらず、賭けもしていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "中学の時にどっちが先に結婚するか賭けていて、友人が独身だとわかったから勝ちを喜んだんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1746971069951542,
      "judge_s": 2.813066919974517,
      "luna_s": 2.813066919974517,
      "total_s": 3.8694347629789263,
      "writer_s": 1.0563678430044092
    }
  },
  {
    "case_id": "U25-e21",
    "record": {
      "comment_id": "U25-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_wrong"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "guess_demoted": true,
            "input_tokens": 2567,
            "latency_s": 0.792989,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.89,
                "q_yesno": 0.1
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.01"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 260,
            "finish_reason": "stop",
            "latency_s": 3.162746,
            "model": "gpt-6-luna",
            "prompt_tokens": 3012,
            "reasoning_tokens": 187
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "年賀状での知らせや賭けの推理で、将棋を一手ずつ指す核心には触れていません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "友人が年賀状で宝くじが当たったと知らせてきて、昔の賭けに勝ったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7932903089968022,
      "judge_s": 3.1628234060190152,
      "luna_s": 3.1628234060190152,
      "total_s": 4.906778419011971,
      "writer_s": 1.7439550129929557
    }
  },
  {
    "case_id": "U25-t01",
    "record": {
      "comment_id": "U25-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "年賀状将棋",
          "debug": {
            "calls": 1,
            "input_tokens": 930,
            "latency_s": 0.190859,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A_bare": 0.86
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.86"
        },
        "luna": {
          "answer": null,
          "bare_term": "年賀状将棋",
          "debug": {
            "completion_tokens": 258,
            "finish_reason": "stop",
            "latency_s": 4.822709,
            "model": "gpt-6-luna",
            "prompt_tokens": 2985,
            "reasoning_tokens": 170
          },
          "error": null,
          "kind": "q_open",
          "reason": "名詞句だけで述語がなく、はい・いいえで答えられる質問ではありません。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "年賀状将棋がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "年賀状将棋？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.19098642698372714,
      "judge_s": 4.822778893983923,
      "luna_s": 4.822778893983923,
      "total_s": 7.6143471819814295,
      "writer_s": 2.7915682879975066
    }
  },
  {
    "case_id": "U25-t02",
    "record": {
      "comment_id": "U25-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "野球部",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.233712,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A_bare": 0.97
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.97"
        },
        "luna": {
          "answer": null,
          "bare_term": "野球部",
          "debug": {
            "completion_tokens": 200,
            "finish_reason": "stop",
            "latency_s": 3.076217,
            "model": "gpt-6-luna",
            "prompt_tokens": 2982,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直してもらいます。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "何が野球部なのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "野球部",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.23382854400551878,
      "judge_s": 3.0762701790081337,
      "luna_s": 3.0762701790081337,
      "total_s": 6.223643885023193,
      "writer_s": 3.1473737060150597
    }
  },
  {
    "case_id": "c-ask_howto-01",
    "record": {
      "comment_id": "c-ask_howto-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_howto"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1427,
            "latency_s": 0.400161,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.0,
                "request": 0.99
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.04
            }
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "段A=request→ask_howto"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 176,
            "finish_reason": "stop",
            "latency_s": 2.541741,
            "model": "gpt-6-luna",
            "prompt_tokens": 2987,
            "reasoning_tokens": 97
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "遊び方を尋ねているため、遊び方の案内をします。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をしてごらん。私が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これどうやって遊ぶの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.4002665279840585,
      "judge_s": 2.5417979809863027,
      "luna_s": 2.5417979809863027,
      "total_s": 3.9169246269739233,
      "writer_s": 1.3751266459876206
    }
  },
  {
    "case_id": "c-greeting-05",
    "record": {
      "comment_id": "c-greeting-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "greeting"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1580,
            "latency_s": 0.396892,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 1.0,
                "request": 0.0
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 1.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.15
            }
          },
          "error": null,
          "kind": "greeting",
          "reason": "段A=reaction→greeting"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 119,
            "finish_reason": "stop",
            "latency_s": 2.638386,
            "model": "gpt-6-luna",
            "prompt_tokens": 2985,
            "reasoning_tokens": 59
          },
          "error": null,
          "kind": "greeting",
          "reason": "初めてのコメントと挨拶を伝えているため。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "こんにちは！初コメントありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "こんにちは、初コメです",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.39701076099299826,
      "judge_s": 2.6384460979897995,
      "luna_s": 2.6384460979897995,
      "total_s": 4.057577028986998,
      "writer_s": 1.4191309309971984
    }
  },
  {
    "case_id": "c-request-04",
    "record": {
      "comment_id": "c-request-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "request"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1429,
            "latency_s": 0.54949,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.22,
                "request": 0.78
              },
              "A2": {
                "ask_hint": 0.28,
                "ask_howto": 0.65,
                "ask_spoiler": 0.07
              },
              "A_bare": 0.51
            }
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "段A=request→ask_howto"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 131,
            "finish_reason": "stop",
            "latency_s": 1.890712,
            "model": "gpt-6-luna",
            "prompt_tokens": 2988,
            "reasoning_tokens": 74
          },
          "error": null,
          "kind": "request",
          "reason": "短めの問題を出してほしいというリクエストです。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！短めの問題も考えてみるね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "短めの問題リクエストです",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5496591519913636,
      "judge_s": 1.8907650260080118,
      "luna_s": 1.8907650260080118,
      "total_s": 3.4223147300072014,
      "writer_s": 1.5315497039991897
    }
  },
  {
    "case_id": "c-emoji_only-03",
    "record": {
      "comment_id": "c-emoji_only-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "emoji_only"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 0,
            "input_tokens": 0,
            "latency_s": 0.0,
            "model": "jev-latest",
            "output_tokens": 0,
            "probabilities": {}
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "段0規則: emoji_only"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 108,
            "finish_reason": "stop",
            "latency_s": 1.831135,
            "model": "gpt-6-luna",
            "prompt_tokens": 2981,
            "reasoning_tokens": 55
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字のみのコメントです。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "びっくりしたね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "😮",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 3.8452009903267026e-05,
      "judge_s": 1.831158927991055,
      "luna_s": 1.831158927991055,
      "total_s": 3.2899347589700483,
      "writer_s": 1.4587758309789933
    }
  },
  {
    "case_id": "c-spam-02",
    "record": {
      "comment_id": "c-spam-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "spam"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1484,
            "latency_s": 0.381372,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 128,
            "probabilities": {
              "A1": {
                "inappropriate": 1.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 1.0,
                "troll": 0.0
              },
              "A_bare": 0.04
            }
          },
          "error": null,
          "kind": "spam",
          "reason": "段A=inappropriate→spam"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 100,
            "finish_reason": "stop",
            "latency_s": 1.908889,
            "model": "gpt-6-luna",
            "prompt_tokens": 2990,
            "reasoning_tokens": 47
          },
          "error": null,
          "kind": "spam",
          "reason": "相互フォローを呼びかけるフォロー稼ぎのコメントです。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "no_reply",
        "text": null
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "フォローしてくれたら相互します！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.38151327200466767,
      "judge_s": 1.908924643008504,
      "luna_s": 1.908924643008504,
      "total_s": 1.9089258899912238,
      "writer_s": 1.2469827197492123e-06
    }
  },
  {
    "case_id": "c-abuse-06",
    "record": {
      "comment_id": "c-abuse-06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "013-fifty-five-year-nengajo",
      "errors": [],
      "fact_sheet_hash": "bb5a6e203be0",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "abuse"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1480,
            "latency_s": 0.431649,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.84,
                "other": 0.0,
                "question_or_guess": 0.13,
                "reaction": 0.03,
                "request": 0.0
              },
              "A2": {
                "abuse": 1.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 0.0
              },
              "A_bare": 0.05
            }
          },
          "error": null,
          "kind": "abuse",
          "reason": "段A=inappropriate→abuse"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 116,
            "finish_reason": "stop",
            "latency_s": 2.005515,
            "model": "gpt-6-luna",
            "prompt_tokens": 2990,
            "reasoning_tokens": 68
          },
          "error": null,
          "kind": "abuse",
          "reason": "問題ではなく、作者本人を攻撃する内容です。"
        }
      },
      "media_id": "local-U25",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "ここではやさしい言葉でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "作者って絶対友達いないでしょ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.4318399559997488,
      "judge_s": 2.0055765110009816,
      "luna_s": 2.0055765110009816,
      "total_s": 2.005600067001069,
      "writer_s": 2.355600008741021e-05
    }
  }
];

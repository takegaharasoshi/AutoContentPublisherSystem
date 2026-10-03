window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U22"] = [
  {
    "case_id": "U22-e01",
    "record": {
      "comment_id": "U22-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4241,
            "latency_s": 1.263779,
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
                "guess": 0.61,
                "question": 0.39
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
              "C": 0.58,
              "D": {
                "irrelevant": 0.0,
                "no": 0.03,
                "yes": 0.97
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
            "completion_tokens": 149,
            "finish_reason": "stop",
            "latency_s": 2.216589,
            "model": "gpt-6-luna",
            "prompt_tokens": 2990,
            "reasoning_tokens": 87
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、半年ごとのふつうの検診を受けているとあります。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！半年ごとに定期検診を受けてるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は半年ごとに定期検診を受けてるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2640964790189173,
      "judge_s": 2.2166476440033875,
      "luna_s": 2.2166476440033875,
      "total_s": 3.983998123992933,
      "writer_s": 1.7673504799895454
    }
  },
  {
    "case_id": "U22-e02",
    "record": {
      "comment_id": "U22-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4277,
            "latency_s": 1.112357,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.18,
                "question": 0.82
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.43,
              "D": {
                "irrelevant": 0.0,
                "no": 0.99,
                "yes": 0.01
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 459,
            "finish_reason": "stop",
            "latency_s": 4.757434,
            "model": "gpt-6-luna",
            "prompt_tokens": 2994,
            "reasoning_tokens": 385
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男は治療ではなく、半年ごとの通常の検診を受けています。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。歯医者に通うのは、歯の治療が目的じゃないんですか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "歯医者に通うのは、歯の治療が目的じゃないんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1128271539928392,
      "judge_s": 4.757488926989026,
      "luna_s": 4.757488926989026,
      "total_s": 9.85658626400982,
      "writer_s": 5.099097337020794
    }
  },
  {
    "case_id": "U22-e03",
    "record": {
      "comment_id": "U22-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4247,
            "latency_s": 1.140433,
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
                "guess": 0.14,
                "question": 0.86
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.1
              },
              "C": 0.34,
              "D": {
                "irrelevant": 0.01,
                "no": 0.97,
                "yes": 0.02
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.10"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 343,
            "finish_reason": "stop",
            "latency_s": 4.171094,
            "model": "gpt-6-luna",
            "prompt_tokens": 2990,
            "reasoning_tokens": 267
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "歯医者になったのは男の幼少期より後で、昔からのかかりつけではありません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。その歯医者は、昔からのかかりつけではないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その歯医者は男の昔からのかかりつけですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1409050070215017,
      "judge_s": 4.171145418018568,
      "luna_s": 4.171145418018568,
      "total_s": 6.692184337036451,
      "writer_s": 2.521038919017883
    }
  },
  {
    "case_id": "U22-e04",
    "record": {
      "comment_id": "U22-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4259,
            "latency_s": 1.190091,
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
                "guess": 0.88,
                "question": 0.12
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
              "C": 0.67,
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
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 246,
            "finish_reason": "stop",
            "latency_s": 2.970094,
            "model": "gpt-6-luna",
            "prompt_tokens": 2991,
            "reasoning_tokens": 175
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男は誰かを待つのではなく、懐かしんでから帰ります。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は診察のあと誰かが来るのを待っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1904580749978777,
      "judge_s": 2.970155524002621,
      "luna_s": 2.970155524002621,
      "total_s": 4.4404101760010235,
      "writer_s": 1.4702546519984026
    }
  },
  {
    "case_id": "U22-e05",
    "record": {
      "comment_id": "U22-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4229,
            "latency_s": 1.235977,
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
                "q_open": 0.07,
                "q_yesno": 0.93
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
              },
              "C": 0.32,
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
            "completion_tokens": 466,
            "finish_reason": "stop",
            "latency_s": 4.89659,
            "model": "gpt-6-luna",
            "prompt_tokens": 2986,
            "reasoning_tokens": 393
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "「意味があるか」を尋ねる、はい／いいえで答えられる質問です。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！同じ席に座ることに意味があるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "同じ席に座ることに意味があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2362973330018576,
      "judge_s": 4.896649811998941,
      "luna_s": 4.896649811998941,
      "total_s": 6.8581461739959195,
      "writer_s": 1.9614963619969785
    }
  },
  {
    "case_id": "U22-e06",
    "record": {
      "comment_id": "U22-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4253,
            "latency_s": 1.230426,
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
                "guess": 0.47,
                "question": 0.53
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.58,
              "D": {
                "irrelevant": 0.38,
                "no": 0.39999999999999997,
                "yes": 0.22
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
            "completion_tokens": 352,
            "finish_reason": "stop",
            "latency_s": 4.355848,
            "model": "gpt-6-luna",
            "prompt_tokens": 2992,
            "reasoning_tokens": 273
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "会話の有無は真相・確定事実から判断できず、核心にも関係しません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかにも聞いてごらん"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は毎回、歯医者の人と話をして帰るんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2307011839875486,
      "judge_s": 4.355925723008113,
      "luna_s": 4.355925723008113,
      "total_s": 6.35829487600131,
      "writer_s": 2.0023691529931966
    }
  },
  {
    "case_id": "U22-e07",
    "record": {
      "comment_id": "U22-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "irrelevant",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4223,
            "latency_s": 1.239964,
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
                "guess": 0.42,
                "question": 0.58
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
              },
              "C": 0.27,
              "D": {
                "irrelevant": 0.42,
                "no": 0.57,
                "yes": 0.01
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
            "completion_tokens": 250,
            "finish_reason": "stop",
            "latency_s": 2.973506,
            "model": "gpt-6-luna",
            "prompt_tokens": 2986,
            "reasoning_tokens": 168
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "家族や友人が町に住んでいるかは、真相・確定事実から判断できません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "その町に家族や友人が住んでいますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2403570429887623,
      "judge_s": 2.973562455008505,
      "luna_s": 2.973562455008505,
      "total_s": 4.181443670007866,
      "writer_s": 1.207881214999361
    }
  },
  {
    "case_id": "U22-e08",
    "record": {
      "comment_id": "U22-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4295,
            "latency_s": 1.234048,
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
                "q_multi": 0.01,
                "q_open": 0.25,
                "q_yesno": 0.74
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.41,
              "D": {
                "irrelevant": 0.25,
                "no": 0.39999999999999997,
                "yes": 0.35
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
            "completion_tokens": 515,
            "finish_reason": "stop",
            "latency_s": 5.044092,
            "model": "gpt-6-luna",
            "prompt_tokens": 2995,
            "reasoning_tokens": 445
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "電車で通うことは示されていますが、電車でなければならない理由は明かされていません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "歯医者に行くのは電車じゃないといけない理由があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2343748240091372,
      "judge_s": 5.0441185100062285,
      "luna_s": 5.0441185100062285,
      "total_s": 6.263316246011527,
      "writer_s": 1.2191977360052988
    }
  },
  {
    "case_id": "U22-e09",
    "record": {
      "comment_id": "U22-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4253,
            "latency_s": 1.252263,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 240,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.44,
              "D": {
                "irrelevant": 0.76,
                "no": 0.16,
                "yes": 0.08
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
            "completion_tokens": 389,
            "finish_reason": "stop",
            "latency_s": 4.307226,
            "model": "gpt-6-luna",
            "prompt_tokens": 2990,
            "reasoning_tokens": 307
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "診察と待合室の滞在時間の比較は、真相・確定事実から判断できません。"
        }
      },
      "media_id": "local-U22",
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
      "shadow_mismatch": false,
      "text": "待合室にいる時間のほうが診察より長いんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2530309229914565,
      "judge_s": 4.307260090019554,
      "luna_s": 4.307260090019554,
      "total_s": 6.659817870036932,
      "writer_s": 2.352557780017378
    }
  },
  {
    "case_id": "U22-e10",
    "record": {
      "comment_id": "U22-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4211,
            "latency_s": 1.364204,
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
                "guess": 0.13,
                "question": 0.87
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02
              },
              "C": 0.23,
              "D": {
                "irrelevant": 0.15,
                "no": 0.02,
                "yes": 0.83
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
            "completion_tokens": 217,
            "finish_reason": "stop",
            "latency_s": 2.874417,
            "model": "gpt-6-luna",
            "prompt_tokens": 2985,
            "reasoning_tokens": 151
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相で、男が育った家は古い木造の家とされています。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その歯医者の建物は木造ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.3646090020192787,
      "judge_s": 2.8744685190031305,
      "luna_s": 2.8744685190031305,
      "total_s": 3.9903593930066563,
      "writer_s": 1.1158908740035258
    }
  },
  {
    "case_id": "U22-e11",
    "record": {
      "comment_id": "U22-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2145,
            "latency_s": 0.576117,
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
                "guess": 0.44,
                "question": 0.56
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
            "completion_tokens": 159,
            "finish_reason": "stop",
            "latency_s": 2.285577,
            "model": "gpt-6-luna",
            "prompt_tokens": 2996,
            "reasoning_tokens": 84
          },
          "error": null,
          "kind": "q_multi",
          "reason": "検診に来ているか、誰かを待っているかの質問が2つあります。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつ聞いてごらん。まずどちらかからだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は歯の検診に来てるの？診察後は誰かを待ってるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5763122149801347,
      "judge_s": 2.2856249600008596,
      "luna_s": 2.2856249600008596,
      "total_s": 4.305271549004829,
      "writer_s": 2.019646589003969
    }
  },
  {
    "case_id": "U22-e12",
    "record": {
      "comment_id": "U22-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2145,
            "latency_s": 0.596307,
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
                "guess": 0.72,
                "question": 0.28
              },
              "A2": {
                "q_multi": 0.96,
                "q_open": 0.03,
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
            "completion_tokens": 193,
            "finish_reason": "stop",
            "latency_s": 2.939942,
            "model": "gpt-6-luna",
            "prompt_tokens": 2994,
            "reasoning_tokens": 116
          },
          "error": null,
          "kind": "q_multi",
          "reason": "座る時期と席の思い出について、二つの質問があります。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらか聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "同じ席に座るのは昔から？その席に何か思い出があるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5964398670184892,
      "judge_s": 2.9399929190112744,
      "luna_s": 2.9399929190112744,
      "total_s": 4.950840011006221,
      "writer_s": 2.010847091994947
    }
  },
  {
    "case_id": "U22-e13",
    "record": {
      "comment_id": "U22-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2670,
            "latency_s": 0.800928,
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
                "guess": 0.16,
                "question": 0.84
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.05,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.05"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 172,
            "finish_reason": "stop",
            "latency_s": 2.459142,
            "model": "gpt-6-luna",
            "prompt_tokens": 2989,
            "reasoning_tokens": 86
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねており、はい／いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男が遠くの歯医者に通う理由を、はい／いいえで答えられる質問にしてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はどうして遠くの歯医者に通ってるんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8011045180028304,
      "judge_s": 2.4591637210105546,
      "luna_s": 2.4591637210105546,
      "total_s": 4.669342994020553,
      "writer_s": 2.2101792730099987
    }
  },
  {
    "case_id": "U22-e14",
    "record": {
      "comment_id": "U22-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2678,
            "latency_s": 0.751913,
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
                "guess": 0.16,
                "question": 0.84
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
              },
              "A3": 0.06,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.06"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 200,
            "finish_reason": "stop",
            "latency_s": 3.211388,
            "model": "gpt-6-luna",
            "prompt_tokens": 2992,
            "reasoning_tokens": 121
          },
          "error": null,
          "kind": "q_open",
          "reason": "「誰を待つか」は自由回答で、はい／いいえでは答えられません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "診察後、待合室で誰かを待っているんですか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "診察が終わったあと、待合室で誰を待っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.752073472016491,
      "judge_s": 3.2114480230084155,
      "luna_s": 3.2114480230084155,
      "total_s": 5.693343249993632,
      "writer_s": 2.481895226985216
    }
  },
  {
    "case_id": "U22-e15",
    "record": {
      "comment_id": "U22-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2674,
            "latency_s": 0.766429,
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
                "guess": 0.05,
                "question": 0.95
              },
              "A2": {
                "q_multi": 0.03,
                "q_open": 0.96,
                "q_yesno": 0.01
              },
              "A3": 0.07,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.07"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 181,
            "finish_reason": "stop",
            "latency_s": 2.550204,
            "model": "gpt-6-luna",
            "prompt_tokens": 2991,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どんな関係」は自由回答で、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男とその町や歯医者に関係があるのかな？はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その町や歯医者と男にはどんな関係があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7666856730065774,
      "judge_s": 2.5502526389900595,
      "luna_s": 2.5502526389900595,
      "total_s": 4.695254596997984,
      "writer_s": 2.1450019580079243
    }
  },
  {
    "case_id": "U22-e16",
    "record": {
      "comment_id": "U22-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 3230,
            "latency_s": 1.04582,
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
                "guess": 0.95,
                "question": 0.05
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.9
              },
              "B2": 0.24
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.90, 矛盾=0.24"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 421,
            "finish_reason": "stop",
            "latency_s": 3.774015,
            "model": "gpt-6-luna",
            "prompt_tokens": 2991,
            "reasoning_tokens": 312
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "歯医者が男の育った家だったという核心を言い当てています。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！その歯医者は男が育った家を改装したもの。男は検診を口実に通い、背丈の傷が残る柱の前で過ごしてから帰る。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "歯医者は男が子どものころ住んでた家だったってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0461228149943054,
      "judge_s": 3.774045408004895,
      "luna_s": 3.774045408004895,
      "total_s": 3.7740654399967752,
      "writer_s": 2.0031991880387068e-05
    }
  },
  {
    "case_id": "U22-e17",
    "record": {
      "comment_id": "U22-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 3342,
            "latency_s": 0.811118,
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
                "point_0": 0.93
              },
              "B2": 0.12
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.93, 矛盾=0.12"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 219,
            "finish_reason": "stop",
            "latency_s": 2.585082,
            "model": "gpt-6-luna",
            "prompt_tokens": 3017,
            "reasoning_tokens": 118
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "歯医者が男の生家であることを言い当てています。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！その歯医者は男が育った家を改装したもの。男は検診を口実に通い、背丈の傷が残る柱の前で過ごしてから帰る。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "歯医者になっていたのは男が育った家なんだね。懐かしい家の中に入るために、検診のたび待合室に残ってたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8113807500049006,
      "judge_s": 2.585116663016379,
      "luna_s": 2.585116663016379,
      "total_s": 2.585124354023719,
      "writer_s": 7.691007340326905e-06
    }
  },
  {
    "case_id": "U22-e18",
    "record": {
      "comment_id": "U22-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "guess_demoted": true,
            "input_tokens": 4301,
            "latency_s": 1.284581,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.12
              },
              "C": 0.3,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.12"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 586,
            "finish_reason": "stop",
            "latency_s": 5.691749,
            "model": "gpt-6-luna",
            "prompt_tokens": 2997,
            "reasoning_tokens": 512
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "建物が男と過去に関係していたかを尋ねる一つの質問です。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その歯医者の建物って、男が昔なにか関わってた場所なんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.284962251986144,
      "judge_s": 5.691806874994654,
      "luna_s": 5.691806874994654,
      "total_s": 7.337897870980669,
      "writer_s": 1.6460909959860146
    }
  },
  {
    "case_id": "U22-e19",
    "record": {
      "comment_id": "U22-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "input_tokens": 3366,
            "latency_s": 0.791854,
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
              "B2": 0.89
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.94, 矛盾=0.89"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 517,
            "finish_reason": "stop",
            "latency_s": 9.526073,
            "model": "gpt-6-luna",
            "prompt_tokens": 3026,
            "reasoning_tokens": 446
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "刻んだ人物について尋ねる一つの質問で、真相から否定できます。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "歯医者は男が育った家で、待合室の柱の傷も残ってたんだね。あの背丈の傷は父親じゃなくて、歯医者を開いた人が刻んだのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7920360759890173,
      "judge_s": 9.526122526993277,
      "luna_s": 9.526122526993277,
      "total_s": 11.166748035990167,
      "writer_s": 1.6406255089968909
    }
  },
  {
    "case_id": "U22-e20",
    "record": {
      "comment_id": "U22-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 4331,
            "latency_s": 1.188275,
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
                "q_multi": 0.01,
                "q_open": 0.08,
                "q_yesno": 0.91
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.47,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 296,
            "finish_reason": "stop",
            "latency_s": 3.829784,
            "model": "gpt-6-luna",
            "prompt_tokens": 3002,
            "reasoning_tokens": 233
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "先生に会うことが理由ではなく、通う理由は建物そのものにあります。"
        }
      },
      "media_id": "local-U22",
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
      "shadow_mismatch": true,
      "text": "昔から通ってる先生に会いたくて、診察を口実に半年ごとに訪ねてるんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1885067349940073,
      "judge_s": 3.8298100719985086,
      "luna_s": 3.8298100719985086,
      "total_s": 5.255834434996359,
      "writer_s": 1.4260243629978504
    }
  },
  {
    "case_id": "U22-e21",
    "record": {
      "comment_id": "U22-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 2547,
            "latency_s": 0.756715,
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
                "q_multi": 0.02,
                "q_open": 0.76,
                "q_yesno": 0.22
              },
              "A_bare": 0.03,
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
            "completion_tokens": 249,
            "finish_reason": "stop",
            "latency_s": 2.790949,
            "model": "gpt-6-luna",
            "prompt_tokens": 2998,
            "reasoning_tokens": 179
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "忘れ物探しの推理で、歯医者が男の生家だったという核心には触れていません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "待合室の席に忘れ物をしていて、診察のたびに探してるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7569146369933151,
      "judge_s": 2.7910281980002765,
      "luna_s": 2.7910281980002765,
      "total_s": 4.437146868993295,
      "writer_s": 1.646118670993019
    }
  },
  {
    "case_id": "U22-t01",
    "record": {
      "comment_id": "U22-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "生家の歯医者",
          "debug": {
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.195487,
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
          "bare_term": "生家の歯医者",
          "debug": {
            "completion_tokens": 499,
            "finish_reason": "stop",
            "latency_s": 4.767558,
            "model": "gpt-6-luna",
            "prompt_tokens": 2979,
            "reasoning_tokens": 422
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語がない語句だけのコメントなので、質問の形を確認できません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「生家の歯医者」って、何が生家の歯医者なのかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "生家の歯医者？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.19555302397930063,
      "judge_s": 4.7675964160007425,
      "luna_s": 4.7675964160007425,
      "total_s": 8.446502820006572,
      "writer_s": 3.6789064040058292
    }
  },
  {
    "case_id": "U22-t02",
    "record": {
      "comment_id": "U22-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "引っ越し",
          "debug": {
            "calls": 1,
            "input_tokens": 928,
            "latency_s": 0.192886,
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
          "bare_term": "引っ越し",
          "debug": {
            "completion_tokens": 144,
            "finish_reason": "stop",
            "latency_s": 2.094564,
            "model": "gpt-6-luna",
            "prompt_tokens": 2975,
            "reasoning_tokens": 67
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直してもらいます。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "引っ越しが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "引っ越し",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.1929395140032284,
      "judge_s": 2.0946107560012024,
      "luna_s": 2.0946107560012024,
      "total_s": 5.765490960009629,
      "writer_s": 3.6708802040084265
    }
  },
  {
    "case_id": "c-ask_spoiler-04",
    "record": {
      "comment_id": "c-ask_spoiler-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "calls": 2,
            "input_tokens": 1419,
            "latency_s": 0.423795,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.08,
                "reaction": 0.0,
                "request": 0.92
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.1
            }
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "段A=request→ask_spoiler"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 320,
            "finish_reason": "stop",
            "latency_s": 3.479691,
            "model": "gpt-6-luna",
            "prompt_tokens": 2977,
            "reasoning_tokens": 229
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "正解を直接尋ねているため、ネタバレ要求と判定します。"
        }
      },
      "media_id": "local-U22",
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
      "shadow_mismatch": false,
      "text": "正解は何なん？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.42391502900864,
      "judge_s": 3.4797556799894664,
      "luna_s": 3.4797556799894664,
      "total_s": 5.12700868700631,
      "writer_s": 1.6472530070168432
    }
  },
  {
    "case_id": "c-greeting-03",
    "record": {
      "comment_id": "c-greeting-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 1576,
            "latency_s": 0.356107,
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
              "A_bare": 0.55
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
            "completion_tokens": 148,
            "finish_reason": "stop",
            "latency_s": 2.191649,
            "model": "gpt-6-luna",
            "prompt_tokens": 2974,
            "reasoning_tokens": 87
          },
          "error": null,
          "kind": "greeting",
          "reason": "挨拶のみで、問題の推理や質問ではありません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "こんちは！来てくれてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "こんちは！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.35618578898720443,
      "judge_s": 2.1917000229877885,
      "luna_s": 2.1917000229877885,
      "total_s": 3.6052440800121985,
      "writer_s": 1.41354405702441
    }
  },
  {
    "case_id": "c-request-02",
    "record": {
      "comment_id": "c-request-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 1588,
            "latency_s": 0.369296,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.8,
                "request": 0.16
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 1.0
              },
              "A_bare": 0.3
            }
          },
          "error": null,
          "kind": "request",
          "reason": "段A=reaction→request"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 148,
            "finish_reason": "stop",
            "latency_s": 2.527065,
            "model": "gpt-6-luna",
            "prompt_tokens": 2981,
            "reasoning_tokens": 91
          },
          "error": null,
          "kind": "request",
          "reason": "動物が登場する問題を希望するリクエストです。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいね、動物の問題も楽しみにしててね！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "動物が出てくるやつ希望",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3694055679952726,
      "judge_s": 2.5271350929979235,
      "luna_s": 2.5271350929979235,
      "total_s": 4.39814338699216,
      "writer_s": 1.8710082939942367
    }
  },
  {
    "case_id": "c-emoji_only-01",
    "record": {
      "comment_id": "c-emoji_only-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "completion_tokens": 91,
            "finish_reason": "stop",
            "latency_s": 2.170004,
            "model": "gpt-6-luna",
            "prompt_tokens": 2975,
            "reasoning_tokens": 43
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけのコメントです。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ふむふむ、ゆっくり考えてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "🤔💭",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 6.247599958442152e-05,
      "judge_s": 2.170056717004627,
      "luna_s": 2.170056717004627,
      "total_s": 4.30235708199325,
      "writer_s": 2.132300364988623
    }
  },
  {
    "case_id": "c-abuse-05",
    "record": {
      "comment_id": "c-abuse-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
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
            "input_tokens": 1486,
            "latency_s": 0.382243,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.91,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.08,
                "request": 0.0
              },
              "A2": {
                "abuse": 1.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 0.0
              },
              "A_bare": 0.04
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
            "completion_tokens": 255,
            "finish_reason": "stop",
            "latency_s": 2.952636,
            "model": "gpt-6-luna",
            "prompt_tokens": 2984,
            "reasoning_tokens": 195
          },
          "error": null,
          "kind": "abuse",
          "reason": "相手の性的嗜好を決めつけ、気持ち悪いと攻撃しているため。"
        }
      },
      "media_id": "local-U22",
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
      "text": "性的なことばっか考えてそうでキモい",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.38237115999800153,
      "judge_s": 2.9526610579923727,
      "luna_s": 2.9526610579923727,
      "total_s": 2.952675473992713,
      "writer_s": 1.4416000340133905e-05
    }
  },
  {
    "case_id": "c-foreign-04",
    "record": {
      "comment_id": "c-foreign-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "foreign"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1417,
            "latency_s": 0.378275,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.0,
                "request": 0.95
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.13
            }
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "段A=request→ask_spoiler"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 178,
            "finish_reason": "stop",
            "latency_s": 2.365727,
            "model": "gpt-6-luna",
            "prompt_tokens": 2974,
            "reasoning_tokens": 113
          },
          "error": null,
          "kind": "foreign",
          "reason": "漢字のみの中国語で、答えを尋ねるコメントです。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "日本語で質問してね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "答案是什么？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3784328470064793,
      "judge_s": 2.3658005300094374,
      "luna_s": 2.3658005300094374,
      "total_s": 3.6171779299911577,
      "writer_s": 1.2513773999817204
    }
  }
];

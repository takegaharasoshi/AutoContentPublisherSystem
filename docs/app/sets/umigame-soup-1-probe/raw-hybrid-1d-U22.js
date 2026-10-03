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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4209,
            "latency_s": 1.140174,
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
                "guess": 0.57,
                "question": 0.43
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
              "C": 0.56,
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
            "completion_tokens": 253,
            "finish_reason": "stop",
            "latency_s": 18.24168,
            "model": "gpt-6-luna",
            "prompt_tokens": 2964,
            "reasoning_tokens": 182
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1404452149872668,
      "judge_s": 18.241716754011577,
      "luna_s": 18.241716754011577,
      "total_s": 19.6117737859895,
      "writer_s": 1.3700570319779217
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4245,
            "latency_s": 1.417894,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.98,
                "reaction": 0.02,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.14,
                "question": 0.86
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.05,
                "q_yesno": 0.95
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.47,
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
            "completion_tokens": 334,
            "finish_reason": "stop",
            "latency_s": 3.160224,
            "model": "gpt-6-luna",
            "prompt_tokens": 2968,
            "reasoning_tokens": 251
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "一つの yes／no 質問。通院の目的は歯の治療ではなく、懐かしい家を訪れることです。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。歯の治療が目的じゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "歯医者に通うのは、歯の治療が目的じゃないんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.4181462319975253,
      "judge_s": 3.1602559630118776,
      "luna_s": 3.1602559630118776,
      "total_s": 4.79848686902551,
      "writer_s": 1.6382309060136322
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4215,
            "latency_s": 1.239224,
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
                "guess": 0.18,
                "question": 0.82
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.11
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
          "reason": "段A=question→q_yesno, 要点最低=0.11"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 247,
            "finish_reason": "stop",
            "latency_s": 2.854234,
            "model": "gpt-6-luna",
            "prompt_tokens": 2964,
            "reasoning_tokens": 168
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "40年後に事情を知って通い始めたため、昔からのかかりつけではありません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。その歯医者は男の昔からのかかりつけじゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その歯医者は男の昔からのかかりつけですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2394391269772314,
      "judge_s": 2.8542857249849476,
      "luna_s": 2.8542857249849476,
      "total_s": 4.31530279899016,
      "writer_s": 1.4610170740052126
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4227,
            "latency_s": 1.187399,
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
              "C": 0.61,
              "D": {
                "irrelevant": 0.02,
                "no": 0.98,
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
            "completion_tokens": 303,
            "finish_reason": "stop",
            "latency_s": 3.068604,
            "model": "gpt-6-luna",
            "prompt_tokens": 2965,
            "reasoning_tokens": 231
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "誰かを待っているのではなく、懐かしんで座っているため。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1875757579982746,
      "judge_s": 3.068630157998996,
      "luna_s": 3.068630157998996,
      "total_s": 4.459606596006779,
      "writer_s": 1.3909764380077831
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4197,
            "latency_s": 1.272092,
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
                "q_open": 0.04,
                "q_yesno": 0.96
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
              },
              "C": 0.31,
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
            "completion_tokens": 286,
            "finish_reason": "stop",
            "latency_s": 8.542248,
            "model": "gpt-6-luna",
            "prompt_tokens": 2960,
            "reasoning_tokens": 212
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "同じ席に座る意味を尋ねる一つのはい・いいえ質問で、真相上意味があります。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2727122580108698,
      "judge_s": 8.542299243999878,
      "luna_s": 8.542299243999878,
      "total_s": 12.405084419995546,
      "writer_s": 3.8627851759956684
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
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "unknown",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4221,
            "latency_s": 1.148885,
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
                "guess": 0.39,
                "question": 0.61
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
              "C": 0.59,
              "D": {
                "irrelevant": 0.38,
                "no": 0.44,
                "yes": 0.18
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "completion_tokens": 540,
            "finish_reason": "stop",
            "latency_s": 5.069294,
            "model": "gpt-6-luna",
            "prompt_tokens": 2966,
            "reasoning_tokens": 471
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "会話の有無は、問題文や確定事実から判断できません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "それは答えに関わらないんだ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は毎回、歯医者の人と話をして帰るんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1492048570071347,
      "judge_s": 5.0693451759871095,
      "luna_s": 5.0693451759871095,
      "total_s": 8.973258464975515,
      "writer_s": 3.903913288988406
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4191,
            "latency_s": 1.327226,
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
                "guess": 0.46,
                "question": 0.54
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
              "C": 0.23,
              "D": {
                "irrelevant": 0.33,
                "no": 0.66,
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
            "completion_tokens": 253,
            "finish_reason": "stop",
            "latency_s": 3.072076,
            "model": "gpt-6-luna",
            "prompt_tokens": 2960,
            "reasoning_tokens": 173
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "家族や友人がその町に住んでいるかは、真相に関係しません。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3275548639940098,
      "judge_s": 3.072129711013986,
      "luna_s": 3.072129711013986,
      "total_s": 4.152799920033431,
      "writer_s": 1.0806702090194449
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
        "prompt_version": "5311b19312cf",
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
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4263,
            "latency_s": 1.225886,
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
                "q_open": 0.3,
                "q_yesno": 0.69
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.39,
              "D": {
                "irrelevant": 0.33,
                "no": 0.42,
                "yes": 0.25
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
            "completion_tokens": 604,
            "finish_reason": "stop",
            "latency_s": 5.788711,
            "model": "gpt-6-luna",
            "prompt_tokens": 2969,
            "reasoning_tokens": 538
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "電車でなければならないかは真相に関係しません。"
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
      "text": "歯医者に行くのは電車じゃないといけない理由があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.226184422004735,
      "judge_s": 5.788881696993485,
      "luna_s": 5.788881696993485,
      "total_s": 21.654208224994363,
      "writer_s": 15.865326528000878
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
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "010-two-hour-dentist",
      "errors": [],
      "fact_sheet_hash": "a58f8fc39e79",
      "final": {
        "answer": "unknown",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4221,
            "latency_s": 1.20264,
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
                "guess": 0.37,
                "question": 0.63
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
              "C": 0.4,
              "D": {
                "irrelevant": 0.74,
                "no": 0.14,
                "yes": 0.12
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "completion_tokens": 389,
            "finish_reason": "stop",
            "latency_s": 3.890099,
            "model": "gpt-6-luna",
            "prompt_tokens": 2964,
            "reasoning_tokens": 298
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "待合室でしばらく過ごすことは分かりますが、診察との長さの比較は示されていません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "それは答えに関わらないんだ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "待合室にいる時間のほうが診察より長いんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2029190799803473,
      "judge_s": 3.890152745996602,
      "luna_s": 3.890152745996602,
      "total_s": 5.608538660017075,
      "writer_s": 1.7183859140204731
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4179,
            "latency_s": 1.268508,
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
              "A_bare": 0.03,
              "B": {
                "point_0": 0.02
              },
              "C": 0.24,
              "D": {
                "irrelevant": 0.23,
                "no": 0.03,
                "yes": 0.74
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
            "completion_tokens": 234,
            "finish_reason": "stop",
            "latency_s": 7.893059,
            "model": "gpt-6-luna",
            "prompt_tokens": 2959,
            "reasoning_tokens": 161
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では、男が育ったのは古い木造の家とされています。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その歯医者の建物は木造ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2687862830061931,
      "judge_s": 7.893096824991517,
      "luna_s": 7.893096824991517,
      "total_s": 11.340505853993818,
      "writer_s": 3.4474090290023014
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.615329,
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
                "guess": 0.45,
                "question": 0.55
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
            "completion_tokens": 208,
            "finish_reason": "stop",
            "latency_s": 2.88592,
            "model": "gpt-6-luna",
            "prompt_tokens": 2970,
            "reasoning_tokens": 126
          },
          "error": null,
          "kind": "q_multi",
          "reason": "検診かどうかと、誰かを待っているかの質問が二つあります。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。どっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は歯の検診に来てるの？診察後は誰かを待ってるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.615460686996812,
      "judge_s": 2.885971924988553,
      "luna_s": 2.885971924988553,
      "total_s": 6.635325325012673,
      "writer_s": 3.7493534000241198
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.63115,
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
                "guess": 0.69,
                "question": 0.31
              },
              "A2": {
                "q_multi": 0.97,
                "q_open": 0.02,
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
            "completion_tokens": 202,
            "finish_reason": "stop",
            "latency_s": 2.319042,
            "model": "gpt-6-luna",
            "prompt_tokens": 2968,
            "reasoning_tokens": 124
          },
          "error": null,
          "kind": "q_multi",
          "reason": "一つのコメントに質問が二つ含まれています。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。どっちか聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "同じ席に座るのは昔から？その席に何か思い出があるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6312867820088286,
      "judge_s": 2.3190683229768183,
      "luna_s": 2.3190683229768183,
      "total_s": 6.098817177000456,
      "writer_s": 3.7797488540236373
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.806687,
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
            "completion_tokens": 190,
            "finish_reason": "stop",
            "latency_s": 7.474711,
            "model": "gpt-6-luna",
            "prompt_tokens": 2963,
            "reasoning_tokens": 97
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねており、はい・いいえでは答えられないため。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「男は〜ですか？」のように、はい／いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はどうして遠くの歯医者に通ってるんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8068945480044931,
      "judge_s": 7.474764800979756,
      "luna_s": 7.474764800979756,
      "total_s": 11.74380761696375,
      "writer_s": 4.269042815983994
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.786962,
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
                "guess": 0.26,
                "question": 0.74
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.97,
                "q_yesno": 0.02
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
            "completion_tokens": 250,
            "finish_reason": "stop",
            "latency_s": 2.768672,
            "model": "gpt-6-luna",
            "prompt_tokens": 2966,
            "reasoning_tokens": 158
          },
          "error": null,
          "kind": "q_open",
          "reason": "「誰を待っているか」は自由回答で、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰を待っているのか、候補を挙げて「〇〇を待っている？」と聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "診察が終わったあと、待合室で誰を待っているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7871673130139243,
      "judge_s": 2.768716608028626,
      "luna_s": 2.768716608028626,
      "total_s": 5.144462665019091,
      "writer_s": 2.375746056990465
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.829983,
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
              "A3": 0.06,
              "A_bare": 0.03
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
            "completion_tokens": 138,
            "finish_reason": "stop",
            "latency_s": 8.425681,
            "model": "gpt-6-luna",
            "prompt_tokens": 2965,
            "reasoning_tokens": 62
          },
          "error": null,
          "kind": "q_open",
          "reason": "関係性を尋ねる、はい・いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "その町や歯医者と男に関係があるのか、はい／いいえで聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その町や歯医者と男にはどんな関係があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8301558470120654,
      "judge_s": 8.425763225008268,
      "luna_s": 8.425763225008268,
      "total_s": 10.881449363019783,
      "writer_s": 2.455686138011515
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
        "prompt_version": "5311b19312cf",
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
            "calls": 3,
            "input_tokens": 1989,
            "latency_s": 0.588011,
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
                "guess": 0.96,
                "question": 0.04
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.89
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.89"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 284,
            "finish_reason": "stop",
            "latency_s": 8.099425,
            "model": "gpt-6-luna",
            "prompt_tokens": 2965,
            "reasoning_tokens": 170
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "歯医者が幼少期に住んでいた家だと、コアの要点を言い当てています。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.588146202993812,
      "judge_s": 8.09946391399717,
      "luna_s": 8.09946391399717,
      "total_s": 8.099477640993427,
      "writer_s": 1.3726996257901192e-05
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
        "prompt_version": "5311b19312cf",
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
            "calls": 3,
            "input_tokens": 2073,
            "latency_s": 0.60787,
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
                "point_0": 0.93
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.93"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 299,
            "finish_reason": "stop",
            "latency_s": 18.829939,
            "model": "gpt-6-luna",
            "prompt_tokens": 2991,
            "reasoning_tokens": 197
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "歯医者が育った家で、懐かしむために通う核心を捉えています。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6081068370258436,
      "judge_s": 18.8299707499973,
      "luna_s": 18.8299707499973,
      "total_s": 18.829975662985817,
      "writer_s": 4.91298851557076e-06
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4269,
            "latency_s": 1.387438,
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
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.13
              },
              "C": 0.29,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.13"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 587,
            "finish_reason": "stop",
            "latency_s": 10.4858,
            "model": "gpt-6-luna",
            "prompt_tokens": 2971,
            "reasoning_tokens": 512
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "建物と男の過去の関わりを一つ尋ねています。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.3881116280099377,
      "judge_s": 10.485853357007727,
      "luna_s": 10.485853357007727,
      "total_s": 11.518220331025077,
      "writer_s": 1.03236697401735
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
        "prompt_version": "5311b19312cf",
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
            "calls": 3,
            "input_tokens": 2091,
            "latency_s": 0.696147,
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
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.95
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.95"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 848,
            "finish_reason": "stop",
            "latency_s": 6.883487,
            "model": "gpt-6-luna",
            "prompt_tokens": 3000,
            "reasoning_tokens": 771
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "核心を述べたうえで、傷を刻んだ人物を確認する質問。真相では父親が刻んでいます。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6964465059863869,
      "judge_s": 6.8835218849999364,
      "luna_s": 6.8835218849999364,
      "total_s": 10.02103472899762,
      "writer_s": 3.1375128439976834
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
        "prompt_version": "5311b19312cf",
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
            "input_tokens": 4299,
            "latency_s": 1.209434,
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
              "C": 0.43,
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
            "completion_tokens": 230,
            "finish_reason": "stop",
            "latency_s": 8.024385,
            "model": "gpt-6-luna",
            "prompt_tokens": 2976,
            "reasoning_tokens": 160
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "通う理由を先生に会うこととしていますが、歯医者が生家という核心には触れていません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。質問で少しずつ考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "昔から通ってる先生に会いたくて、診察を口実に半年ごとに訪ねてるんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2097001880174503,
      "judge_s": 8.02442747898749,
      "luna_s": 8.02442747898749,
      "total_s": 9.05801944900304,
      "writer_s": 1.03359197001555
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.945271,
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
                "q_open": 0.75,
                "q_yesno": 0.23
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
            "completion_tokens": 138,
            "finish_reason": "stop",
            "latency_s": 2.016445,
            "model": "gpt-6-luna",
            "prompt_tokens": 2972,
            "reasoning_tokens": 67
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "待合室で探し物をするという推理で、歯医者が生家だった点には触れていません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の考え方もしてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "待合室の席に忘れ物をしていて、診察のたびに探してるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.9455069430114236,
      "judge_s": 2.0164655510161538,
      "luna_s": 2.0164655510161538,
      "total_s": 2.822771705017658,
      "writer_s": 0.8063061540015042
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
        "prompt_version": "5311b19312cf",
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
          "bare_term": "生家の歯医者",
          "debug": {
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.233636,
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
              "A_bare": 0.88
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.88"
        },
        "luna": {
          "answer": null,
          "bare_term": "生家の歯医者",
          "debug": {
            "completion_tokens": 310,
            "finish_reason": "stop",
            "latency_s": 2.934185,
            "model": "gpt-6-luna",
            "prompt_tokens": 2953,
            "reasoning_tokens": 221
          },
          "error": null,
          "kind": "q_open",
          "reason": "名詞句だけで、はい・いいえで答えられる質問になっていません。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "生家の歯医者がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "生家の歯医者？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.23370975299621932,
      "judge_s": 2.934234568005195,
      "luna_s": 2.934234568005195,
      "total_s": 7.760582085000351,
      "writer_s": 4.826347516995156
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.194527,
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
            "completion_tokens": 220,
            "finish_reason": "stop",
            "latency_s": 38.135274,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 142
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直しを促します。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.19460854699718766,
      "judge_s": 38.135324794013286,
      "luna_s": 38.135324794013286,
      "total_s": 47.63850674699643,
      "writer_s": 9.503181952983141
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.436153,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.1,
                "reaction": 0.0,
                "request": 0.9
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.11
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
            "completion_tokens": 183,
            "finish_reason": "stop",
            "latency_s": 2.887041,
            "model": "gpt-6-luna",
            "prompt_tokens": 2951,
            "reasoning_tokens": 99
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "正解を尋ねているため、ネタバレ希望と判定しました。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.4362563080212567,
      "judge_s": 2.88706636702409,
      "luna_s": 2.88706636702409,
      "total_s": 4.468699841032503,
      "writer_s": 1.581633474008413
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.520201,
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
              "A_bare": 0.48
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
            "completion_tokens": 184,
            "finish_reason": "stop",
            "latency_s": 2.515986,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 116
          },
          "error": null,
          "kind": "greeting",
          "reason": "挨拶のみのコメントなので、歓迎の相づちを返します。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5203301969741005,
      "judge_s": 2.5160408949886914,
      "luna_s": 2.5160408949886914,
      "total_s": 3.8063372729811817,
      "writer_s": 1.2902963779924903
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.429064,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.72,
                "request": 0.23
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
              "A_bare": 0.33
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
            "completion_tokens": 111,
            "finish_reason": "stop",
            "latency_s": 2.024814,
            "model": "gpt-6-luna",
            "prompt_tokens": 2955,
            "reasoning_tokens": 54
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
        "text": "リクエストありがとう！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "動物が出てくるやつ希望",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.42917063800268807,
      "judge_s": 2.024875795992557,
      "luna_s": 2.024875795992557,
      "total_s": 5.473967904981691,
      "writer_s": 3.4490921089891344
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
        "prompt_version": "5311b19312cf",
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
            "completion_tokens": 113,
            "finish_reason": "stop",
            "latency_s": 1.904123,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 59
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ふむふむ、ありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "🤔💭",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 6.39770005363971e-05,
      "judge_s": 1.9041565629886463,
      "luna_s": 1.9041565629886463,
      "total_s": 3.245605832984438,
      "writer_s": 1.3414492699957918
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.410672,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.89,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.1,
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
            "completion_tokens": 145,
            "finish_reason": "stop",
            "latency_s": 17.685842,
            "model": "gpt-6-luna",
            "prompt_tokens": 2958,
            "reasoning_tokens": 92
          },
          "error": null,
          "kind": "abuse",
          "reason": "性的な内容を含み、相手を侮辱する表現です。"
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
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.41080188800697215,
      "judge_s": 17.68586892998428,
      "luna_s": 17.68586892998428,
      "total_s": 17.68589750197134,
      "writer_s": 2.8571987058967352e-05
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
        "prompt_version": "5311b19312cf",
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
            "latency_s": 0.369774,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.0,
                "request": 0.96
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
            "completion_tokens": 120,
            "finish_reason": "stop",
            "latency_s": 1.848969,
            "model": "gpt-6-luna",
            "prompt_tokens": 2948,
            "reasoning_tokens": 54
          },
          "error": null,
          "kind": "foreign",
          "reason": "ひらがな・カタカナを含まない中国語の文と判断しました。"
        }
      },
      "media_id": "local-U22",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "日本語で質問してね。待ってるよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "答案是什么？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.3698588100087363,
      "judge_s": 1.8490197689970955,
      "luna_s": 1.8490197689970955,
      "total_s": 3.4666175589954946,
      "writer_s": 1.617597789998399
    }
  }
];

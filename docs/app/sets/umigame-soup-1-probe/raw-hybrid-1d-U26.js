window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U26"] = [
  {
    "case_id": "U26-e01",
    "record": {
      "comment_id": "U26-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4325,
            "latency_s": 1.200285,
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
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.48,
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
            "completion_tokens": 206,
            "finish_reason": "stop",
            "latency_s": 2.650694,
            "model": "gpt-6-luna",
            "prompt_tokens": 3070,
            "reasoning_tokens": 139
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、日本語を覚える前も毎日会話していたとあります。"
        }
      },
      "media_id": "local-U26",
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
      "text": "日本語を覚える前も、二人は毎日会話してたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.200610432017129,
      "judge_s": 2.6507515530101955,
      "luna_s": 2.6507515530101955,
      "total_s": 3.621241988003021,
      "writer_s": 0.9704904349928256
    }
  },
  {
    "case_id": "U26-e02",
    "record": {
      "comment_id": "U26-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4271,
            "latency_s": 1.189417,
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
                "guess": 0.87,
                "question": 0.13
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
              "C": 0.48,
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
            "completion_tokens": 341,
            "finish_reason": "stop",
            "latency_s": 4.13672,
            "model": "gpt-6-luna",
            "prompt_tokens": 3062,
            "reasoning_tokens": 264
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では息子が通訳し、夫は仕事で帰りが遅かったためです。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "夫が間に入って通訳してた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1897600060037803,
      "judge_s": 4.136777242994867,
      "luna_s": 4.136777242994867,
      "total_s": 5.635318862972781,
      "writer_s": 1.4985416199779138
    }
  },
  {
    "case_id": "U26-e03",
    "record": {
      "comment_id": "U26-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4277,
            "latency_s": 1.262849,
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
                "guess": 0.55,
                "question": 0.45
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.06,
              "B": {
                "point_0": 0.07
              },
              "C": 0.23,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.07"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 266,
            "finish_reason": "stop",
            "latency_s": 3.050924,
            "model": "gpt-6-luna",
            "prompt_tokens": 3063,
            "reasoning_tokens": 189
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "間に入っていた人物が家族かを尋ねる一つの質問で、確定事実から判断できます。"
        }
      },
      "media_id": "local-U26",
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
      "text": "間に入って伝えてたのは家族？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2632248990121298,
      "judge_s": 3.050989342009416,
      "luna_s": 3.050989342009416,
      "total_s": 4.609097005013609,
      "writer_s": 1.5581076630041935
    }
  },
  {
    "case_id": "U26-e04",
    "record": {
      "comment_id": "U26-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4307,
            "latency_s": 1.24026,
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
                "guess": 0.49,
                "question": 0.51
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
              "C": 0.42,
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
            "completion_tokens": 165,
            "finish_reason": "stop",
            "latency_s": 2.143018,
            "model": "gpt-6-luna",
            "prompt_tokens": 3067,
            "reasoning_tokens": 96
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、この春から辞書を使って自分で勉強したとあります。"
        }
      },
      "media_id": "local-U26",
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
      "text": "女は最近、辞書で日本語を勉強したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2407186509808525,
      "judge_s": 2.1430735909962095,
      "luna_s": 2.1430735909962095,
      "total_s": 3.203696215990931,
      "writer_s": 1.0606226249947213
    }
  },
  {
    "case_id": "U26-e05",
    "record": {
      "comment_id": "U26-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4295,
            "latency_s": 1.130044,
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
                "guess": 0.93,
                "question": 0.07
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
              "C": 0.35,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
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
            "completion_tokens": 311,
            "finish_reason": "stop",
            "latency_s": 3.48978,
            "model": "gpt-6-luna",
            "prompt_tokens": 3065,
            "reasoning_tokens": 233
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、義母の性格や考え方はこの10年で変わっていないとされています。"
        }
      },
      "media_id": "local-U26",
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
      "text": "義母の性格がこの10年で変わった？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1304028340091463,
      "judge_s": 3.489808587008156,
      "luna_s": 3.489808587008156,
      "total_s": 5.1702782420034055,
      "writer_s": 1.6804696549952496
    }
  },
  {
    "case_id": "U26-e06",
    "record": {
      "comment_id": "U26-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4283,
            "latency_s": 1.178729,
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
                "guess": 0.94,
                "question": 0.06
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.02
              },
              "C": 0.36,
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
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 238,
            "finish_reason": "stop",
            "latency_s": 2.931414,
            "model": "gpt-6-luna",
            "prompt_tokens": 3066,
            "reasoning_tokens": 167
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、近所の人は何もしていないとされています。"
        }
      },
      "media_id": "local-U26",
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
      "text": "近所の人が悪口を吹き込んだの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1790725199971348,
      "judge_s": 2.9314428210200276,
      "luna_s": 2.9314428210200276,
      "total_s": 5.030940343014663,
      "writer_s": 2.0994975219946355
    }
  },
  {
    "case_id": "U26-e07",
    "record": {
      "comment_id": "U26-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4283,
            "latency_s": 1.379325,
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
                "guess": 0.01,
                "question": 0.99
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
              "C": 0.37,
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
            "completion_tokens": 218,
            "finish_reason": "stop",
            "latency_s": 2.90414,
            "model": "gpt-6-luna",
            "prompt_tokens": 3066,
            "reasoning_tokens": 155
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "今も同じ家で暮らしていると確定事実にあります。"
        }
      },
      "media_id": "local-U26",
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
      "text": "二人は今も同じ家に住んでるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.37950557100703,
      "judge_s": 2.904170157999033,
      "luna_s": 2.904170157999033,
      "total_s": 4.95578565300093,
      "writer_s": 2.051615495001897
    }
  },
  {
    "case_id": "U26-e08",
    "record": {
      "comment_id": "U26-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4307,
            "latency_s": 1.139255,
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
                "q_multi": 0.09,
                "q_open": 0.03,
                "q_yesno": 0.88
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
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
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 158,
            "finish_reason": "stop",
            "latency_s": 2.605653,
            "model": "gpt-6-luna",
            "prompt_tokens": 3066,
            "reasoning_tokens": 99
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、けんかの話題は料理や家事とされています。"
        }
      },
      "media_id": "local-U26",
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
      "text": "言い合いの話題は料理とか家事だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1394985699735116,
      "judge_s": 2.6057248710130807,
      "luna_s": 2.6057248710130807,
      "total_s": 4.478324808005709,
      "writer_s": 1.8725999369926285
    }
  },
  {
    "case_id": "U26-e09",
    "record": {
      "comment_id": "U26-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4325,
            "latency_s": 1.13313,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 238,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.98,
                "reaction": 0.01,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.03,
                "q_yesno": 0.96
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.01
              },
              "C": 0.36,
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
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 186,
            "finish_reason": "stop",
            "latency_s": 2.51226,
            "model": "gpt-6-luna",
            "prompt_tokens": 3068,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "出身国は問題に関係ないと確定事実にあるため。"
        }
      },
      "media_id": "local-U26",
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
      "text": "女がどこの国から来たかって、問題に関係ある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.133331121003721,
      "judge_s": 2.512288477999391,
      "luna_s": 2.512288477999391,
      "total_s": 4.067831844004104,
      "writer_s": 1.5555433660047129
    }
  },
  {
    "case_id": "U26-e10",
    "record": {
      "comment_id": "U26-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 5,
            "input_tokens": 3000,
            "latency_s": 0.957101,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 198,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.2,
                "question": 0.8
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
              "C": 0.18
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.01"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 168,
            "finish_reason": "stop",
            "latency_s": 2.732083,
            "model": "gpt-6-luna",
            "prompt_tokens": 3063,
            "reasoning_tokens": 110
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、夫は仕事で帰りが遅かったとあります。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！ほかにも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "夫は仕事で遅く帰ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.9573198219877668,
      "judge_s": 2.732139476982411,
      "luna_s": 2.732139476982411,
      "total_s": 4.808724402973894,
      "writer_s": 2.076584925991483
    }
  },
  {
    "case_id": "U26-e11",
    "record": {
      "comment_id": "U26-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 2135,
            "latency_s": 0.58102,
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
                "guess": 0.14,
                "question": 0.86
              },
              "A2": {
                "q_multi": 0.98,
                "q_open": 0.02,
                "q_yesno": 0.0
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
            "completion_tokens": 173,
            "finish_reason": "stop",
            "latency_s": 2.103309,
            "model": "gpt-6-luna",
            "prompt_tokens": 3072,
            "reasoning_tokens": 100
          },
          "error": null,
          "kind": "q_multi",
          "reason": "通訳役と夫の在宅状況について、質問が二つあります。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどちらか一つ聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "誰が二人の間で訳してたの？夫は家にいなかったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.5811713680159301,
      "judge_s": 2.103366750990972,
      "luna_s": 2.103366750990972,
      "total_s": 3.794629450974753,
      "writer_s": 1.6912626999837812
    }
  },
  {
    "case_id": "U26-e12",
    "record": {
      "comment_id": "U26-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 2165,
            "latency_s": 0.599742,
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
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.96,
                "q_open": 0.04,
                "q_yesno": 0.0
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
            "completion_tokens": 184,
            "finish_reason": "stop",
            "latency_s": 2.275838,
            "model": "gpt-6-luna",
            "prompt_tokens": 3077,
            "reasoning_tokens": 100
          },
          "error": null,
          "kind": "q_multi",
          "reason": "日本語を覚えた時期と、言い合いの内容を尋ねる質問が二つあります。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "日本語が話せるようになったのはいつ？二人は何のことで言い合ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6003036290057935,
      "judge_s": 2.275895364000462,
      "luna_s": 2.275895364000462,
      "total_s": 4.1192605959950015,
      "writer_s": 1.8433652319945395
    }
  },
  {
    "case_id": "U26-e13",
    "record": {
      "comment_id": "U26-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 2686,
            "latency_s": 0.804675,
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
                "guess": 0.04,
                "question": 0.96
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
            "completion_tokens": 191,
            "finish_reason": "stop",
            "latency_s": 2.524824,
            "model": "gpt-6-luna",
            "prompt_tokens": 3074,
            "reasoning_tokens": 106
          },
          "error": null,
          "kind": "q_open",
          "reason": "「なぜ」と理由を尋ねており、はい／いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してごらん。誰のことか分かるように書いてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "なぜ日本語を覚えてから、二人は毎日けんかするようになったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.804951814992819,
      "judge_s": 2.5248863070155494,
      "luna_s": 2.5248863070155494,
      "total_s": 3.9834534770052414,
      "writer_s": 1.458567169989692
    }
  },
  {
    "case_id": "U26-e14",
    "record": {
      "comment_id": "U26-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "latency_s": 1.018994,
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
                "guess": 0.07,
                "question": 0.93
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 1.0,
                "q_yesno": 0.0
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
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.316696,
            "model": "gpt-6-luna",
            "prompt_tokens": 3071,
            "reasoning_tokens": 79
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねており、はい／いいえでは答えられません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰が仲がいいと思っていたのかも含めて、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どうして二人は10年間も近所で仲がいいと思われていたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0193711410101969,
      "judge_s": 2.3167856379877776,
      "luna_s": 2.3167856379877776,
      "total_s": 3.7568892799899913,
      "writer_s": 1.4401036420022137
    }
  },
  {
    "case_id": "U26-e15",
    "record": {
      "comment_id": "U26-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 2630,
            "latency_s": 0.741438,
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
                "guess": 0.25,
                "question": 0.75
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.98,
                "q_yesno": 0.02
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
            "completion_tokens": 323,
            "finish_reason": "stop",
            "latency_s": 3.129917,
            "model": "gpt-6-luna",
            "prompt_tokens": 3063,
            "reasoning_tokens": 236
          },
          "error": null,
          "kind": "q_open",
          "reason": "「いつから」ははい／いいえで答えられず、指す対象も曖昧です。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰が何を言ったのか分かるようにして、はい／いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "彼女はそれをいつから言ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7417030119977426,
      "judge_s": 3.129973378003342,
      "luna_s": 3.129973378003342,
      "total_s": 5.380159129999811,
      "writer_s": 2.2501857519964688
    }
  },
  {
    "case_id": "U26-e16",
    "record": {
      "comment_id": "U26-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 3608,
            "latency_s": 0.778403,
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
                "point_0": 0.87
              },
              "B2": 0.06
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.87, 矛盾=0.06"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 486,
            "finish_reason": "stop",
            "latency_s": 4.657281,
            "model": "gpt-6-luna",
            "prompt_tokens": 3138,
            "reasoning_tokens": 371
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "息子が不満を和らげて通訳した仕掛けと、その後の変化まで説明しています。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "息子が母と義母の通訳をしていたが、けんかを避けるため互いの不満をやさしい言葉に作り替えていた。息子が寮に入り、母が日本語を覚えて本音を直接聞くと、二人は言い合いを始め、通訳が作り話だったと気づいた。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7787207920046058,
      "judge_s": 4.65732191799907,
      "luna_s": 4.65732191799907,
      "total_s": 4.657334187999368,
      "writer_s": 1.2270000297576189e-05
    }
  },
  {
    "case_id": "U26-e17",
    "record": {
      "comment_id": "U26-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 3444,
            "latency_s": 0.793391,
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
                "point_0": 0.77
              },
              "B2": 0.19
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.77, 矛盾=0.19"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 408,
            "finish_reason": "stop",
            "latency_s": 3.911358,
            "model": "gpt-6-luna",
            "prompt_tokens": 3102,
            "reasoning_tokens": 284
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "息子が悪口を好意的に変えて訳し、日本語習得後に本音が伝わった点まで合っています。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！息子が嫁と義母の言葉を作り替えて通訳していた。女が日本語を覚えて本音が伝わり、けんかが始まった。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "息子が嫁と義母の言葉を仲直りのために作り替えて訳していた。日本語を覚えた嫁に本音が伝わり、けんかが始まった、ってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.793747545016231,
      "judge_s": 3.911418236006284,
      "luna_s": 3.911418236006284,
      "total_s": 3.9114224769873545,
      "writer_s": 4.2409810703247786e-06
    }
  },
  {
    "case_id": "U26-e18",
    "record": {
      "comment_id": "U26-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "calls": 5,
            "guess_demoted": true,
            "input_tokens": 3116,
            "latency_s": 1.076029,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 200,
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
                "q_multi": 0.09,
                "q_open": 0.27,
                "q_yesno": 0.64
              },
              "A3": 0.24,
              "A_bare": 0.02,
              "B": {
                "point_0": 0.19
              }
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.19"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 447,
            "finish_reason": "stop",
            "latency_s": 4.82514,
            "model": "gpt-6-luna",
            "prompt_tokens": 3080,
            "reasoning_tokens": 380
          },
          "error": null,
          "kind": "guess_close",
          "reason": "家族が間に入る点には触れていますが、核心の言い換えまでは示せていません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えながら、推理を続けてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "会話の間にいつも家族が入って訳していて、その人の伝え方が変わったんじゃない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.0763033399998676,
      "judge_s": 4.825198473001365,
      "luna_s": 4.825198473001365,
      "total_s": 6.944124683010159,
      "writer_s": 2.1189262100087944
    }
  },
  {
    "case_id": "U26-e19",
    "record": {
      "comment_id": "U26-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 1998,
            "latency_s": 0.606888,
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
              "A_bare": 0.03,
              "B": {
                "point_0": 0.41
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.41"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 247,
            "finish_reason": "stop",
            "latency_s": 3.25978,
            "model": "gpt-6-luna",
            "prompt_tokens": 3078,
            "reasoning_tokens": 177
          },
          "error": null,
          "kind": "guess_close",
          "reason": "言葉を良い方に変えて伝えた点は触れていますが、誰がしたかが特定されていません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "誰かが2人の言葉をわざと良い言葉に変えて伝えてたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.607147383998381,
      "judge_s": 3.2598360430274624,
      "luna_s": 3.2598360430274624,
      "total_s": 5.001276815019082,
      "writer_s": 1.7414407719916198
    }
  },
  {
    "case_id": "U26-e20",
    "record": {
      "comment_id": "U26-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 2571,
            "latency_s": 0.881015,
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
                "q_open": 0.87,
                "q_yesno": 0.11
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 239,
            "finish_reason": "stop",
            "latency_s": 2.874484,
            "model": "gpt-6-luna",
            "prompt_tokens": 3083,
            "reasoning_tokens": 168
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "けんかの理由を推測していますが、通訳で言葉を変えた仕掛けには触れていません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "義母がこの10年で急に意地悪になり、嫁が腹を立てたから毎日けんかしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8814094139961526,
      "judge_s": 2.874541468976531,
      "luna_s": 2.874541468976531,
      "total_s": 4.18572738696821,
      "writer_s": 1.3111859179916792
    }
  },
  {
    "case_id": "U26-e21",
    "record": {
      "comment_id": "U26-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "guess_demoted": true,
            "input_tokens": 2531,
            "latency_s": 0.771451,
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
                "q_open": 0.69,
                "q_yesno": 0.3
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.02"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 349,
            "finish_reason": "stop",
            "latency_s": 4.255158,
            "model": "gpt-6-luna",
            "prompt_tokens": 3076,
            "reasoning_tokens": 280
          },
          "error": null,
          "kind": "guess_close",
          "reason": "伝言の食い違いには触れていますが、誰が何をしたかの推理が真相とは異なります。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "近所の人が二人の間で嘘を吹き込み、仲を悪くしたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7717442880093586,
      "judge_s": 4.255223044019658,
      "luna_s": 4.255223044019658,
      "total_s": 6.820819529006258,
      "writer_s": 2.5655964849865995
    }
  },
  {
    "case_id": "U26-b22",
    "record": {
      "comment_id": "U26-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4301,
            "latency_s": 1.148814,
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
                "guess": 0.19,
                "question": 0.81
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
              "C": 0.52,
              "D": {
                "irrelevant": 0.23,
                "no": 0.75,
                "yes": 0.02
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
            "completion_tokens": 451,
            "finish_reason": "stop",
            "latency_s": 4.811695,
            "model": "gpt-6-luna",
            "prompt_tokens": 3067,
            "reasoning_tokens": 373
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "義母が日本語以外も話せたかは、真相や確定事実から判断できません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "義母は日本語以外の言葉を話してたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1490626449813135,
      "judge_s": 4.811741581012029,
      "luna_s": 4.811741581012029,
      "total_s": 6.642592092015548,
      "writer_s": 1.8308505110035185
    }
  },
  {
    "case_id": "U26-b23",
    "record": {
      "comment_id": "U26-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4271,
            "latency_s": 1.169265,
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
                "guess": 0.01,
                "question": 0.99
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
              "C": 0.71,
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
            "completion_tokens": 266,
            "finish_reason": "stop",
            "latency_s": 2.976586,
            "model": "gpt-6-luna",
            "prompt_tokens": 3064,
            "reasoning_tokens": 194
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相で義母との同居が示されているため、同じ家に住んでいました。"
        }
      },
      "media_id": "local-U26",
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
      "text": "2人は同じ家に住んでたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1696136219834443,
      "judge_s": 2.9766128479968756,
      "luna_s": 2.9766128479968756,
      "total_s": 4.593584499991266,
      "writer_s": 1.6169716519943904
    }
  },
  {
    "case_id": "U26-b24",
    "record": {
      "comment_id": "U26-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4253,
            "latency_s": 1.209755,
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
                "guess": 0.23,
                "question": 0.77
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
              "C": 0.31,
              "D": {
                "irrelevant": 0.24,
                "no": 0.76,
                "yes": 0.0
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
            "completion_tokens": 263,
            "finish_reason": "stop",
            "latency_s": 3.303865,
            "model": "gpt-6-luna",
            "prompt_tokens": 3059,
            "reasoning_tokens": 192
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "義母の出身地は真相・確定事実から判断できません。"
        }
      },
      "media_id": "local-U26",
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
      "shadow_mismatch": true,
      "text": "義母も外国出身なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.210051955014933,
      "judge_s": 3.3039277759962715,
      "luna_s": 3.3039277759962715,
      "total_s": 4.255629343999317,
      "writer_s": 0.9517015680030454
    }
  },
  {
    "case_id": "U26-b25",
    "record": {
      "comment_id": "U26-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 4271,
            "latency_s": 1.198852,
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
                "guess": 0.03,
                "question": 0.97
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
              "C": 0.53,
              "D": {
                "irrelevant": 0.0,
                "no": 0.98,
                "yes": 0.02
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
            "completion_tokens": 453,
            "finish_reason": "stop",
            "latency_s": 5.213662,
            "model": "gpt-6-luna",
            "prompt_tokens": 3063,
            "reasoning_tokens": 383
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "夫は通訳役ではなく、平日はほとんど家にいません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。夫はけんかに関係していないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "夫はけんかに関係してるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1991359440144151,
      "judge_s": 5.213723666995065,
      "luna_s": 5.213723666995065,
      "total_s": 7.463896541972645,
      "writer_s": 2.2501728749775793
    }
  },
  {
    "case_id": "U26-t01",
    "record": {
      "comment_id": "U26-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "cb5eb45c4241",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "息子の通訳",
          "debug": {
            "calls": 1,
            "input_tokens": 930,
            "latency_s": 0.179882,
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
              "A_bare": 0.8
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.80"
        },
        "luna": {
          "answer": null,
          "bare_term": "息子の通訳",
          "debug": {
            "completion_tokens": 400,
            "finish_reason": "stop",
            "latency_s": 4.053468,
            "model": "gpt-6-luna",
            "prompt_tokens": 3057,
            "reasoning_tokens": 317
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない名詞句で、はい・いいえで答えられる質問になっていません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "息子の通訳がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "息子の通訳？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.1799914709990844,
      "judge_s": 4.053520144982031,
      "luna_s": 4.053520144982031,
      "total_s": 8.335330870992038,
      "writer_s": 4.281810726010008
    }
  },
  {
    "case_id": "U26-t02",
    "record": {
      "comment_id": "U26-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "cb5eb45c4241",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "富士山",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.219823,
            "model": "jev-latest",
            "output_tokens": 78,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.01,
                "request": 0.0
              },
              "A_bare": 0.98
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.98"
        },
        "luna": {
          "answer": null,
          "bare_term": "富士山",
          "debug": {
            "completion_tokens": 207,
            "finish_reason": "stop",
            "latency_s": 2.698751,
            "model": "gpt-6-luna",
            "prompt_tokens": 3054,
            "reasoning_tokens": 121
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない名詞だけのコメントなので、はい／いいえで答えられない質問として扱います。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "富士山が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "富士山",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.21991956702549942,
      "judge_s": 2.6987788760161493,
      "luna_s": 2.6987788760161493,
      "total_s": 4.160921348026022,
      "writer_s": 1.462142472009873
    }
  },
  {
    "case_id": "c-ask_howto-02",
    "record": {
      "comment_id": "c-ask_howto-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 1431,
            "latency_s": 0.417058,
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
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.05
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
            "completion_tokens": 165,
            "finish_reason": "stop",
            "latency_s": 2.266018,
            "model": "gpt-6-luna",
            "prompt_tokens": 3059,
            "reasoning_tokens": 81
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "遊び方として、何をコメントすればよいか尋ねています。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる質問をコメントしてごらん。私が答えるよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "何をコメントしたらいいの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.4172043120197486,
      "judge_s": 2.266042205999838,
      "luna_s": 2.266042205999838,
      "total_s": 5.8950841940240934,
      "writer_s": 3.6290419880242553
    }
  },
  {
    "case_id": "c-cheer-01",
    "record": {
      "comment_id": "c-cheer-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "cheer"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1590,
            "latency_s": 0.468182,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 1.0,
                "request": 0.0
              },
              "A2": {
                "chat": 0.01,
                "cheer": 0.89,
                "complaint": 0.0,
                "greeting": 0.1,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.08
            }
          },
          "error": null,
          "kind": "cheer",
          "reason": "段A=reaction→cheer"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 206,
            "finish_reason": "stop",
            "latency_s": 2.499046,
            "model": "gpt-6-luna",
            "prompt_tokens": 3061,
            "reasoning_tokens": 144
          },
          "error": null,
          "kind": "cheer",
          "reason": "投稿へのねぎらいと応援のコメントで、問題内容への質問ではありません。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！楽しんでいってね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "今日も投稿おつかれさま！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.4685698190005496,
      "judge_s": 2.4991012410027906,
      "luna_s": 2.4991012410027906,
      "total_s": 4.277327223011525,
      "writer_s": 1.7782259820087347
    }
  },
  {
    "case_id": "c-request-05",
    "record": {
      "comment_id": "c-request-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 1592,
            "latency_s": 0.394559,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.98,
                "request": 0.02
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
              "A_bare": 0.07
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
            "completion_tokens": 167,
            "finish_reason": "stop",
            "latency_s": 3.910105,
            "model": "gpt-6-luna",
            "prompt_tokens": 3061,
            "reasoning_tokens": 110
          },
          "error": null,
          "kind": "request",
          "reason": "次に出す問題のテーマをリクエストしているため。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！家族ものも楽しみにしててね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "次は家族もの出してほしいな",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3946771170012653,
      "judge_s": 3.910172064002836,
      "luna_s": 3.910172064002836,
      "total_s": 5.568999012990389,
      "writer_s": 1.658826948987553
    }
  },
  {
    "case_id": "c-emoji_only-04",
    "record": {
      "comment_id": "c-emoji_only-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "completion_tokens": 125,
            "finish_reason": "stop",
            "latency_s": 4.811346,
            "model": "gpt-6-luna",
            "prompt_tokens": 3053,
            "reasoning_tokens": 73
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "反応ありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "👍✨",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 3.632897278293967e-05,
      "judge_s": 4.811610737990122,
      "luna_s": 4.811610737990122,
      "total_s": 6.224736675969325,
      "writer_s": 1.4131259379792027
    }
  },
  {
    "case_id": "c-spam-03",
    "record": {
      "comment_id": "c-spam-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 1486,
            "latency_s": 0.399097,
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
              "A_bare": 0.06
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
            "completion_tokens": 97,
            "finish_reason": "stop",
            "latency_s": 1.620204,
            "model": "gpt-6-luna",
            "prompt_tokens": 3064,
            "reasoning_tokens": 44
          },
          "error": null,
          "kind": "spam",
          "reason": "副業への誘導とプロフィールのリンク案内を含む宣伝コメントです。"
        }
      },
      "media_id": "local-U26",
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
      "text": "副業に興味ある人はプロフのリンクへ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3991892930062022,
      "judge_s": 1.6202332380053122,
      "luna_s": 1.6202332380053122,
      "total_s": 1.6202342250035144,
      "writer_s": 9.8699820227921e-07
    }
  },
  {
    "case_id": "c-abuse-07",
    "record": {
      "comment_id": "c-abuse-07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "014-kind-interpreter",
      "errors": [],
      "fact_sheet_hash": "cb5eb45c4241",
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
            "input_tokens": 1490,
            "latency_s": 0.381914,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.99,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.01,
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
            "completion_tokens": 101,
            "finish_reason": "stop",
            "latency_s": 1.761668,
            "model": "gpt-6-luna",
            "prompt_tokens": 3064,
            "reasoning_tokens": 52
          },
          "error": null,
          "kind": "abuse",
          "reason": "コメントしている人たちを侮辱する内容です。"
        }
      },
      "media_id": "local-U26",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "みんなが楽しめる言葉でお願いね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "ここでコメントしてる奴ら全員頭おかしい",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3821483840001747,
      "judge_s": 1.761730030993931,
      "luna_s": 1.761730030993931,
      "total_s": 1.7617358650022652,
      "writer_s": 5.8340083342045546e-06
    }
  }
];

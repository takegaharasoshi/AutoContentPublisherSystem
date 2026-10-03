window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U27"] = [
  {
    "case_id": "U27-e01",
    "record": {
      "comment_id": "U27-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4304,
            "latency_s": 1.181123,
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
                "guess": 0.06,
                "question": 0.94
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.07
              },
              "C": 0.7,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.07"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 240,
            "finish_reason": "stop",
            "latency_s": 3.628991,
            "model": "gpt-6-luna",
            "prompt_tokens": 3022,
            "reasoning_tokens": 162
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "一問のはい・いいえ質問。本物の車ではなく、家の中で動かしています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は本物の車を公道で運転しているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1813893660146277,
      "judge_s": 3.629027146002045,
      "luna_s": 3.629027146002045,
      "total_s": 4.839712018001592,
      "writer_s": 1.2106848719995469
    }
  },
  {
    "case_id": "U27-e02",
    "record": {
      "comment_id": "U27-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4310,
            "latency_s": 1.261849,
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
                "guess": 0.7,
                "question": 0.3
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.01,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.07
              },
              "C": 0.6,
              "D": {
                "irrelevant": 0.02,
                "no": 0.95,
                "yes": 0.03
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.07"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 353,
            "finish_reason": "stop",
            "latency_s": 4.656333,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 283
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "妻や子どもたちは運転席にいる人ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。妻や子どもたちの誰かが運転席にいるんですか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "妻や子どもたちの誰かが運転席にいるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2622628640092444,
      "judge_s": 4.656387873983476,
      "luna_s": 4.656387873983476,
      "total_s": 7.530496666004183,
      "writer_s": 2.8741087920207065
    }
  },
  {
    "case_id": "U27-e03",
    "record": {
      "comment_id": "U27-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4250,
            "latency_s": 1.148041,
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
                "guess": 0.9,
                "question": 0.1
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
              "C": 0.55,
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
            "completion_tokens": 305,
            "finish_reason": "stop",
            "latency_s": 3.894075,
            "model": "gpt-6-luna",
            "prompt_tokens": 3015,
            "reasoning_tokens": 232
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、車は自動運転ではなく男自身が動かしています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車は自動運転の車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.148351301002549,
      "judge_s": 3.894130959000904,
      "luna_s": 3.894130959000904,
      "total_s": 5.071154019009555,
      "writer_s": 1.1770230600086506
    }
  },
  {
    "case_id": "U27-e04",
    "record": {
      "comment_id": "U27-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4358,
            "latency_s": 1.244665,
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
                "guess": 0.24,
                "question": 0.76
              },
              "A2": {
                "q_multi": 0.02,
                "q_open": 0.01,
                "q_yesno": 0.97
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.03
              },
              "C": 0.68,
              "D": {
                "irrelevant": 0.01,
                "no": 0.92,
                "yes": 0.07
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
            "completion_tokens": 519,
            "finish_reason": "stop",
            "latency_s": 5.660789,
            "model": "gpt-6-luna",
            "prompt_tokens": 3028,
            "reasoning_tokens": 442
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男は本物の自動車を運転しておらず、運転経験があるとはいえません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかにも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は運転免許を持っていないだけで、運転の経験はあるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.245066047005821,
      "judge_s": 5.6608175080036744,
      "luna_s": 5.6608175080036744,
      "total_s": 7.306844016013201,
      "writer_s": 1.6460265080095269
    }
  },
  {
    "case_id": "U27-e05",
    "record": {
      "comment_id": "U27-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": "no",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4322,
            "latency_s": 1.255821,
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
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.04
              },
              "C": 0.56,
              "D": {
                "irrelevant": 0.06,
                "no": 0.44,
                "yes": 0.5
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
            "completion_tokens": 472,
            "finish_reason": "stop",
            "latency_s": 5.270501,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 391
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "実際の車内移動ではなく、家族は遊びそのものを楽しんでいます。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": true,
      "text": "家族は車の中で移動そのものを楽しんでるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2562531440053135,
      "judge_s": 5.270539667981211,
      "luna_s": 5.270539667981211,
      "total_s": 6.727904344967101,
      "writer_s": 1.4573646769858897
    }
  },
  {
    "case_id": "U27-e06",
    "record": {
      "comment_id": "U27-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4316,
            "latency_s": 1.22824,
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
                "guess": 0.67,
                "question": 0.33
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
              "C": 0.66,
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
            "completion_tokens": 242,
            "finish_reason": "stop",
            "latency_s": 3.343833,
            "model": "gpt-6-luna",
            "prompt_tokens": 3022,
            "reasoning_tokens": 174
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では家の中を走り、遊園地などの施設内ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "この車は遊園地などの施設の中を走るものですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2285122370230965,
      "judge_s": 3.34385866401135,
      "luna_s": 3.34385866401135,
      "total_s": 4.772742365021259,
      "writer_s": 1.4288837010099087
    }
  },
  {
    "case_id": "U27-e07",
    "record": {
      "comment_id": "U27-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4292,
            "latency_s": 1.163946,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.19
              },
              "C": 0.7,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.19"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 3.729,
            "model": "gpt-6-luna",
            "prompt_tokens": 3020,
            "reasoning_tokens": 175
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、男は車の外から動かしているとあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！車の外から車を動かしてるんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は車の外から車を動かしてるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1641546600149013,
      "judge_s": 3.7290537930093706,
      "luna_s": 3.7290537930093706,
      "total_s": 7.248344074992929,
      "writer_s": 3.519290281983558
    }
  },
  {
    "case_id": "U27-e08",
    "record": {
      "comment_id": "U27-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4322,
            "latency_s": 1.179712,
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
                "guess": 0.02,
                "question": 0.98
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.13
              },
              "C": 0.66,
              "D": {
                "irrelevant": 0.56,
                "no": 0.35,
                "yes": 0.09
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.13"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 439,
            "finish_reason": "stop",
            "latency_s": 5.070718,
            "model": "gpt-6-luna",
            "prompt_tokens": 3025,
            "reasoning_tokens": 364
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "移動にかかる時間は真相・確定事実に示されていません。"
        }
      },
      "media_id": "local-U27",
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
      "text": "家族は長い距離を何時間もかけて移動するんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.179912224994041,
      "judge_s": 5.070750876009697,
      "luna_s": 5.070750876009697,
      "total_s": 6.9290727940096986,
      "writer_s": 1.8583219180000015
    }
  },
  {
    "case_id": "U27-e09",
    "record": {
      "comment_id": "U27-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4292,
            "latency_s": 1.164836,
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
                "guess": 0.05,
                "question": 0.95
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.05
              },
              "C": 0.38,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.05"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 266,
            "finish_reason": "stop",
            "latency_s": 3.937441,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 194
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では本物の自動車ではないため、ガソリンで走る車ではありません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ガソリンで走る車じゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "乗っているのはガソリンで走る車ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.1651129689998925,
      "judge_s": 3.937495696998667,
      "luna_s": 3.937495696998667,
      "total_s": 6.2005419280030765,
      "writer_s": 2.2630462310044095
    }
  },
  {
    "case_id": "U27-e10",
    "record": {
      "comment_id": "U27-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4298,
            "latency_s": 1.268882,
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
                "guess": 0.09,
                "question": 0.91
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.46
              },
              "C": 0.77,
              "D": {
                "irrelevant": 0.0,
                "no": 0.98,
                "yes": 0.02
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.46"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 221,
            "finish_reason": "stop",
            "latency_s": 2.724384,
            "model": "gpt-6-luna",
            "prompt_tokens": 3020,
            "reasoning_tokens": 136
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "ハンドルを握って操作しているかを尋ねる一問。車の外から動かしているため、いいえ。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。自分でハンドルを操作してはいないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は自分でハンドルを操作してるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.2692332080041524,
      "judge_s": 2.72443216398824,
      "luna_s": 2.72443216398824,
      "total_s": 4.9905505489732604,
      "writer_s": 2.2661183849850204
    }
  },
  {
    "case_id": "U27-e11",
    "record": {
      "comment_id": "U27-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 2150,
            "latency_s": 0.60711,
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
                "guess": 0.3,
                "question": 0.7
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
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.274668,
            "model": "gpt-6-luna",
            "prompt_tokens": 3029,
            "reasoning_tokens": 83
          },
          "error": null,
          "kind": "q_multi",
          "reason": "一つのコメントに、道路を走るかと誰が運転するかの質問が二つあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。どっちから聞こうか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "車は実際に道路を走ってるの？男以外の誰かが運転してるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6073442249908112,
      "judge_s": 2.274733347003348,
      "luna_s": 2.274733347003348,
      "total_s": 3.873095110990107,
      "writer_s": 1.5983617639867589
    }
  },
  {
    "case_id": "U27-e12",
    "record": {
      "comment_id": "U27-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "latency_s": 0.630202,
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
                "guess": 0.91,
                "question": 0.09
              },
              "A2": {
                "q_multi": 0.98,
                "q_open": 0.0,
                "q_yesno": 0.02
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
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 2.337661,
            "model": "gpt-6-luna",
            "prompt_tokens": 3027,
            "reasoning_tokens": 83
          },
          "error": null,
          "kind": "q_multi",
          "reason": "はい・いいえで答えられる質問が二つ含まれています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。まずはどちらか1つ聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これは遊園地の乗り物なの？家族は運転ごっこをしてるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.6304303009819705,
      "judge_s": 2.3377162599936128,
      "luna_s": 2.3377162599936128,
      "total_s": 3.6304862499819137,
      "writer_s": 1.292769989988301
    }
  },
  {
    "case_id": "U27-e13",
    "record": {
      "comment_id": "U27-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 2676,
            "latency_s": 0.795835,
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
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.03,
              "A_bare": 0.02
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
            "completion_tokens": 177,
            "finish_reason": "stop",
            "latency_s": 2.969357,
            "model": "gpt-6-luna",
            "prompt_tokens": 3025,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうやって」と尋ねる、はい／いいえでは答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はいかいいえで答えられる形にして、聞き直してごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "免許がない男は、どうやって車を走らせているんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7961997870006599,
      "judge_s": 2.969384010997601,
      "luna_s": 2.969384010997601,
      "total_s": 5.497889177000616,
      "writer_s": 2.528505166003015
    }
  },
  {
    "case_id": "U27-e14",
    "record": {
      "comment_id": "U27-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 2672,
            "latency_s": 0.777028,
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
                "q_multi": 0.01,
                "q_open": 0.97,
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
            "completion_tokens": 245,
            "finish_reason": "stop",
            "latency_s": 3.151411,
            "model": "gpt-6-luna",
            "prompt_tokens": 3023,
            "reasoning_tokens": 166
          },
          "error": null,
          "kind": "q_open",
          "reason": "「誰の運転か」は、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "誰のことか分かるようにして、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "妻と子どもたちは誰の運転で移動しているんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7772846900043078,
      "judge_s": 3.1514736440149136,
      "luna_s": 3.1514736440149136,
      "total_s": 5.787860363023356,
      "writer_s": 2.636386719008442
    }
  },
  {
    "case_id": "U27-e15",
    "record": {
      "comment_id": "U27-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 2672,
            "latency_s": 0.768941,
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
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.06,
                "q_open": 0.93,
                "q_yesno": 0.01
              },
              "A3": 0.04,
              "A_bare": 0.05
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
            "completion_tokens": 186,
            "finish_reason": "stop",
            "latency_s": 2.822651,
            "model": "gpt-6-luna",
            "prompt_tokens": 3024,
            "reasoning_tokens": 102
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どこからどこまで」は場所を尋ねる質問で、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形にして、聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "「長い道のり」とは、どこからどこまでのことですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7691698959970381,
      "judge_s": 2.8226777180097997,
      "luna_s": 2.8226777180097997,
      "total_s": 5.551624202984385,
      "writer_s": 2.7289464849745855
    }
  },
  {
    "case_id": "U27-e16",
    "record": {
      "comment_id": "U27-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 3274,
            "latency_s": 0.781728,
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
              "A_bare": 0.06,
              "B": {
                "point_0": 0.86
              },
              "B2": 0.09
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.86, 矛盾=0.09"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 291,
            "finish_reason": "stop",
            "latency_s": 3.462537,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 191
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "人生ゲームの車の駒を動かしたという核心を言い当てています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男が走らせているのは人生ゲームの車の駒。妻と子どもはピンで乗せていて、おもちゃなので免許はいらない。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "人生ゲームの車の駒を動かしてたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7819669609889388,
      "judge_s": 3.4625973280053586,
      "luna_s": 3.4625973280053586,
      "total_s": 3.4626145490037743,
      "writer_s": 1.7220998415723443e-05
    }
  },
  {
    "case_id": "U27-e17",
    "record": {
      "comment_id": "U27-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 3390,
            "latency_s": 0.773244,
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
                "point_0": 0.96
              },
              "B2": 0.11
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.96, 矛盾=0.11"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 223,
            "finish_reason": "stop",
            "latency_s": 2.776234,
            "model": "gpt-6-luna",
            "prompt_tokens": 3045,
            "reasoning_tokens": 115
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "人生ゲームの車の駒を動かしていたという核心を言い当てています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男が走らせているのは人生ゲームの車の駒。妻と子どもはピンで乗せていて、おもちゃなので免許はいらない。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "家族で人生ゲームをしていて、男が車の駒を盤の道に沿って進めてたんだね。免許がなくてもできるわけだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.773499630013248,
      "judge_s": 2.7762964249996003,
      "luna_s": 2.7762964249996003,
      "total_s": 2.7763027920154855,
      "writer_s": 6.367015885189176e-06
    }
  },
  {
    "case_id": "U27-e18",
    "record": {
      "comment_id": "U27-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 3334,
            "latency_s": 0.832752,
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
                "point_0": 0.58
              },
              "B2": 0.09
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.58, 矛盾=0.09"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 182,
            "finish_reason": "stop",
            "latency_s": 2.439764,
            "model": "gpt-6-luna",
            "prompt_tokens": 3037,
            "reasoning_tokens": 116
          },
          "error": null,
          "kind": "guess_close",
          "reason": "すごろくの車の駒という核心には触れていますが、人生ゲームとは特定できていません。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "家族で何かのすごろくをしていて、車の駒を長い道に沿って進めてるんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.8330238070047926,
      "judge_s": 2.439818931015907,
      "luna_s": 2.439818931015907,
      "total_s": 4.3921357940125745,
      "writer_s": 1.9523168629966676
    }
  },
  {
    "case_id": "U27-e19",
    "record": {
      "comment_id": "U27-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 3390,
            "latency_s": 0.769424,
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
                "point_0": 0.95
              },
              "B2": 0.95
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.95, 矛盾=0.95"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 213,
            "finish_reason": "stop",
            "latency_s": 2.931571,
            "model": "gpt-6-luna",
            "prompt_tokens": 3047,
            "reasoning_tokens": 149
          },
          "error": null,
          "kind": "guess_close",
          "reason": "人生ゲームの車の駒には触れていますが、家族の楽しみ方に誤りがあります。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えながら、推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "人生ゲームの車の駒を進めてるんだね。楽しんでるのは男だけで、妻と子どもは嫌々付き合わされてるのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7697080119978637,
      "judge_s": 2.9316277990001254,
      "luna_s": 2.9316277990001254,
      "total_s": 5.475193761987612,
      "writer_s": 2.5435659629874863
    }
  },
  {
    "case_id": "U27-e20",
    "record": {
      "comment_id": "U27-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 4364,
            "latency_s": 1.248824,
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
                "q_open": 0.06,
                "q_yesno": 0.93
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.02
              },
              "C": 0.32,
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
            "completion_tokens": 170,
            "finish_reason": "stop",
            "latency_s": 2.517791,
            "model": "gpt-6-luna",
            "prompt_tokens": 3028,
            "reasoning_tokens": 98
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "妻が運転し男が道案内をするという推理で、人生ゲームの車の駒には触れていません。"
        }
      },
      "media_id": "local-U27",
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
      "shadow_mismatch": true,
      "text": "妻が運転していて、男は助手席から道案内をしてるだけなんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 1.249277983995853,
      "judge_s": 2.517842560017016,
      "luna_s": 2.517842560017016,
      "total_s": 3.6695887800015043,
      "writer_s": 1.1517462199844886
    }
  },
  {
    "case_id": "U27-e21",
    "record": {
      "comment_id": "U27-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 2561,
            "latency_s": 0.767298,
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
                "q_multi": 0.05,
                "q_open": 0.58,
                "q_yesno": 0.37
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.03
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.03"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 326,
            "finish_reason": "stop",
            "latency_s": 3.892739,
            "model": "gpt-6-luna",
            "prompt_tokens": 3035,
            "reasoning_tokens": 246
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "遊園地の乗り物という推理で、人生ゲームの車の駒には触れていません。"
        }
      },
      "media_id": "local-U27",
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
      "text": "車型の遊園地の乗り物に家族で乗って、男が運転手役をしてるんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.7675559329800308,
      "judge_s": 3.8928018410224468,
      "luna_s": 3.8928018410224468,
      "total_s": 5.058570170018356,
      "writer_s": 1.1657683289959095
    }
  },
  {
    "case_id": "U27-t01",
    "record": {
      "comment_id": "U27-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "人生ゲーム",
          "debug": {
            "calls": 1,
            "input_tokens": 930,
            "latency_s": 0.194899,
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
              "A_bare": 0.85
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.85"
        },
        "luna": {
          "answer": null,
          "bare_term": "人生ゲーム",
          "debug": {
            "completion_tokens": 169,
            "finish_reason": "stop",
            "latency_s": 2.492442,
            "model": "gpt-6-luna",
            "prompt_tokens": 3007,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "q_open",
          "reason": "語句だけのコメントは、推理ではなく q_open として扱います。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "人生ゲームが何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "人生ゲーム？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.1949930810078513,
      "judge_s": 2.4924973959859926,
      "luna_s": 2.4924973959859926,
      "total_s": 6.0578864039853215,
      "writer_s": 3.565389007999329
    }
  },
  {
    "case_id": "U27-t02",
    "record": {
      "comment_id": "U27-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "遊園地",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.175805,
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
          "bare_term": "遊園地",
          "debug": {
            "completion_tokens": 248,
            "finish_reason": "stop",
            "latency_s": 2.898019,
            "model": "gpt-6-luna",
            "prompt_tokens": 3007,
            "reasoning_tokens": 156
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、はい／いいえで答えられない質問として扱います。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "遊園地の何が気になるのかな？はい・いいえで答えられる質問にしてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "遊園地",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.17591052400530316,
      "judge_s": 2.8980475300049875,
      "luna_s": 2.8980475300049875,
      "total_s": 5.575223878986435,
      "writer_s": 2.6771763489814475
    }
  },
  {
    "case_id": "c-ask_howto-03",
    "record": {
      "comment_id": "c-ask_howto-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 1435,
            "latency_s": 0.390184,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 124,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.2,
                "reaction": 0.02,
                "request": 0.78
              },
              "A2": {
                "ask_hint": 0.01,
                "ask_howto": 0.98,
                "ask_spoiler": 0.01
              },
              "A_bare": 0.06
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
            "latency_s": 1.951294,
            "model": "gpt-6-luna",
            "prompt_tokens": 3015,
            "reasoning_tokens": 56
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "遊び方として、質問の答え方を尋ねています。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "そうだよ！はい・いいえで答えられる質問をしてごらん。私が答えるよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "はい・いいえで答えればいい感じ？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3903435739921406,
      "judge_s": 1.951352243020665,
      "luna_s": 1.951352243020665,
      "total_s": 4.272942236013478,
      "writer_s": 2.3215899929928128
    }
  },
  {
    "case_id": "c-cheer-02",
    "record": {
      "comment_id": "c-cheer-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 1580,
            "latency_s": 0.486678,
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
                "chat": 0.0,
                "cheer": 1.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.06
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
            "completion_tokens": 95,
            "finish_reason": "stop",
            "latency_s": 1.780225,
            "model": "gpt-6-luna",
            "prompt_tokens": 3009,
            "reasoning_tokens": 34
          },
          "error": null,
          "kind": "cheer",
          "reason": "応援の言葉なので、励ましへのお礼を返します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "応援ありがとう！うれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "応援してます！",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.48677080898778513,
      "judge_s": 1.7802822350058705,
      "luna_s": 1.7802822350058705,
      "total_s": 2.8734088109922595,
      "writer_s": 1.093126575986389
    }
  },
  {
    "case_id": "c-complaint-01",
    "record": {
      "comment_id": "c-complaint-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "complaint"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1596,
            "latency_s": 0.380645,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 149,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.04,
                "reaction": 0.7,
                "request": 0.26
              },
              "A2": {
                "chat": 0.0,
                "cheer": 0.0,
                "complaint": 0.97,
                "greeting": 0.0,
                "impression": 0.01,
                "mention": 0.0,
                "request": 0.02
              },
              "A_bare": 0.05
            }
          },
          "error": null,
          "kind": "complaint",
          "reason": "段A=reaction→complaint"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 139,
            "finish_reason": "stop",
            "latency_s": 2.070141,
            "model": "gpt-6-luna",
            "prompt_tokens": 3014,
            "reasoning_tokens": 75
          },
          "error": null,
          "kind": "complaint",
          "reason": "問題の説明が足りないという指摘のため、クレームに分類します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "教えてくれてありがとう、確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "これちょっと説明足りなくない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.380733185011195,
      "judge_s": 2.0701989730005153,
      "luna_s": 2.0701989730005153,
      "total_s": 3.7218926190107595,
      "writer_s": 1.6516936460102443
    }
  },
  {
    "case_id": "c-emoji_only-05",
    "record": {
      "comment_id": "c-emoji_only-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "latency_s": 1.89238,
            "model": "gpt-6-luna",
            "prompt_tokens": 3013,
            "reasoning_tokens": 37
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字だけのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U27",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "参加ありがとう、楽しんでね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "🕵️‍♂️❓",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 5.08539960719645e-05,
      "judge_s": 1.8924330320151057,
      "luna_s": 1.8924330320151057,
      "total_s": 3.60873582601198,
      "writer_s": 1.7163027939968742
    }
  },
  {
    "case_id": "c-spam-04",
    "record": {
      "comment_id": "c-spam-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "input_tokens": 1478,
            "latency_s": 0.379601,
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
              "A_bare": 0.12
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
            "completion_tokens": 90,
            "finish_reason": "stop",
            "latency_s": 1.737962,
            "model": "gpt-6-luna",
            "prompt_tokens": 3012,
            "reasoning_tokens": 40
          },
          "error": null,
          "kind": "spam",
          "reason": "投資案件を宣伝し、DMへ誘導しているため。"
        }
      },
      "media_id": "local-U27",
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
      "text": "投資案件紹介中！DMください",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.37969043501652777,
      "judge_s": 1.7380289130087476,
      "luna_s": 1.7380289130087476,
      "total_s": 1.7380297950003296,
      "writer_s": 8.819915819913149e-07
    }
  },
  {
    "case_id": "c-abuse-08",
    "record": {
      "comment_id": "c-abuse-08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "de7b20ee3a37",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "015-unlicensed-driver",
      "errors": [],
      "fact_sheet_hash": "78e56e441eae",
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
            "latency_s": 0.368497,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
            "probabilities": {
              "A1": {
                "inappropriate": 0.98,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 0.02
              },
              "A2": {
                "abuse": 0.92,
                "personal_info": 0.06,
                "spam": 0.0,
                "troll": 0.02
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
            "completion_tokens": 141,
            "finish_reason": "stop",
            "latency_s": 2.328618,
            "model": "gpt-6-luna",
            "prompt_tokens": 3019,
            "reasoning_tokens": 92
          },
          "error": null,
          "kind": "abuse",
          "reason": "作者に裸の写真を求める性的な内容のため"
        }
      },
      "media_id": "local-U27",
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
      "text": "作者の顔写真あげてよ、脱いでるやつ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T18:26:24Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T18:26:24Z"
      }
    },
    "timing": {
      "jev_s": 0.3686807060148567,
      "judge_s": 2.328666474990314,
      "luna_s": 2.328666474990314,
      "total_s": 2.328670263988897,
      "writer_s": 3.788998583331704e-06
    }
  }
];

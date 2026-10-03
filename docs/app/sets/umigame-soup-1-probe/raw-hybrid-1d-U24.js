window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U24"] = [
  {
    "case_id": "U24-e01",
    "record": {
      "comment_id": "U24-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4150,
            "latency_s": 1.26546,
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
                "point_0": 0.03
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
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 172,
            "finish_reason": "stop",
            "latency_s": 7.402405,
            "model": "gpt-6-luna",
            "prompt_tokens": 2916,
            "reasoning_tokens": 112
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、10年ほど毎朝同じ道を走っているとあります。"
        }
      },
      "media_id": "local-U24",
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
      "text": "男は毎朝同じ通学路を走ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2657616699871141,
      "judge_s": 7.402428494999185,
      "luna_s": 7.402428494999185,
      "total_s": 10.717295120994095,
      "writer_s": 3.3148666259949096
    }
  },
  {
    "case_id": "U24-e02",
    "record": {
      "comment_id": "U24-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4168,
            "latency_s": 1.430117,
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
                "guess": 0.12,
                "question": 0.88
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
              "C": 0.61,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.11"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 239,
            "finish_reason": "stop",
            "latency_s": 8.191291,
            "model": "gpt-6-luna",
            "prompt_tokens": 2916,
            "reasoning_tokens": 169
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "子どもたちは窓から男の姿を見て、急いで家を出ています。"
        }
      },
      "media_id": "local-U24",
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
      "text": "小学生たちは男を見てから走り出したんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.4304524609760847,
      "judge_s": 8.191318658995442,
      "luna_s": 8.191318658995442,
      "total_s": 9.514314735977678,
      "writer_s": 1.3229960769822355
    }
  },
  {
    "case_id": "U24-e03",
    "record": {
      "comment_id": "U24-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
      "final": {
        "answer": "unknown",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4192,
            "latency_s": 1.269496,
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
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.01
              },
              "C": 0.72,
              "D": {
                "irrelevant": 0.07,
                "no": 0.93,
                "yes": 0.0
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
            "completion_tokens": 335,
            "finish_reason": "stop",
            "latency_s": 3.719429,
            "model": "gpt-6-luna",
            "prompt_tokens": 2917,
            "reasoning_tokens": 261
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "学校の始業時刻が普段と違ったかは、真相にも確定事実にもありません。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "それは答えに関わらないんだ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "この日は学校の始業時刻がいつもより早かったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2697472879954148,
      "judge_s": 3.7194851099920925,
      "luna_s": 3.7194851099920925,
      "total_s": 11.690088795003248,
      "writer_s": 7.970603685011156
    }
  },
  {
    "case_id": "U24-e04",
    "record": {
      "comment_id": "U24-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4186,
            "latency_s": 1.164174,
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
                "guess": 0.6,
                "question": 0.4
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
              "C": 0.71,
              "D": {
                "irrelevant": 0.0,
                "no": 0.89,
                "yes": 0.11
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
            "completion_tokens": 342,
            "finish_reason": "stop",
            "latency_s": 3.530601,
            "model": "gpt-6-luna",
            "prompt_tokens": 2918,
            "reasoning_tokens": 256
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "追い抜く意図を問う質問。真相では遅刻を避けるために走っており、追い抜く目的ではありません。"
        }
      },
      "media_id": "local-U24",
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
      "shadow_mismatch": false,
      "text": "子どもたちは男を追い抜こうとして走ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1644687509979121,
      "judge_s": 3.530624686012743,
      "luna_s": 3.530624686012743,
      "total_s": 4.528464832023019,
      "writer_s": 0.9978401460102759
    }
  },
  {
    "case_id": "U24-e05",
    "record": {
      "comment_id": "U24-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4150,
            "latency_s": 1.275307,
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
                "point_0": 0.02
              },
              "C": 0.39,
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
            "completion_tokens": 169,
            "finish_reason": "stop",
            "latency_s": 2.654205,
            "model": "gpt-6-luna",
            "prompt_tokens": 2916,
            "reasoning_tokens": 92
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、男は子どもたちに何も言っていないとされています。"
        }
      },
      "media_id": "local-U24",
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
      "shadow_mismatch": false,
      "text": "男は子どもたちに何か声をかけましたか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2756442009995226,
      "judge_s": 2.6542668559995946,
      "luna_s": 2.6542668559995946,
      "total_s": 3.52596958502545,
      "writer_s": 0.8717027290258557
    }
  },
  {
    "case_id": "U24-e06",
    "record": {
      "comment_id": "U24-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "unknown",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4174,
            "latency_s": 1.227944,
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
              "C": 0.31,
              "D": {
                "irrelevant": 0.53,
                "no": 0.02,
                "yes": 0.45
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
            "completion_tokens": 376,
            "finish_reason": "stop",
            "latency_s": 4.436875,
            "model": "gpt-6-luna",
            "prompt_tokens": 2917,
            "reasoning_tokens": 318
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "皆で同じ学校へ向かい、同じ校門に到着しています。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！小学生たちは全員、同じ学校に通ってるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "小学生たちは全員、同じ学校に通ってるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2281561190029606,
      "judge_s": 4.436923981003929,
      "luna_s": 4.436923981003929,
      "total_s": 6.223475190985482,
      "writer_s": 1.7865512099815533
    }
  },
  {
    "case_id": "U24-e07",
    "record": {
      "comment_id": "U24-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4162,
            "latency_s": 1.200448,
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
                "guess": 0.79,
                "question": 0.21
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
              "C": 0.39,
              "D": {
                "irrelevant": 0.08,
                "no": 0.92,
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
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 38.65452,
            "model": "gpt-6-luna",
            "prompt_tokens": 2916,
            "reasoning_tokens": 157
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "走ることを楽しんでいたかは、真相や確定事実から判断できず、仕掛けにも関係ありません。"
        }
      },
      "media_id": "local-U24",
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
      "text": "子どもたちは走るのを楽しんでいるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2007094619912095,
      "judge_s": 38.65454824597691,
      "luna_s": 38.65454824597691,
      "total_s": 41.719793095981004,
      "writer_s": 3.065244850004092
    }
  },
  {
    "case_id": "U24-e08",
    "record": {
      "comment_id": "U24-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4204,
            "latency_s": 1.255527,
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
                "guess": 0.22,
                "question": 0.78
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.05,
                "q_yesno": 0.95
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.03
              },
              "C": 0.52,
              "D": {
                "irrelevant": 0.01,
                "no": 0.1,
                "yes": 0.89
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 756,
            "finish_reason": "stop",
            "latency_s": 11.732066,
            "model": "gpt-6-luna",
            "prompt_tokens": 2922,
            "reasoning_tokens": 683
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "用事があり早く出たため、いつもと異なる事情がありました。"
        }
      },
      "media_id": "local-U24",
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
      "text": "男が早く出たのは、いつもと違う出来事があったからですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2558860830031335,
      "judge_s": 11.73210756701883,
      "luna_s": 11.73210756701883,
      "total_s": 12.884562198014464,
      "writer_s": 1.152454630995635
    }
  },
  {
    "case_id": "U24-e09",
    "record": {
      "comment_id": "U24-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4180,
            "latency_s": 1.109669,
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
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.02,
                "q_yesno": 0.98
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.01
              },
              "C": 0.36,
              "D": {
                "irrelevant": 0.82,
                "no": 0.01,
                "yes": 0.17
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
            "completion_tokens": 216,
            "finish_reason": "stop",
            "latency_s": 2.607817,
            "model": "gpt-6-luna",
            "prompt_tokens": 2920,
            "reasoning_tokens": 140
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "地区が同じかどうかは、子どもたちが走り出した理由に関係しません。"
        }
      },
      "media_id": "local-U24",
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
      "text": "通学路沿いの家は、どれも同じ地区にあるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1099582019960508,
      "judge_s": 2.607852293003816,
      "luna_s": 2.607852293003816,
      "total_s": 3.8902941620035563,
      "writer_s": 1.28244186899974
    }
  },
  {
    "case_id": "U24-e10",
    "record": {
      "comment_id": "U24-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4162,
            "latency_s": 1.362721,
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
                "guess": 0.08,
                "question": 0.92
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.04,
              "B": {
                "point_0": 0.02
              },
              "C": 0.37,
              "D": {
                "irrelevant": 0.98,
                "no": 0.01,
                "yes": 0.01
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
            "completion_tokens": 258,
            "finish_reason": "stop",
            "latency_s": 8.172704,
            "model": "gpt-6-luna",
            "prompt_tokens": 2915,
            "reasoning_tokens": 187
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "ランドセルの有無は真相に関係しないためです。"
        }
      },
      "media_id": "local-U24",
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
      "text": "小学生はランドセルを背負ってたんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.362956782017136,
      "judge_s": 8.172729803976836,
      "luna_s": 8.172729803976836,
      "total_s": 9.588433541968698,
      "writer_s": 1.415703737991862
    }
  },
  {
    "case_id": "U24-e11",
    "record": {
      "comment_id": "U24-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2139,
            "latency_s": 0.590267,
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
            "completion_tokens": 131,
            "finish_reason": "stop",
            "latency_s": 2.105297,
            "model": "gpt-6-luna",
            "prompt_tokens": 2920,
            "reasoning_tokens": 51
          },
          "error": null,
          "kind": "q_multi",
          "reason": "先生かどうか、走らせたかどうかの質問が二つあります。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。どちらか一つ聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は子どもたちの先生なの？走って学校に向かわせたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5904295920045115,
      "judge_s": 2.105353146995185,
      "luna_s": 2.105353146995185,
      "total_s": 66.80484117299784,
      "writer_s": 64.69948802600265
    }
  },
  {
    "case_id": "U24-e12",
    "record": {
      "comment_id": "U24-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2148,
            "latency_s": 0.674038,
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
                "q_multi": 0.92,
                "q_open": 0.01,
                "q_yesno": 0.07
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
            "latency_s": 2.091297,
            "model": "gpt-6-luna",
            "prompt_tokens": 2926,
            "reasoning_tokens": 80
          },
          "error": null,
          "kind": "q_multi",
          "reason": "一つのコメントに、走り出した理由と追いかけていたかの質問が二つあります。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。まずはどっちか聞いてごらん😉"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "子どもたちは男を見つけて走り出したの？男を追いかけてたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6741609110031277,
      "judge_s": 2.0913228150166105,
      "luna_s": 2.0913228150166105,
      "total_s": 3.595563045993913,
      "writer_s": 1.5042402309773024
    }
  },
  {
    "case_id": "U24-e13",
    "record": {
      "comment_id": "U24-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2650,
            "latency_s": 0.756769,
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
                "guess": 0.03,
                "question": 0.97
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 1.0,
                "q_yesno": 0.0
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
            "completion_tokens": 173,
            "finish_reason": "stop",
            "latency_s": 2.188876,
            "model": "gpt-6-luna",
            "prompt_tokens": 2916,
            "reasoning_tokens": 89
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねており、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "子どもたちについて、はい／いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "子どもたちはどうして急に走り出したんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7569077310035937,
      "judge_s": 2.188903216010658,
      "luna_s": 2.188903216010658,
      "total_s": 5.078034625999862,
      "writer_s": 2.8891314099892043
    }
  },
  {
    "case_id": "U24-e14",
    "record": {
      "comment_id": "U24-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2642,
            "latency_s": 0.763331,
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
                "guess": 0.22,
                "question": 0.78
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.04,
              "A_bare": 0.03
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
            "completion_tokens": 144,
            "finish_reason": "stop",
            "latency_s": 8.001923,
            "model": "gpt-6-luna",
            "prompt_tokens": 2913,
            "reasoning_tokens": 62
          },
          "error": null,
          "kind": "q_open",
          "reason": "「何をしている人か」は自由回答で、一つに絞れない質問です。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男が何をしているか、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は通学路で何をしている人なんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7635210919834208,
      "judge_s": 8.001950707985088,
      "luna_s": 8.001950707985088,
      "total_s": 12.468319504958345,
      "writer_s": 4.466368796973256
    }
  },
  {
    "case_id": "U24-e15",
    "record": {
      "comment_id": "U24-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2666,
            "latency_s": 0.792253,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 176,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.71,
                "reaction": 0.0,
                "request": 0.29
              },
              "A1b": {
                "guess": 0.01,
                "question": 0.99
              },
              "A2": {
                "q_multi": 0.02,
                "q_open": 0.98,
                "q_yesno": 0.0
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
            "completion_tokens": 208,
            "finish_reason": "stop",
            "latency_s": 7.764127,
            "model": "gpt-6-luna",
            "prompt_tokens": 2921,
            "reasoning_tokens": 114
          },
          "error": null,
          "kind": "q_open",
          "reason": "誰が誰を追い抜いたかを尋ねる、はい・いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。誰のことかも書いてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "誰が誰を追い抜いたのか、状況をもう少し知りたいです。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.7924317500146572,
      "judge_s": 7.764156901015667,
      "luna_s": 7.764156901015667,
      "total_s": 9.331459300999995,
      "writer_s": 1.567302399984328
    }
  },
  {
    "case_id": "U24-e16",
    "record": {
      "comment_id": "U24-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2003,
            "latency_s": 0.65774,
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
                "guess": 0.95,
                "question": 0.05
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.88
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.88"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 2.430835,
            "model": "gpt-6-luna",
            "prompt_tokens": 2926,
            "reasoning_tokens": 125
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "子どもたちが毎日、男を合図に家を出ていたと指摘しています。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！子どもたちは毎朝同じ時刻に走る男を合図に家を出ていた。男が早く走った朝、遅刻だと思い込んで飛び出した。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "子どもたちは毎日、男が走ってくるのを合図に家を出てたってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.6578776789829135,
      "judge_s": 2.4308847619977314,
      "luna_s": 2.4308847619977314,
      "total_s": 2.430896581005072,
      "writer_s": 1.1819007340818644e-05
    }
  },
  {
    "case_id": "U24-e17",
    "record": {
      "comment_id": "U24-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2090,
            "latency_s": 0.597248,
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
                "point_0": 0.67
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.67"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 319,
            "finish_reason": "stop",
            "latency_s": 8.674551,
            "model": "gpt-6-luna",
            "prompt_tokens": 2949,
            "reasoning_tokens": 209
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "毎朝、男を家を出る合図にしていたという核心を言い当てています。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！子どもたちは毎朝同じ時刻に走る男を合図に家を出ていた。男が早く走った朝、遅刻だと思い込んで飛び出した。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "子どもたちは毎朝、走ってくる男を学校へ出る合図にしてたんだね。いつもより早く通ったから、勘違いして先に走り出したのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.5974466369953007,
      "judge_s": 8.674600251979427,
      "luna_s": 8.674600251979427,
      "total_s": 8.67460441897856,
      "writer_s": 4.1669991333037615e-06
    }
  },
  {
    "case_id": "U24-e18",
    "record": {
      "comment_id": "U24-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "guess_close"
      },
      "judgements": {
        "jev": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 4252,
            "latency_s": 1.121207,
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
                "guess": 0.92,
                "question": 0.08
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.03,
                "q_yesno": 0.96
              },
              "A_bare": 0.03,
              "B": {
                "point_0": 0.3
              },
              "C": 0.36,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.30"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 398,
            "finish_reason": "stop",
            "latency_s": 4.247263,
            "model": "gpt-6-luna",
            "prompt_tokens": 2931,
            "reasoning_tokens": 325
          },
          "error": null,
          "kind": "guess_close",
          "reason": "男が通る時間と子どもの出発の関係には触れていますが、合図としていた点までは特定できていません。"
        }
      },
      "media_id": "local-U24",
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
      "shadow_mismatch": true,
      "text": "男がいつも通る時間と、子どもたちが家を出る時間に何か関係があるんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.1215249660017435,
      "judge_s": 4.247302536998177,
      "luna_s": 4.247302536998177,
      "total_s": 5.590926771983504,
      "writer_s": 1.3436242349853273
    }
  },
  {
    "case_id": "U24-e19",
    "record": {
      "comment_id": "U24-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2102,
            "latency_s": 0.571201,
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
                "point_0": 0.97
              }
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.97"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 130,
            "finish_reason": "stop",
            "latency_s": 2.009495,
            "model": "gpt-6-luna",
            "prompt_tokens": 2953,
            "reasoning_tokens": 63
          },
          "error": null,
          "kind": "guess_close",
          "reason": "毎日男を合図に出ていた点は合っていますが、その日の時刻の推理に誤りがあります。"
        }
      },
      "media_id": "local-U24",
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
      "text": "子どもたちは毎日男を合図に家を出てたけど、その日は男がいつもより遅く走ってきたから、遅刻しそうだと勘違いして急いだんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.571366393007338,
      "judge_s": 2.0095410060021095,
      "luna_s": 2.0095410060021095,
      "total_s": 5.476220734009985,
      "writer_s": 3.4666797280078754
    }
  },
  {
    "case_id": "U24-e20",
    "record": {
      "comment_id": "U24-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 4264,
            "latency_s": 1.249034,
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
                "q_open": 0.28,
                "q_yesno": 0.71
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.04
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
          "reason": "段A=question→q_yesno, 要点最低=0.04"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 222,
            "finish_reason": "stop",
            "latency_s": 2.872588,
            "model": "gpt-6-luna",
            "prompt_tokens": 2931,
            "reasoning_tokens": 155
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "子どもたちが男を合図に毎日家を出ていた点には触れていません。"
        }
      },
      "media_id": "local-U24",
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
      "text": "男がいつもより早く走り始めたから、子どもたちも競争だと思って走ったんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 1.2492788909876253,
      "judge_s": 2.872641399007989,
      "luna_s": 2.872641399007989,
      "total_s": 4.1589697930030525,
      "writer_s": 1.2863283939950634
    }
  },
  {
    "case_id": "U24-e21",
    "record": {
      "comment_id": "U24-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 2554,
            "latency_s": 0.874894,
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
                "q_multi": 0.04,
                "q_open": 0.73,
                "q_yesno": 0.23
              },
              "A_bare": 0.02,
              "B": {
                "point_0": 0.04
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.04"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 288,
            "finish_reason": "stop",
            "latency_s": 3.113798,
            "model": "gpt-6-luna",
            "prompt_tokens": 2928,
            "reasoning_tokens": 215
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "先生や朝の運動という推理で、子どもたちが男を合図にしていた核心には触れていません。"
        }
      },
      "media_id": "local-U24",
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
      "text": "男は学校の先生で、子どもたちを走らせる朝の運動をしてたんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.8750235560000874,
      "judge_s": 3.1138376529852394,
      "luna_s": 3.1138376529852394,
      "total_s": 6.186784335994162,
      "writer_s": 3.0729466830089223
    }
  },
  {
    "case_id": "U24-t01",
    "record": {
      "comment_id": "U24-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "aeaba231b36a",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "合図",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.198437,
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
              "A_bare": 0.91
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.91"
        },
        "luna": {
          "answer": null,
          "bare_term": "合図",
          "debug": {
            "completion_tokens": 179,
            "finish_reason": "stop",
            "latency_s": 7.313204,
            "model": "gpt-6-luna",
            "prompt_tokens": 2902,
            "reasoning_tokens": 98
          },
          "error": null,
          "kind": "q_open",
          "reason": "「合図？」は述語のない語句だけのコメントです。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "合図がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "合図？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.19851226499304175,
      "judge_s": 7.313376665988471,
      "luna_s": 7.313376665988471,
      "total_s": 16.092966353986412,
      "writer_s": 8.779589687997941
    }
  },
  {
    "case_id": "U24-t02",
    "record": {
      "comment_id": "U24-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "aeaba231b36a",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "黄色い帽子",
          "debug": {
            "calls": 1,
            "input_tokens": 929,
            "latency_s": 0.198196,
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
              "A_bare": 0.97
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.97"
        },
        "luna": {
          "answer": null,
          "bare_term": "黄色い帽子",
          "debug": {
            "completion_tokens": 199,
            "finish_reason": "stop",
            "latency_s": 7.768233,
            "model": "gpt-6-luna",
            "prompt_tokens": 2903,
            "reasoning_tokens": 123
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問として聞き直しをお願いします。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "何が黄色い帽子なのか教えてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "黄色い帽子",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.19826395300333388,
      "judge_s": 7.768292725988431,
      "luna_s": 7.768292725988431,
      "total_s": 10.31825227299123,
      "writer_s": 2.5499595470028
    }
  },
  {
    "case_id": "c-ask_spoiler-05",
    "record": {
      "comment_id": "c-ask_spoiler-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 1417,
            "latency_s": 0.429174,
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
                "ask_howto": 0.0,
                "ask_spoiler": 1.0
              },
              "A_bare": 0.44
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
            "completion_tokens": 260,
            "finish_reason": "stop",
            "latency_s": 8.027878,
            "model": "gpt-6-luna",
            "prompt_tokens": 2904,
            "reasoning_tokens": 179
          },
          "error": null,
          "kind": "ask_spoiler",
          "reason": "答えの解説を求めているコメントです。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問には答えられるけど、真相は教えられないよ。質問で少しずつ絞ってみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "解説まだー？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.42932108099921606,
      "judge_s": 8.027905258990359,
      "luna_s": 8.027905258990359,
      "total_s": 9.5353782849852,
      "writer_s": 1.507473025994841
    }
  },
  {
    "case_id": "c-greeting-04",
    "record": {
      "comment_id": "c-greeting-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 1574,
            "latency_s": 0.430427,
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
                "chat": 0.01,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.99,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.62
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
            "completion_tokens": 127,
            "finish_reason": "stop",
            "latency_s": 1.752004,
            "model": "gpt-6-luna",
            "prompt_tokens": 2903,
            "reasoning_tokens": 67
          },
          "error": null,
          "kind": "greeting",
          "reason": "挨拶のみのコメントで、問題への質問や推理はありません。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "やっほー！来てくれてうれしいよ☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "やっほー",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.43057726800907403,
      "judge_s": 1.7520592979853973,
      "luna_s": 1.7520592979853973,
      "total_s": 4.750021556974389,
      "writer_s": 2.9979622589889914
    }
  },
  {
    "case_id": "c-request-03",
    "record": {
      "comment_id": "c-request-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "input_tokens": 1590,
            "latency_s": 0.423045,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.66,
                "request": 0.33
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
              "A_bare": 0.14
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
            "completion_tokens": 126,
            "finish_reason": "stop",
            "latency_s": 1.923014,
            "model": "gpt-6-luna",
            "prompt_tokens": 2905,
            "reasoning_tokens": 69
          },
          "error": null,
          "kind": "request",
          "reason": "怖めの問題を出してほしいというリクエストです。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "リクエストありがとう！怖めもいいね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "怖めの問題もお願いします",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.4231920809834264,
      "judge_s": 1.9230763000086881,
      "luna_s": 1.9230763000086881,
      "total_s": 4.381445239007007,
      "writer_s": 2.458368938998319
    }
  },
  {
    "case_id": "c-emoji_only-02",
    "record": {
      "comment_id": "c-emoji_only-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "completion_tokens": 131,
            "finish_reason": "stop",
            "latency_s": 7.456407,
            "model": "gpt-6-luna",
            "prompt_tokens": 2901,
            "reasoning_tokens": 75
          },
          "error": null,
          "kind": "emoji_only",
          "reason": "絵文字のみのコメントなので、emoji_onlyに分類します。"
        }
      },
      "media_id": "local-U24",
      "parent_id": null,
      "problem_schema_version": 2,
      "reply": {
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "見てくれてありがとう☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "😂👏",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 4.511198494583368e-05,
      "judge_s": 7.456461406021845,
      "luna_s": 7.456461406021845,
      "total_s": 9.280043363018194,
      "writer_s": 1.8235819569963496
    }
  },
  {
    "case_id": "c-spam-01",
    "record": {
      "comment_id": "c-spam-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "calls": 0,
            "input_tokens": 0,
            "latency_s": 0.0,
            "model": "jev-latest",
            "output_tokens": 0,
            "probabilities": {}
          },
          "error": null,
          "kind": "spam",
          "reason": "段0規則: spam"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 116,
            "finish_reason": "stop",
            "latency_s": 1.755987,
            "model": "gpt-6-luna",
            "prompt_tokens": 2908,
            "reasoning_tokens": 68
          },
          "error": null,
          "kind": "spam",
          "reason": "新作の宣伝と外部リンクを含むため。"
        }
      },
      "media_id": "local-U24",
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
      "text": "新作はこちら https://example.invalid/deal",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 3.051597741432488e-05,
      "judge_s": 1.7560256919823587,
      "luna_s": 1.7560256919823587,
      "total_s": 1.7560327340033837,
      "writer_s": 7.0420210249722e-06
    }
  },
  {
    "case_id": "c-foreign-05",
    "record": {
      "comment_id": "c-foreign-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "5311b19312cf",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "012-early-morning-run",
      "errors": [],
      "fact_sheet_hash": "aeaba231b36a",
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
            "calls": 1,
            "input_tokens": 932,
            "latency_s": 0.191299,
            "major": "other",
            "model": "jev-latest",
            "output_tokens": 76,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.94,
                "question_or_guess": 0.0,
                "reaction": 0.06,
                "request": 0.0
              },
              "A_bare": 0.05
            }
          },
          "error": null,
          "kind": "foreign",
          "reason": "段A=other→foreign"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 163,
            "finish_reason": "stop",
            "latency_s": 7.45079,
            "model": "gpt-6-luna",
            "prompt_tokens": 2906,
            "reasoning_tokens": 104
          },
          "error": null,
          "kind": "foreign",
          "reason": "韓国語のコメントで、日本語ではありません。"
        }
      },
      "media_id": "local-U24",
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
      "shadow_mismatch": false,
      "text": "이거 정말 재밌어요",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-03T09:17:58Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-03T09:17:58Z"
      }
    },
    "timing": {
      "jev_s": 0.19134900599601679,
      "judge_s": 7.450873808003962,
      "luna_s": 7.450873808003962,
      "total_s": 9.085569690010743,
      "writer_s": 1.6346958820067812
    }
  }
];

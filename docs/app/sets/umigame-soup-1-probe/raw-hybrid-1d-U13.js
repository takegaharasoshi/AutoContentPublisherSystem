window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["hybrid-1d/U13"] = [
  {
    "case_id": "U13-e01",
    "record": {
      "comment_id": "U13-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5079,
            "latency_s": 1.282782,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.04,
              "B": {
                "point_0": {
                  "close": 0.24,
                  "hit": 0.15
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.0
                }
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
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 235,
            "finish_reason": "stop",
            "latency_s": 3.43359,
            "model": "gpt-6-luna",
            "prompt_tokens": 3376,
            "reasoning_tokens": 172
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実では、男の家のポストではなく集まりの場で手渡されています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。男の家のポストに届いたの？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙って男の家のポストに届いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.283100172993727,
      "judge_s": 3.433656499022618,
      "luna_s": 3.433656499022618,
      "total_s": 5.444105912116356,
      "writer_s": 2.0104494130937383
    }
  },
  {
    "case_id": "U13-e02",
    "record": {
      "comment_id": "U13-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5091,
            "latency_s": 1.153162,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.02,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.060000000000000005,
                  "hit": 0.01
                }
              },
              "C": 0.46,
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
            "completion_tokens": 205,
            "finish_reason": "stop",
            "latency_s": 2.853463,
            "model": "gpt-6-luna",
            "prompt_tokens": 3379,
            "reasoning_tokens": 139
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "手紙は意図して保管されており、配達に何十年もかかったのではありません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "郵便屋さんが何十年もかけて配達したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.153564172098413,
      "judge_s": 2.8535148450173438,
      "luna_s": 2.8535148450173438,
      "total_s": 4.376609604922123,
      "writer_s": 1.5230947599047795
    }
  },
  {
    "case_id": "U13-e03",
    "record": {
      "comment_id": "U13-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5067,
            "latency_s": 1.314121,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.15,
                "question": 0.85
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.08,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.04,
                  "hit": 0.02
                }
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
          "reason": "段A=question→q_yesno, 要点最低=0.02"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 221,
            "finish_reason": "stop",
            "latency_s": 2.61258,
            "model": "gpt-6-luna",
            "prompt_tokens": 3375,
            "reasoning_tokens": 155
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "学校の行事で書かれた手紙だと確定事実にあります。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "学校の行事で書かれた手紙なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3145533009665087,
      "judge_s": 2.612672023009509,
      "luna_s": 2.612672023009509,
      "total_s": 3.6063514250563458,
      "writer_s": 0.9936794020468369
    }
  },
  {
    "case_id": "U13-e04",
    "record": {
      "comment_id": "U13-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5079,
            "latency_s": 1.199517,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.84,
                "question": 0.16
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.04,
              "B": {
                "point_0": {
                  "close": 0.18,
                  "hit": 0.09
                },
                "point_1": {
                  "close": 0.53,
                  "hit": 0.12
                }
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
          "reason": "段A=question→q_yesno, 要点最低=0.09"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 174,
            "finish_reason": "stop",
            "latency_s": 2.476777,
            "model": "gpt-6-luna",
            "prompt_tokens": 3375,
            "reasoning_tokens": 120
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "あとで読まれるよう意図して保管されていました。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "あとで読まれるように保管されてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.199836408952251,
      "judge_s": 2.4768293109955266,
      "luna_s": 2.4768293109955266,
      "total_s": 3.781172064016573,
      "writer_s": 1.3043427530210465
    }
  },
  {
    "case_id": "U13-e05",
    "record": {
      "comment_id": "U13-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5073,
            "latency_s": 1.142073,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.64,
                "question": 0.36
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.27,
                  "hit": 0.1
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.61,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 202,
            "finish_reason": "stop",
            "latency_s": 3.583241,
            "model": "gpt-6-luna",
            "prompt_tokens": 3375,
            "reasoning_tokens": 132
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、書いた男の子は男の息子ではないと示されています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "書いた男の子って、男の息子なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.1424283690284938,
      "judge_s": 3.583386866026558,
      "luna_s": 3.583386866026558,
      "total_s": 5.084375923965126,
      "writer_s": 1.5009890579385683
    }
  },
  {
    "case_id": "U13-e06",
    "record": {
      "comment_id": "U13-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 5565,
            "latency_s": 1.755238,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.76,
                "question": 0.24
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A3": 0.78,
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.53,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 236,
            "finish_reason": "stop",
            "latency_s": 2.6902,
            "model": "gpt-6-luna",
            "prompt_tokens": 3371,
            "reasoning_tokens": 165
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男の子は有名人ではないと確定事実にあるため。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。有名人ではなかったんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その子は有名人だったの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.755672935047187,
      "judge_s": 2.6902422659331933,
      "luna_s": 2.6902422659331933,
      "total_s": 5.614674332900904,
      "writer_s": 2.924432066967711
    }
  },
  {
    "case_id": "U13-e07",
    "record": {
      "comment_id": "U13-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 5586,
            "latency_s": 1.401375,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
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
              "A3": 0.88,
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.23,
                  "hit": 0.03
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.82,
              "D": {
                "irrelevant": 0.0,
                "no": 0.92,
                "yes": 0.08
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 278,
            "finish_reason": "stop",
            "latency_s": 3.069214,
            "model": "gpt-6-luna",
            "prompt_tokens": 3373,
            "reasoning_tokens": 212
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "真相では、男はその子に一度も会ったことがありません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。男はその子に会ったことがある？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はその子に会ったことがある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.401818023994565,
      "judge_s": 3.069243893958628,
      "luna_s": 3.069243893958628,
      "total_s": 6.1978367529809475,
      "writer_s": 3.1285928590223193
    }
  },
  {
    "case_id": "U13-e08",
    "record": {
      "comment_id": "U13-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5115,
            "latency_s": 1.107288,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.58,
                "question": 0.42
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.02,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.64,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 351,
            "finish_reason": "stop",
            "latency_s": 3.960462,
            "model": "gpt-6-luna",
            "prompt_tokens": 3381,
            "reasoning_tokens": 279
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "夢の中身は問題に関係ないと確定事実に明記されているため。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙に書かれてた夢の内容って、答えに関係ある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.107681919937022,
      "judge_s": 3.960516001912765,
      "luna_s": 3.960516001912765,
      "total_s": 5.4561323469970375,
      "writer_s": 1.4956163450842723
    }
  },
  {
    "case_id": "U13-e09",
    "record": {
      "comment_id": "U13-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5067,
            "latency_s": 1.197451,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.49,
                  "hit": 0.3
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.52,
              "D": {
                "irrelevant": 0.0,
                "no": 0.0,
                "yes": 1.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 254,
            "finish_reason": "stop",
            "latency_s": 3.300731,
            "model": "gpt-6-luna",
            "prompt_tokens": 3376,
            "reasoning_tokens": 183
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実で、男は手紙の宛先どおりの正しい受け取り手です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！手紙の宛先は男で合ってたよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙の宛先は男で合ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.1977745370240882,
      "judge_s": 3.3007834979798645,
      "luna_s": 3.3007834979798645,
      "total_s": 5.561030286946334,
      "writer_s": 2.2602467889664695
    }
  },
  {
    "case_id": "U13-e10",
    "record": {
      "comment_id": "U13-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5061,
            "latency_s": 1.238122,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.03,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.4,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 340,
            "finish_reason": "stop",
            "latency_s": 4.018462,
            "model": "gpt-6-luna",
            "prompt_tokens": 3375,
            "reasoning_tokens": 262
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "確定事実に、男は手紙を受け取っても驚かなかったとあります。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男は手紙を読んで驚いてた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2384948149556294,
      "judge_s": 4.018516950076446,
      "luna_s": 4.018516950076446,
      "total_s": 5.276214511017315,
      "writer_s": 1.2576975609408692
    }
  },
  {
    "case_id": "U13-e11",
    "record": {
      "comment_id": "U13-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2115,
            "latency_s": 0.665323,
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
                "q_multi": 0.95,
                "q_open": 0.05,
                "q_yesno": 0.0
              },
              "A_bare": 0.04
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
            "completion_tokens": 123,
            "finish_reason": "stop",
            "latency_s": 1.89144,
            "model": "gpt-6-luna",
            "prompt_tokens": 3376,
            "reasoning_tokens": 45
          },
          "error": null,
          "kind": "q_multi",
          "reason": "「いつ書いたの？」と「誰が書いたの？」の二つの質問があります。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつ聞いてごらん。どっちからにする？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙はいつ書いたの？誰が書いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6655506379902363,
      "judge_s": 1.8914656169945374,
      "luna_s": 1.8914656169945374,
      "total_s": 3.6828869309974834,
      "writer_s": 1.791421314002946
    }
  },
  {
    "case_id": "U13-e12",
    "record": {
      "comment_id": "U13-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2136,
            "latency_s": 0.623306,
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
                "guess": 0.0,
                "question": 1.0
              },
              "A2": {
                "q_multi": 0.99,
                "q_open": 0.01,
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
            "completion_tokens": 201,
            "finish_reason": "stop",
            "latency_s": 2.672174,
            "model": "gpt-6-luna",
            "prompt_tokens": 3383,
            "reasoning_tokens": 116
          },
          "error": null,
          "kind": "q_multi",
          "reason": "受け取った場所と郵便で届いたかの、二つの質問が含まれています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問は1つずつコメントしてね。まずはどちらか聞いてごらん☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どこで手紙を受け取ったの？それは郵便で届いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6235267559532076,
      "judge_s": 2.6722024379996583,
      "luna_s": 2.6722024379996583,
      "total_s": 4.520616954076104,
      "writer_s": 1.8484145160764456
    }
  },
  {
    "case_id": "U13-e13",
    "record": {
      "comment_id": "U13-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "latency_s": 0.82069,
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
                "q_open": 0.99,
                "q_yesno": 0.01
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
            "completion_tokens": 170,
            "finish_reason": "stop",
            "latency_s": 2.13693,
            "model": "gpt-6-luna",
            "prompt_tokens": 3382,
            "reasoning_tokens": 86
          },
          "error": null,
          "kind": "q_open",
          "reason": "「なぜ」と理由を尋ねる、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "なぜ男は、その子がどんな子か誰よりよく知っていたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8208274591015652,
      "judge_s": 2.1369758039945737,
      "luna_s": 2.1369758039945737,
      "total_s": 4.529322589980438,
      "writer_s": 2.3923467859858647
    }
  },
  {
    "case_id": "U13-e14",
    "record": {
      "comment_id": "U13-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2652,
            "latency_s": 0.794304,
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
                "q_multi": 0.0,
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.22,
              "A_bare": 0.02
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.22"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 221,
            "finish_reason": "stop",
            "latency_s": 2.546386,
            "model": "gpt-6-luna",
            "prompt_tokens": 3378,
            "reasoning_tokens": 129
          },
          "error": null,
          "kind": "q_open",
          "reason": "「どうして」と理由を尋ねる、はい／いいえで答えられない質問です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞き直してみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "どうして男はその子に一度も会っていないの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.7944312930339947,
      "judge_s": 2.546478986972943,
      "luna_s": 2.546478986972943,
      "total_s": 4.687772779958323,
      "writer_s": 2.1412937929853797
    }
  },
  {
    "case_id": "U13-e15",
    "record": {
      "comment_id": "U13-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 5586,
            "latency_s": 1.334757,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
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
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A3": 0.77,
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.08,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.66,
              "D": {
                "irrelevant": 0.01,
                "no": 0.9,
                "yes": 0.09
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 227,
            "finish_reason": "stop",
            "latency_s": 3.324184,
            "model": "gpt-6-luna",
            "prompt_tokens": 3373,
            "reasoning_tokens": 150
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "「その子」と「彼」は問題文の人物を指す二択質問で、会ったことはありません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その子は彼に会ったことがある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.335056142997928,
      "judge_s": 3.3242285690503195,
      "luna_s": 3.3242285690503195,
      "total_s": 4.680992822046392,
      "writer_s": 1.3567642529960722
    }
  },
  {
    "case_id": "U13-e16",
    "record": {
      "comment_id": "U13-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4410,
            "latency_s": 0.731238,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                "point_0": {
                  "close": 0.99,
                  "hit": 0.98
                },
                "point_1": {
                  "close": 1.0,
                  "hit": 0.99
                }
              },
              "B2": 0.1
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.98, 矛盾=0.10"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 269,
            "finish_reason": "stop",
            "latency_s": 3.315199,
            "model": "gpt-6-luna",
            "prompt_tokens": 3432,
            "reasoning_tokens": 160
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "手紙の主が昔の男自身で、タイムカプセルに入っていた点も当てています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男が小学生のころ、未来の自分宛てに書いた手紙を学校のタイムカプセルに入れ、50年後の同窓会で受け取った。書いた子は昔の男自身だからよく知っているし、自分には会えなかったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.7315231040120125,
      "judge_s": 3.3152683340013027,
      "luna_s": 3.3152683340013027,
      "total_s": 3.3152748339343816,
      "writer_s": 6.4999330788850784e-06
    }
  },
  {
    "case_id": "U13-e17",
    "record": {
      "comment_id": "U13-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4378,
            "latency_s": 0.85456,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                "point_0": {
                  "close": 0.99,
                  "hit": 0.95
                },
                "point_1": {
                  "close": 1.0,
                  "hit": 1.0
                }
              },
              "B2": 0.12
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.95, 矛盾=0.12"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 367,
            "finish_reason": "stop",
            "latency_s": 3.595303,
            "model": "gpt-6-luna",
            "prompt_tokens": 3424,
            "reasoning_tokens": 257
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "子どもの頃の本人とタイムカプセルの両方を明確に当てています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "小学生の男が未来の自分に宛てて書いた手紙を、学校のタイムカプセルから同窓会で受け取った。書いた子は昔の自分だから、誰より知っていても会ったことはないってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8547901050187647,
      "judge_s": 3.595357840997167,
      "luna_s": 3.595357840997167,
      "total_s": 3.595360553939827,
      "writer_s": 2.712942659854889e-06
    }
  },
  {
    "case_id": "U13-e18",
    "record": {
      "comment_id": "U13-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2878,
            "latency_s": 0.615905,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                "point_0": {
                  "close": 0.7100000000000001,
                  "hit": 0.17
                },
                "point_1": {
                  "close": 0.97,
                  "hit": 0.01
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.01"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 258,
            "finish_reason": "stop",
            "latency_s": 3.028211,
            "model": "gpt-6-luna",
            "prompt_tokens": 3391,
            "reasoning_tokens": 193
          },
          "error": null,
          "kind": "guess_close",
          "reason": "手紙が長く保管されていた点には触れていますが、核心の説明には届いていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "学校で書かれた古い手紙が何十年も保管されていて、男に渡ったんじゃない？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6161577220773324,
      "judge_s": 3.0282362279249355,
      "luna_s": 3.0282362279249355,
      "total_s": 4.530735412961803,
      "writer_s": 1.5024991850368679
    }
  },
  {
    "case_id": "U13-e19",
    "record": {
      "comment_id": "U13-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 3,
            "input_tokens": 2842,
            "latency_s": 0.591584,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
              "A_bare": 0.05,
              "B": {
                "point_0": {
                  "close": 0.99,
                  "hit": 0.96
                },
                "point_1": {
                  "close": 0.12,
                  "hit": 0.03
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.03"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 414,
            "finish_reason": "stop",
            "latency_s": 4.578075,
            "model": "gpt-6-luna",
            "prompt_tokens": 3380,
            "reasoning_tokens": 348
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "書いた子が男自身かを一つだけ確認する質問です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "手紙を書いた男の子って、昔の男自身なんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.5917695329990238,
      "judge_s": 4.578131975024007,
      "luna_s": 4.578131975024007,
      "total_s": 6.387102992972359,
      "writer_s": 1.8089710179483518
    }
  },
  {
    "case_id": "U13-e20",
    "record": {
      "comment_id": "U13-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 3397,
            "latency_s": 0.737425,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 231,
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
                "q_open": 0.83,
                "q_yesno": 0.16
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.01,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.06,
                  "hit": 0.0
                }
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 241,
            "finish_reason": "stop",
            "latency_s": 3.26426,
            "model": "gpt-6-luna",
            "prompt_tokens": 3385,
            "reasoning_tokens": 174
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "郵便の遅配という明確な誤りで、核心の要点には触れていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。質問で少しずつ絞ってみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "郵便局が配達を忘れていて、50年後に遅れて届けたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.7375994039466605,
      "judge_s": 3.2643116409890354,
      "luna_s": 3.2643116409890354,
      "total_s": 4.511687602032907,
      "writer_s": 1.247375961043872
    }
  },
  {
    "case_id": "U13-e21",
    "record": {
      "comment_id": "U13-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 3429,
            "latency_s": 0.816613,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 231,
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
                "q_multi": 0.06,
                "q_open": 0.63,
                "q_yesno": 0.31
              },
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.18000000000000002,
                  "hit": 0.04
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              }
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 144,
            "finish_reason": "stop",
            "latency_s": 2.351696,
            "model": "gpt-6-luna",
            "prompt_tokens": 3391,
            "reasoning_tokens": 78
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "手紙の主を息子という別人としており、核心の要点に触れていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の考え方もしてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙を書いたのは男の息子で、男はその子のことを周りから聞いて知ったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8168969629332423,
      "judge_s": 2.3517535889986902,
      "luna_s": 2.3517535889986902,
      "total_s": 3.3769767018966377,
      "writer_s": 1.0252231128979474
    }
  },
  {
    "case_id": "U13-b22",
    "record": {
      "comment_id": "U13-b22",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5043,
            "latency_s": 1.236945,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.0
                }
              },
              "C": 0.4,
              "D": {
                "irrelevant": 0.0,
                "no": 1.0,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 284,
            "finish_reason": "stop",
            "latency_s": 3.318147,
            "model": "gpt-6-luna",
            "prompt_tokens": 3372,
            "reasoning_tokens": 222
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "手紙は自宅のポストではなく、集まりの場で本人に手渡されています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。手紙は郵便で届いたんじゃないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙は郵便で届いたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2373186240438372,
      "judge_s": 3.318193148006685,
      "luna_s": 3.318193148006685,
      "total_s": 5.97505402402021,
      "writer_s": 2.656860876013525
    }
  },
  {
    "case_id": "U13-b23",
    "record": {
      "comment_id": "U13-b23",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 5558,
            "latency_s": 1.353564,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
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
              "A3": 0.81,
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.02,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.64,
              "D": {
                "irrelevant": 0.02,
                "no": 0.97,
                "yes": 0.01
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 335,
            "finish_reason": "stop",
            "latency_s": 3.348717,
            "model": "gpt-6-luna",
            "prompt_tokens": 3371,
            "reasoning_tokens": 262
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男の子は男自身の子どもの頃であり、父親ではありません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。次の質問もどうぞ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "男はその子の父親なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3540954580530524,
      "judge_s": 3.3487618829822168,
      "luna_s": 3.3487618829822168,
      "total_s": 5.40901921200566,
      "writer_s": 2.060257329023443
    }
  },
  {
    "case_id": "U13-b24",
    "record": {
      "comment_id": "U13-b24",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 5593,
            "latency_s": 1.366051,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
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
              "A3": 0.7,
              "A_bare": 0.02,
              "B": {
                "point_0": {
                  "close": 0.12,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.48,
              "D": {
                "irrelevant": 0.05,
                "no": 0.95,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "completion_tokens": 311,
            "finish_reason": "stop",
            "latency_s": 4.41116,
            "model": "gpt-6-luna",
            "prompt_tokens": 3375,
            "reasoning_tokens": 239
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男がその子を知っていたのは、仕事を通じてではありません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "いいえ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "仕事を通じてその子を知ってたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3663919829996303,
      "judge_s": 4.4112422209000215,
      "luna_s": 4.4112422209000215,
      "total_s": 5.5459372729528695,
      "writer_s": 1.134695052052848
    }
  },
  {
    "case_id": "U13-b25",
    "record": {
      "comment_id": "U13-b25",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": "yes",
        "decision": "luna",
        "kind": "q_yesno"
      },
      "judgements": {
        "jev": {
          "answer": "no",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "input_tokens": 5055,
            "latency_s": 1.223802,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.71,
                "question": 0.29
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.02,
                  "hit": 0.01
                }
              },
              "C": 0.45,
              "D": {
                "irrelevant": 0.02,
                "no": 0.65,
                "yes": 0.33
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
            "completion_tokens": 295,
            "finish_reason": "stop",
            "latency_s": 3.892223,
            "model": "gpt-6-luna",
            "prompt_tokens": 3373,
            "reasoning_tokens": 222
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男は手紙を書いた子の成長後の本人なので、届く前から知っていた。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "手紙が届く前から知ってた？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.2242254529846832,
      "judge_s": 3.8922851940151304,
      "luna_s": 3.8922851940151304,
      "total_s": 5.372182318940759,
      "writer_s": 1.4798971249256283
    }
  },
  {
    "case_id": "U13-b26",
    "record": {
      "comment_id": "U13-b26",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "guess_demoted": true,
            "input_tokens": 5565,
            "latency_s": 1.390694,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
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
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A3": 0.78,
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.57,
              "D": {
                "irrelevant": 0.19,
                "no": 0.81,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 207,
            "finish_reason": "stop",
            "latency_s": 3.418599,
            "model": "gpt-6-luna",
            "prompt_tokens": 3372,
            "reasoning_tokens": 133
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "主治医かどうかは真相や確定事実から判断できません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "男はその子の主治医なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3909132990520447,
      "judge_s": 3.4186579739907756,
      "luna_s": 3.4186579739907756,
      "total_s": 4.72295920108445,
      "writer_s": 1.3043012270936742
    }
  },
  {
    "case_id": "U13-b27",
    "record": {
      "comment_id": "U13-b27",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "calls": 7,
            "input_tokens": 5565,
            "latency_s": 1.417932,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 315,
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
              "A3": 0.76,
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.53,
              "D": {
                "irrelevant": 0.01,
                "no": 0.04,
                "yes": 0.95
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "completion_tokens": 303,
            "finish_reason": "stop",
            "latency_s": 3.783443,
            "model": "gpt-6-luna",
            "prompt_tokens": 3371,
            "reasoning_tokens": 233
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "手紙を書いたのは男の幼少期の本人で、実在した子どもです。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "その子は実在する子なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.4183401130139828,
      "judge_s": 3.7834896879503503,
      "luna_s": 3.7834896879503503,
      "total_s": 5.272934344015084,
      "writer_s": 1.4894446560647339
    }
  },
  {
    "case_id": "U13-b28",
    "record": {
      "comment_id": "U13-b28",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5025,
            "latency_s": 1.329933,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.51,
              "D": {
                "irrelevant": 0.01,
                "no": 0.99,
                "yes": 0.0
              }
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "luna": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "completion_tokens": 288,
            "finish_reason": "stop",
            "latency_s": 3.878832,
            "model": "gpt-6-luna",
            "prompt_tokens": 3369,
            "reasoning_tokens": 211
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "男の知名度は真相に関係せず、確定事実からも判断できません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "男は有名人なの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3303067809902132,
      "judge_s": 3.878899198025465,
      "luna_s": 3.878899198025465,
      "total_s": 5.447985708946362,
      "writer_s": 1.5690865109208971
    }
  },
  {
    "case_id": "U13-k01",
    "record": {
      "comment_id": "U13-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4218,
            "latency_s": 0.736524,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                "point_0": {
                  "close": 0.9299999999999999,
                  "hit": 0.86
                },
                "point_1": {
                  "close": 0.97,
                  "hit": 0.9
                }
              },
              "B2": 0.18
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.86, 矛盾=0.18"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 470,
            "finish_reason": "stop",
            "latency_s": 4.60166,
            "model": "gpt-6-luna",
            "prompt_tokens": 3398,
            "reasoning_tokens": 361
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "書き手が男自身で、未来向けに埋めた学校の箱にも触れています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "書き手は幼い頃の男自身で、学校の記念箱を掘り出して未来向けの手紙が届いたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.7368572190171108,
      "judge_s": 4.60172583500389,
      "luna_s": 4.60172583500389,
      "total_s": 4.601743267965503,
      "writer_s": 1.7432961612939835e-05
    }
  },
  {
    "case_id": "U13-k02",
    "record": {
      "comment_id": "U13-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 4214,
            "latency_s": 0.800212,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 209,
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
                "point_0": {
                  "close": 0.94,
                  "hit": 0.73
                },
                "point_1": {
                  "close": 0.98,
                  "hit": 0.95
                }
              },
              "B2": 0.1
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.73, 矛盾=0.10"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 302,
            "finish_reason": "stop",
            "latency_s": 3.532363,
            "model": "gpt-6-luna",
            "prompt_tokens": 3395,
            "reasoning_tokens": 186
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "少年が男自身で、手紙を将来読むため学校に埋めた企画から出た点を両方当てています。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！手紙は小学生の男が未来の自分へ書いたもの。50年後、同窓会でタイムカプセルから受け取った。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙の少年は昔の男で、校内の埋蔵企画に将来読むものとして預けられていたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.8005988920340315,
      "judge_s": 3.5324162259930745,
      "luna_s": 3.5324162259930745,
      "total_s": 3.5324226999655366,
      "writer_s": 6.473972462117672e-06
    }
  },
  {
    "case_id": "U13-k03",
    "record": {
      "comment_id": "U13-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2908,
            "latency_s": 0.642803,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                "point_0": {
                  "close": 0.98,
                  "hit": 0.95
                },
                "point_1": {
                  "close": 0.8400000000000001,
                  "hit": 0.05
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.05"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 341,
            "finish_reason": "stop",
            "latency_s": 4.690075,
            "model": "gpt-6-luna",
            "prompt_tokens": 3400,
            "reasoning_tokens": 270
          },
          "error": null,
          "kind": "guess_close",
          "reason": "書き手が男の子どもの頃の本人という要点は当たっていますが、タイムカプセルには触れていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "書き手は男が子どもだった頃の本人で、何十年も経ってから学校の記念行事で手紙が渡ったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.6430073860101402,
      "judge_s": 4.690152170020156,
      "luna_s": 4.690152170020156,
      "total_s": 5.949187573976815,
      "writer_s": 1.2590354039566591
    }
  },
  {
    "case_id": "U13-k04",
    "record": {
      "comment_id": "U13-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2887,
            "latency_s": 0.590291,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                "point_0": {
                  "close": 0.87,
                  "hit": 0.09
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.96
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.09"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 364,
            "finish_reason": "stop",
            "latency_s": 4.363034,
            "model": "gpt-6-luna",
            "prompt_tokens": 3394,
            "reasoning_tokens": 297
          },
          "error": null,
          "kind": "guess_close",
          "reason": "将来用に埋めた箱は当てていますが、書いた子が男自身とは述べていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙を書いた子は同じ学校の卒業生で、将来用に埋めておいた箱から届いたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.5905675459653139,
      "judge_s": 4.363073818036355,
      "luna_s": 4.363073818036355,
      "total_s": 5.562918727984652,
      "writer_s": 1.1998449099482968
    }
  },
  {
    "case_id": "U13-k05",
    "record": {
      "comment_id": "U13-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 2878,
            "latency_s": 0.588872,
            "major": "guess",
            "model": "jev-latest",
            "output_tokens": 187,
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
                "point_0": {
                  "close": 0.28,
                  "hit": 0.05
                },
                "point_1": {
                  "close": 0.98,
                  "hit": 0.01
                }
              }
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.01"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 218,
            "finish_reason": "stop",
            "latency_s": 3.06981,
            "model": "gpt-6-luna",
            "prompt_tokens": 3394,
            "reasoning_tokens": 149
          },
          "error": null,
          "kind": "guess_close",
          "reason": "学校の手紙が長年保管された点には触れていますが、書き手が男自身とは述べていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙は古い学校の記念品で、何十年も保管されてから男の手元に来たんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.5891742530511692,
      "judge_s": 3.06993203505408,
      "luna_s": 3.06993203505408,
      "total_s": 4.6225844520376995,
      "writer_s": 1.5526524169836193
    }
  },
  {
    "case_id": "U13-k06",
    "record": {
      "comment_id": "U13-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 5187,
            "latency_s": 1.314956,
            "major": "question",
            "model": "jev-latest",
            "output_tokens": 293,
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
                "q_open": 0.27,
                "q_yesno": 0.72
              },
              "A_bare": 0.03,
              "B": {
                "point_0": {
                  "close": 0.03,
                  "hit": 0.02
                },
                "point_1": {
                  "close": 0.04,
                  "hit": 0.01
                }
              },
              "C": 0.24,
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
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 138,
            "finish_reason": "stop",
            "latency_s": 2.264958,
            "model": "gpt-6-luna",
            "prompt_tokens": 3391,
            "reasoning_tokens": 74
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "郵便の遅配という推理で、核心となる要点には触れていません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "住所を間違えていた昔の手紙が、郵便局から何十年も遅れて届いたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 1.3153551549185067,
      "judge_s": 2.2650083389598876,
      "luna_s": 2.2650083389598876,
      "total_s": 3.8803069329587743,
      "writer_s": 1.6152985939988866
    }
  },
  {
    "case_id": "U13-t01",
    "record": {
      "comment_id": "U13-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "タイムカプセル",
          "debug": {
            "calls": 1,
            "input_tokens": 931,
            "latency_s": 0.179913,
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
          "bare_term": "タイムカプセル",
          "debug": {
            "completion_tokens": 147,
            "finish_reason": "stop",
            "latency_s": 2.513411,
            "model": "gpt-6-luna",
            "prompt_tokens": 3367,
            "reasoning_tokens": 72
          },
          "error": null,
          "kind": "q_open",
          "reason": "名詞だけのコメントなので、推理ではなく q_open と判定します。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "タイムカプセルの何が気になるのかな？はい・いいえで聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "タイムカプセル",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.18000089097768068,
      "judge_s": 2.5134588849032298,
      "luna_s": 2.5134588849032298,
      "total_s": 6.492133054882288,
      "writer_s": 3.978674169979058
    }
  },
  {
    "case_id": "U13-t02",
    "record": {
      "comment_id": "U13-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "同窓会",
          "debug": {
            "calls": 1,
            "input_tokens": 929,
            "latency_s": 0.183897,
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
              "A_bare": 0.9
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.90"
        },
        "luna": {
          "answer": null,
          "bare_term": "同窓会",
          "debug": {
            "completion_tokens": 168,
            "finish_reason": "stop",
            "latency_s": 2.70749,
            "model": "gpt-6-luna",
            "prompt_tokens": 3367,
            "reasoning_tokens": 94
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、質問の形をお願いする。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "同窓会が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "同窓会？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.18394771101884544,
      "judge_s": 2.7075175039935857,
      "luna_s": 2.7075175039935857,
      "total_s": 5.677902619005181,
      "writer_s": 2.970385115011595
    }
  },
  {
    "case_id": "U13-t03",
    "record": {
      "comment_id": "U13-t03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "q_open"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": "手紙",
          "debug": {
            "calls": 1,
            "input_tokens": 927,
            "latency_s": 0.178897,
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
              "A_bare": 0.93
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.93"
        },
        "luna": {
          "answer": null,
          "bare_term": "手紙",
          "debug": {
            "completion_tokens": 193,
            "finish_reason": "stop",
            "latency_s": 2.864832,
            "model": "gpt-6-luna",
            "prompt_tokens": 3365,
            "reasoning_tokens": 106
          },
          "error": null,
          "kind": "q_open",
          "reason": "述語のない語句だけのコメントなので、はい・いいえでは答えられません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "手紙がどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "手紙？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.1789534860290587,
      "judge_s": 2.8648758199997246,
      "luna_s": 2.8648758199997246,
      "total_s": 5.149255351047032,
      "writer_s": 2.284379531047307
    }
  },
  {
    "case_id": "c-ask_hint-03",
    "record": {
      "comment_id": "c-ask_hint-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "ask_hint"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1425,
            "latency_s": 0.415593,
            "major": "request",
            "model": "jev-latest",
            "output_tokens": 122,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 1.0
              },
              "A2": {
                "ask_hint": 1.0,
                "ask_howto": 0.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.13
            }
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "段A=request→ask_hint"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 218,
            "finish_reason": "stop",
            "latency_s": 2.964553,
            "model": "gpt-6-luna",
            "prompt_tokens": 3370,
            "reasoning_tokens": 135
          },
          "error": null,
          "kind": "ask_hint",
          "reason": "考え方のヒントを求めているため、ヒント希望と判断しました。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ヒントは出せないけど、質問で少しずつ絞っていこうね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "考え方のヒントある？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.4157666719984263,
      "judge_s": 2.9646087089786306,
      "luna_s": 2.9646087089786306,
      "total_s": 4.6568801059620455,
      "writer_s": 1.6922713969834149
    }
  },
  {
    "case_id": "c-impression-02",
    "record": {
      "comment_id": "c-impression-02",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "impression"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1588,
            "latency_s": 0.368068,
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
                "cheer": 0.01,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.99,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.07
            }
          },
          "error": null,
          "kind": "impression",
          "reason": "段A=reaction→impression"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 190,
            "finish_reason": "stop",
            "latency_s": 3.196842,
            "model": "gpt-6-luna",
            "prompt_tokens": 3372,
            "reasoning_tokens": 130
          },
          "error": null,
          "kind": "impression",
          "reason": "問題について、考える楽しさと面白さを伝える感想です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "楽しんでくれてうれしいよ！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "毎回考えちゃう、面白い",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.3681440450018272,
      "judge_s": 3.1968656209064648,
      "luna_s": 3.1968656209064648,
      "total_s": 5.391825132886879,
      "writer_s": 2.1949595119804144
    }
  },
  {
    "case_id": "c-chat-01",
    "record": {
      "comment_id": "c-chat-01",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "chat"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1584,
            "latency_s": 0.410791,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 148,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 1.0,
                "request": 0.0
              },
              "A2": {
                "chat": 1.0,
                "cheer": 0.0,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.0,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.04
            }
          },
          "error": null,
          "kind": "chat",
          "reason": "段A=reaction→chat"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 226,
            "finish_reason": "stop",
            "latency_s": 3.474011,
            "model": "gpt-6-luna",
            "prompt_tokens": 3369,
            "reasoning_tokens": 165
          },
          "error": null,
          "kind": "chat",
          "reason": "問題への質問や推理ではなく、今日の暑さについての雑談です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ほんと、暑いね〜😌"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "今日めっちゃ暑いね",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.4109345090109855,
      "judge_s": 3.474068778101355,
      "luna_s": 3.474068778101355,
      "total_s": 4.998037739074789,
      "writer_s": 1.5239689609734342
    }
  },
  {
    "case_id": "c-complaint-05",
    "record": {
      "comment_id": "c-complaint-05",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
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
            "input_tokens": 1594,
            "latency_s": 0.402186,
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
                "cheer": 0.0,
                "complaint": 0.58,
                "greeting": 0.0,
                "impression": 0.42,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.06
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
            "completion_tokens": 151,
            "finish_reason": "stop",
            "latency_s": 2.219285,
            "model": "gpt-6-luna",
            "prompt_tokens": 3374,
            "reasoning_tokens": 86
          },
          "error": null,
          "kind": "complaint",
          "reason": "最近の問題が難しすぎるという、問題への指摘です。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "教えてくれてありがとう、確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "最近ちょっと難しすぎるかも…",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.4023565669776872,
      "judge_s": 2.219335717963986,
      "luna_s": 2.219335717963986,
      "total_s": 3.533758023986593,
      "writer_s": 1.3144223060226068
    }
  },
  {
    "case_id": "c-troll-04",
    "record": {
      "comment_id": "c-troll-04",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "troll"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1580,
            "latency_s": 0.396366,
            "major": "reaction",
            "model": "jev-latest",
            "output_tokens": 150,
            "probabilities": {
              "A1": {
                "inappropriate": 0.43,
                "other": 0.0,
                "question_or_guess": 0.05,
                "reaction": 0.52,
                "request": 0.0
              },
              "A2": {
                "chat": 0.15,
                "cheer": 0.0,
                "complaint": 0.04,
                "greeting": 0.0,
                "impression": 0.81,
                "mention": 0.0,
                "request": 0.0
              },
              "A_bare": 0.45
            }
          },
          "error": null,
          "kind": "impression",
          "reason": "段A=reaction→impression"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 159,
            "finish_reason": "stop",
            "latency_s": 2.575488,
            "model": "gpt-6-luna",
            "prompt_tokens": 3369,
            "reasoning_tokens": 105
          },
          "error": null,
          "kind": "troll",
          "reason": "意味の取れない文字列で、質問や推理として判別できません。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "何か聞きたいことがあったら、質問してね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": true,
      "text": "あああ???ぴょ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.3965265799779445,
      "judge_s": 2.575545433908701,
      "luna_s": 2.575545433908701,
      "total_s": 2.5755499489605427,
      "writer_s": 4.51505184173584e-06
    }
  },
  {
    "case_id": "c-personal_info-03",
    "record": {
      "comment_id": "c-personal_info-03",
      "commenter_id": "probe",
      "config": {
        "consensus": true,
        "judge_mode": "hybrid",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "1d-luna",
        "shadow": true
      },
      "content_key": "004-fifty-year-letter",
      "errors": [],
      "fact_sheet_hash": "fde385625dde",
      "final": {
        "answer": null,
        "decision": "luna",
        "kind": "personal_info"
      },
      "judgements": {
        "jev": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "input_tokens": 1500,
            "latency_s": 0.418163,
            "major": "inappropriate",
            "model": "jev-latest",
            "output_tokens": 129,
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
                "personal_info": 0.97,
                "spam": 0.0,
                "troll": 0.03
              },
              "A_bare": 0.07
            }
          },
          "error": null,
          "kind": "personal_info",
          "reason": "段A=inappropriate→personal_info"
        },
        "luna": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "completion_tokens": 86,
            "finish_reason": "stop",
            "latency_s": 1.784686,
            "model": "gpt-6-luna",
            "prompt_tokens": 3377,
            "reasoning_tokens": 36
          },
          "error": null,
          "kind": "personal_info",
          "reason": "住所にあたる個人情報が含まれているため。"
        }
      },
      "media_id": "local-U13",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "no_reply",
        "text": null
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": false,
      "text": "住所は東京都テスト区サンプル町000-0000です",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-07T23:44:37Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-07T23:44:37Z"
      }
    },
    "timing": {
      "jev_s": 0.41831159102730453,
      "judge_s": 1.7847405130742118,
      "luna_s": 1.7847405130742118,
      "total_s": 1.7847440129844472,
      "writer_s": 3.4999102354049683e-06
    }
  }
];

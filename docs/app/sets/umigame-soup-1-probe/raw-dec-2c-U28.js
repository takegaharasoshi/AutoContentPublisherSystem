window.PROBE_RAW = window.PROBE_RAW || {};
window.PROBE_RAW["dec-2c/U28"] = [
  {
    "case_id": "U28-e01",
    "record": {
      "comment_id": "U28-e01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.79,
                "point_1": 0.91
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3553,
            "latency_s": 1.407226,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.14,
                  "hit": 0.05
                },
                "point_1": {
                  "close": 0.06,
                  "hit": 0.03
                }
              },
              "C": 0.97,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.03"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 23,
          "latency_s": 1.364282,
          "model": "gpt-6-luna",
          "prompt_tokens": 1438,
          "reasoning_tokens": 0,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！その調子で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は以前にもウミガメのスープを飲んだことがありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.407606009976007,
      "jev_s": null,
      "judge_s": 1.407606009976007,
      "luna_s": null,
      "total_s": 2.7782925360370427,
      "writer_s": 1.3706865260610357
    }
  },
  {
    "case_id": "U28-e02",
    "record": {
      "comment_id": "U28-e02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.44
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.94,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.7
              }
            },
            "input_tokens": 3571,
            "latency_s": 1.357611,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.28,
                "question": 0.72
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
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
              "C": 0.72,
              "D": {
                "irrelevant": 0.0,
                "no": 0.2,
                "yes": 0.8
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 136,
          "latency_s": 2.451589,
          "model": "gpt-6-luna",
          "prompt_tokens": 1442,
          "reasoning_tokens": 103,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！スープの味に覚えがあったからだよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男が泣いたのは、スープの味に覚えがあったからですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3580160840647295,
      "jev_s": null,
      "judge_s": 1.3580160840647295,
      "luna_s": null,
      "total_s": 3.8102641630684957,
      "writer_s": 2.452248079003766
    }
  },
  {
    "case_id": "U28-e03",
    "record": {
      "comment_id": "U28-e03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.76
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.88,
                "point_1": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.99
              }
            },
            "input_tokens": 3523,
            "latency_s": 1.435656,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.08,
                  "hit": 0.03
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.68,
              "D": {
                "irrelevant": 0.0,
                "no": 0.01,
                "yes": 0.99
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 60,
          "latency_s": 1.744563,
          "model": "gpt-6-luna",
          "prompt_tokens": 1433,
          "reasoning_tokens": 36,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔、遭難した経験があるんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.4359739649808034,
      "jev_s": null,
      "judge_s": 1.4359739649808034,
      "luna_s": null,
      "total_s": 3.181502289022319,
      "writer_s": 1.7455283240415156
    }
  },
  {
    "case_id": "U28-e04",
    "record": {
      "comment_id": "U28-e04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.04
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.93
              }
            },
            "input_tokens": 3595,
            "latency_s": 1.477832,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.48,
                "question": 0.52
              },
              "A2": {
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
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
              "C": 0.83,
              "D": {
                "irrelevant": 0.0,
                "no": 0.05,
                "yes": 0.95
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 13,
          "latency_s": 1.387113,
          "model": "gpt-6-luna",
          "prompt_tokens": 1443,
          "reasoning_tokens": 0,
          "slot": "判定語だけ"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "本物だと聞いたことで、男の過去の記憶がよみがえったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.4781274360138923,
      "jev_s": null,
      "judge_s": 1.4781274360138923,
      "luna_s": null,
      "total_s": 2.8668458430329338,
      "writer_s": 1.3887184070190415
    }
  },
  {
    "case_id": "U28-e05",
    "record": {
      "comment_id": "U28-e05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.93,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.46
              }
            },
            "input_tokens": 3571,
            "latency_s": 1.397759,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.05,
                  "hit": 0.03
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.84,
              "D": {
                "irrelevant": 0.01,
                "no": 0.35,
                "yes": 0.64
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 112,
          "latency_s": 1.966237,
          "model": "gpt-6-luna",
          "prompt_tokens": 1442,
          "reasoning_tokens": 77,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！飲む前から本物かどうか疑っていたんだね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを飲む前から、男は本物かどうか疑っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.398228143923916,
      "jev_s": null,
      "judge_s": 1.398228143923916,
      "luna_s": null,
      "total_s": 3.3655635869363323,
      "writer_s": 1.9673354430124164
    }
  },
  {
    "case_id": "U28-e06",
    "record": {
      "comment_id": "U28-e06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "irrelevant",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 1.0,
                "point_1": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.25
              }
            },
            "input_tokens": 3505,
            "latency_s": 1.392953,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.01
                }
              },
              "C": 0.35,
              "D": {
                "irrelevant": 0.21,
                "no": 0.29,
                "yes": 0.5
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 129,
          "latency_s": 2.640874,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 96,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "そのレストランは海辺にありますか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.3933632950065657,
      "jev_s": null,
      "judge_s": 1.3933632950065657,
      "luna_s": null,
      "total_s": 4.0349940310698,
      "writer_s": 2.6416307360632345
    }
  },
  {
    "case_id": "U28-e07",
    "record": {
      "comment_id": "U28-e07",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 0.99
              },
              "B": {
                "point_0": 1.0,
                "point_1": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.52
              }
            },
            "input_tokens": 3529,
            "latency_s": 1.437955,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.0,
                "q_open": 0.01,
                "q_yesno": 0.99
              },
              "A_bare": 0.0,
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
              "C": 0.68,
              "D": {
                "irrelevant": 0.04,
                "no": 0.28,
                "yes": 0.68
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 167,
          "latency_s": 2.466094,
          "model": "gpt-6-luna",
          "prompt_tokens": 1435,
          "reasoning_tokens": 135,
          "slot": "判定語 + 復唱"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！シェフは男のことを知っていたよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "シェフは男のことを知っていたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.4383267640369013,
      "jev_s": null,
      "judge_s": 1.4383267640369013,
      "luna_s": null,
      "total_s": 3.905661227996461,
      "writer_s": 2.46733446395956
    }
  },
  {
    "case_id": "U28-e08",
    "record": {
      "comment_id": "U28-e08",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "yes",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "yes",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.96
              },
              "A2": {
                "kind": 0.96
              },
              "B": {
                "point_0": 0.94,
                "point_1": 0.99
              },
              "C": {},
              "D": {
                "answer": 0.94
              }
            },
            "input_tokens": 3577,
            "latency_s": 1.415364,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_open": 0.03,
                "q_yesno": 0.97
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.04,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.0
                }
              },
              "C": 0.71,
              "D": {
                "irrelevant": 0.01,
                "no": 0.03,
                "yes": 0.96
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 70,
          "latency_s": 1.606018,
          "model": "gpt-6-luna",
          "prompt_tokens": 1442,
          "reasoning_tokens": 41,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい！ふむふむ、次はどうかな？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はスープを飲んで、何か別のものを思い出したんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.4157036590622738,
      "jev_s": null,
      "judge_s": 1.4157036590622738,
      "luna_s": null,
      "total_s": 3.022912319051102,
      "writer_s": 1.607208659988828
    }
  },
  {
    "case_id": "U28-e09",
    "record": {
      "comment_id": "U28-e09",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": "irrelevant",
        "decision": "decisions",
        "kind": "q_yesno"
      },
      "judgements": {
        "decisions": {
          "answer": "irrelevant",
          "bare_term": null,
          "debug": {
            "calls": 6,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "A2": {
                "kind": 1.0
              },
              "B": {
                "point_0": 0.97,
                "point_1": 1.0
              },
              "C": {},
              "D": {
                "answer": 0.22
              }
            },
            "input_tokens": 3541,
            "latency_s": 1.48761,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.0,
                "q_open": 0.0,
                "q_yesno": 1.0
              },
              "A_bare": 0.0,
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
              "C": 0.48,
              "D": {
                "irrelevant": 0.2,
                "no": 0.32,
                "yes": 0.48
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_yesno",
          "reason": "段A=question→q_yesno, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 91,
          "latency_s": 2.060705,
          "model": "gpt-6-luna",
          "prompt_tokens": 1436,
          "reasoning_tokens": 58,
          "slot": "判定語 + 一言"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "関係ないよ。ほかのことも聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを出したのは、その店のシェフ本人ですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.4881413920084015,
      "jev_s": null,
      "judge_s": 1.4881413920084015,
      "luna_s": null,
      "total_s": 3.5499536760617048,
      "writer_s": 2.0618122840533033
    }
  },
  {
    "case_id": "U28-e10",
    "record": {
      "comment_id": "U28-e10",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 5,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.5
              },
              "A2": {
                "kind": 0.94
              },
              "B": {
                "point_0": 0.96,
                "point_1": 1.0
              },
              "C": {}
            },
            "input_tokens": 2684,
            "latency_s": 1.59944,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.75,
                "question": 0.25
              },
              "A2": {
                "q_multi": 0.01,
                "q_open": 0.03,
                "q_yesno": 0.96
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.03,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              },
              "C": 0.09
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 78,
          "latency_s": 2.143749,
          "model": "gpt-6-luna",
          "prompt_tokens": 1438,
          "reasoning_tokens": 44,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔、ウミガメを飼っていたんでしょか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.599726389045827,
      "jev_s": null,
      "judge_s": 1.599726389045827,
      "luna_s": null,
      "total_s": 3.7445779510308057,
      "writer_s": 2.1448515619849786
    }
  },
  {
    "case_id": "U28-e11",
    "record": {
      "comment_id": "U28-e11",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_multi"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.93
              }
            },
            "input_tokens": 1538,
            "latency_s": 0.677694,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_open": 0.01,
                "q_yesno": 0.04
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 133,
          "latency_s": 2.43246,
          "model": "gpt-6-luna",
          "prompt_tokens": 1449,
          "reasoning_tokens": 93,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。どちらか一つから聞いてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は過去にウミガメを食べたことがあるの？その時の出来事を思い出したの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.677869084989652,
      "jev_s": null,
      "judge_s": 0.677869084989652,
      "luna_s": null,
      "total_s": 3.1110551060410216,
      "writer_s": 2.4331860210513696
    }
  },
  {
    "case_id": "U28-e12",
    "record": {
      "comment_id": "U28-e12",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_multi"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.68
              },
              "A2": {
                "kind": 0.31
              }
            },
            "input_tokens": 1529,
            "latency_s": 0.68605,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.54,
                "q_open": 0.1,
                "q_yesno": 0.36
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_multi",
          "reason": "段A=question→q_multi"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 102,
          "latency_s": 1.944799,
          "model": "gpt-6-luna",
          "prompt_tokens": 1446,
          "reasoning_tokens": 64,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "質問はひとつずつコメントしてね。順番に聞いていこうか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープの味が記憶と違ったの？本物だと聞いて何かに気づいたの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6862371839815751,
      "jev_s": null,
      "judge_s": 0.6862371839815751,
      "luna_s": null,
      "total_s": 2.6319510439643636,
      "writer_s": 1.9457138599827886
    }
  },
  {
    "case_id": "U28-e13",
    "record": {
      "comment_id": "U28-e13",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.64
              },
              "A3": {}
            },
            "input_tokens": 1889,
            "latency_s": 0.931914,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.01,
                "q_open": 0.76,
                "q_yesno": 0.23
              },
              "A3": 0.0,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 126,
          "latency_s": 2.254905,
          "model": "gpt-6-luna",
          "prompt_tokens": 1441,
          "reasoning_tokens": 75,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "「男は本物か確かめた？」のように、はい・いいえで答えられる形で聞いてごらん。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はなぜ本物のウミガメかどうか確かめたんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9322488789912313,
      "jev_s": null,
      "judge_s": 0.9322488789912313,
      "luna_s": null,
      "total_s": 3.188356848899275,
      "writer_s": 2.2561079699080437
    }
  },
  {
    "case_id": "U28-e14",
    "record": {
      "comment_id": "U28-e14",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.62
              },
              "A2": {
                "kind": 0.99
              },
              "A3": {}
            },
            "input_tokens": 1881,
            "latency_s": 0.891336,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_open": 0.99,
                "q_yesno": 0.01
              },
              "A3": 0.0,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 128,
          "latency_s": 2.588782,
          "model": "gpt-6-luna",
          "prompt_tokens": 1439,
          "reasoning_tokens": 84,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男が何を思い出したのか、はい・いいえで答えられる質問にしてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "スープを飲んだとき、男は何を思い出したんでしょう？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.8916344399331138,
      "jev_s": null,
      "judge_s": 0.8916344399331138,
      "luna_s": null,
      "total_s": 3.4815292949788272,
      "writer_s": 2.5898948550457135
    }
  },
  {
    "case_id": "U28-e15",
    "record": {
      "comment_id": "U28-e15",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.94
              },
              "A2": {
                "kind": 0.99
              },
              "A3": {}
            },
            "input_tokens": 1889,
            "latency_s": 1.01011,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A3": 0.0,
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A=question→q_open, 再確認=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 154,
          "latency_s": 2.883885,
          "model": "gpt-6-luna",
          "prompt_tokens": 1441,
          "reasoning_tokens": 106,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "男に過去に何があったのか、はい・いいえで答えられる形で聞いてみてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男が泣き崩れるまでに、どんな過去があったんですか？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.0103504529688507,
      "jev_s": null,
      "judge_s": 1.0103504529688507,
      "luna_s": null,
      "total_s": 3.8952877540141344,
      "writer_s": 2.8849373010452837
    }
  },
  {
    "case_id": "U28-e16",
    "record": {
      "comment_id": "U28-e16",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 5,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.88
              },
              "A2": {
                "kind": 0.52
              },
              "B": {
                "point_0": 0.51,
                "point_1": 0.94
              },
              "B2": {}
            },
            "input_tokens": 3360,
            "latency_s": 1.178403,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.02,
                "q_open": 0.3,
                "q_yesno": 0.68
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.8400000000000001,
                  "hit": 0.67
                },
                "point_1": {
                  "close": 0.98,
                  "hit": 0.96
                }
              },
              "B2": 0.01
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=question→guess_correct, 要点最低=0.67, 矛盾=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "昔ウミガメのスープだと言われて飲んだものが、仲間の肉だったってこと？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.1786685469560325,
      "jev_s": null,
      "judge_s": 1.1786685469560325,
      "luna_s": null,
      "total_s": 1.178682325873524,
      "writer_s": 1.3778917491436005e-05
    }
  },
  {
    "case_id": "U28-e17",
    "record": {
      "comment_id": "U28-e17",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 1.0
              },
              "B": {
                "point_0": 0.56,
                "point_1": 0.86
              },
              "B2": {}
            },
            "input_tokens": 3121,
            "latency_s": 0.914757,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.9299999999999999,
                  "hit": 0.71
                },
                "point_1": {
                  "close": 0.97,
                  "hit": 0.91
                }
              },
              "B2": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.71, 矛盾=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "昔、仲間の肉をウミガメのスープだと言われて飲んだんだね。本物の味が違って、あの時の嘘に気づいたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9149277729447931,
      "jev_s": null,
      "judge_s": 0.9149277729447931,
      "luna_s": null,
      "total_s": 0.9149334589019418,
      "writer_s": 5.68595714867115e-06
    }
  },
  {
    "case_id": "U28-e18",
    "record": {
      "comment_id": "U28-e18",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.98
              },
              "B": {
                "point_0": 0.49,
                "point_1": 0.67
              }
            },
            "input_tokens": 2043,
            "latency_s": 0.64836,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.79,
                  "hit": 0.66
                },
                "point_1": {
                  "close": 0.22,
                  "hit": 0.06
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.06"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 78,
          "latency_s": 1.680653,
          "model": "gpt-6-luna",
          "prompt_tokens": 1451,
          "reasoning_tokens": 47,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！推理を続けてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流していたとき、仲間からウミガメのスープだと言われて飲んだことがあったんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6484778900630772,
      "jev_s": null,
      "judge_s": 0.6484778900630772,
      "luna_s": null,
      "total_s": 2.3462238269858062,
      "writer_s": 1.697745936922729
    }
  },
  {
    "case_id": "U28-e19",
    "record": {
      "comment_id": "U28-e19",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.94
              },
              "B": {
                "point_0": 0.42,
                "point_1": 0.73
              }
            },
            "input_tokens": 2085,
            "latency_s": 0.678363,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.97,
                "question": 0.03
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.39,
                  "hit": 0.26
                },
                "point_1": {
                  "close": 0.9299999999999999,
                  "hit": 0.82
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.26"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 89,
          "latency_s": 3.85317,
          "model": "gpt-6-luna",
          "prompt_tokens": 1465,
          "reasoning_tokens": 56,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "仲間の肉をウミガメのスープだと言われて飲んだんだね。でもそのとき仲間はみんな助かって、あとで一緒に帰れたのか。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6785074439831078,
      "jev_s": null,
      "judge_s": 0.6785074439831078,
      "luna_s": null,
      "total_s": 4.532434631953947,
      "writer_s": 3.8539271879708394
    }
  },
  {
    "case_id": "U28-e20",
    "record": {
      "comment_id": "U28-e20",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_wrong"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.96
              },
              "A2": {
                "kind": 0.64
              },
              "B": {
                "point_0": 1.0,
                "point_1": 0.99
              }
            },
            "guess_demoted": true,
            "input_tokens": 2352,
            "latency_s": 1.298939,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A2": {
                "q_multi": 0.04,
                "q_open": 0.76,
                "q_yesno": 0.2
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.0,
                  "hit": 0.0
                },
                "point_1": {
                  "close": 0.01,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 76,
          "latency_s": 1.783041,
          "model": "gpt-6-luna",
          "prompt_tokens": 1448,
          "reasoning_tokens": 39,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか？"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男はウミガメが大好きで、食べてしまったことが悲しくて泣いたんでしょ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 1.2991892619756982,
      "jev_s": null,
      "judge_s": 1.2991892619756982,
      "luna_s": null,
      "total_s": 3.083318233024329,
      "writer_s": 1.7841289710486308
    }
  },
  {
    "case_id": "U28-e21",
    "record": {
      "comment_id": "U28-e21",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_wrong"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.83
              },
              "B": {
                "point_0": 0.97,
                "point_1": 0.88
              }
            },
            "guess_demoted": true,
            "input_tokens": 2372,
            "latency_s": 0.942578,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.02,
                "q_open": 0.89,
                "q_yesno": 0.09
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.02,
                  "hit": 0.01
                },
                "point_1": {
                  "close": 0.08,
                  "hit": 0.01
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 30,
          "latency_s": 1.068937,
          "model": "gpt-6-luna",
          "prompt_tokens": 1453,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。別の可能性も考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "子どものころに飼っていたカメがこのスープに使われたと思い込んで、悲しくなったんだと思う。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9428115150658414,
      "jev_s": null,
      "judge_s": 0.9428115150658414,
      "luna_s": null,
      "total_s": 2.0294537520967424,
      "writer_s": 1.086642237030901
    }
  },
  {
    "case_id": "U28-k01",
    "record": {
      "comment_id": "U28-k01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A1b": {
                "qg": 0.96
              },
              "B": {
                "point_0": 0.72,
                "point_1": 0.99
              },
              "B2": {}
            },
            "input_tokens": 3085,
            "latency_s": 0.945495,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.99,
                "reaction": 0.0,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.98,
                "question": 0.02
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.89,
                  "hit": 0.81
                },
                "point_1": {
                  "close": 1.0,
                  "hit": 0.99
                }
              },
              "B2": 0.01
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.81, 矛盾=0.01"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流中に亀のスープと聞かされて口にした一杯は、実は仲間の肉から作られてたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9457480609416962,
      "jev_s": null,
      "judge_s": 0.9457480609416962,
      "luna_s": null,
      "total_s": 0.9457632090197876,
      "writer_s": 1.5148078091442585e-05
    }
  },
  {
    "case_id": "U28-k02",
    "record": {
      "comment_id": "U28-k02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_correct"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 1.0
              },
              "B": {
                "point_0": 0.67,
                "point_1": 0.96
              },
              "B2": {}
            },
            "input_tokens": 3097,
            "latency_s": 0.973517,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.79,
                  "hit": 0.78
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.97
                }
              },
              "B2": 0.02
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_correct",
          "reason": "段A=guess→guess_correct, 要点最低=0.78, 矛盾=0.02"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "正解！男は遭難中、ウミガメのスープだと言われて亡くなった仲間の肉を飲んでいた。本物の味でそれに気づいた。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流中に亀の汁だと渡されて飲んだ一杯は仲間の肉で、男は正体に後から気づいたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9737579319626093,
      "jev_s": null,
      "judge_s": 0.9737579319626093,
      "luna_s": null,
      "total_s": 0.9737638359656557,
      "writer_s": 5.904003046452999e-06
    }
  },
  {
    "case_id": "U28-k03",
    "record": {
      "comment_id": "U28-k03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 0.98
              },
              "A1b": {
                "qg": 0.98
              },
              "B": {
                "point_0": 0.85,
                "point_1": 0.79
              }
            },
            "input_tokens": 2046,
            "latency_s": 0.707209,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.98,
                "reaction": 0.01,
                "request": 0.01
              },
              "A1b": {
                "guess": 0.99,
                "question": 0.01
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.9500000000000001,
                  "hit": 0.9
                },
                "point_1": {
                  "close": 0.94,
                  "hit": 0.08
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.08"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 73,
          "latency_s": 2.289557,
          "model": "gpt-6-luna",
          "prompt_tokens": 1452,
          "reasoning_tokens": 40,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "漂流中、ウミガメの汁だと説明されて飲んだけど、材料は口にしてはいけないものだったんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7074901279993355,
      "jev_s": null,
      "judge_s": 0.7074901279993355,
      "luna_s": null,
      "total_s": 2.9981293519958854,
      "writer_s": 2.29063922399655
    }
  },
  {
    "case_id": "U28-k04",
    "record": {
      "comment_id": "U28-k04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 0.98
              },
              "A1b": {
                "qg": 1.0
              },
              "B": {
                "point_0": 0.86,
                "point_1": 0.93
              },
              "B2": {}
            },
            "input_tokens": 3093,
            "latency_s": 0.982821,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.01,
                "question_or_guess": 0.98,
                "reaction": 0.01,
                "request": 0.0
              },
              "A1b": {
                "guess": 1.0,
                "question": 0.0
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.9400000000000001,
                  "hit": 0.91
                },
                "point_1": {
                  "close": 0.99,
                  "hit": 0.95
                }
              },
              "B2": 0.9
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.91, 矛盾=0.90"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 85,
          "latency_s": 1.798199,
          "model": "gpt-6-luna",
          "prompt_tokens": 1457,
          "reasoning_tokens": 56,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し考えてみようか。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "以前、亀のスープだと言われて飲んだのは仲間の肉だった。でも漂流仲間は全員無事に帰れたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.983136220020242,
      "jev_s": null,
      "judge_s": 0.983136220020242,
      "luna_s": null,
      "total_s": 2.78182969102636,
      "writer_s": 1.7986934710061178
    }
  },
  {
    "case_id": "U28-k05",
    "record": {
      "comment_id": "U28-k05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_close"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 3,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.94
              },
              "B": {
                "point_0": 0.7,
                "point_1": 1.0
              }
            },
            "input_tokens": 2034,
            "latency_s": 0.715765,
            "major": "guess",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A1b": {
                "guess": 0.97,
                "question": 0.03
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.9600000000000001,
                  "hit": 0.16
                },
                "point_1": {
                  "close": 0.0,
                  "hit": 0.0
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_close",
          "reason": "段A=guess→guess_close, 要点最低=0.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 88,
          "latency_s": 1.824073,
          "model": "gpt-6-luna",
          "prompt_tokens": 1448,
          "reasoning_tokens": 54,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "惜しい！もう少し推理を続けてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "男は昔もウミガメの汁を飲み、今のものとは味が違うと感じたんだね。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.7160217990167439,
      "jev_s": null,
      "judge_s": 0.7160217990167439,
      "luna_s": null,
      "total_s": 2.5621605099877343,
      "writer_s": 1.8461387109709904
    }
  },
  {
    "case_id": "U28-k06",
    "record": {
      "comment_id": "U28-k06",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "guess_wrong"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 4,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A1b": {
                "qg": 0.98
              },
              "A2": {
                "kind": 0.63
              },
              "B": {
                "point_0": 0.85,
                "point_1": 0.93
              }
            },
            "guess_demoted": true,
            "input_tokens": 2368,
            "latency_s": 0.982035,
            "major": "question",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "q_multi": 0.06,
                "q_open": 0.75,
                "q_yesno": 0.19
              },
              "A_bare": 0.0,
              "B": {
                "point_0": {
                  "close": 0.1,
                  "hit": 0.07
                },
                "point_1": {
                  "close": 0.05,
                  "hit": 0.02
                }
              }
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "guess_wrong",
          "reason": "段A=question→guess_wrong, 要点最低=0.02"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 87,
          "latency_s": 1.420461,
          "model": "gpt-6-luna",
          "prompt_tokens": 1452,
          "reasoning_tokens": 49,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "残念、ちがうよ。ほかの可能性も考えてみようか☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "今日の椀は偽物で、シェフが男の昔話を信じ込ませるために嘘をついたんだ。",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.9823338909773156,
      "jev_s": null,
      "judge_s": 0.9823338909773156,
      "luna_s": null,
      "total_s": 2.40407792001497,
      "writer_s": 1.4217440290376544
    }
  },
  {
    "case_id": "U28-t01",
    "record": {
      "comment_id": "U28-t01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "仲間の肉",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 1.0
              }
            },
            "input_tokens": 778,
            "latency_s": 0.244653,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 1.0,
                "reaction": 0.0,
                "request": 0.0
              },
              "A_bare": 0.98
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 0.98"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "仲間の肉が何のことか、もう少し詳しく教えて！"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "仲間の肉？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.24476161890197545,
      "jev_s": null,
      "judge_s": 0.24476161890197545,
      "luna_s": null,
      "total_s": 3.517584143904969,
      "writer_s": 3.2728225250029936
    }
  },
  {
    "case_id": "U28-t02",
    "record": {
      "comment_id": "U28-t02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [
        "writer: writer did not ask what bare_term means"
      ],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "q_open"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": "レモン",
          "debug": {
            "calls": 1,
            "confidence": {
              "A1": {
                "major": 0.57
              }
            },
            "input_tokens": 776,
            "latency_s": 0.21494,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.01,
                "other": 0.01,
                "question_or_guess": 0.66,
                "reaction": 0.32,
                "request": 0.0
              },
              "A_bare": 1.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "q_open",
          "reason": "段A語句のみ: 1.00"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "fallback_template",
        "text": "レモンがどうしたのか聞かせてね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "レモン",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.21503832400776446,
      "jev_s": null,
      "judge_s": 0.21503832400776446,
      "luna_s": null,
      "total_s": 3.2278008420253173,
      "writer_s": 3.012762518017553
    }
  },
  {
    "case_id": "c-ask_howto-04",
    "record": {
      "comment_id": "c-ask_howto-04",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "ask_howto"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1053,
            "latency_s": 0.445959,
            "major": "request",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.0,
                "request": 1.0
              },
              "A2": {
                "ask_hint": 0.0,
                "ask_howto": 1.0,
                "ask_spoiler": 0.0
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "ask_howto",
          "reason": "段A=request→ask_howto"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 35,
          "latency_s": 1.26598,
          "model": "gpt-6-luna",
          "prompt_tokens": 1431,
          "reasoning_tokens": 0,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "はい、はい／いいえで答えられる質問をコメントすると、探偵が答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "質問したら返事もらえるの？",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.44607824098784477,
      "jev_s": null,
      "judge_s": 0.44607824098784477,
      "luna_s": null,
      "total_s": 1.7129585939692333,
      "writer_s": 1.2668803529813886
    }
  },
  {
    "case_id": "c-cheer-03",
    "record": {
      "comment_id": "c-cheer-03",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "cheer"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 1.0
              },
              "A2": {
                "kind": 0.91
              }
            },
            "input_tokens": 1154,
            "latency_s": 0.467144,
            "major": "reaction",
            "model": "gpt-6-luna",
            "output_tokens": 0,
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
                "cheer": 0.92,
                "complaint": 0.0,
                "greeting": 0.0,
                "impression": 0.07,
                "mention": 0.0,
                "request": 0.01
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "cheer",
          "reason": "段A=reaction→cheer"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 60,
          "latency_s": 1.644641,
          "model": "gpt-6-luna",
          "prompt_tokens": 1426,
          "reasoning_tokens": 34,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "ありがとう！楽しみにしててね☺️"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "更新たのしみにしてる〜",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4672818460967392,
      "jev_s": null,
      "judge_s": 0.4672818460967392,
      "luna_s": null,
      "total_s": 2.1123678700532764,
      "writer_s": 1.6450860239565372
    }
  },
  {
    "case_id": "c-complaint-02",
    "record": {
      "comment_id": "c-complaint-02",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "complaint"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.99
              },
              "A2": {
                "kind": 0.57
              }
            },
            "input_tokens": 1162,
            "latency_s": 0.403063,
            "major": "reaction",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.0,
                "other": 0.0,
                "question_or_guess": 0.01,
                "reaction": 0.99,
                "request": 0.0
              },
              "A2": {
                "chat": 0.01,
                "cheer": 0.01,
                "complaint": 0.63,
                "greeting": 0.01,
                "impression": 0.28,
                "mention": 0.01,
                "request": 0.05
              },
              "A_bare": 0.0
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "complaint",
          "reason": "段A=reaction→complaint"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "debug": {
          "completion_tokens": 63,
          "latency_s": 1.49883,
          "model": "gpt-6-luna",
          "prompt_tokens": 1430,
          "reasoning_tokens": 36,
          "slot": "（この種別では使わない）"
        },
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "llm",
        "text": "教えてくれてありがとう、確認するね。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "前の投稿と設定が被ってる気がする",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.4031369179720059,
      "jev_s": null,
      "judge_s": 0.4031369179720059,
      "luna_s": null,
      "total_s": 1.9026791229844093,
      "writer_s": 1.4995422050124034
    }
  },
  {
    "case_id": "c-troll-01",
    "record": {
      "comment_id": "c-troll-01",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "troll"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 2,
            "confidence": {
              "A1": {
                "major": 0.9
              },
              "A2": {
                "kind": 1.0
              }
            },
            "input_tokens": 1091,
            "latency_s": 0.611306,
            "major": "inappropriate",
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {
              "A1": {
                "inappropriate": 0.92,
                "other": 0.0,
                "question_or_guess": 0.0,
                "reaction": 0.08,
                "request": 0.0
              },
              "A2": {
                "abuse": 0.0,
                "personal_info": 0.0,
                "spam": 0.0,
                "troll": 1.0
              },
              "A_bare": 0.88
            },
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "troll",
          "reason": "段A=inappropriate→troll"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
      "parent_id": null,
      "problem_schema_version": 3,
      "reply": {
        "guard": null,
        "over_80": false,
        "reply_id": null,
        "source": "template",
        "text": "質問なら、はい・いいえで答えるよ。"
      },
      "schema_version": 1,
      "set_code": "umigame-soup-1",
      "shadow_mismatch": null,
      "text": "ぬぬぬぬぬ",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 0.6115505320485681,
      "jev_s": null,
      "judge_s": 0.6115505320485681,
      "luna_s": null,
      "total_s": 0.6115698260255158,
      "writer_s": 1.9293976947665215e-05
    }
  },
  {
    "case_id": "c-spam-05",
    "record": {
      "comment_id": "c-spam-05",
      "commenter_id": "probe",
      "config": {
        "consensus": false,
        "judge_mode": "decisions",
        "luna_model": "gpt-6-luna",
        "prompt_version": "cc9071fb8900",
        "reply_variant": "2c-luna",
        "shadow": false
      },
      "content_key": "016-umigame-soup",
      "errors": [],
      "fact_sheet_hash": "c81ff384e8a1",
      "final": {
        "answer": null,
        "decision": "decisions",
        "kind": "spam"
      },
      "judgements": {
        "decisions": {
          "answer": null,
          "bare_term": null,
          "debug": {
            "calls": 0,
            "confidence": {},
            "input_tokens": 0,
            "latency_s": 0.0,
            "model": "gpt-6-luna",
            "output_tokens": 0,
            "probabilities": {},
            "refusals": {
              "count": 0,
              "names": []
            }
          },
          "error": null,
          "kind": "spam",
          "reason": "段0規則: spam"
        },
        "jev": null,
        "luna": null
      },
      "media_id": "local-U28",
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
      "shadow_mismatch": null,
      "text": "無料プレゼント応募は固定リンクから→ https://example.invalid/gift",
      "times": {
        "comment_created_at": null,
        "judged_at": "2026-10-08T06:51:13Z",
        "replied_at": null,
        "webhook_received_at": "2026-10-08T06:51:13Z"
      }
    },
    "timing": {
      "decisions_s": 7.588998414576054e-06,
      "jev_s": null,
      "judge_s": 7.588998414576054e-06,
      "luna_s": null,
      "total_s": 1.0345946066081524e-05,
      "writer_s": 2.7569476515054703e-06
    }
  }
];
